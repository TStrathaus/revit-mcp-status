# Drawings and scans together: 2D information as the prior for modelling

State 26.10.2026: the facts reader (`scan2revit/plans/facts.py`, F17) and the review page (F18) are built; alignment, conflicts and drawn facts as priors (F19, F20) are not. Decided by the user on 24.10.2026: the 2D drawings are
analysed **first** and act as the prior; the scan measures the geometry and wins on geometry; the drawings win
on what a scan cannot see. Every extracted piece of information is a **fact** in `facts.json` per project; a
person verifies the facts on a **review page** at gate 1 before the builders use them. Decisions:
`decisions.md`; the local LLM's part: `local-llm.md`; the feature list: `open-tasks.md` (F17 to F24).

## 0. What the analysis looks for first (user, 26.10.2026)

The analysis of drawings and documents looks first for the **construction**: the materials, the structure
(load-bearing or not, concrete, masonry, timber, steel), and the **thicknesses and layers of slabs and walls**
(build-up legends, section details, wall types in a legend, specifications). Geometry the scan measures better
comes second.

**Independent sources only verify each other.** Drawings made from the scan (or from a model built from the scan)
carry the scan's own values: they are not a second source. Each source in `facts.json` records where it comes
from (`origin`: design, construction, as-built survey, derived from the scan); facts of a source derived from the
scan are not used as a check against the scan. (26.10.2026: a test house's plan set had been drawn from the model
of its point cloud, so its storey heights and walls could not verify the scan.)

## 1. Why

A scan sees surfaces: wall faces, floor tops, ceiling undersides, openings where they are open. It does not see
what is inside a wall or slab, behind furniture, above a suspended ceiling, the names of rooms, or the build-up
of a floor. Drawings carry exactly that, but they show the design, not necessarily the building as it is. So:

| Question | Who answers it | Why |
|---|---|---|
| Where is a wall face, a floor top, an opening edge | scan | measured; drawings may be outdated |
| How thick is a wall seen from one side only | drawing (verified), else assumed | the scan sees one face |
| What is a slab made of, how thick is the structural slab | section or build-up legend | the scan sees only the finished surfaces |
| Storey heights, levels (OK FFB, OK RFB, UK RD) | scan where seen; drawing for the rest and as a check | sections carry every level, scans only what was scanned |
| Room names, numbers, units, use | drawing (room stamps, room schedules) | not in a scan |
| Door and window sizes, sill and head where the scan saw none | drawing (labels, elevations, schedules) | a closed door or a slice route shows no head |
| Walls the scan missed (behind furniture, dense floors) | drawing as hypothesis, scan as test | the drawn wall tells the detector where to look |

Conflicts beyond the tolerance of a fact type (table 3) go to a person; the model never quietly takes the
drawing over a measurement.

## 2. Catalogue: what 2D sources carry and how to get it

Sources by kind: **plan** (Grundriss), **section** (Schnitt), **elevation** (Ansicht), **detail / build-up
legend** (Aufbauten, Details), **schedule** (door, window, room lists), **site plan** (Situation, Lageplan),
**title block** (on every sheet). Methods: **V-text** text of a vector PDF or DXF read by rules (patterns,
position); **V-geom** vector geometry (fills, lines, arcs, hatches); **R-vision** raster or scanned sheets
(own reader, plan-extract, local vision model); **LLM-text** a text block classified or parsed by the local
LLM when the rules give no clear answer (always proposed, never accepted automatically); **human** entered on
the review page.

| # | Information | Source | Method | Fact type | Used by (stage) | Verify |
|---|---|---|---|---|---|---|
| 1 | Scale (1:50, 1:100) | title block, scale bar | V-text, else dimension chains | `sheet.scale` | every reader | yes, once per sheet |
| 2 | Sheet kind, storey, plan number, date, revision | title block | V-text, LLM-text | `sheet.meta` | intake, ordering | bulk |
| 3 | Storey drawings on a sheet and their labels | plan | V-geom clusters + labels (built: `plans/sheet.py`) | `sheet.drawing` | plans man | bulk |
| 4 | North arrow, orientation | plan, site plan | V-geom (arrow symbol), human | `site.north` | structure man (true north) | yes |
| 5 | Survey coordinates, footprint on the site | site plan | V-text (LV95 values), V-geom | `site.position` | structure man, alignment | yes |
| 6 | Levels: OK FFB, OK RFB, UK RD per storey | section, elevation, plan level marks | V-text (+2.75, ±0.00, labels) + level symbols (A2 in development) | `level.mark` | structure man | yes |
| 7 | Storey height, clear room height | section | from 6; room height labels (LH 2.40) | `level.height` | structure man, rooms | from 6 |
| 8 | Floor build-up: layers, thickness each, total | section, build-up legend | V-text block near the cut ("Parkett 15, Unterlagsboden 70, Trittschall 20, Beton 220"), LLM-text to parse | `buildup.floor` | load-bearing man (slab thickness), family man | yes |
| 9 | Wall build-up: layers, total thickness | build-up legend, details, plan hatches | V-text, hatch pattern per layer | `buildup.wall` | family man, load-bearing man | yes |
| 10 | Roof build-up, roof pitch, eaves and ridge heights | section, elevation | V-text, V-geom (roof lines) | `roof.*` | later: roofs | yes |
| 11 | Wall position and thickness | plan | V-geom (built: wall pairs, wall fills) | `wall.drawn` | prior for detection and for one-sided walls | conflicts only |
| 12 | Wall kind: load-bearing, masonry, concrete, drywall | plan hatches, legend | V-geom hatch classes, LLM-text for the legend | `wall.kind` | family man (later typed walls) | yes |
| 13 | Openings: position, width | plan | V-geom (built) | `opening.drawn` | fit man (prior), check | conflicts only |
| 14 | Door and window labels (T 90/210, F 120/140, BRH 90) | plan | V-text near the opening, LLM-text where unclear | `opening.size` | fit man: width, height, sill | yes |
| 15 | Swing side and hinge | plan | V-geom (built: arcs, swing chains) | `opening.swing` | fit man | conflicts only |
| 16 | Window sill and head heights | elevation, section | V-geom (window outlines against levels) | `opening.heights` | fit man (replaces assumed heights of the slice route) | yes |
| 17 | Room stamps: name, number, unit, area, floor finish | plan | V-text (built: `plans/sheet.py` stamps), LLM-text for odd stamps | `room.stamp` | fit man (rooms) | bulk; conflicts |
| 18 | Room schedule: name, number, area, use | schedule | V-text table reader, LLM-text | `room.schedule` | fit man, check (areas) | yes |
| 19 | Stairs: risers, riser and tread (17 St. 17.6/27), direction | plan, section | V-text, V-geom (built for plans) | `stair.drawn` | load-bearing man (stairs) | yes |
| 20 | Slab openings, shafts | plan (crossed boxes, labels), section | V-geom (crossed box = shaft, see filters), V-text | `slab.opening` | load-bearing man | yes |
| 21 | Columns, beams, downstand beams | plan (dashed outlines), section | V-geom, V-text | `structure.member` | later: F8 | yes |
| 22 | Section cut lines (A-A) and their position in plan | plan | V-text + V-geom (cut markers) | `sheet.cut` | links section facts to plan positions | bulk |
| 23 | Grid axes | plan | V-text + long dash-dot lines | `grid.axis` | alignment, later grids in Revit | bulk |
| 24 | Dimension chains: exact distances | plan, section | V-text numbers on dimension lines | `dimension` | checks (drawn vs measured), scale check | no (used as checks) |
| 25 | Ceiling: suspended ceiling height | section, ceiling plan | V-text | `ceiling.height` | later: ceilings | yes |
| 26 | Facade: materials, openings per storey | elevation | V-geom, LLM-text for notes | `facade.*` | check against the facade scan (F16) | bulk |
| 27 | Terrain, ground floor height above terrain | elevation, section, site plan | V-text level marks | `site.terrain` | structure man | yes |
| 28 | Fire ratings (EI30 doors, fire walls) | plan labels, door schedule | V-text | `opening.fire`, `wall.fire` | later: type parameters | yes |
| 29 | Notes that are not building (furniture, dimensions, annotation) | all | filters (built: `plans/filters.json`) | none (listed in qa) | – | no |

`scan2revit/plans/facts.py` (26.10.2026) writes facts.json with a crop per fact: scale, storey drawings, walls with written thickness, openings, swings, room stamps with area, dimension chains, storey heights and slabs from section height chains, level marks, labels (build-ups, opening sizes, roof pitch). Build-up legends, schedules and level marks are tested on hand-written input only; sheet.meta, site plan, grid axes, sill and head from raster elevations are still to build.

## 3. Facts: what is stored, and how

One file per project: `scan2revit/data/projects/<project>/project/facts.json` (git-ignored like all project data):

```json
{
  "schema": "scan2revit.facts/1",
  "sources": [
    {"id": "S1", "file": "A60.pdf", "sha256": "...", "kind": "plan", "pages": [0], "scale": 100}
  ],
  "alignment": {"source": "S1", "drawing": "EG", "to": "scan frame", "rotation_deg": 0.0,
                "translation": [0.0, 0.0], "rms_m": 0.0, "status": "proposed"},
  "facts": [
    {"id": "F-0042", "type": "buildup.floor", "subject": {"level": "1.OG"},
     "value": {"layers": [["Parkett", 0.015], ["Unterlagsboden", 0.07], ["Trittschall", 0.02], ["Beton", 0.22]],
               "total": 0.325},
     "unit": "m", "where": {"source": "S3", "page": 0, "bbox_pt": [412, 220, 530, 290], "crop": "crops/F-0042.jpeg"},
     "method": "V-text", "confidence": 0.9, "status": "proposed",
     "verified_by": null, "verified_at": null, "note": "", "conflicts": []}
  ]
}
```

- `status`: proposed, accepted, corrected (value replaced by the person, the original kept in `note`),
  rejected. The builders use accepted and corrected facts only; proposed facts are listed as open.
- `confidence`: from the reader (a clean pattern match high, an LLM answer at most 0.6); it orders the review.
- `conflicts`: filled after the scan is read: `{"with": "scan", "measured": ..., "difference": ..., "decision":
  null}`. Tolerances per fact type (start values, decision D-6): levels 3 cm, wall thickness 2 cm, opening
  width 5 cm, sill and head 5 cm, room area 3 %, slab total 3 cm.
- `alignment`: drawing coordinates to the scan frame, one per storey drawing: 2D fit of drawn wall axes to the
  scan's wall axes (rotation, translation, scale check against the sheet scale); verified like a fact.
- `plan.json` carries references, not copies: an element built with a drawn value gets `"fact": "F-0042"` and
  its source flag (section 6).

## 4. Verification by a person: the review page

A local tool (`scan2revit/tools/facts_review.py`, built 26.10.2026; `--gate` prints the open facts and holds the build phases) serves a review page on localhost for one project:

- one card per fact: the crop of the drawing where it was read, the value, the method and confidence, and for a
  conflict the measured value next to it;
- per card: accept, correct (enter the value), reject; bulk accept for one fact type above a confidence;
- order: conflicts first, then low confidence, then the rest by type;
- every decision is written into `facts.json` (`verified_by`, `verified_at`) and logged on the scoreboard
  (S1) as an action of the person;
- the project manager holds gate 1 until no fact of the types the build needs is still proposed.

The page runs only on this machine and reads the project folder; nothing leaves it (customer drawings).

## 5. The standard plan, updated (phases)

The changes to the team's phases (`agent-team.md`, applied after the current development round is merged):

| Phase | Who | New or changed |
|---|---|---|
| 1 Intake | project manager | lists every source by kind (plan, section, elevation, build-up, schedule, site, scan, IFC) |
| 2a **Drawings first** | plans man | reads every sheet: catalogue rows 1-29 into `facts.json`, crops for the review page; no geometry decisions yet |
| 2b Input check | point cloud man, IFC man | as today, with the facts as priors: expected levels for the vertical sections, expected walls as hypotheses for the slice route (search the scan near each drawn wall), expected thicknesses for one-sided walls |
| 2c Alignment | plans man + point cloud man | drawing to scan frame per storey; conflicts filled in `facts.json` |
| **Gate 1** | project manager, the user | review page: facts and conflicts decided; data quality, coordinates, storeys |
| 3 Structure | structure man | levels from the scan where measured, else from accepted level facts; every level says which |
| 4 Families | family man | wall and floor types; build-up facts kept as type data (decision D-5 on layered types) |
| 5 Load-bearing | load-bearing man | slab thickness from accepted build-ups where the scan sees only the surfaces; one-sided walls with the drawn thickness |
| 6 Fit-out | fit man | room names and numbers from stamps placed onto the scan's rooms through the alignment; opening heights from accepted facts |
| 7 Check | checker | new: drawn vs measured (every accepted fact with a measured counterpart: difference and verdict), unused facts listed |

## 6. Measured, drawn, assumed

The modelling guideline knows measured and assumed (section 2, `scan2revit source`). With drawings a third
source appears: **drawn** (taken from an accepted fact). Proposal for the guideline (decision D-4, not yet in
`SKILL.md`): `scan2revit source` = `measured`, `drawn: <what> (F-0042)`, `assumed: <what>`; a drawn value never
replaces a measured one without a conflict decision.

## 7. Development order

1. F17 fact store and catalogue readers for the types already half built (rows 1, 3, 6, 11, 13, 15, 17), then
   sections (6, 7, 8) and labels (14, 16, 19). Built 26.10.2026; next by priority (section 0): construction:
   build-up legends, wall types, materials and structure (F23 moved up).
2. F18 review page.
3. F19 alignment of drawings to the scan frame.
4. F20 priors in modelling: levels, one-sided wall thickness, slab thickness, opening heights, room names.
5. F21 drawn vs measured in the checker.
6. F23 build-up parsing, with the local LLM where the rules give no answer (F22, `local-llm.md`).

Test data: a building with **construction drawings that do not come from its scan** (design or execution
drawings with sections, build-ups, wall types) and a point cloud (inside and outside) is needed for steps 3 to 6.
The sheets used so far were drawn from the model of the scan: fine for reading (steps 1 and 2), useless for
verification. Candidate: the Schependomlaan data set (design model in ArchiCAD and IFC, point clouds, drone;
`test-data-sources.md`), download after the user's go.
