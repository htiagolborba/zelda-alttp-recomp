#!/usr/bin/env python3
"""Build an allowlisted, ROM-free release archive from an existing native build."""
import argparse
import hashlib
import json
import plistlib
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def copy(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=['macos', 'windows'])
    p.add_argument('--version', default='0.1.0')
    p.add_argument('--sdl-license', type=Path, required=True)
    args = p.parse_args()
    if not all(c.isalnum() or c in '.-_' for c in args.version):
        p.error('Invalid version')
    name = f'Zelda-ALttP-{args.version}-{args.platform}-x86_64'
    stage = ROOT / 'build' / 'packages' / name
    # Never reuse a stage: stale ROM-derived assets must not enter a release.
    if stage.exists():
        p.error(f'Staging folder already exists: {stage}. Use a new version or move it aside.')
    stage.mkdir(parents=True)
    for f in ['README.md', 'CREDITS.md', 'project-info.json']:
        copy(ROOT / f, stage / f)
    copy(ROOT / 'zelda3/LICENSE.txt', stage / 'LICENSE.txt')
    copy(ROOT / 'LICENSE', stage / 'ADAPTATION-LICENSE.txt')
    copy(ROOT / 'zelda3/third_party/opus-1.3.1-stripped/COPYING', stage / 'OPUS-LICENSE.txt')
    copy(args.sdl_license, stage / 'SDL2-LICENSE.txt')
    copy(ROOT / 'scripts/prepare-assets.py', stage / 'tools/prepare-assets.py')
    copy(ROOT / 'zelda3/other/3x5_font.png', stage / 'tools/other/3x5_font.png')
    for file in (ROOT / 'zelda3/assets').iterdir():
        if file.suffix in ['.py', '.bin']:
            copy(file, stage / 'tools/extractor' / file.name)
    (stage / 'tools/requirements.txt').write_text('Pillow==12.0.0\nPyYAML==6.0.3\n')
    if args.platform == 'windows':
        for f in ['zelda3.exe', 'SDL2.dll']:
            copy(ROOT / 'build/windows' / f, stage / f)
        copy(ROOT / 'zelda3/zelda3.ini', stage / 'zelda3.ini')
        copy(ROOT / 'packaging/Launch-Windows.cmd', stage / 'Launch-Windows.cmd')
    else:
        from PIL import Image
        contents = stage / 'Zelda ALttP.app/Contents'
        copy(ROOT / 'zelda3/zelda3', contents / 'MacOS/zelda3')
        copy(ROOT / 'packaging/launch-macos.sh', contents / 'MacOS/launch')
        (contents / 'MacOS/launch').chmod(0o755)
        for src in ['zelda3/zelda3.ini', 'CREDITS.md', 'project-info.json', 'zelda3/LICENSE.txt']:
            copy(ROOT / src, contents / 'Resources' / Path(src).name)
        copy(args.sdl_license, contents / 'Resources/SDL2-LICENSE.txt')
        with Image.open(ROOT / 'zelda3/src/platform/win32/triforce.ico') as icon:
            icon.save(contents / 'Resources/Triforce.icns', format='ICNS')
        info = dict(CFBundleName='Zelda ALttP', CFBundleDisplayName='Zelda ALttP',
                    CFBundleIdentifier='local.zelda.alttp', CFBundleExecutable='launch',
                    CFBundlePackageType='APPL', CFBundleIconFile='Triforce.icns',
                    CFBundleVersion=args.version, CFBundleShortVersionString=args.version,
                    NSHighResolutionCapable=True,
                    NSHumanReadableCopyright='2026 Hiran Tiago Lins Borba — macOS/Windows adaptation. See CREDITS.md.',
                    ZeldaProjectAuthor='Hiran Tiago Lins Borba',
                    ZeldaProjectWebsite='https://github.com/htiagolborba',
                    ZeldaProjectLocation='Toronto, ON, CA')
        with (contents / 'Info.plist').open('wb') as f:
            plistlib.dump(info, f)
    files = sorted(f for f in stage.rglob('*') if f.is_file())
    manifest = {str(f.relative_to(stage)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    (stage / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    archive = out / (name + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob('*')):
            if f.is_file():
                if f.suffix.lower() in ['.sfc', '.smc', '.pcm', '.spc', '.brr', '.yaml'] or f.name == 'zelda3_assets.dat':
                    raise ValueError(f'Forbidden release asset: {f}')
                z.write(f, f.relative_to(stage.parent))
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{checksum}  {archive.name}\n')
    print(archive)


if __name__ == '__main__':
    main()
