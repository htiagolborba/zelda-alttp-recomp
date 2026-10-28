#!/usr/bin/env python3
"""Build the SDL-free experimental gameplay library; no ROM needed for compilation."""
import argparse
import platform
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent


def sources():
    excluded = {'main.c','config.c','opengl.c','glsl_shader.c'}
    return [p for p in sorted((ROOT/'zelda3/src').glob('*.c')) if p.name not in excluded] + list(sorted((ROOT/'zelda3/snes').glob('*.c'))) + [ROOT/'zelda3/third_party/opus-1.3.1-stripped/opus_decoder_amalgam.c']


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cc',default='clang')
    p.add_argument('--target',choices=['macos','windows'],default='windows' if platform.system()=='Windows' else 'macos')
    p.add_argument('--godot',action='store_true',help='Build the Godot bridge instead of the standalone C library')
    args=p.parse_args()
    out=ROOT/'build/core-host';out.mkdir(parents=True,exist_ok=True)
    name='libalttp_core.dylib' if args.target=='macos' else 'alttp_core.dll'
    extra=[]
    if args.godot:
        out=ROOT/'presentation/godot/native/bin';out.mkdir(parents=True,exist_ok=True)
        name='libalttp_core_godot.macos.x86_64.dylib' if args.target=='macos' else 'alttp_core_godot.windows.x86_64.dll'
        extra=['-DALTTP_WITH_CORE_HOST=1','-I',str(ROOT/'native/godot_probe/include'),str(ROOT/'native/godot_probe/probe.c'),str(ROOT/'native/core_host/godot_bridge.c')]
    cmd=[args.cc,'-O2','-Werror','-std=c11','-fvisibility=hidden',
         '-DALTTP_CORE_HOST=1','-DSYSTEM_VOLUME_MIXER_AVAILABLE=0',
         '-I',str(ROOT/'zelda3'),'-I',str(ROOT/'native/core_host'),
         '-dynamiclib' if args.target=='macos' else '-shared',
         *(['-arch','x86_64'] if args.target=='macos' else []),
         *extra,*map(str,sources()),str(ROOT/'native/core_host/core_host.c'),*(['-lm'] if args.target=='macos' else []),'-o',str(out/name)]
    subprocess.run(cmd,check=True)
    data=(out/name).read_bytes()
    if args.target=='macos':
        assert data[:4]==b'\xcf\xfa\xed\xfe' and int.from_bytes(data[4:8],'little')==0x01000007
    else:
        offset=int.from_bytes(data[0x3c:0x40],'little')
        assert data[:2]==b'MZ' and data[offset:offset+4]==b'PE\0\0' and int.from_bytes(data[offset+4:offset+6],'little')==0x8664
    print(out/name)
if __name__=='__main__':main()
