# macOS setup and development entry points

**Hiran Tiago Lins Borba · Toronto, ON, CA**

[Project profile](https://github.com/htiagolborba) · [Credits](CREDITS.md)

## Choose the right workflow

For the stable desktop game, use the [main README](README.md#getting-started), [macOS release notes](docs/RELEASE-NOTES-macos.md) and [release procedure](docs/RELEASING.md). Stable packages retain the original 2D presentation.

For current private 3D work, start with [current status](docs/CURRENT-STATUS.md) and [Claude/AI handoff](docs/AI-HANDOFF.md). On the owner's Mac, an ignored local pointer routes to the private implementation. The early public Godot laboratory is not private checkpoint 85.

## Existing native build path

The recorded local baseline is Intel x86_64 macOS with Apple Clang/Command Line Tools and SDL2. No Apple Silicon native build or physical-controller compatibility is newly verified by this documentation update. Do not reinstall working tools merely to resume documentation or art work.

Use the main README's asset-preparation instructions with your own compatible USA revision 0 ROM. Public releases do not include a ROM or generated runtime assets. The code in zelda3/ is the existing reverse-engineered C reimplementation from snesrev/zelda3; extracting data does not recover Nintendo's original source code.

After preparing local assets/dependencies, run `./build-macos.sh` from the repository root. Rebuilding the executable does not automatically update an existing application bundle; follow the release packaging instructions for a new bundle.

The supplied application launcher resolves configuration/assets/saves under `~/Library/Application Support/Zelda ALttP/`. Back up saves before replacing a package. Current stable application bundles are not Developer ID signed/notarized. Launch, audio, controller, save and transition checks must be reported within their actual tested scope.

Historical machine-specific extraction commands and initial setup observations have been superseded by the maintained public instructions above. They are retained in Git history, not presented as the current working environment.
