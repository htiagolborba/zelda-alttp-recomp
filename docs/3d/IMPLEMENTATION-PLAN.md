# First implementation backlog

Status: M0 partially implemented. See [M0 results](M0-RESULTS.md) for verified work and [setup instructions](GETTING-STARTED.md) to run the laboratory. Remaining milestones are proposed work.
Owner: Hiran Tiago Lins Borba.

## M0 — Validate the development path

- Record Windows version, GPU driver, Godot renderer/driver and editor version.
- Pin a stable Godot build and matching native-extension bindings.
- Build a minimal native extension that loads, reports a version and unloads.
- Repeat the extension load test on the Intel Mac.
- Show the same small original-geometry scene on Forward+ and Compatibility.
- Record a frame-time capture and screenshot for each profile.
- Select and pin Blender/export settings; confirm animated GLB round trip.

Deliverable: a reproducible toolchain and compatibility report. Do not install
or generate the full game's art before this gate.

## M1 — Prove the gameplay boundary

Initial implementation and scoped parity tests are now recorded in [M1 results](M1-RESULTS.md). Audio output, persistent experimental saves, wider fixtures and native Windows validation remain open.

- Inventory dependencies of asset loading, initialization, stepping, reference
  rendering, replay, audio and file access.
- Extract host services incrementally while preserving the SDL executable.
- Provide structured error handling, one-instance lifecycle and cleanup.
- Implement a minimal copied snapshot: scene identity and player state first.
- Define input mapping, audio schedule and deterministic comparison fixtures.
- Compare the old and new hosts before adding model complexity.

Deliverable: C-core bridge proof with documented limits and reference comparison.

## M2 — Align primitive geometry with gameplay

- Identify Link’s house area/room data and a reproducible start state.
- Define origins/units and author a tiny local map overlay.
- Show capsules/boxes and validated movement from core snapshots.
- Visualize obstacle footprints and interaction/transition regions.
- Test interpolation, facing, jump/elevation distinction and one doorway.
- Add stable entity generations and a resynchronization path.

Deliverable: graybox video with debug overlays, no independent Godot movement.

## M3 — Set the art target

- Produce a player silhouette study and one environment kit.
- Build one polished corner at the actual gameplay camera scale.
- Tune color, materials, lighting, readability and roof cutaway behavior.
- Maintain original asset provenance and actual triangle/material counts.
- Capture both renderer profiles and accept their intentional differences.

Deliverable: approved visual target scene; label it as a prototype.

## M4 — Assemble the playable slice

- Integrate one enemy, one interaction, one attack, hurt feedback and visibility.
- Preserve core audio and HUD information required for play.
- Validate external/interior transitions and the experimental save namespace.
- Test keyboard and Xbox controller on the actual Windows PC.
- Run the repeatable performance route and record p95/p99 frame times.
- Package experimental builds separately from stable reference releases.

Deliverable: a bounded playable preview that meets BLUEPRINT.md acceptance criteria.

## Required inputs for the next work session

1. Access to the Windows checkout and the ability to run Godot/native builds.
2. A local compatible ROM/asset bundle on that PC; it must not be uploaded to CI.
3. Confirmation of Windows/driver versions during M0, not guessed from GPU model.
4. Visual choices to review through the first art target, rather than committing
   to an untested camera or complete model set in advance.

## Progress reporting

Report each milestone as planned, in progress, blocked with a concrete reason,
or verified with evidence. Record build/load tests separately from gameplay and
art acceptance. Update the public README only when capabilities are implemented
and tested; keep future visuals clearly identified as work in progress.
