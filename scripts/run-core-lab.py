#!/usr/bin/env python3
"""Launch the experimental Godot/C integration with a local canonical asset bundle."""
import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--assets',type=Path,required=True)
p.add_argument('--sram',type=Path,help='Optional 8 KiB read-only SRAM import; the source is never written')
p.add_argument('--godot',type=Path)
p.add_argument('--renderer',choices=['gl_compatibility','forward_plus','mobile'],default='gl_compatibility')
p.add_argument('--smoke',action='store_true',help='Stop after 240 controlled ticks')
p.add_argument('--capture',type=Path,help='Save a viewport capture (requires a graphical session)')
args=p.parse_args();assets=args.assets.resolve()
if not assets.is_file() or hashlib.sha256(assets.read_bytes()).hexdigest()!='0fe2e4bd75d70f06fb9a74cd3a9cb336c838149b831b56e8792114a89292c793':
    p.error('Use the canonical USA asset bundle generated from your ROM by scripts/prepare-assets.py')
if args.sram and (not args.sram.is_file() or args.sram.stat().st_size!=8192):p.error('SRAM import must be an existing 8192-byte file')
version=json.loads((ROOT/'native/godot_probe/toolchain.json').read_text())['version']
base=ROOT/f'.tools/godot-{version}'
engine=args.godot or (base/'Godot.app/Contents/MacOS/Godot' if platform.system()=='Darwin' else base/f'Godot_v{version}-stable_win64_console.exe')
if not engine.is_file():p.error('Run scripts/setup-godot.py first or provide --godot')
lib='libalttp_core_godot.macos.x86_64.dylib' if platform.system()=='Darwin' else 'alttp_core_godot.windows.x86_64.dll'
if not (ROOT/'presentation/godot/native/bin'/lib).exists():p.error('Build the gameplay bridge with scripts/build-core-host.py --godot first')
report=ROOT/'build/core-host/interactive-report.json';report.parent.mkdir(parents=True,exist_ok=True)
command=[str(engine.resolve()),'--path',str(ROOT/'presentation/godot'),'--rendering-method',args.renderer,'--',f'--assets={assets}',f'--report={report}']
if args.sram:command.append(f'--sram={args.sram.resolve()}')
if args.smoke:command.append('--core-smoke')
if args.capture:
    dest=args.capture.resolve();dest.parent.mkdir(parents=True,exist_ok=True);command.append(f'--capture={dest}')
raise SystemExit(subprocess.run(command).returncode)
