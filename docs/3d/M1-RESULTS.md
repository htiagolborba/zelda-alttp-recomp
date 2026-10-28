# M1 initial integration results — 2026-10-27

Project lead: **Hiran Tiago Lins Borba**. Development assistance: OpenAI Codex.

**Status:** the initial C/Godot integration works locally on macOS Intel. M1 is
still in progress; this is not a complete 3D port or a certified gameplay release.

## Evidence

| Check | Result and scope |
| --- | --- |
| SDL-free core build | Built a standalone C library without SDL window, input or audio-device code |
| Native Godot class | Registered `AlttpCoreBridge`; constructors, calls, structured errors and teardown tested in the actual engine |
| Cold-start parity | All 1,875 controlled ticks matched the reference SDL host |
| Read-only SRAM parity | Another 1,875 ticks matched; the original SRAM file hash remained unchanged |
| Compared data | RAM, SRAM, VRAM, SPC RAM, reference framebuffer and synthesized PCM; one FNV-1a checksum per tick |
| Godot versus standalone C | Same complete snapshot after 240 ticks with identical scripted input |
| AddressSanitizer | 2,000 ticks completed without a reported address error on the selected route |
| macOS renderer | Live 2D reference view displayed alongside the 3D blockout using OpenGL Compatibility on D700 |
| Windows | Gameplay GDExtension DLL cross-compiled; native Windows execution remains pending |

The parity routes cover startup/menu transitions and reach indoor gameplay.
They do not cover every room, enemy, combat action, inventory state or transition.
The checksum is non-cryptographic and the tests do not prove original SNES ROM
or cross-platform equivalence. Both hosts used the same explicit configuration
and the same offline audio schedule, not an asynchronous live audio device.

The PPU width must be explicitly configured to 256 pixels, matching the selected
framebuffer. That setup is performed by the original SDL main function and is
now also performed by the extracted host. The address-safety test includes the
framebuffer path and cleanup after this configuration was established.

![Actual C/Godot integration viewport](images/m1-core-integration.png)

This image was captured during the game's intro. The right panel is generated
by the same C simulation that supplies the snapshots. No second game process or
Godot gameplay controller generates that reference. The marker is hidden while
the C core is outside normal indoor/outdoor gameplay.

## Implemented interfaces

The Godot class accepts `open`, `step`, `snapshot`, `frame`, and `close` requests.
State is copied into versioned data/JSON rather than exposing mutable RAM to
GDScript. Keyboard/controller code produces the upstream 12-bit input layout.
Only keyboard/scripted input is covered by the local tests; physical controller
verification is still open.

PPU/HDMA and audio synthesis remain part of the tick. PCM output is muted.
An existing SRAM file may be imported read-only, and disk save requests are
suppressed and counted. The original stable SDL host keeps its disk-save path
because these changes are guarded by `ALTTP_CORE_HOST`.

## Open limitations

- One session per process, owned by one thread; restart to reopen.
- No audible PCM transport or persistent experimental saves yet.
- Diagnostic frame transfer uses a temporary hex/String path at 10 Hz.
- The scene's models and collision footprints are not mapped to the real area.
- A marker can follow source X/Y, but elevation, jump Z and animation semantics
  have not been integrated; raw Z is not treated as world height.
- Windows native loading, RTX Forward+ and physical controllers are unverified.
- The asset loader expects trusted, canonical locally extracted data; legacy
  assertions and all possible malformed-resource failures are not sandboxed.
- M0's Blender/animated-GLB workflow validation remains outstanding.

## Next gate

Validate the new CI boundary tests on both operating systems, broaden local
fixtures, implement proper PCM/save transport, and create a collision-aligned
indoor/outdoor graybox before expanding the visual content.

See [setup and architecture details](CORE-INTEGRATION.md) and
[the development update](../updates/2026-10-27-m1-core.md).
