# Features and effort

State 25.10.2026 13:22. Written by `tools/effort.py` from `documentation/open-tasks.md`, `documentation/scoring.md` and the Claude Code session records; do not edit by hand.

Measured 15.10.2026 to 25.10.2026: 97 requests, the lead 22.3 h active, agents 3.1 h, 14.8 M new tokens (input, cache writes, output) and 927.4 M tokens read from the cache; the tables show new tokens. Active time counts every pause as at most 5 minutes. Built features from before 15.10.2026 have no figures. Agents started by hand, outside a workflow, count under the lead; an agent that worked on several features counts in each of their rows, the bold totals count it once. Loops: a checking agent (reviewer, checker) after a building one (developer, builders). Estimates: S about 1 h and 0.5 M tokens, M about 2.5 h and 1.5 M, L about 6 h and 4 M (`open-tasks.md`).

| Overall | Features | Estimate | Measured time | Agents | Loops | Tokens |
|---|---|---|---|---|---|---|
| Built | 64 | 38.5 h, 22.0 M | 19.6 h | – | – | 8.2 M |
| In progress and planned | 45 | 126.5 h, 78.8 M | 1.9 h | – | – | 1.3 M |
| **All requests measured** | **109** | **165.0 h, 100.8 M** | **25.4 h** (lead 22.3 h, agents 3.1 h) | **26** | **7** | **14.8 M** |

## Pointcloud2Revit

### Built (19)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| Slice-weighted storeys (walls 0.3-0.7 m, windows 1.1-1.3 m) | Function | 4 | – | 1.8 h | – | – | 234 k |
| Slice route: walls, doors, windows, rooms, floor from two 20 cm slices (`slice2d`) | Function | 4 | – | 1.6 h | – | – | 531 k |
| Slabs and levels from vertical sections (`sections`), refined where neighbours differ | Function | 3 | – | 1.3 h | – | – | 173 k |
| F16 External parts of the point cloud (`pointcloud/facade.py`): exterior walls measured, slab outline from the facade ring (closed stepwise), edge on the walls' outer face, courtyards as voids | Function | 5 | M (~2.5 h, ~1.5 M tokens) | 49 min | – | – | 859 k |
| Slab regions per floor from horizontal slices: outlines, voids (shafts, stairwells, courtyards), galleries | Function | 4 | – | 39 min | – | – | 120 k |
| F14 Slab outlines with straight, square edges instead of the 10 cm raster (fewer Revit warnings) | Function | 3 | S (~1 h, ~0.5 M tokens) | 16 min | – | – | 84 k |
| A4 Scan coverage per storey: share of every wall and of the outline seen, coverage image | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 12 min | 5 (9 min) / 5 (2 min) / – | 5 | 210 k |
| Curved walls | Function | 4 | – | – | – | – | – |
| Door swing and hinge side | Function | 4 | – | – | – | – | – |
| Doors and windows from holes in the faces | Function | 4 | – | – | – | – | – |
| E57 reader (real scans, in blocks) | Function | 4 | – | – | – | – | – |
| External scans (drone, facade) in the survey frame (`facade`): exterior walls seen from inside get their measured thickness, slab outlines from the facade ring, courtyards as voids | Function | 4 | – | – | – | – | – |
| Ghost points (glass, mirrors) | Function | 3 | – | – | – | – | – |
| Large scans: thinning to 2 cm | Function | 4 | – | – | – | – | – |
| Levels and storeys from the scan | Function | 5 | – | – | – | – | – |
| Rooms, floor outline | Function | 4 | – | – | – | – | – |
| Stairs, slab openings | Function | 4 | – | – | – | – | – |
| Storeys merged in the survey frame, vertical check | Function | 4 | – | – | – | – | – |
| Straight walls (faces, thickness, squaring, joins) | Function | 4 | – | – | – | – | – |
| **Total built (19)** | | | **6.0 h, 3.5 M** | **6.7 h** | **10** | **5** | **2.2 M** |

### Planned (13)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| F3 Room separation lines where the slice route's rooms have no wall | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 17 min | – | – | 59 k |
| F12 Sloped elements: sloped roofs and ceilings, knee walls from the scan; slice route: measured opening heights, one wall from its upper and lower face | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 1 min | – | – | 6 k |
| Apartment scan with floor plan (test 25.10.2026, public sample of a scanner vendor, one storey, 8.9 M points): the outline and the large room fit (58.75 m2 against 60.5 m2 of the vendor's floor plan), but most interior walls are missed although the scan shows them: 2814 wall-face pairs rejected for floor or ceiling points between the faces; the floor spreads 7.8 cm (tilt or scans not aligned), the floor and ceiling bands reach into the walls. In Revit 22 of 25 checks: the rooms are placed but not enclosed | Gap | 5 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Car parks and halls (test 25.10.2026 on a public car park scan, one scan position, 28 M points, 125 x 130 m): the slice route finds wall fragments only (46 pieces, 39 under 1 m), no columns, the room follows the scanner's line of sight; the floor falls 35 cm and comes out as five levels; outer walls 30-40 m from the scanner are thin in points | Gap | 4 | L (~6 h, ~4 M tokens) | – | – | – | – |
| Doors and windows: few found on real floors | Gap | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| F1 Wall detection on densely partitioned real floors: real project data (details private) | Function | 5 | L (~6 h, ~4 M tokens) | – | – | – | – |
| F13 Stairs and ramps in the voids of the slab regions (steps in thin horizontal slices) | Function | 4 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Galleries: missed at 3 m section spacing, not built as their own Revit level yet | Gap | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| LAS / LAZ scans: `laspy[lazrs]` installed, a chunked reader with the 2 cm voxel thinning (as for E57), input report and slice route on LAS; first test file the Kladno station (6.5 GB, CC BY, `test-data-sources.md`) | Function | 3 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| Memory: large real storeys still take much memory on the full route real project data (details private) | Gap | 2 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Slab voids under 5 m2 are not cut | Gap | 2 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| Stairs: straight runs only; curved walls: circular arcs only | Gap | 2 | L (~6 h, ~4 M tokens) | – | – | – | – |
| Two more test scans (a house, one scan station; an office floor, two stations) are Trimble RealWorks projects (`.rwp`, scans `.rwcx`, a closed format): no reader here; needs an E57 export from Trimble RealWorks (Create tzf Scan, then Export E57 structured) | Task | 3 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| **Total planned (13)** | | | **38.5 h, 24.0 M** | **18 min** | **0** | **–** | **65 k** |

**Pointcloud2Revit: still to do estimated 38.5 h, 24.0 M; measured so far 7.0 h and 2.3 M tokens (features and other requests).**

Other requests on Pointcloud2Revit (status, documentation, runs, fixes not tied to one feature): 2, 3 min, 4 k tokens.

## IFC2Revit

### Built (10)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| A3 IFC pre-check: what Revit will refuse (degenerate arcs, short pieces, duplicates), fixed where safe, reported | Function | 4 | S (~1 h, ~0.5 M tokens) | 27 min | 13 (13 min) / 7 (2 min) / 5 (1 min) | 7 | 409 k |
| F7 Slab holes and openings from the IFC | Function | 3 | M (~2.5 h, ~1.5 M tokens) | 27 min | 13 (13 min) / 7 (2 min) / 5 (1 min) | 7 | 409 k |
| F10 Door swing from the IFC: single-swing doors from the placement (opens towards local +Y) and the operation type (hinge side) | Function | 2 | S (~1 h, ~0.5 M tokens) | 11 min | – | – | 66 k |
| Revit test of the whole real IFC building through pyRevit (0.7) | Task | 5 | S (~1 h, ~0.5 M tokens) | 11 min | – | – | 66 k |
| All storeys in one model (`merge.py`) | Function | 4 | – | – | – | – | – |
| One storey to native Revit (`ifc.py`) | Function | 5 | – | – | – | – | – |
| Openings on the right wall piece, panes left out | Function | 4 | – | – | – | – | – |
| Pre-check of what Revit refuses (`ifc/precheck.py`), wall pieces at their base offset, slab holes | Function | 4 | – | – | – | – | – |
| Rooms without `IfcSpace` (cells between the walls) | Function | 4 | – | – | – | – | – |
| Synthetic IFC example and tests | Function | 4 | – | – | – | – | – |
| **Total built (10)** | | | **5.5 h, 3.0 M** | **1.3 h** | **50** | **14** | **948 k** |

### Planned (8)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| Doors on locked (fire-rated) families keep their size real project data (details private) | Gap | 4 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| F5 Stairs with landings (IFC flights; also for scans) | Function | 3 | L (~6 h, ~4 M tokens) | – | – | – | – |
| F6 Wall types by the IFC type name | Function | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| F8 Columns and beams | Function | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| F9 Curtain walls with their doors and windows | Function | 3 | L (~6 h, ~4 M tokens) | – | – | – | – |
| IFC wall pieces assigned to a storey they do not stand in (base offsets of a whole storey up or down): built at their true height they no longer bound that level's rooms | Gap | 4 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| IFC: a few walls and their openings Revit refuses ("Wand kann nicht erstellt werden"), doors in curved walls | Gap | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Rooms without `IfcSpace`: areas off where walls overlap | Gap | 2 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| **Total planned (8)** | | | **24.0 h, 15.0 M** | **–** | **0** | **–** | **–** |

**IFC2Revit: still to do estimated 24.0 h, 15.0 M; measured so far 1.3 h and 959 k tokens (features and other requests).**

Other requests on IFC2Revit (status, documentation, runs, fixes not tied to one feature): 1, 4 min, 11 k tokens.

## Plans2Revit

### Built (14)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| Raster plans through plan-extract (`fpx.py`) | Function | 4 | – | 40 min | – | – | 152 k |
| Plan sheets with several storeys (`plans/sheet.py`): drawings split, storey labels, ordered bottom first, aligned | Function | 5 | M (~2.5 h, ~1.5 M tokens) | 28 min | – | – | 127 k |
| Room stamps: name, unit as Revit department, number storey.unit.nn, a room at every stamp | Function | 4 | – | 28 min | – | – | 127 k |
| Plan sheets: small symbols drawn in wall colour outside the building became wall stubs; a door beside a window in one gap got only the window | Gap | 3 | S (~1 h, ~0.5 M tokens) | 11 min | – | – | 66 k |
| Walls drawn as filled areas, openings where the wall colour is absent, swings from chains of short lines | Function | 4 | – | 9 min | – | – | 92 k |
| Clutter filter (built-in units, sanitary, text masks, annotation), list in the guideline and `plans/filters.json` | Function | 4 | – | 6 min | – | – | 73 k |
| plan-extract run locally | Function | 1 | – | 2 min | – | – | 9 k |
| CAD sheet with several storeys (`sheet.py`): drawings split, storey labels, scale from the title block | Function | 4 | – | – | – | – | – |
| Clutter filter: built-in units, sanitary, text masks, annotation; list in the modelling guideline, machine list `plans/filters.json` | Function | 4 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| DXF and vector PDF | Function | 4 | – | – | – | – | – |
| Own raster reader | Function | 0 | – | – | – | – | – |
| Rooms with the data of their stamps: name, unit (Revit "Abteilung"), number storey.unit.nn; a room at every stamp | Function | 5 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Several storeys, aligned | Function | 4 | – | – | – | – | – |
| Walls drawn as filled areas in vector PDFs: wall rectangles, openings where the rendered wall colour is absent, swings from chains of short lines | Function | 4 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| **Total built (14)** | | | **9.5 h, 5.5 M** | **2.1 h** | **0** | **–** | **647 k** |

### In progress (1)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| Storey heights from the elevations sheet (levels and heights instead of the assumed storey height) | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 12 min | 5 (9 min) / 5 (2 min) / – | 5 | 210 k |
| **Total in progress (1)** | | | **2.5 h, 1.5 M** | **12 min** | **10** | **5** | **210 k** |

### Planned (8)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| Rooms on a real sheet not all closed by walls: real project data (details private) after the corner joins, stub and jog fixes and knee walls (24.10.2026) | Gap | 3 | S (~1 h, ~0.5 M tokens) | 12 min | 5 (9 min) / 5 (2 min) / – | 5 | 210 k |
| plan-extract run locally: blocked, the segmenter model is not public | Gap | 2 | – | 2 min | – | – | 9 k |
| F11 Own raster reader instead of plan-extract | Function | 3 | L (~6 h, ~4 M tokens) | – | – | – | – |
| F4 Raster PDF (scanned plan) into Revit: **postponed** (22.10.2026) | Function | 4 | S to L (1-6 h, 0.5-4 M tokens) | – | – | – | – |
| Handwritten measurements on a scanned plan (other ink) as checks, kept out of the geometry | Function | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Knee walls under a sloping roof built as wide as the drawn band (thickness and height flagged assumed) | Gap | 3 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| Orientation and scale from the sheet: scale from the title block ("1 : 100") done; turning a sheet whose text is not upright not built yet | Function | 5 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| plan-extract results: one room the walls do not close; never run on a real result | Gap | 2 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| **Total planned (8)** | | | **16.0 h, 9.8 M** | **13 min** | **10** | **5** | **219 k** |

**Plans2Revit: still to do estimated 18.5 h, 11.2 M; measured so far 2.6 h and 1.5 M tokens (features and other requests).**

Other requests on Plans2Revit (status, documentation, runs, fixes not tied to one feature): 1, 6 min, 419 k tokens.

## Shared: core, Revit side, agent team

### Built (21)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| Images: a plan per level and a 3D view, JPEG | Function | 4 | – | 2.1 h | – | – | 473 k |
| Revit through the pyRevit agent runtime (stages, read back, checks) | Function | 4 | – | 1.4 h | – | – | 206 k |
| End-to-end runner (start, calls, checks, report) | Function | 4 | – | 1.3 h | – | – | 229 k |
| Unattended runs: failure dialogs answered and logged | Function | 5 | – | 54 min | – | – | 224 k |
| Agent team: 9 agents, workflow with gates, phase tool for one model | Function | 3 | – | 35 min | – / – / 1 (0 min) | – | 963 k |
| A1 Machine-readable input reports for every route (verdict per item) | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 27 min | 13 (13 min) / 7 (2 min) / 5 (1 min) | 7 | 409 k |
| S1 Agent scoreboard: actions, findings, defects found and fixed, gate verdicts and check scores per agent and project, summed up over projects | Function | 5 | M (~2.5 h, ~1.5 M tokens) | 27 min | 13 (13 min) / 7 (2 min) / 5 (1 min) | 7 | 409 k |
| V1 Rule ids in the modelling guideline, each rule with its Revit check; R2 table rule -> check | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 27 min | 13 (13 min) / 7 (2 min) / 5 (1 min) | 7 | 409 k |
| V2 Comparison with a reference (an IFC of the same building) as a standard checker step, LOA tolerances | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 27 min | 13 (13 min) / 7 (2 min) / 5 (1 min) | 7 | 409 k |
| Revit API check (`tools/api_check.py`) | Function | 4 | – | 22 min | – | – | 22 k |
| Room tags (Raumstempel) with the area in every floor plan of a room's level, room data of the input (name, number, unit, use, finishes), the rooms' interior fill shown in the floor plans (rule G-9.6) | Function | 4 | S (~1 h, ~0.5 M tokens) | 14 min | – | – | 68 k |
| R1 Rule proposals: agents propose guideline changes in their handover, the project manager collects them, the user approves | Function | 4 | S (~1 h, ~0.5 M tokens) | 12 min | 5 (9 min) / 5 (2 min) / – | 5 | 210 k |
| V3 Each Revit run compared with the previous one: checks gained, lost, still failing | Function | 3 | S (~1 h, ~0.5 M tokens) | 12 min | 5 (9 min) / 5 (2 min) / – | 5 | 210 k |
| F15 Modelling guideline: phase "Existing" for every element, a parameter measured / assumed on walls, floors, doors and windows | Function | 3 | S (~1 h, ~0.5 M tokens) | 11 min | – | – | 66 k |
| F27 Browser viewer with That Open Company libraries (ifc.js: `@thatopen/components`, `web-ifc`): model, scan slices and deviation colours on localhost, for the review loop and the fact review | Function | 4 | M (~2.5 h, ~1.5 M tokens) | 8 min | – | – | 72 k |
| Agent team bookkeeping: scoreboard, rule ids with checks, rule proposals, run comparison | Function | 3 | – | 7 min | – | – | 66 k |
| Comparison with a reference plan per LOA class (`core/compare.py`) | Function | 3 | – | – | – | – | – |
| Door and window types for every size | Function | 4 | – | – | – | – | – |
| Input reports with verdicts (`core/inputs.py`), scan coverage | Function | 3 | – | – | – | – | – |
| Unattended runs: check that the pyRevit agent host answers Revit's failure dialogs like the old add-in | Task | 4 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| Wall types for every thickness | Function | 4 | – | – | – | – | – |
| **Total built (21)** | | | **17.5 h, 10.0 M** | **9.6 h** | **121** | **38** | **4.4 M** |

### In progress (1)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| F24 Agent team phases updated for drawings first (phase 2a, alignment 2c, review at gate 1, drawn vs measured in the check) | Task | 4 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| **Total in progress (1)** | | | **1.0 h, 500 k** | **–** | **0** | **–** | **–** |

### Planned (14)

| Feature | Kind | Value | Estimate | Time | Agents (building / checking / other) | Loops | Tokens |
|---|---|---|---|---|---|---|---|
| F22 Local LLM helper (`local-llm.md`): text classification, build-up parsing, raster reading; always proposed facts, checked by code | Function | 3 | M (~2.5 h, ~1.5 M tokens) | 20 min | 8 (4 min) / 2 (1 min) / 5 (1 min) | 2 | 210 k |
| Agent team: first model built in Revit, phase by phase with its gates | Task | 4 | M (~2.5 h, ~1.5 M tokens) | 15 min | 8 (4 min) / 2 (1 min) / 5 (1 min) | 2 | 199 k |
| F17 Facts from drawings: catalogue of 29 information types from plans, sections, elevations, build-up legends, schedules, site plans into `facts.json` per project (`drawings-and-scans.md`) | Function | 5 | L (~6 h, ~4 M tokens) | 15 min | 8 (4 min) / 2 (1 min) / 5 (1 min) | 2 | 199 k |
| GitHub sources: licence and security check before any skill or code is taken; pinned and listed (`github-sources.md`) | Task | 3 | S (~1 h, ~0.5 M tokens) | 15 min | 8 (4 min) / 2 (1 min) / 5 (1 min) | 2 | 199 k |
| F25 Deviation analysis: the built model against the scan, per element (signed median, 95 %, LOA share, coverage, verdict pass / fail / not verifiable), missed-element candidates, bias per class, coloured images per storey (`deviation-and-review.md` 1) | Function | 5 | L (~6 h, ~4 M tokens) | 1 min | – | – | 6 k |
| F26 Review and correction as one loop: flagged items shown with scan and deviation, a person accepts, moves, changes, deletes or adds, the plan is edited, the stages and checks run again, every decision on the scoreboard (`deviation-and-review.md` 2); planned agent: review man | Function | 5 | L (~6 h, ~4 M tokens) | 1 min | – | – | 6 k |
| F28 Meshing: not in the modelling routes (research 25.10.2026, `deviation-and-review.md` 3); possibly for the viewer and as reference surface of non-planar elements | Task | 2 | S (~1 h, ~0.5 M tokens) | 1 min | – | – | 6 k |
| F18 Review page: a person accepts, corrects or rejects every fact at gate 1, crops of the drawing beside each value | Function | 5 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| F19 Drawings aligned to the scan frame per storey (2D fit of wall axes, person confirms) | Function | 5 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| F2 A door and a window family with free size in the blank project (the template) | Function | 4 | S (~1 h, ~0.5 M tokens) | – | – | – | – |
| F20 Drawn facts as priors in modelling: levels, thickness of one-sided walls, slab thickness, opening heights, room names on scan rooms, drawn walls as hypotheses for the slice route | Function | 5 | L (~6 h, ~4 M tokens) | – | – | – | – |
| F21 Checker: drawn vs measured for every accepted fact, unused facts listed | Function | 4 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| F23 Build-ups (floor, wall, roof) parsed into layers and thicknesses; slab thickness from them | Function | 4 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| Point clouds from Autodesk ReCap (RCP / RCS): link into the Revit copy, read the slices with point cloud filters through pyRevit, on into the slice route | Function | 3 | M (~2.5 h, ~1.5 M tokens) | – | – | – | – |
| **Total planned (14)** | | | **44.5 h, 28.0 M** | **1.2 h** | **60** | **8** | **826 k** |

**Shared: still to do estimated 45.5 h, 28.5 M; measured so far 14.5 h and 10.0 M tokens (features and other requests).**

Other requests on Shared (status, documentation, runs, fixes not tied to one feature): 39, 3.7 h, 4.8 M tokens.

## Tasks with agents

| Date | Task | Sub-project | Lead | Agent | Role | Time | Tokens | Cache reads |
|---|---|---|---|---|---|---|---|---|
| 17.10.2026 | Agent team | shared | 35 min, 913 k | project-manager | input / lead | 0 min | 50 k | 278 k |
| | | | | **1 agents, 0 loops** | | **0 min** | **50 k** | **278 k** |
| 24.10.2026 | Feature round: developers and reviewers | shared | 6 min, 232 k | dev:agents | building | 19 min | 310 k | 10.1 M |
|  |  |  |  | dev:inputs | building | 17 min | 271 k | 9.8 M |
|  |  |  |  | dev:ifc | building | 24 min | 389 k | 21.1 M |
|  |  |  |  | dev:plans | building | 32 min | 481 k | 26.5 M |
|  |  |  |  | dev:checker | building | 11 min | 167 k | 3.9 M |
|  |  |  |  | review:checker | checking | 4 min | 96 k | 1.3 M |
|  |  |  |  | review:inputs | checking | 4 min | 77 k | 1.2 M |
|  |  |  |  | review:agents | checking | 4 min | 108 k | 2.0 M |
|  |  |  |  | review:ifc | checking | 3 min | 80 k | 1.0 M |
|  |  |  |  | review:plans | checking | 4 min | 98 k | 1.0 M |
| | | | | **10 agents, 5 loops** | | **2.0 h** | **2.1 M** | **78.0 M** |
| 24.10.2026 | Plans (drawings first, local LLM, GitHub); merge of the feature round; team test | shared | 1.5 h, 584 k | project-manager | input / lead | 1 min | 39 k | 185 k |
|  |  |  |  | point-cloud-man | input / lead | 6 min | 141 k | 2.9 M |
|  |  |  |  | project-manager | input / lead | 1 min | 48 k | 147 k |
|  |  |  |  | structure-man | building | 5 min | 99 k | 1.6 M |
|  |  |  |  | family-man | building | 2 min | 61 k | 1.1 M |
|  |  |  |  | loadbearing-man | building | 4 min | 93 k | 1.7 M |
|  |  |  |  | project-manager | input / lead | 3 min | 80 k | 447 k |
|  |  |  |  | fit-man | building | 2 min | 75 k | 1.2 M |
|  |  |  |  | checker | checking | 3 min | 114 k | 1.4 M |
|  |  |  |  | loadbearing-man | building | 5 min | 85 k | 1.8 M |
|  |  |  |  | structure-man | building | 8 min | 108 k | 2.6 M |
|  |  |  |  | family-man | building | 8 min | 137 k | 3.6 M |
|  |  |  |  | fit-man | building | 6 min | 86 k | 1.8 M |
|  |  |  |  | checker | checking | 3 min | 110 k | 1.3 M |
|  |  |  |  | project-manager | input / lead | 4 min | 126 k | 1.7 M |
| | | | | **15 agents, 2 loops** | | **1.0 h** | **1.4 M** | **23.4 M** |
