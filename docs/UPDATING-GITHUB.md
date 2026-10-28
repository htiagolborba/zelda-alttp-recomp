# Maintaining the GitHub project history

Owner: Hiran Tiago Lins Borba. All public-facing updates should be written in English.

## For each meaningful implementation step

1. Update the README's latest-development summary and current status.
2. Add a dated entry to `CHANGELOG.md`, separating implemented, verified and pending work.
3. Add milestone notes under `docs/updates/` using [the template](updates/TEMPLATE.md).
4. Include an actual screenshot/recording where useful. Label static scenes,
   concepts and gameplay accurately; keep the source image under an appropriate
   documentation folder and use repository-relative Markdown image links.
5. Record verification details in the appropriate technical report. Do not turn
   a successful compile into a claim of tested gameplay or hardware support.
6. Commit the code and documentation together, or make a clearly named follow-up
   documentation commit. Push through GitHub Desktop and review Actions results.
7. Update pending CI evidence after the relevant workflow actually passes.

## Development updates versus game releases

A commit or a successful workflow does not require a new published game release.
README/changelog/milestone notes provide a continuous public development history.

Use a GitHub Release when there is a deliberate, clearly scoped version or
preview to distribute. A source-only infrastructure preview must be described
as such; do not attach an old stable 2D ZIP as if it were the new 3D prototype.
The M0 workflow currently uploads diagnostic logs/reports, not a playable 3D build.

For stable macOS/Windows package releases, use [the release procedure](RELEASING.md),
bump the required version fields together, validate the actual packages, and
review the platform notes. Existing versioned releases are not overwritten by
an unrelated development update.

## First recorded 3D milestone

- [M0 development update — October 27, 2026](updates/2026-10-27-m0.md)
- [M0 setup](3d/GETTING-STARTED.md)
- [M0 verification report](3d/M0-RESULTS.md)
- [Changelog](../CHANGELOG.md)
