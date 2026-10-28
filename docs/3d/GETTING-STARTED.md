# Run the M0 3D laboratory

For the optional live C integration, see [CORE-INTEGRATION.md](CORE-INTEGRATION.md). The no-ROM M0 mode described here remains available.

Owner: Hiran Tiago Lins Borba. Status: an executable lifecycle/renderer probe,
not a playable 3D port. No ROM is loaded by this prototype.

## What is implemented

- Godot 4.7.2 pinned by official release URL and SHA-256.
- A small C GDExtension with an explicit ABI revision, version check,
  initialization and shutdown callbacks. The official generated interface
  header is vendored with its original copyright/license notice.
- An original procedural scene: terrain, house, foliage, a stationary marker,
  directional lighting and an orthographic camera.
- A real-engine headless test that verifies library loading, scene creation,
  report output and clean native shutdown.
- A separate CI workflow for Windows x86_64 and macOS Intel lifecycle tests.

The probe does **not** expose gameplay state, bind the C core to GDScript,
provide a controllable Link, load ALttP maps, or contain final character art.
The eventual C++ scene bridge is still planned; the M0 library deliberately
uses the C interface directly to validate the smallest native boundary first.

![M0 procedural laboratory on macOS, without gameplay integration](images/m0-laboratory.png)

## Windows: main development PC

1. Pull the latest project commit on the Windows PC.
2. Install Python 3.10+ if it is not already available.
3. Install Visual Studio Build Tools with the Desktop development with C++
   workload, including the MSVC x64 compiler and Windows SDK. Use an x64
   Native Tools / Developer Command Prompt so `cl` is on PATH.
4. From the repository root in that command prompt:

```bat
python scripts\setup-godot.py
python scripts\build-godot-probe.py
python scripts\test-godot-probe.py --godot .tools\godot-4.7.2\Godot_v4.7.2-stable_win64_console.exe
```

The setup script downloads only the official engine archive and checks its
pinned hash before extracting it into `.tools/`. The build uses MSVC; no Godot
C++ binding package or third-party Python dependencies are needed for this probe.

Open the Compatibility baseline first:

```bat
.tools\godot-4.7.2\Godot_v4.7.2-stable_win64_console.exe --path presentation\godot --rendering-method gl_compatibility
```

Then evaluate Forward+ on the RTX PC:

```bat
.tools\godot-4.7.2\Godot_v4.7.2-stable_win64_console.exe --path presentation\godot --rendering-method forward_plus
```

The explicit command-line override leaves the cross-machine Compatibility
default intact. Record actual renderer, driver and adapter from the engine log.
Mouse wheel adjusts zoom; Escape exits. There is no gameplay movement yet.

## macOS Intel

Install Apple's Command Line Tools if needed, then run from the repository root:

```sh
python3 scripts/setup-godot.py
python3 scripts/build-godot-probe.py
python3 scripts/test-godot-probe.py \
  --godot .tools/godot-4.7.2/Godot.app/Contents/MacOS/Godot
.tools/godot-4.7.2/Godot.app/Contents/MacOS/Godot \
  --path presentation/godot --rendering-method gl_compatibility
```

The current local machine has been tested with the D700 OpenGL Compatibility
renderer. That does not certify other GPU/driver combinations or Apple Silicon.
An `--arch arm64` compile option exists, but its output must be tested on the
matching machine before claiming support.

## Capture a viewport and hardware report

Create a `build/m0` directory first. Use absolute output paths:

```sh
/path/to/Godot --path presentation/godot --rendering-method gl_compatibility \
  -- --capture=/absolute/path/build/m0/laboratory.png \
     --report=/absolute/path/build/m0/renderer-report.json
```

On Windows use the same arguments with the console EXE, Windows absolute paths,
and quotes around paths with spaces. `--capture` waits 90 frames, exports the
viewport and exits. The JSON records renderer, adapter, engine and whether the
native extension loaded. The short static frame-time sample is **not** the
blueprint's 120-second gameplay benchmark.

`--report` alone does not automatically end an interactive run. For a headless
report without rendering use the supplied smoke-test script.

## Expected smoke-test markers

```text
ALTTP_NATIVE_READY abi=1 godot=4.7.2
ALTTP_SCENE_READY native_loaded=true gameplay_connected=false
ALTTP_M0_REPORT ...
ALTTP_NATIVE_STOPPED
PASS: Godot loaded the native probe, initialized the scene, and shut down cleanly.
```

A missing library, wrong engine version, script error or missing lifecycle marker
fails the test. Logs and JSON reports are written under `build/3d-native/`.
Native binaries, engine downloads and `.godot/` caches remain ignored by Git.

## CI and remaining M0 work

The `3D native probe` workflow builds the library and runs the actual engine
headlessly on both target OSes. It uploads logs/reports, not a playable release.
Headless success does not test a real GPU, controller, audio output, or gameplay.

Still required: Windows MSVC build/load test, Forward+ rendering on the actual
RTX PC, the cross-machine visual comparison, pinned Blender tooling and animated
GLB import round trip. Only then close M0 and begin the gameplay-core extraction
specified in [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md).
