# Architecture decisions — draft

Owner: Hiran Tiago Lins Borba. Date: 2026-10-25.
All decisions below are proposed until their validation gates pass.

## ADR-001 — Retain the C gameplay core

Retain existing rules and implement a presentation bridge. Rewriting gameplay
inside a new engine would duplicate years of reverse engineering and make
behavioral regressions harder to isolate. PPU/APU dependencies still require
an audit; this is not a promise that core extraction is straightforward.

## ADR-002 — Evaluate Godot 4 plus GDExtension first

| Candidate | Fit for this project | Cost / tradeoff |
| --- | --- | --- |
| Godot 4 + native bridge | Scene editor, 3D pipeline, desktop exports, native-library extension path | Extract the C host, maintain ABI/builds and renderer profiles |
| Unity + native plugin | Established scene/animation tools and native plugin path | Additional C# layer, runtime/tooling and licensing evaluation |
| Unreal + native module | Extensive 3D tooling and C++ integration | Larger build/tooling footprint and more infrastructure than the first slice needs |
| Custom renderer in the SDL host | Close to current C loop | Must build scene tools, animation, materials, lighting and content pipeline |
| Nintendo Switch game's engine | Not an available project dependency | Engine/source/assets are not supplied or licensed for use here |

Recommendation: first test Godot, because a scene/asset editor and native-library
boundary suit the proposed slice. This is an engineering judgment, not a claim
that other engines are incapable. Pin exact compatible Godot/godot-cpp versions
only after Windows and macOS extension smoke tests.

## ADR-003 — Windows high profile and Mac compatibility profile

The user supplied an i9-14900K / RTX 5060 Ti 16 GB Windows PC for development.
Use it for Forward+ evaluation and visual authoring. Keep the Intel/D700 Mac as
a Compatibility renderer test machine. Renderer feature parity is not assumed;
accept authored lighting alternatives while preserving gameplay readability.
Measure before publishing fps claims or minimum specs.

## ADR-004 — One core, two possible presentations

Support one gameplay instance. Debug 2D and new 3D views consume the same tick
stream. Do not advance a second core to generate a reference image. Keep stable
2D packages available independently from experimental 3D packages.

## ADR-005 — Original asset production

Author models, materials, rigs and animations rather than extracting them from
Link’s Awakening. Use glTF 2.0 as the proposed interchange format. Keep derived
ALttP map data local and separate from distributable original art.

## ADR-006 — No production rollout before a slice

Choose one outdoor/interior pair and a tightly bounded feature set. Measure the
integration and asset effort there before estimating a complete game. No full
remake deadline is assigned by this blueprint.

## Evidence and documentation

- [Native libraries with GDExtension](https://docs.godotengine.org/en/stable/tutorials/scripting/gdextension/what_is_gdextension.html)
- [Renderer choices and hardware tradeoffs](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)
- [Recommended 3D import formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
- Local source audit recorded in ARCHITECTURE.md.
