#!/usr/bin/env python3
"""Local-only integration/parity tests. Requires a user's prepared assets, never CI uploads."""
import argparse
import ctypes
import hashlib
import json
import platform
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent


def library():
    lib=ctypes.CDLL(str((ROOT/'build/core-host'/('alttp_core.dll' if platform.system()=='Windows' else 'libalttp_core.dylib')).resolve()))
    lib.alttp_core_open.argtypes=[ctypes.c_char_p,ctypes.c_char_p]
    lib.alttp_core_json.restype=ctypes.c_char_p
    lib.alttp_core_error.restype=ctypes.c_char_p
    lib.alttp_core_frame_hex.restype=ctypes.c_char_p
    return lib


def sequence():
    # Title/menu navigation + all 12 input bits and opposing directions.
    result=[0]*1800
    for start in range(480,1800,120):result[start]=8
    for bit in range(12):result.extend([1<<bit]*3+[0]*3)
    result.extend([48,192,0])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets',required=True,type=Path)
    p.add_argument('--sram',type=Path)
    p.add_argument('--reference',type=Path,help='Compiled controlled legacy-host runner')
    p.add_argument('--output',type=Path,default=ROOT/'build/core-host/parity-report.json')
    args=p.parse_args();assets=args.assets.resolve();sram=args.sram.resolve() if args.sram else None
    assert hashlib.sha256(assets.read_bytes()).hexdigest()=='0fe2e4bd75d70f06fb9a74cd3a9cb336c838149b831b56e8792114a89292c793','Use the validated USA resource bundle for this fixture.'
    before=hashlib.sha256(sram.read_bytes()).hexdigest() if sram else None
    lib=library()
    assert not lib.alttp_core_open(b'/missing/local-bundle',None)
    with tempfile.TemporaryDirectory(prefix='alttp-validation-') as temp:
        work=Path(temp)
        cases=[b'bad',bytearray(assets.read_bytes()),bytearray(assets.read_bytes())]
        cases[1][80:84]=(999).to_bytes(4,'little')
        cases[2][84:88]=(0xffffffff).to_bytes(4,'little')
        for i,data in enumerate(cases):
            invalid=work/f'invalid-{i}.dat';invalid.write_bytes(data)
            assert not lib.alttp_core_open(str(invalid).encode(),None),'Invalid asset metadata accepted'
        short=work/'short-sram.bin';short.write_bytes(bytes(8191))
        assert not lib.alttp_core_open(str(assets).encode(),str(short).encode()),'Short SRAM accepted'
    assert lib.alttp_core_open(str(assets).encode(),str(sram).encode() if sram else None),lib.alttp_core_error()
    assert not lib.alttp_core_open(str(assets).encode(),None),'Duplicate open must be rejected'
    assert not lib.alttp_core_step(65535),'Unsupported input bits must be rejected'
    inputs=sequence();states=[]
    for buttons in inputs:
        assert lib.alttp_core_step(buttons),lib.alttp_core_error()
        states.append(json.loads(lib.alttp_core_json()))
    frame=bytes.fromhex(lib.alttp_core_frame_hex().decode());assert len(frame)==256*224*4
    assert set(frame[3::4])=={255}
    lib.alttp_core_close()
    assert not lib.alttp_core_step(0),'Closed core must reject ticks'
    assert not lib.alttp_core_open(str(assets).encode(),None),'A second session must require a process restart'
    if sram:assert hashlib.sha256(sram.read_bytes()).hexdigest()==before,'Imported SRAM changed'
    parity=False
    if args.reference:
        with tempfile.TemporaryDirectory(prefix='alttp-reference-') as temp:
            work=Path(temp);(work/'zelda3_assets.dat').write_bytes(assets.read_bytes())
            source=work/'input.txt';source.write_text('\n'.join(map(str,inputs))+'\n')
            result=subprocess.run([str(args.reference.resolve()),str(sram) if sram else '-',str(source)],cwd=work,capture_output=True,text=True,timeout=90,check=False)
            assert result.returncode==0,(result.returncode,result.stderr,result.stdout[-500:])
            lines=[line.split() for line in result.stdout.splitlines() if line and line.split()[0].isdigit()]
            assert len(lines)==len(states),(len(lines),len(states),result.stderr)
            for state,line in zip(states,lines):
                assert [str(state['tick']),state['state_hash'],str(state['module']),str(state['submodule']),str(state['x']),str(state['y'])]==line,('Parity mismatch',state,line)
            assert not (work/'saves').exists(),'Reference fixture unexpectedly wrote saves'
            parity=True
    report={'ticks':len(inputs),'compared_every_tick':parity,'parity':parity,'asset_sha256':hashlib.sha256(assets.read_bytes()).hexdigest(),'imported_sram_read_only':bool(sram),'audio_schedule':'one 534-sample 32000 Hz stereo batch per tick; muted','last_snapshot':states[-1],'modules_observed':sorted(set(s['module'] for s in states)),'scope':'Controlled offline host parity, not SNES-ROM equivalence or complete gameplay certification'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
