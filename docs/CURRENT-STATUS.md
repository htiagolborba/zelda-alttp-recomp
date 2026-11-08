# Current development status — November 8, 2026

**Project lead: Hiran Tiago Lins Borba · Toronto, ON, CA.** This is a documentation checkpoint covering existing implementation through private candidate 85. It is not a new downloadable 3D release.

## Delivered and checked

| Track | Observed progress | Limit |
| --- | --- | --- |
| Public desktop game | Existing macOS/Windows packaging and upstream SDL2 controller input | Stable packages retain 2D graphics; physical controller/platform coverage remains bounded |
| Earlier C-driven 3D prototype | Selected house, cellar and outdoor gameplay-route evidence | Does not establish complete world/story coverage |
| Exterior visual baseline |82 resource records freshly rendered in candidate 84 |80 normal plus two special resources; partial art, not82 finished maps |
| Latest landscape kit |11 representative mixed-size resources rendered cleanly in candidate 85 | Affected-family checks, not a full85 atlas |
| Art-region browser | Realm/region selectors, Focus/Overview; actual UI rendering checked | Manual interaction coverage is not certified |
| Indoor visual inventory |320 retained source-resource records, including defaults/unused layouts | Not320 completed rooms; reused images do not certify the latest renderer |

Shared visual work includes source-aligned house facades/foundations/roof details, earth-path masks, water/ripples/shoreline foam, authored low banks, deterministic canopy variation and static actor previews. The missing-house predicate was repaired by comparing JSON numbers as explicit integers.

Interior inventory currently records22,412 supported descriptors including repeated layouts, partial adapters for 174/328 source object families,1,470 pending source entries and two explicit wrapped ceiling omissions. There are863 static indoor actor placements across175 records and 291 exterior first-part spawn previews. These counts measure data/art representation, not unique finished scenes, native AI or game completion.

## What remains

The miniature/diorama presentation is still experimental. R1 visual-region quality gate remains open. Main work: source-specific terrain and elevation, generic contour replacement, architecture fidelity/scale, source layers/overlays, special-area variants, missing object families, animation and broad native-state integration. The main pyramid remains unfinished.

Art studios remain separate from the broadly playable renderer. Authored0.35-unit banks do not recover native physical elevation. Static actor art does not prove animation, collision or combat. No reliable whole-remake completion percentage or finish date has been established.

## Working method

One agent, macOS first, visible geographic/content-kit batches. Reuse current assets and accepted evidence; run affected render checks for art, native regressions when behavior/C/audio/saves change. Review actual images because a clean process can still produce visually wrong output. Preserve rejected receipts, including the stale-region-width failure corrected before the final11-resource batch.

The broader art presentation will be connected to native gameplay after its visual production gates. No Windows build or new binary release is part of this update. See [the latest report](updates/2026-11-08-landscape-and-handoff.md), [AI handoff](AI-HANDOFF.md) and [image provenance](images/2026-11-08/manifest.json).
