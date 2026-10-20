# Open functions and tasks

State 20.10.2026, scan2revit 0.7.0. One table per sub-project, then what all three share. Sources: the gaps
and the future functions of `scoring.md` (numbers F1 to F15 are its future functions), the build log and the
status of the Revit tests. Published at https://tstrathaus.github.io/revit-mcp-status/open.html; a commit that
changes this file, `scoring.md` or the modelling guideline updates the site (`tools/publish_status.py`, run by
the git hook in `tools/hooks/`). Public page: no project names, customer file names or data paths here.

Kind: **Function** a new capability, **Gap** a known weakness of an existing one, **Task** testing,
decisions and upkeep. Value 1 to 5 (5 = most useful), effort S (hours), M (a day or two), L (more).

## Pointcloud2Revit

Scans (E57, PLY, LAS) to levels, walls, openings, floors, stairs and rooms. Code `scan2revit/pointcloud/`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Task | Revit test of the four scan examples through pyRevit (0.7) | 5 | S | `tools/revit_e2e.py --only synthetic_two_storey,curved_bay,stair_two_storey,slices` |
| Function | F1 Wall detection on densely partitioned real floors (hotel rooms): full route finds a tenth of the walls | 5 | L | build on the slice route (39-49 % of the IFC wall length found) |
| Function | F3 Room separation lines where the slice route's rooms have no wall, so rooms close in Revit | 4 | M | reuse the passage lines of the plan-extract route |
| Function | F13 Stairs and ramps in the voids of the slab regions (steps in thin horizontal slices) | 4 | M | – |
| Function | F12 Slice route: measured opening heights, sloped roofs, one wall from its upper and lower face | 3 | M | a third slice or the top of each gap |
| Function | F14 Slab outlines with straight, square edges instead of the 10 cm raster (fewer Revit warnings) | 3 | S | – |
| Gap | Galleries: missed at 3 m section spacing, not built as their own Revit level yet | 3 | M | – |
| Gap | Doors and windows: few found on real floors | 3 | M | after F1 |
| Gap | Stairs: straight runs only; curved walls: circular arcs only | 2 | L | stairs with landings: F5 |
| Gap | Memory: storeys of 8-9 M points still take 10-18 GB on the full route | 2 | M | slice route by default |
| Gap | Slab voids under 5 m2 are not cut | 2 | S | – |

## IFC2Revit

IFC storeys to native Revit elements, all storeys in one model. Code `scan2revit/ifc/` and `core/merge.py`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Task | Revit test of the synthetic IFC house and of the whole real IFC building through pyRevit (0.7) | 5 | S | `tools/revit_e2e.py --only ifc_house`, then the real building with `--plan` |
| Gap | Doors on locked (fire-rated) families keep their size: 798 of 841 doors right on the real building | 4 | S | F2 (a door family with free size) |
| Function | F5 Stairs with landings (IFC flights; also for scans) | 3 | L | – |
| Function | F6 Wall types by the IFC type name | 3 | M | – |
| Function | F7 Slab holes and openings from the IFC | 3 | M | – |
| Function | F8 Columns and beams | 3 | M | – |
| Function | F9 Curtain walls with their doors and windows | 3 | L | – |
| Gap | Rooms without `IfcSpace`: areas off where walls overlap | 2 | M | – |
| Function | F10 Door swing from the IFC | 2 | S | – |

## Plans2Revit

2D plans to Revit: DXF and vector PDF, raster plans through plan-extract results. Code `scan2revit/plans/`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Task | Revit test of the five plan examples through pyRevit (0.7) | 5 | S | `tools/revit_e2e.py --only plan2d_pdf,plan2d_two_storey_pdf,fpx_golden,fpx_two_storey` |
| Function | F4 Raster PDF (scanned plan) into Revit | 4 | S to L | **decision (you)**: plan-extract's segmenter model, an own reader (F11) or the web app (the plan leaves the machine) |
| Task | First real plan through the route: a real measured PDF plan is waiting in the data folder | 4 | S | depends on F4 if it is a raster PDF |
| Gap | plan-extract run locally: blocked, the segmenter model is not public | 3 | – | ask BBL for the model or decide F4 |
| Gap | plan-extract results: one room the walls do not close; never run on a real result | 3 | S | a real result |
| Function | F11 Own raster reader instead of plan-extract | 3 | L | decision in F4 |

## Shared: core, Revit side, agent team

The plan schema, wall geometry, merge, the Revit side through pyRevit 7, the modelling guideline and the
agent team. Code `scan2revit/core/`, `tools/`, `.claude/`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Task | Revit test of all nine examples through the pyRevit agent runtime: the first since the move from the add-in | 5 | S | `tools/revit_e2e.py --auto-approve`, then compare with the 0.5 results (218 of 218) |
| Task | Unattended runs: check that the pyRevit agent host answers Revit's failure dialogs like the old add-in | 4 | S | the whole IFC building as the hard case |
| Function | F2 A door and a window family with free size in the blank project (the template) | 4 | S | **you**: load the families into the template |
| Task | Agent team: first model built in Revit, phase by phase with its gates | 4 | M | the synthetic project first, then a real building |
| Function | F15 Modelling guideline: phase "Existing" for every element, a parameter measured / assumed on walls, floors, doors and windows | 3 | S | – |
