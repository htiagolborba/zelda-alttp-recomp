#ifndef ALTTP_CORE_HOST_H
#define ALTTP_CORE_HOST_H
#include <stdint.h>
#include <stddef.h>
#ifdef _WIN32
#define ALTTP_CORE_EXPORT __declspec(dllexport)
#else
#define ALTTP_CORE_EXPORT __attribute__((visibility("default")))
#endif
/* One session per process, one calling thread. Input uses the upstream low-12
 * mask: B=1,Y=2,Select=4,Start=8,Up=16,Down=32,Left=64,Right=128,
 * A=256,X=512,L=1024,R=2048. Frame/audio work is completed inside step(). */
typedef struct AlttpSnapshot {
  uint32_t abi_version, struct_size, tick, scene_generation;
  uint32_t module, submodule, x, y, z_raw, facing, indoors, area, room;
  uint32_t joypad_h, joypad_l, health, player_active, save_requests;
  uint64_t state_hash;
} AlttpSnapshot;
ALTTP_CORE_EXPORT int alttp_core_open(const char *assets_path, const char *sram_path);
ALTTP_CORE_EXPORT int alttp_core_step(uint32_t buttons);
ALTTP_CORE_EXPORT int alttp_core_snapshot(AlttpSnapshot *out, uint32_t size);
ALTTP_CORE_EXPORT const char *alttp_core_json(void);
ALTTP_CORE_EXPORT const char *alttp_core_frame_hex(void);
ALTTP_CORE_EXPORT const char *alttp_core_error(void);
ALTTP_CORE_EXPORT void alttp_core_close(void);
uint64_t alttp_core_fingerprint(const void *pixels, const void *pcm);
void alttp_core_sram_write_requested(void);
#endif
