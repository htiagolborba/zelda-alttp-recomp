/* Copyright (c) 2026 Hiran Tiago Lins Borba. MIT; see root LICENSE.
 * Single-threaded experimental host. No window/device, cwd changes or save writes. */
#include "core_host.h"
#include <setjmp.h>
#include <stdio.h>
#include <string.h>
#ifdef _WIN32
#include <windows.h>
static DWORD owner;
static int same_thread(void) { return owner == GetCurrentThreadId(); }
#else
#include <pthread.h>
static pthread_t owner;
static int same_thread(void) { return pthread_equal(owner, pthread_self()); }
#endif
/* Include platform headers before upstream register/memory-access macros. */
#ifdef FORCEINLINE
#undef FORCEINLINE
#endif
#include "src/assets.h"
#include "src/config.h"
#include "src/zelda_rtl.h"
#include "src/audio.h"
#include "src/spc_player.h"
#include "snes/ppu.h"
#include "snes/dma.h"
#include "src/variables.h"

Config g_config;
const uint8 *g_asset_ptrs[kNumberOfAssets];
uint32 g_asset_sizes[kNumberOfAssets];
MemBlk FindInAssetArray(int asset, int idx) {
  return FindIndexInMemblk((MemBlk){g_asset_ptrs[asset],g_asset_sizes[asset]},idx);
}
static uint8_t *asset_data;
static uint32_t pixels[256 * 224];
static int16_t pcm[534 * 2];
static char frame_hex[256 * 224 * 8 + 1], error_text[256], json_text[1024];
static AlttpSnapshot snapshot;
static int live, consumed, fatal_guard;
static jmp_buf fatal_jump;
static uint32_t previous_scene[4];
extern void ZeldaCoreHostReleaseRecorder(void);

/* These hooks are called only on the owning simulation thread. No audio
 * callback thread is created; no-op locks are not a general thread-safe API. */
void ZeldaApuLock(void) {}
void ZeldaApuUnlock(void) {}
void NORETURN Die(const char *error) {
  snprintf(error_text, sizeof(error_text), "Core fatal: %.220s", error);
  if (fatal_guard) longjmp(fatal_jump, 1);
  abort();
}
const char *alttp_core_error(void) { return error_text; }
static int fail(const char *text) {
  snprintf(error_text, sizeof(error_text), "%s", text);
  return 0;
}
static uint32_t read32(const uint8_t *p) {
  return (uint32_t)p[0] | (uint32_t)p[1]<<8 | (uint32_t)p[2]<<16 | (uint32_t)p[3]<<24;
}
static uint64_t hash_bytes(uint64_t hash, const void *data, size_t n) {
  const uint8_t *p = data;
  for (size_t i = 0; i < n; i++) hash = (hash ^ p[i]) * UINT64_C(1099511628211);
  return hash;
}
uint64_t alttp_core_fingerprint(const void *frame, const void *sound) {
  uint64_t h = UINT64_C(14695981039346656037);
  h = hash_bytes(h, g_ram, sizeof(g_ram));
  h = hash_bytes(h, g_zenv.sram, 8192);
  h = hash_bytes(h, g_zenv.ppu->vram, sizeof(g_zenv.ppu->vram));
  h = hash_bytes(h, g_zenv.player->ram, sizeof(g_zenv.player->ram));
  h = hash_bytes(h, frame, sizeof(pixels));
  return hash_bytes(h, sound, sizeof(pcm));
}
static void copy_snapshot(void) {
  uint32_t key[4] = {main_module_index, player_is_indoors,
                     overworld_area_index, dungeon_room_index};
  if (memcmp(key, previous_scene, sizeof(key))) {
    snapshot.scene_generation++;
    memcpy(previous_scene, key, sizeof(key));
  }
  snapshot.abi_version = 1;
  snapshot.struct_size = sizeof(snapshot);
  snapshot.module = main_module_index;
  snapshot.submodule = submodule_index;
  snapshot.x = link_x_coord; snapshot.y = link_y_coord;
  snapshot.z_raw = link_z_coord;
  snapshot.facing = link_direction_facing;
  snapshot.indoors = player_is_indoors;
  snapshot.area = overworld_area_index; snapshot.room = dungeon_room_index;
  snapshot.joypad_h = joypad1H_last; snapshot.joypad_l = joypad1L_last;
  snapshot.health = link_health_current;
  snapshot.player_active = main_module_index == 7 || main_module_index == 9;
  snapshot.state_hash = alttp_core_fingerprint(pixels, pcm);
}
void alttp_core_sram_write_requested(void) { snapshot.save_requests++; }
int alttp_core_open(const char *path, const char *sram_path) {
  if (consumed || live) return fail("Only one core session is supported per process; restart to reopen.");
  if (!path || !*path) return fail("Provide an absolute path to your locally extracted asset bundle.");
  FILE *f = fopen(path, "rb");
  if (!f) return fail("Cannot open local asset bundle.");
  if (fseek(f, 0, SEEK_END)) { fclose(f); return fail("Cannot seek asset file."); }
  long n = ftell(f);
  if (n < 88 + kNumberOfAssets * 4 || n > 32 * 1024 * 1024) {
    fclose(f); return fail("Invalid asset file length.");
  }
  rewind(f);
  asset_data = malloc((size_t)n);
  if (!asset_data) { fclose(f); return fail("Cannot allocate asset buffer."); }
  size_t got = fread(asset_data, 1, (size_t)n, f);
  fclose(f);
  static const uint8_t signature[] = { kAssets_Sig };
  if (got != (size_t)n || memcmp(asset_data, signature, 48) ||
      read32(asset_data+80) != kNumberOfAssets) goto bad_assets;
  uint64_t offset = 88 + kNumberOfAssets * 4 + (uint64_t)read32(asset_data+84);
  for (size_t i = 0; i < kNumberOfAssets; i++) {
    uint32_t size = read32(asset_data + 88 + i * 4);
    offset = (offset + 3) & ~UINT64_C(3);
    if (offset > (uint64_t)n || size > (uint64_t)n - offset) goto bad_assets;
    g_asset_ptrs[i] = asset_data + offset; g_asset_sizes[i] = size;
    offset += size;
  }
  uint8_t sram[8192] = {0};
  if (sram_path && *sram_path) {
    f = fopen(sram_path, "rb");
    if (!f) { fail("Cannot open SRAM import."); goto import_failed; }
    size_t amount = fread(sram, 1, sizeof(sram), f);
    int extra = fgetc(f); fclose(f);
    if (amount != sizeof(sram) || extra != EOF) {
      fail("SRAM import must be exactly 8192 bytes."); goto import_failed;
    }
  }
#ifdef _WIN32
  owner = GetCurrentThreadId();
#else
  owner = pthread_self();
#endif
  consumed = 1;
  memset(&g_config, 0, sizeof(g_config));
  memset(g_ram, 0, sizeof(g_ram));
  memset(&snapshot, 0, sizeof(snapshot));
  g_wanted_zelda_features = 0;
  fatal_guard = 1;
  if (setjmp(fatal_jump)) { fatal_guard = 0; alttp_core_close(); return 0; }
  ZeldaInitialize();
  /* Match the SDL host: no widescreen; the reference buffer is 256 pixels. */
  g_zenv.ppu->extraLeftRight = 0;
  memcpy(g_zenv.sram, sram, sizeof(sram));
  ZeldaEnableMsu(0);
  ZeldaSetLanguage(NULL);
  live = 1; fatal_guard = 0; error_text[0] = 0;
  copy_snapshot();
  return 1;
bad_assets:
  fail("Invalid/corrupt asset table or incompatible asset signature.");
import_failed:
  free(asset_data); asset_data = NULL;
  memset(g_asset_ptrs, 0, sizeof(g_asset_ptrs));
  memset(g_asset_sizes, 0, sizeof(g_asset_sizes));
  return 0;
}
int alttp_core_step(uint32_t buttons) {
  if (!live) return fail("Core is not open.");
  if (!same_thread()) return fail("Core calls must remain on their owning thread.");
  if (buttons > 4095) return fail("Input contains unsupported bits.");
  fatal_guard = 1;
  if (setjmp(fatal_jump)) { fatal_guard = 0; alttp_core_close(); return 0; }
  ZeldaRunFrame((int)buttons);
  /* Keep PPU/HDMA work even when its diagnostic pixels are hidden. */
  ZeldaDrawPpuFrame((uint8_t *)pixels, 256 * 4, 0);
  /* Preserve APU feedback with one 534-sample synthesis batch per tick.
   * PCM is deliberately discarded for now; no competing audio device. */
  ZeldaRenderAudio(pcm, 534, 2);
  snapshot.tick++;
  copy_snapshot();
  fatal_guard = 0;
  return 1;
}
int alttp_core_snapshot(AlttpSnapshot *out, uint32_t size) {
  if (!live || !same_thread() || !out || size != sizeof(snapshot)) return 0;
  memcpy(out, &snapshot, sizeof(snapshot));
  return 1;
}
const char *alttp_core_json(void) {
  if (!live || !same_thread()) return "{\"ok\":false,\"error\":\"Core is not open on this thread\"}";
  snprintf(json_text, sizeof(json_text),
    "{\"ok\":true,\"abi\":1,\"tick\":%u,\"scene_generation\":%u,"
    "\"module\":%u,\"submodule\":%u,\"x\":%u,\"y\":%u,\"z_raw\":%u,"
    "\"facing\":%u,\"indoors\":%u,\"area\":%u,\"room\":%u,"
    "\"joypad_h\":%u,\"joypad_l\":%u,\"health\":%u,\"player_active\":%s,"
    "\"save_requests\":%u,\"state_hash\":\"%016llx\"}",
    snapshot.tick,snapshot.scene_generation,snapshot.module,snapshot.submodule,
    snapshot.x,snapshot.y,snapshot.z_raw,snapshot.facing,snapshot.indoors,
    snapshot.area,snapshot.room,snapshot.joypad_h,snapshot.joypad_l,snapshot.health,
    snapshot.player_active ? "true" : "false",snapshot.save_requests,
    (unsigned long long)snapshot.state_hash);
  return json_text;
}
const char *alttp_core_frame_hex(void) {
  if (!live || !same_thread()) return "";
  static const char hex[] = "0123456789abcdef";
  for (size_t i=0;i<256*224;i++) {
    uint32_t p=pixels[i];
    uint8_t rgba[4]={(uint8_t)(p>>16),(uint8_t)(p>>8),(uint8_t)p,255};
    for (size_t c=0;c<4;c++) { frame_hex[i*8+c*2]=hex[rgba[c]>>4];frame_hex[i*8+c*2+1]=hex[rgba[c]&15]; }
  }
  frame_hex[sizeof(frame_hex)-1]=0;
  return frame_hex;
}
void alttp_core_close(void) {
  if (consumed && !same_thread()) return;
  live = 0;
  ZeldaCoreHostReleaseRecorder();
  if (g_zenv.player) { dsp_free(g_zenv.player->dsp); free(g_zenv.player); }
  if (g_zenv.ppu) ppu_free(g_zenv.ppu);
  if (g_zenv.dma) dma_free(g_zenv.dma);
  free(g_zenv.sram); memset(&g_zenv, 0, sizeof(g_zenv));
  free(asset_data); asset_data=NULL;
  memset(g_asset_ptrs,0,sizeof(g_asset_ptrs));
  memset(g_asset_sizes,0,sizeof(g_asset_sizes));
}
