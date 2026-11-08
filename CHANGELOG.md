# Changelog

Project lead: **Hiran Tiago Lins Borba** · Toronto, ON, Canada.

This log separates implemented work from planned capabilities. A development
milestone is not automatically a new downloadable game release.

## Unreleased — experimental 3D laboratory

### 2026-11-08 — landscape presentation and portable development handoff

Documentation/screenshots milestone covering private work through candidate 85. Public stable binaries and early 3D scaffolding are unchanged; no new release or Windows build.

- Expanded private source/prop/actor art through82:22,412 descriptors including repeated defaults,174/328 partial source-family adapters, 1,470 pending entries, two ceiling omissions;863 static indoor placements in 175 records and 291 exterior first-part previews. Inventory is not completed gameplay.
- Restored missing source-aligned houses via explicit numeric door-predicate comparison; added shared facade/foundation/trim/roof details.
- Added source-mask earth paths and water/ripple/shoreline surfaces, authored offline low-bank volumes and deterministic canopy variation with preserved root anchors.
- Added interactive art-region navigation, Focus and Overview. Actual UI rendering checked; manual controls not fully exercised.
- Recorded82 clean fresh exterior resource renders in84 and eleven clean affected landscape renders in85. Preserved failed batch02 and its fresh-room-width repair; no new native gameplay acceptance inferred.
- Added full-area original BG2/3D plan comparison and four labeled real-capture boards with hashed provenance. Different framing/state and stand-in scenery are disclosed.
- Reorganized documentation navigation, current status, public/private architecture and Claude/AI entry points. Local private routing is ignored by Git; historical links preserved. Project overview and credits updated in English.
- Prepared an English LinkedIn draft with image order/alt text. Nothing posted automatically.
- Next: source-specific terrain/elevation, coherent region silhouettes, layers/overlays and architecture/special-area refinement; broader native-state integration follows the visual gates. No reliable game-wide percentage.

[Detailed report and comparisons](docs/updates/2026-11-08-landscape-and-handoff.md) · [Current status](docs/CURRENT-STATUS.md).

### 2026-11-02 — source-driven visual production milestone

This entry summarizes private implementation since the previous published checkpoint. The public commit contains documentation and screenshots only; stable binaries and public prototype code are unchanged.

#### Exterior content and architecture

- Retained 80 normal decoded overworld resource baselines and added separate offline previews for special resources 128 (grove/under-bridge shared resource) and 129 (Zora Falls). Special entrance transforms, story variants and runtime overlays remain pending.
- Expanded shared terrain/foliage/water/rock/path art and eight regional biome styles.
- Added 300 source-adjacent fence rails across the normal baseline; disconnected source gaps remain open.
- Added 27 local house composites across 16 resources, including one building represented by two boundary-clipped pieces. These are placements, not 27 unique buildings.
- Added 58 landmark placements, including cave/skull facades and first-pass sanctuary, temple and tower architecture. The main pyramid remains unfinished; a portal proxy is not a reconstructed pyramid.
- Added a textured two-leaf castle gate under the existing exact source closed-bar predicate, with a procedural fallback. Authored model fitting does not change native gate state or collision.
- Reused a shared triplanar stone material on appropriate castle/temple/sanctuary masonry while preserving presentation cutaways.
- Extended art-only first-part exterior actor previews from 134 to 147 placements, including 13 static Armos placements. No AI, statue activation or combat acceptance is implied.

#### Indoor visual production

- Produced a fresh 320-resource art baseline, including unused/default-only resources. This does not represent 320 completed playable rooms.
- Prepended all eight literal native base layouts before per-resource object layers.
- Compiled 19,972 supported source-object descriptors, including repeated base-layout objects. Added partial source-order floor/wall cell composition and grouped geometry.
- Expanded walls/corners, floor fills, ceiling masks, rails, block rows, furniture, stairs, carpets, torches, water, spikes, holes, columns, statues and curtains.
- Added 508 static portal archetypes: 300 ordinary, 105 small-key and 103 two-way shutter descriptors. Runtime lock and shutter behavior remain deferred.
- Added 715 straight edge descriptors: 326 water edges and 389 pit edges. Native conditional endpoint/corner semantics remain incomplete.
- Reused converted wooden flooring and shared stone materials; propagated authored themes through 21 nonconflicting source palette groups. These themes do not certify native RGB colors or dungeon membership.
- Expanded static actor art to 286 source placements in 87 indoor resources, including Orange Stalfos, Gibdo, Wizzrobe, Bubble and Leever adapters. Source plane tags are retained; elevation, spawning and state rules are unfinished.

#### Production efficiency, verification and recorded issues

- Moved to reusable content batches and render/load checks rather than repeated cellar gameplay runs. Existing native gameplay routes remain separate evidence.
- Added incremental image reuse only when room JSON is identical, preserving image hashes and actual rendering provenance. Retained images are not current-renderer validation.
- Rendered all 320 resources freshly in batch 56, followed by targeted deltas of 230 themed, 62 edge-trim and 28 actor-bearing resources. Successful batches reported no logged errors or failed PNG writes.
- Preserved failed receipts: a Leever clip required an isolated repair; static Armos acceptance does not resolve its earlier animation failure; scenery-template cleanup and a material typing error were fixed before clean replacement renders.
- Kept two wrapped resource-268 ceiling strips as explicit omissions. Unknown overlay semantics, BG1/BG2 ordering and unsupported families remain documented.
- Added five comparison/gallery boards with hashed source-image provenance: original/reference vs. redesigned presentation, earlier/current interiors, and six exterior environments.
- Refreshed the README, detailed development report, GitHub discussion draft, LinkedIn draft and GitHub Desktop commit instructions in English.

#### Scope and next work

- Current production target: macOS. No Windows build, new release, native C behavior change or gameplay replay was performed for this documentation update.
- Private models, textures, ROM/game data, keys, saves, absolute private paths and prototype candidates are excluded from the public changes.
- Next: remaining visual families, source layers/overlays, special architecture and refinement; then broader native-state gameplay integration and route validation.
- [Full report and image gallery](docs/updates/2026-11-02-visual-production.md). Upstream reverse engineering remains credited to snesrev/zelda3; original game/art belongs to Nintendo.

### 2026-11-01 — private macOS prototype progress

- Published three same-state, side-by-side screenshots from actual original/3D rendering sessions: opening house, house exterior and pot carrying.
- Documented private connected outdoor presentation, reusable indoor props, carry animations, native PCM audio, isolated saves and Game Over/continue recovery.
- Recorded bounded regression evidence, source-map pipeline coverage and explicit unfinished work; offline previews and conversion checks are distinguished from live gameplay.
- Added an English LinkedIn draft and comparison-image posting guide.
- Documentation milestone only: no private models, textures, game data, keys, saves or prototype candidate files are published; stable downloads remain 2D. No Windows build was requested for this update.
- See [the detailed update](docs/updates/2026-11-01-native-3d-progress.md).


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
