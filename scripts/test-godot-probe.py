#!/usr/bin/env python3
"""Run the real Godot lifecycle smoke test without a ROM, SDL, or a display."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', required=True, type=Path)
    parser.add_argument('--core-api', action='store_true', help='Also test the core class and structured errors without ROM assets')
    args = parser.parse_args()
    output = ROOT / 'build/3d-native'
    output.mkdir(parents=True, exist_ok=True)
    report = output / ('headless-core-api-report.json' if args.core_api else 'headless-report.json')
    if report.exists():
        # Do not accept a stale report from an earlier successful run.
        report.replace(output / 'headless-report.previous.json')
    command = [str(args.godot.resolve()), '--headless', '--path',
               str(ROOT / 'presentation/godot'), '--', '--core-api-smoke' if args.core_api else '--smoke', f'--report={report}']
    run = subprocess.run(command, capture_output=True, text=True, timeout=45)
    log = run.stdout + run.stderr
    (output / ('headless-core-api-test.log' if args.core_api else 'headless-test.log')).write_text(log)
    print(log)
    if run.returncode or 'SCRIPT ERROR:' in log or 'ERROR:' in log:
        raise SystemExit('Godot smoke test failed; inspect build/3d-native/headless-test.log')
    for marker in ['ALTTP_NATIVE_READY abi=1 godot=4.7.2', 'ALTTP_SCENE_READY',
                   'ALTTP_M0_REPORT', 'ALTTP_NATIVE_STOPPED']:
        if marker not in log:
            raise SystemExit(f'Missing lifecycle marker: {marker}')
    if args.core_api and 'ALTTP_CORE_API_SMOKE_PASSED no_assets=true' not in log:
        raise SystemExit('Native core API boundary test did not pass')
    result = json.loads(report.read_text())
    assert result['native_extension_loaded'] is True
    assert result['gameplay_core_connected'] is False
    print('PASS: Godot loaded the native probe, initialized the scene, and shut down cleanly.')


if __name__ == '__main__':
    main()
