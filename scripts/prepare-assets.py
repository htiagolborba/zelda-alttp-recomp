#!/usr/bin/env python3
"""Extract a user's ROM locally; no ROM or derived game assets are distributed."""
import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED = '66871d66be19ad2c34c927d6b14cd8eb6fc3181965b6e517cb361f7316009cfb'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    parser.add_argument('--output', type=Path, default=Path('zelda3_assets.dat'))
    args = parser.parse_args()
    rom = args.rom.resolve()
    if hashlib.sha256(rom.read_bytes()).hexdigest() != EXPECTED:
        parser.error('ROM hash mismatch. Use the unmodified USA revision 0 ROM (1 MiB).')
    here = Path(__file__).resolve().parent
    source = here / 'extractor'
    if not source.is_dir():
        source = here.parent / 'zelda3' / 'assets'
    output = args.output.resolve()
    with tempfile.TemporaryDirectory(prefix='zelda-alttp-') as tmp:
        work = Path(tmp)
        assets = work / 'assets'
        assets.mkdir()
        (assets / 'sprites').mkdir()
        (work / 'other').mkdir()
        shutil.copy2(source.parent / 'other/3x5_font.png', work / 'other/3x5_font.png')
        for path in source.iterdir():
            if path.suffix in ('.py', '.bin'):
                shutil.copy2(path, assets / path.name)
        subprocess.run([sys.executable, str(assets / 'restool.py'),
                        '--extract-from-rom', '--rom', str(rom)], check=True)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(work / 'zelda3_assets.dat', output)
    print(f'Assets created: {output}')


if __name__ == '__main__':
    main()
