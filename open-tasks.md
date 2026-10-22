# Open functions and tasks

State 20.10.2026, scan2revit 0.7.0. All nine examples pass in Revit through pyRevit (218 of 218). One table per sub-project, then what all three share. Sources: the gaps
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
| Function | F1 Wall detection on densely partitioned real floors: real project data (details private) | 5 | L | build on the slice route real project data (details private) |
| Function | F3 Room separation lines where the slice route's rooms have no wall, so rooms close in Revit | 4 | M | reuse the passage lines of the plan-extract route |
| Function | F13 Stairs and ramps in the voids of the slab regions (steps in thin horizontal slices) | 4 | M | – |
| Function | F12 Slice route: measured opening heights, sloped roofs, one wall from its upper and lower face | 3 | M | a third slice or the top of each gap |
| Function | F14 Slab outlines with straight, square edges instead of the 10 cm raster (fewer Revit warnings) | 3 | S | – |
| Gap | Galleries: missed at 3 m section spacing, not built as their own Revit level yet | 3 | M | – |
| Gap | Doors and windows: few found on real floors | 3 | M | after F1 |
| Gap | Stairs: straight runs only; curved walls: circular arcs only | 2 | L | stairs with landings: F5 |
| Gap | Memory: large real storeys still take much memory on the full route real project data (details private) | 2 | M | slice route by default |
| Gap | Slab voids under 5 m2 are not cut | 2 | S | – |

## IFC2Revit

IFC storeys to native Revit elements, all storeys in one model. Code `scan2revit/ifc/` and `core/merge.py`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Task | Revit test of the whole real IFC building through pyRevit (0.7; the synthetic IFC house passes) | 5 | S | `tools/revit_e2e.py --plan` with the merged plan of all storeys |
| Gap | Doors on locked (fire-rated) families keep their size real project data (details private) | 4 | S | F2 (a door family with free size) |
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
| Function | Plan sheets with several storeys (`plans/sheet.py`): drawings split, storey labels, ordered bottom first, aligned | 5 | M | done on one real CAD sheet (four storeys); a test needs example sheets from the user |
| Function | Orientation and scale from the sheet: scale from the title block ("1 : 100") done; turning a sheet whose text is not upright not built yet | 5 | S | a turned sheet as example |
| Function | Rooms with the data of their stamps: name, unit (Revit "Abteilung"), number storey.unit.nn; a room at every stamp | 5 | M | done; Revit run of the real sheet next (department check) |
| Function | Clutter filter: built-in units, sanitary, text masks, annotation; list in the modelling guideline, machine list `plans/filters.json` | 4 | M | done; furniture only implicitly (no wall pairs) |
| Function | Walls drawn as filled areas in vector PDFs: wall rectangles, openings where the rendered wall colour is absent, swings from chains of short lines | 4 | S | done |
| Gap | Rooms on a real sheet not all closed by walls: real project data (details private) (corner joins, stair walls, knee walls under a sloping roof drawn as roof bands) | 4 | M | knee walls as walls of their own height; joins of stubs |
| Function | F4 Raster PDF (scanned plan) into Revit: **postponed** (22.10.2026) | 4 | S to L | own reader for filled walls preferred; OCR of room stamps; scale from stamps or dimensions |
| Function | Handwritten measurements on a scanned plan (other ink) as checks, kept out of the geometry | 3 | M | with F4 |
| Gap | plan-extract run locally: blocked, the segmenter model is not public | 2 | – | only needed for thin-line or sketched plans |
| Gap | plan-extract results: one room the walls do not close; never run on a real result | 2 | S | a real result |
| Function | F11 Own raster reader instead of plan-extract | 3 | L | part of F4 |

## Shared: core, Revit side, agent team

The plan schema, wall geometry, merge, the Revit side through pyRevit 7, the modelling guideline and the
agent team. Code `scan2revit/core/`, `tools/`, `.claude/`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Task | Unattended runs: check that the pyRevit agent host answers Revit's failure dialogs like the old add-in | 4 | S | the whole IFC building as the hard case |
| Function | F2 A door and a window family with free size in the blank project (the template) | 4 | S | **you**: load the families into the template |
| Task | Agent team: first model built in Revit, phase by phase with its gates | 4 | M | the synthetic project first, then a real building |
| Function | F15 Modelling guideline: phase "Existing" for every element, a parameter measured / assumed on walls, floors, doors and windows | 3 | S | – |
