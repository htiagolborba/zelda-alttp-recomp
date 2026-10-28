# 3D presentation blueprint

**Project:** Zelda ALttP — macOS & Windows
**Project lead:** Hiran Tiago Lins Borba · Toronto, ON, Canada
**Status:** Draft specification, revision 0.1 — 2026-10-25
**Scope:** Design specification. A minimal M0 native lifecycle probe and procedural scene now exist; an initial gameplay bridge is now implemented and tested locally, while the modeled game world remains unimplemented. See [M1 results](M1-RESULTS.md). See [M0 results](M0-RESULTS.md).

## 1. Product direction

Present A Link to the Past through a handcrafted miniature world while retaining
the existing C implementation of its gameplay. The visual reference is the
rounded, toy-like diorama presentation of Link’s Awakening for Nintendo Switch.

This is a new presentation layer using a publicly available engine and newly
authored assets. The Nintendo engine, source code, models, and animations are
not available in this project. A 2D texture upscale does not produce the target.

**First deliverable:** a small playable outdoor area connected to one interior,
with movement, one interaction, a basic attack, one simple enemy, a scene
transition, and save/load validation. These are completion criteria, not a
claim that these features are currently implemented in 3D.

## 2. Scope boundaries

Included in the first playable slice:

- One bounded outdoor space, preferably the area around Link’s house.
- One matching interior, after verifying its actual area/room IDs in extracted data.
- A newly authored stylized player model with a minimal animation set.
- A modular house, ground, tree, bush, rock, doorway, and one interactable prop.
- One enemy already governed by the C core, selected after the entity audit.
- Orthographic or near-orthographic camera, lighting, shadows, and readable HUD.
- Keyboard and Xbox-style controller input on Windows; macOS compatibility check.
- Original audio through a controlled bridge, plus a 2D reference/debug view.

Deferred: the full overworld, Dark World, bosses, every dungeon, swimming,
complex elevation puzzles, complete cinematics, multiplayer, new combat rules,
new items, and a full UI redesign. A static art scene may precede integration,
but it must be labeled as an art prototype rather than a playable remake.

## 3. Proposed stack and ownership

| Layer | Proposal | Responsibility |
| --- | --- | --- |
| Gameplay | Existing C code | Rules, movement, collisions, AI, damage, inventory, progression |
| Native adapter | C ABI with a thin C++ GDExtension wrapper | Lifecycle, input translation, snapshots, audio transport, save requests |
| Presentation | Godot 4 stable, exact version pinned after a compatibility spike | Scene graph, camera, animation, materials, UI, rendering |
| Scene logic | GDScript | View orchestration and tooling, not duplicated gameplay rules |
| Asset authoring | Blender; version chosen and pinned at the asset-pipeline spike | Meshes, UVs, rigs, animation, glTF 2.0 exports |
| Content tooling | Python | Local extracted-data inspection, conversion, schema validation |
| Delivery | Existing GitHub Actions plus native-extension/export jobs | Separate experimental 3D packages and reference 2D releases |

Godot 4.7.2 is now installed and tested for the M0/M1 prototype on macOS. The current bridge uses the C GDExtension interface directly; the proposed C++ wrapper is not installed. Cross-platform validation remains open.
GDExtension loads native libraries; it does not automatically make the existing
SDL executable an embeddable library. See [the architecture](ARCHITECTURE.md)
and [the engine decision](DECISIONS.md).

## 4. Development machines and graphics profiles

| Role | Machine | Policy |
| --- | --- | --- |
| Main 3D development and visual reference | User-reported Windows PC: Core i9-14900K, RTX 5060 Ti 16 GB | Evaluate Forward+ first; measure real performance and driver compatibility |
| Compatibility development/test | Observed macOS Intel system with AMD FirePro D700 | Evaluate Compatibility renderer; Metal support alone does not certify modern renderer support |
| Additional targets | Other Windows PCs and Apple Silicon | Not certified; add machines to the test matrix before advertising support |

Do not assume the two D700 GPUs form one combined rendering resource. Record
which adapter and renderer are actually active. Hardware names above describe
development machines, not published minimum requirements.

**Provisional performance targets, not measured results:**

- Windows reference PC: 1920×1080, 60 fps, frame-time p95 <= 16.7 ms over a
  repeatable 120-second slice route after warm-up; report p99 and stutters too.
- Mac compatibility profile: begin at 1280×720, 30 fps, p95 <= 33.3 ms on the
  same route. A 30 fps display must still preserve 60 core simulation ticks/s.
- Measure CPU, GPU, memory, loading stalls, and input latency before assigning
  sub-budgets or claiming minimum supported hardware.
- A higher-quality 1440p profile is optional after the slice passes; 4K is not a gate.

## 5. Visual specification

### Camera and scale

Use an inclined camera with initial pitch experiments around 45–60 degrees
below the horizon, a fixed world-aligned yaw, and orthographic projection first.
These are tuning ranges. Approve the camera against doorways, obstacles, attack
reach, and navigation before modeling the full slice.

Start with **16 source pixels = 1 world unit** as an adjustable conversion,
not a declaration of physical meters. Verify actual tile/object units in each
exported data format. Map game X/Y to the ground plane and represent jump Z
separately from floor/elevation. Never infer floor height from a jumping sprite.

The wider camera must not reveal incomplete neighboring areas. Define camera
bounds and masked borders independently from the original 2D scroll values.

### Shape, material, and lighting

- Rounded silhouettes, restrained bevels, chunky foliage, and readable props.
- Stylized PBR materials with painted color, moderate roughness, and controlled
  highlights; avoid photorealistic surface noise at gameplay scale.
- One primary directional light and restrained fill/environment lighting.
- Consistent contact shadows and ambient grounding; use authored/baked
  alternatives when a renderer lacks a selected screen-space effect.
- Optional subtle bloom and shallow diorama depth of field on the high profile.
  Disable depth of field by default during gameplay validation and on the
  compatibility profile; critical enemies and interactables must stay readable.
- Roof/wall fading or cutaways when the player is occluded. These affect the
  presentation only and must not change gameplay collision.

### Initial asset budgets

Working caps for the slice, to revise after profiling:

| Asset | Initial budget |
| --- | --- |
| Player | <= 15,000 triangles, one compact rig, <= 4 materials |
| Simple enemy | <= 8,000 triangles |
| Repeated environment prop | Usually 200–3,000 triangles; exceptions documented |
| Textures | 512–1024 for props; up to 2048 for a hero asset where justified |
| Lighting | One shadow-casting sun; extra shadow lights require a measured reason |

Count triangles after export. These caps are production constraints, not
predictions of what the hardware can handle. Prefer shared materials and
instancing for repeated vegetation. Keep an asset registry with creator,
source, license, revision, pivot convention, and intended semantic ID.

### Animation

Minimum player set: idle, walk, sword attack, interact, hit, and transition
visibility/fade. Use visual variants for facing as needed. Runtime positions
come from the core. Animation root motion must not move the gameplay entity.
Do not trigger damage from an animation event; it must follow the core state.
Exact attack phase and facing mappings remain audit tasks.

## 6. Functional requirements

- **FR-01:** Step one core instance at the established 60-tick cadence.
- **FR-02:** Preserve identical gameplay outcomes for the same initial state,
  feature configuration, input sequence, and controlled audio schedule.
- **FR-03:** Create immutable, versioned view snapshots after ticks; presentation
  must not write directly to gameplay globals.
- **FR-04:** Provide stable scene/entity identities, including slot generation.
- **FR-05:** Keep collision, combat, item interaction, and progression authoritative
  in C. Godot physics may serve debug queries or visual effects only.
- **FR-06:** Treat 3D model replacement as a semantic mapping, not sprite-tile
  replacement. Unknown entities get a labeled placeholder or explicit 2D mode.
- **FR-07:** Handle scene changes, reset, load, teleport, and discontinuities
  without interpolating across unrelated positions or identities.
- **FR-08:** Retain working reference rendering and expose it from the same tick
  stream. The debug view must not run a second gameplay simulation.
- **FR-09:** Preserve core audio semantics and synchronize access explicitly.
- **FR-10:** Use a separate experimental save directory; import reference SRAM
  by copying, never by modifying the only existing user save.
- **FR-11:** Record unsupported areas/features clearly. An automatic 2D fallback
  is a planned capability that must be implemented and tested before advertising it.
- **FR-12:** Release no ROM, extracted world data, or Nintendo Switch assets.

## 7. Definition of done for the first slice

- Player can traverse the selected area and interior, attack one enemy, perform
  one interaction, enter/exit a doorway, save, reload, and continue.
- Collision debug overlays align with visible obstacle footprints and doorways.
- Replay comparisons pass the defined deterministic fixtures before/after the
  host separation; audio scheduling is included in the fixtures.
- Keyboard and a physical Xbox-compatible controller pass the Windows checklist.
- macOS compatibility build loads the extension and displays the bounded slice.
- Camera does not hide critical gameplay or reveal unmapped regions.
- Both renderer profiles meet their measured targets or document an explicit
  revised target; no performance certification is inferred from the PC specs.
- Art sources and exported assets have recorded provenance and licenses.
- A new user can follow experimental setup instructions without replacing the
  stable 2D install or uploading a ROM to CI.

## 8. Milestones and gates

| Milestone | Concrete output | Gate before moving on |
| --- | --- | --- |
| M0 — Host/engine spike | Pinned Godot/build versions, extension smoke build, renderer report on both machines | Extension loads on Windows/macOS; renderer and driver selected from evidence |
| M1 — Core extraction | Headless-capable lifecycle and copied snapshots, reference tests | Same simulation results as the current host under controlled inputs/audio |
| M2 — Spatial graybox | Primitive player, ground, one doorway and obstacle; debug overlays | Coordinate/elevation mapping and scene transitions proven |
| M3 — Art target | One polished corner with original assets and camera/lighting presets | Visual direction accepted; screenshots labeled accurately |
| M4 — Playable slice | Integrated outdoor/interior slice, enemy, interaction, sound, saves | Functional and performance criteria above pass |
| M5 — Expansion plan | Asset coverage list, editor/converter workflow, measured effort per area | Decide whether and how to expand beyond the slice |

M1 and M2 protect the project from producing attractive scenes that cannot stay
aligned with the game. M3 can use a standalone art scene while M1 is investigated,
but no gameplay claims should be made for that scene.

## 9. Risks and mitigations

| Risk | Mitigation / stop condition |
| --- | --- |
| Core tightly coupled to host and PPU | Audit dependencies; retain emulated subsystem state; prove extraction before art expansion |
| 2D art encodes impossible 3D geometry | Author per-area height/cutaway overrides; document exceptions |
| Dynamic tile changes are missing from snapshots | Instrument relevant changes; test bushes, doors, destroyed objects, and scene phases |
| Audio affects logic/replay outcomes | Controlled APU schedule and serialized state access; compare with reference host |
| Renderer differs across older/newer GPUs | Separate presets and explicit parity criteria; test both machines early |
| Model production grows beyond capacity | Modular kit and a small slice; inventory coverage before promising a full remake |
| Asset availability mistaken for ownership | Author new assets; keep provenance and upstream attribution |
| 3D work disrupts stable releases | Experimental branch/packages and independent save namespace |

## 10. Decisions still open

1. Exact Godot/godot-cpp/Blender versions after M0.
2. Validated first area/room IDs and reproducible starting state.
3. Renderer profile supported by the D700 and which visual effects differ.
4. Minimal semantic events needed for the chosen enemy and interaction.
5. Whether to keep a transitional SDL audio backend during M1; the final host
   should have one explicit audio owner, not competing SDL and Godot devices.
6. Final camera, palette, character proportions, and asset quality bar after M3.

## References

- [Godot native extensions](https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/what_is_gdextension.html)
- [Godot renderer overview](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)
- [Godot 3D import formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
- [Godot procedural audio stream](https://docs.godotengine.org/en/stable/classes/class_audiostreamgenerator.html)
- Existing source audit: `zelda3/src/main.c`, `zelda_rtl.h`, `zelda_rtl.c`,
  `variables.h`, `audio.h`, and the local asset extraction tools.
