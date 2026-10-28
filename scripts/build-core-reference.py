#!/usr/bin/env python3
"""Build the unmodified SDL-host reference harness on macOS for local parity tests."""
import argparse
import os
import shutil
import shlex
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sdl-config',default=os.environ.get('SDL2_CONFIG') or shutil.which('sdl2-config') or str(ROOT/'.tools/sdl2/bin/sdl2-config'))
args=parser.parse_args();sdl=Path(args.sdl_config)
if not sdl.exists():parser.error('Provide SDL2 development files with --sdl-config /path/to/sdl2-config')
flags=shlex.split(subprocess.check_output([str(sdl),'--cflags'],text=True))
libs=shlex.split(subprocess.check_output([str(sdl),'--static-libs'],text=True))
source=[p for p in sorted((ROOT/'zelda3/src').glob('*.c')) if p.name!='main.c']
source+=list(sorted((ROOT/'zelda3/snes').glob('*.c')))
source += [ROOT/'zelda3/third_party/gl_core/gl_core_3_1.c',ROOT/'zelda3/third_party/opus-1.3.1-stripped/opus_decoder_amalgam.c',ROOT/'tests/core_host/reference_runner.c']
out=ROOT/'build/core-host/reference-runner';out.parent.mkdir(parents=True,exist_ok=True)
legacy=(ROOT/'zelda3/src/main.c').read_text()
entry='int main(int argc, char** argv) {'
assert legacy.count(entry)==1
(out.parent/'reference_legacy_main.c').write_text(legacy.replace(entry,'int alttp_original_sdl_main_not_invoked(int argc, char** argv) {',1))
subprocess.run(['clang','-O2','-Werror','-DSYSTEM_VOLUME_MIXER_AVAILABLE=0','-I',str(ROOT/'zelda3'),'-I',str(ROOT/'zelda3/src'),'-I',str(out.parent),*flags,*map(str,source),*libs,'-o',str(out)],check=True)
print(out)
