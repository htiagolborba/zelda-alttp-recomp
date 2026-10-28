#!/usr/bin/env python3
"""Local-only Godot/core parity smoke; no user resources are uploaded to CI."""
import argparse
import ctypes
import hashlib
import json
import platform
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--godot',required=True,type=Path);p.add_argument('--assets',required=True,type=Path);p.add_argument('--sram',type=Path)
args=p.parse_args()
assets=args.assets.resolve();sram=args.sram.resolve() if args.sram else None
assert hashlib.sha256(assets.read_bytes()).hexdigest()=='0fe2e4bd75d70f06fb9a74cd3a9cb336c838149b831b56e8792114a89292c793'
out=ROOT/'build/core-host';out.mkdir(exist_ok=True,parents=True)
report=out/'godot-integration.json'
command=[str(args.godot.resolve()),'--headless','--path',str(ROOT/'presentation/godot'),'--',f'--assets={assets}','--core-smoke',f'--report={report}']
if sram:command.append(f'--sram={sram}')
run=subprocess.run(command,capture_output=True,text=True,timeout=45)
log=run.stdout+run.stderr;(out/'godot-integration.log').write_text(log);print(log)
assert run.returncode==0 and 'SCRIPT ERROR:' not in log and 'ERROR:' not in log
assert 'ALTTP_CORE_CONNECTED' in log and 'ALTTP_CORE_SMOKE_PASSED ticks=240' in log
assert log.count('ALTTP_NATIVE_STOPPED')==2
result=json.loads(report.read_text());assert result['gameplay_core_connected'] is True
state=result['core_snapshot'];assert state['tick']==240
lib=ctypes.CDLL(str((out/('alttp_core.dll' if platform.system()=='Windows' else 'libalttp_core.dylib')).resolve()))
lib.alttp_core_open.argtypes=[ctypes.c_char_p,ctypes.c_char_p];lib.alttp_core_json.restype=ctypes.c_char_p
assert lib.alttp_core_open(str(assets).encode(),str(sram).encode() if sram else None)
for i in range(240):assert lib.alttp_core_step(16 if 60<=i<90 else 0)
expected=json.loads(lib.alttp_core_json());lib.alttp_core_close()
assert expected==state,('Godot/C snapshot mismatch',expected,state)
print('PASS: Godot and standalone C produce the same state after 240 controlled ticks.')
