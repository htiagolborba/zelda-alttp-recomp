# Changelog

Project lead: **Hiran Tiago Lins Borba** · Toronto, ON, Canada.

This log separates implemented work from planned capabilities. A development
milestone is not automatically a new downloadable game release.

## Unreleased — experimental 3D laboratory

### 2026-10-27 — M1: initial C gameplay bridge

- Added an SDL-free C gameplay host, copied snapshots, Godot commands, native input mapping and a live reference panel from the same simulation.
- Preserved PPU/HDMA and scheduled muted audio synthesis; added optional read-only SRAM import and suppressed preview disk saves.
- Matched all 3,750 controlled ticks against the reference host (cold start and imported SRAM), matched Godot/standalone state after 240 ticks, and completed a 2,000-tick AddressSanitizer route.
- Cross-compiled the Windows gameplay DLL; native Windows execution remains pending.
- Added local verification scripts, no-ROM API-boundary CI tests, an actual capture, and [full M1 notes](docs/updates/2026-10-27-m1-core.md).
- Still pending: audible PCM output, persistent experimental saves, collision-aligned 3D areas, broader fixtures, physical-controller tests and Blender/GLB validation.

The following M0 entry records the earlier static baseline; its limitations describe that milestone at the time.

### 2026-10-27 — M0: first executable implementation

**Status:** M0 partially implemented; native lifecycle and rendering verified on
macOS. This is a static technical prototype, not a playable 3D port.

### Added

- Godot 4.7.2 toolchain lock with official download URLs and SHA-256 verification.
- Native C GDExtension lifecycle probe with ABI/version validation and explicit
  initialization/shutdown markers.
- Original procedural 3D scene with terrain, house, foliage, stationary marker,
  orthographic camera, lighting and shadows.
- Python setup/build tools, a real-engine headless smoke test, and a dedicated
  macOS/Windows diagnostic CI workflow.
- Actual macOS viewport capture, setup instructions and a verification report.

### Changed

- Stable release automation ignores 3D-only build scripts and preserves existing
  versioned releases instead of attempting to recreate them.
- Blueprint/backlog now distinguish the running M0 probe from the future gameplay bridge.

### Verified

- macOS native compilation, C ABI loading, real-engine initialization and shutdown.
- OpenGL Compatibility rendering on the AMD FirePro D700.
- Windows x86_64 DLL cross-compilation; execution on Windows remains pending.

### Not implemented / pending

- No C gameplay-core integration, controllable character, ALttP map conversion,
  combat, save integration, or final game models in the 3D scene.
- Windows native-engine load, RTX Forward+ evaluation, Blender version selection,
  and animated GLB import validation remain open.
- The new 3D workflow has not yet been verified remotely at the time of this entry.

[Full milestone notes](docs/updates/2026-10-27-m0.md) ·
[Setup](docs/3d/GETTING-STARTED.md) · [Evidence](docs/3d/M0-RESULTS.md)

## 2026-10-25 — desktop adaptation foundation

- Prepared macOS Intel and Windows x86_64 builds based on snesrev/zelda3.
- Added platform packaging, Triforce application icons, author credits and licenses.
- Added local ROM validation/asset preparation and ROM-free release packages.
- Created separate platform draft-release automation and verified the platform
  builds and Windows executable-loader check in GitHub Actions.
- User reported launching the macOS package successfully.
- Documented the 3D blueprint, architecture and phased implementation plan.

Original reverse-engineering work remains credited to snesrev/zelda3 contributors;
original game content belongs to Nintendo. See [CREDITS.md](CREDITS.md).


## Private research milestone — 2026-10-28

- Documented the C-driven animated 3D opening-room prototype and bounded macOS validation.
- Added an actual runtime 2D/3D comparison at matching simulation tick 6300.
- Clarified pending playable-slice, audio/save, Windows/controller and performance gates.
- No stable binary or public 3D assets changed. See [milestone](docs/updates/2026-10-28-styled-room.md).
