/* Controlled reference harness: retain the original SDL host's static loader
 * and helpers, but drive the exact same offline frame/audio schedule. */
#include <SDL.h>
#include "reference_legacy_main.c"
#include "../../zelda3/src/spc_player.h"
static uint64_t hash_data(uint64_t h,const void *data,size_t n) {
  const uint8_t *p=data;
  for(size_t i=0;i<n;i++)h=(h^p[i])*UINT64_C(1099511628211);
  return h;
}
int main(int argc,char **argv) {
  if(argc!=3)return 2;
  /* Run in an isolated directory containing the user's local bundle. */
  memset(&g_config,0,sizeof(g_config));
  LoadAssets();ZeldaInitialize();
  g_zenv.ppu->extraLeftRight=0;
  ZeldaEnableMsu(0);ZeldaSetLanguage(NULL);
  if(strcmp(argv[1],"-")) {
    FILE *f=fopen(argv[1],"rb");if(!f)return 3;
    if(fread(g_zenv.sram,1,8192,f)!=8192)return 4;fclose(f);
  }
  g_audio_mutex=SDL_CreateMutex();if(!g_audio_mutex)return 5;
  uint32_t pixels[256*224]={0};int16_t audio[534*2]={0};
  FILE *inputs=fopen(argv[2],"r");if(!inputs)return 6;
  unsigned buttons;unsigned tick=0;
  while(fscanf(inputs,"%u",&buttons)==1) {
    ZeldaRunFrame((int)buttons);
    ZeldaDrawPpuFrame((uint8_t*)pixels,256*4,0);
    ZeldaRenderAudio(audio,534,2);
    uint64_t h=UINT64_C(14695981039346656037);
    h=hash_data(h,g_ram,sizeof(g_ram));h=hash_data(h,g_zenv.sram,8192);
    h=hash_data(h,g_zenv.ppu->vram,sizeof(g_zenv.ppu->vram));
    h=hash_data(h,g_zenv.player->ram,sizeof(g_zenv.player->ram));
    h=hash_data(h,pixels,sizeof(pixels));h=hash_data(h,audio,sizeof(audio));
    printf("%u %016llx %u %u %u %u\n",++tick,(unsigned long long)h,
      main_module_index,submodule_index,link_x_coord,link_y_coord);
  }
  fclose(inputs);SDL_DestroyMutex(g_audio_mutex);return 0;
}
