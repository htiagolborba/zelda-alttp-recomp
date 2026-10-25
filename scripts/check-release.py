#!/usr/bin/env python3
"""Verify release contents, manifests, and executable architecture without a ROM."""
import hashlib
import json
import struct
import sys
import zipfile
from pathlib import Path


def check(path):
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        entries = {i.filename: i for i in z.infolist() if not i.is_dir()}
        roots = {name.split('/')[0] for name in entries}
        assert len(roots) == 1, 'Expected one top-level folder'
        root = roots.pop() + '/'
        files = {name[len(root):]: z.read(name) for name in entries}
        for name in files:
            assert '..' not in Path(name).parts and not name.startswith('/'), name
            assert Path(name).suffix.lower() not in {'.sfc', '.smc', '.yaml', '.pcm', '.brr', '.spc'}, name
            assert Path(name).name != 'zelda3_assets.dat', name
        manifest = json.loads(files['MANIFEST.json'])
        assert set(manifest) == set(files) - {'MANIFEST.json'}, 'Manifest file list mismatch'
        for name, digest in manifest.items():
            assert hashlib.sha256(files[name]).hexdigest() == digest, name
        assert all(f in files for f in ['README.md', 'CREDITS.md', 'LICENSE.txt',
                                       'ADAPTATION-LICENSE.txt', 'SDL2-LICENSE.txt',
                                       'OPUS-LICENSE.txt', 'tools/prepare-assets.py',
                                       'tools/extractor/restool.py', 'tools/requirements.txt',
                                       'tools/other/3x5_font.png'])
        if '-windows-' in path.name:
            exe = files['zelda3.exe']
            assert exe[:2] == b'MZ'
            offset = struct.unpack_from('<I', exe, 0x3c)[0]
            assert exe[offset:offset+4] == b'PE\0\0'
            assert struct.unpack_from('<H', exe, offset+4)[0] == 0x8664, 'Expected Windows x86_64'
            assert 'SDL2.dll' in files and 'Launch-Windows.cmd' in files
        else:
            exe = files['Zelda ALttP.app/Contents/MacOS/zelda3']
            assert exe[:4] == b'\xcf\xfa\xed\xfe', 'Expected 64-bit Mach-O'
            assert struct.unpack_from('<I', exe, 4)[0] == 0x01000007, 'Expected macOS x86_64'
            for name in ['Zelda ALttP.app/Contents/MacOS/zelda3', 'Zelda ALttP.app/Contents/MacOS/launch']:
                assert (entries[root + name].external_attr >> 16) & 0o111, 'Missing executable permission'
        expected = path.with_suffix('.zip.sha256').read_text().split()[0]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        print(f'PASS: {path.name} ({len(files)} files, no ROM/runtime asset bundle)')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        check(arg)
