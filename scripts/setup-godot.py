#!/usr/bin/env python3
"""Download the exact official Godot editor pinned for the M0 probe; verify SHA-256."""
import hashlib
import json
import platform
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    lock = json.loads((ROOT / 'native/godot_probe/toolchain.json').read_text())
    host = platform.system()
    suffix = {'Darwin': 'macos.universal.zip', 'Windows': 'win64.exe.zip'}.get(host)
    if suffix is None:
        raise SystemExit('M0 currently configures macOS and Windows only.')
    name = next(name for name in lock['artifacts'] if name.endswith(suffix))
    artifact = lock['artifacts'][name]
    cache = ROOT / '.tools/downloads'
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / name
    if not archive.exists():
        partial = archive.with_suffix('.partial')
        print(f'Downloading official engine: {artifact["url"]}', flush=True)
        urllib.request.urlretrieve(artifact['url'], partial)
        if hashlib.sha256(partial.read_bytes()).hexdigest() != artifact['sha256']:
            raise SystemExit('Download checksum mismatch; refusing to install.')
        partial.replace(archive)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != artifact['sha256']:
        raise SystemExit('Cached archive checksum mismatch; refusing to install.')
    dest = ROOT / f'.tools/godot-{lock["version"]}'
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            out = (dest / member.filename).resolve()
            if not out.is_relative_to(dest.resolve()):
                raise SystemExit('Unsafe archive path')
        z.extractall(dest)
    if host == 'Darwin':
        executable = dest / 'Godot.app/Contents/MacOS/Godot'
        executable.chmod(0o755)
    else:
        executable = dest / f'Godot_v{lock["version"]}-stable_win64_console.exe'
        if not executable.exists():
            executable = dest / f'Godot_v{lock["version"]}-stable_win64.exe'
    print(f'Verified Godot {lock["version"]}: {executable}')
    print('Run scripts/build-godot-probe.py, then scripts/test-godot-probe.py --godot <path above>')


if __name__ == '__main__':
    main()
