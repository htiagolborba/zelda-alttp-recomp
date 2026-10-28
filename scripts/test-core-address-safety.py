#!/usr/bin/env python3
"""macOS local AddressSanitizer check; requires a trusted user's asset bundle."""
import argparse
import runpy
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,required=True);args=p.parse_args()
build=runpy.run_path(str(ROOT/'scripts/build-core-host.py'))
out=ROOT/'build/core-host/address-safety';out.parent.mkdir(parents=True,exist_ok=True)
subprocess.run(['clang','-O1','-g','-fsanitize=address','-fno-omit-frame-pointer','-std=c11',
 '-DALTTP_CORE_HOST=1','-DSYSTEM_VOLUME_MIXER_AVAILABLE=0','-I',str(ROOT/'zelda3'),
 '-I',str(ROOT/'native/core_host'),*map(str,build['sources']()),str(ROOT/'native/core_host/core_host.c'),
 str(ROOT/'tests/core_host/address_safety.c'),'-lm','-o',str(out)],check=True)
subprocess.run([str(out),str(args.assets.resolve())],check=True)
