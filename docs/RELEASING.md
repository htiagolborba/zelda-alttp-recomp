# Release procedure

Release owner: Hiran Tiago Lins Borba · Toronto, ON, Canada.

## Before the first upload

The local workspace was originally inside a parent Git repository. Publish this
project as its own repository; do not add or push the parent Desktop directory.
Review the source file list before creating a commit. `.gitignore` excludes ROMs,
extracted resources, local applications, toolchains, builds, and release archives.
Never force-add those ignored resources.

The source repository must retain the original license notices. Runtime game
resources are generated locally from the user's ROM, not checked into GitHub.
The packager copies an explicit file set and checks for ROMs and runtime assets.

## Version and builds

1. Update `VERSION`, the diagnostic `--version` text in `zelda3/src/main.c`, and
   the version resource in `packaging/windows.rc` together.
2. Update release notes for each platform.
3. Run the Platform releases workflow with the version and drafts disabled.
4. Download both artifacts. Check their `.sha256` files and internal manifests.
5. Validate the extracted artifacts on real target machines.

## Manual validation checklist

- [ ] Windows executable loader check passes on the Windows CI runner.
- [ ] macOS app starts from the extracted archive after local asset preparation.
- [ ] Windows launcher starts the game after local asset preparation.
- [ ] ROM extraction rejects an incorrect hash with a clear error.
- [ ] Title screen, new game, movement, combat, and room transitions work.
- [ ] Audio playback works without obvious glitches.
- [ ] Configuration and saves persist after restart.
- [ ] Keyboard controls match the README.
- [ ] Xbox controller input is tested over Bluetooth and USB where available.
- [ ] Archive contains all required licenses and credits.
- [ ] No ROM, `zelda3_assets.dat`, extracted maps, or extracted audio is included.
- [ ] Release notes describe actual tests and known limitations.

The executable `--version` check verifies loading and SDL linkage; it does not
exercise rendering, audio playback, game logic, saves, or controller hardware.
CI does not receive a ROM and therefore does not perform gameplay tests.

## Create the two releases

Run Platform releases with `Create draft releases` enabled. The workflow creates
`v<VERSION>-macos` and `v<VERSION>-windows`, each with its own ZIP and checksum.
Existing releases are not overwritten automatically. If a draft already exists,
inspect it before changing or replacing its files.

Review both drafts on GitHub, then publish them. Link to the published release
pages from the README and any announcement. Do not claim native Apple Silicon
support, a completed visual remake, or verified controller compatibility beyond
what has actually been tested.

## Current local validation

- macOS reference build: compiled with Apple Clang 21.
- Windows build: cross-compiled with LLVM-MinGW 20260616 and SDL2 2.32.10.
- Windows execution and gameplay: pending a Windows runner/device.
- GitHub workflow: prepared locally; execution in the destination repository pending.
- Visual and physical controller tests: pending.
