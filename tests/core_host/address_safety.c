#include "core_host.h"
#include <stdio.h>
#include <string.h>
int main(int argc,char **argv) {
  if(argc!=2)return 2;
  if(!alttp_core_open(argv[1],NULL)) { puts(alttp_core_error());return 3; }
  AlttpSnapshot state;
  memset(&state,0,sizeof(state));
  if(alttp_core_snapshot(&state,1))return 4;
  for(unsigned i=0;i<2000;i++) {
    unsigned buttons=i>=1800?(1u<<((i-1800)%12)):0;
    if(!alttp_core_step(buttons))return 5;
    if(!alttp_core_snapshot(&state,sizeof(state)))return 6;
  }
  if(strlen(alttp_core_frame_hex())!=256*224*8)return 7;
  printf("ASAN_CORE_PASS tick=%u module=%u\n",state.tick,state.module);
  alttp_core_close();return 0;
}
