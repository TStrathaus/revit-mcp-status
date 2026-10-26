# Rules and setup for approval

State 26.10.2026. What changed in the modelling rules and in the setup, for the user to approve, change or
reject. Approved items lose their "proposed" mark in the guideline (`scan2revit/skills/modeling/SKILL.md`);
rejected ones are taken out, with the reason in `documentation/decisions.md`.

## 1. Modelling rules

| Rule | State | What it says | Why |
|---|---|---|---|
| G-9.2 Room separation lines | **set by the user** 26.10.2026; wording to confirm | Walls with their doors and openings bound a room. A separation line only (1) where a room does not close otherwise: one short line across the gap (passage, wide opening, a wall piece the scan did not see); (2) where the input divides a space without a wall (a foyer drawn as "Entrance" and "Foyer"). Never along whole room outlines, never where a wall stands, never more lines than it takes. A room that still does not close is listed for the person. | The rule of 25.10.2026 drew a line along every room edge outside a wall: 1240 lines on a four-storey house, most of them useless. The code still follows the old rule: it is rebuilt to the new one once the rule is confirmed. |
| G-6.5 Slab inside the building | proposed | A slab never reaches beyond the building. A scan holding inside and outside together is split by the exterior walls; the outside points are used as the external scan (G-6.3: outline at the facade). Floor points outside the exterior walls (terrace, terrain) are not slab; a balcony or terrace slab is its own element and is listed. | The house build's slabs ran out over terrace and garden in ragged shapes. |
| G-8.3 Columns | proposed | Free-standing columns found in the scan become column elements (structural families first, else architectural) of their shape, rectangular or round, at their place and rotation, from their level to the storey height; a column's faces are not also walls. | Columns from scans are built now (F8); the checks use this rule. |
| G-11.7 Column type names | proposed | `scan2revit column <w> x <d> mm`, `scan2revit column round <d> mm`, to 10 mm. | Same naming as walls and floors. |
| G-11.8 Model file name | proposed | `<project>_v<setup>_<info>.rvt`, e.g. `house_v0.8.0-9459e42_scan-only.rvt`. | Asked by the user: project, version and short info in the file name. |
| G-13.5 Build register | proposed | Every build is recorded with its setup (Builds page). A later setup never overwrites a build: a rebuild gets a new file next to the old one; test models are kept the same way. | Asked by the user: builds listed with the setup version they were built with. |

## 2. Setup

| Item | State | What it is |
|---|---|---|
| Setup version | **0.8.0** set 26.10.2026 | scan2revit version (`pyproject.toml`) plus the git commit; `+dev` when tracked files were changed and not committed. Minor version up when what a build produces changes (new element kind, new route, changed rule); fixes keep the version and differ by the commit. History on the Versions page. |
| Model file names | built | `revit_project.py open --info "scan only" [--inputs ...] [--rebuild]` names the model by G-11.8; the e2e runner names its test models `<example>_v<setup>_e2e.rvt`. Projects from before keep `model.rvt`. |
| Build register | built | `scan2revit/data/builds.json` (on this machine, git-ignored: it names real projects); `py -m scan2revit.core.builds list`; the Builds page is rendered from it on every publish, real projects private. |
| Test models kept | built | The e2e runner saves every built model through Revit's Save button next to its report (`--no-keep-models` to skip). |
| Revit dialogs | built | Revit's Save is found on Revit's main window (not a hidden helper window) and pressed without the mouse; a minimized Revit is restored first. |
| pyRevit agent policy | **auto** (set 26.10.2026 at the user's request) | No "allow changes from pyRevit" prompt in Revit. Stages delete only their own elements (G-13.1). |
| Template | `revit_test/blank.rvt` | The blank project every build copies; its file hash is in each build's record. It has **no column family**: decision below. |
| Revit, pyRevit | Revit 2025, pyRevit 7 | Recorded per build. |

## 3. Open decisions

| Decision | Options | Proposal |
|---|---|---|
| Column family for the columns stage | (a) the user loads a rectangular and a round column family into `blank.rvt`; (b) the stage makes its own simple family from Revit's family template | (a) now, (b) later |
| Separation lines in the scan route | rebuild the slice route's room closing to G-9.2 (gap lines only) before the next build | after G-9.2 is confirmed |
| Slab outline from one combined cloud | build the inside / outside split (G-6.5) and run the facade step on it | after G-6.5 is approved |

## 4. Questionable results (open tasks, kind "Questionable")

Slab outlines over terrace and garden; 1240 separation lines; 11 openings on four storeys of a house; columns in a
house not verified; storey heights from scan and sections differ by 10-17 cm on two storeys; plan images not
cropped to the building. Details and next steps: Open items page.
