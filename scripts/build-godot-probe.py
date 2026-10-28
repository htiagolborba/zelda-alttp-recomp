#!/usr/bin/env python3
"""Build the ROM-free M0 GDExtension lifecycle probe, without external bindings."""
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['macos', 'windows'],
                        default='windows' if platform.system() == 'Windows' else 'macos')
    parser.add_argument('--arch', choices=['x86_64', 'arm64'], default='x86_64')
    parser.add_argument('--cc', help='Compiler executable, e.g. clang or an LLVM-MinGW cross compiler')
    args = parser.parse_args()
    if args.target == 'windows' and args.arch != 'x86_64':
        parser.error('Windows ARM64 has not been configured')
    source = ROOT / 'native/godot_probe/probe.c'
    include = source.parent / 'include'
    lock = json.loads((source.parent / 'toolchain.json').read_text())
    digest = hashlib.sha256((include / 'gdextension_interface.h').read_bytes()).hexdigest()
    if digest != lock['interface_header_sha256']:
        parser.error('Vendored Godot interface header hash mismatch')
    output_dir = ROOT / 'presentation/godot/native/bin'
    output_dir.mkdir(parents=True, exist_ok=True)
    work = ROOT / 'build/3d-native'
    work.mkdir(parents=True, exist_ok=True)
    compiler = args.cc or ('cl' if args.target == 'windows' and platform.system() == 'Windows' else 'clang')
    if not shutil.which(compiler):
        parser.error(f'Compiler not found: {compiler}. See docs/3d/GETTING-STARTED.md.')
    if args.target == 'macos':
        output = output_dir / f'libalttp_probe.macos.{args.arch}.dylib'
        command = [compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-O2',
                   '-fvisibility=hidden', '-dynamiclib', '-arch', args.arch,
                   '-I', str(include), str(source), '-o', str(output)]
    else:
        output = output_dir / 'alttp_probe.windows.x86_64.dll'
        if Path(compiler).name.lower() in ('cl', 'cl.exe'):
            command = [compiler, '/nologo', '/LD', '/W4', '/WX', '/std:c11', '/O2',
                       f'/I{include}', str(source), '/link', f'/OUT:{output}']
        else:
            command = [compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-O2',
                       '-shared', '-I', str(include), str(source), '-o', str(output)]
    subprocess.run(command, cwd=work, check=True)
    print(f'Built: {output}')


if __name__ == '__main__':
    main()
