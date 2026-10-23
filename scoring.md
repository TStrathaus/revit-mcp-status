# Scoring: current functionality and future functions

State 23.10.2026. Section 12 of the research log scores the outside options; this table scores what this
repository does itself. Update it when a score changes, with the evidence. How the models are built:
the modelling guideline `scan2revit/skills/modeling/SKILL.md` (https://tstrathaus.github.io/revit-mcp-status/modeling.html).

## Scale

Maturity 0 to 5:

| Score | Meaning |
|---|---|
| 0 | not started |
| 1 | designed only |
| 2 | code exists, not verified |
| 3 | passes the synthetic tests and the benchmark, or runs on real data without Revit |
| 4 | passes in a real Revit (`scan2revit/tools/revit_e2e.py`) |
| 5 | proven on real project data in Revit, measured against a reference |

Future functions: value 1 to 5 (5 = most useful), effort S (hours), M (a day or two), L (more).

## Current functionality

| Topic | Function | Score | Evidence | Gap |
|---|---|---|---|---|
| Convert point clouds | Levels and storeys from the scan | 5 | real project data (details private) | – |
| Convert point clouds | Straight walls (faces, thickness, squaring, joins) | 4 | all scan examples in Revit; real project data (details private) | densely partitioned real floors: real project data (details private) |
| Convert point clouds | Curved walls | 4 | `curved_bay`: radius exact in Revit | circular arcs only |
| Convert point clouds | Doors and windows from holes in the faces | 4 | scan examples in Revit: all hosted, sills to the millimetre | few found on real floors |
| Convert point clouds | Door swing and hinge side | 4 | door facing checks pass in Revit | – |
| Convert point clouds | Ghost points (glass, mirrors) | 3 | benchmark S9: 97 % removed | – |
| Convert point clouds | Stairs, slab openings | 4 | three stair examples in Revit, 16 risers, tread right | straight runs only |
| Convert point clouds | Rooms, floor outline | 4 | scan examples: rooms bounded, areas within 3 %; slivers under 1 m2 left out | – |
| Convert point clouds | E57 reader (real scans, in blocks) | 4 | real project data (details private) | – |
| Convert point clouds | Large scans: thinning to 2 cm | 4 | real project data (details private) | – |
| Convert point clouds | Slice-weighted storeys (walls 0.3-0.7 m, windows 1.1-1.3 m) | 4 | real project data (details private) | real project data (details private) |
| Convert point clouds | Slice route: walls, doors, windows, rooms, floor from two 20 cm slices (`slice2d`) | 4 | synthetic (bench SL1-SL5): all walls (faces within 1 mm), doors with swing, windows, rooms; example all 18 checks in Revit (0.7, through pyRevit). real project data (details private) | rooms not closed in Revit where walls are missing; opening heights given, not measured; sloped roofs |
| Convert point clouds | Slabs and levels from vertical sections (`sections`), refined where neighbours differ | 3 | synthetic: floors exact, slab thickness within 2 cm, gallery found, beds and a ramp no level; real project data (details private); floors and slab thickness go into the slice route | a gallery real project data (details private) is missed at 3 m spacing; some slab thicknesses from few pairs; galleries not built as their own Revit level yet |
| Convert point clouds | Slab regions per floor from horizontal slices: outlines, voids (shafts, stairwells, courtyards), galleries | 4 | synthetic: floor regions, a stairwell void, a hidden floor filled, the gallery; real project data (details private) | outlines from a 10 cm raster (Revit sketch warnings); voids under 5 m2 not cut; stairs in the voids not read |
| Convert point clouds | Storeys merged in the survey frame, vertical check | 4 | real project data (details private) | – |
| Convert floor plans | DXF and vector PDF | 4 | plan examples in Revit, all checks | – |
| Convert floor plans | Several storeys, aligned | 4 | two-storey PDF in Revit, stair and void right | – |
| Convert floor plans | CAD sheet with several storeys (`sheet.py`): drawings split, storey labels, scale from the title block | 3 | real project data (details private) | sheets with turned text; no test yet (example sheets from the user) |
| Convert floor plans | Walls drawn as filled areas, openings where the wall colour is absent, swings from chains of short lines | 3 | real project data (details private) | corner joins of short stubs; knee walls under a sloping roof drawn as roof bands |
| Convert floor plans | Room stamps: name, unit as Revit department, number storey.unit.nn, a room at every stamp | 3 | real project data (details private); department set and checked by the runner, tested in the stand-in | first Revit run of a real sheet |
| Convert floor plans | Clutter filter (built-in units, sanitary, text masks, annotation), list in the guideline and `plans/filters.json` | 3 | real sheet: crossed boxes, circles and masks left out, windows drawn as crossed boxes kept | furniture only implicitly |
| Convert floor plans | Raster plans through plan-extract (`fpx.py`) | 4 | plan-extract examples in Revit | one room the walls do not close; never on a real result |
| Convert floor plans | plan-extract run locally | 1 | repository cloned | blocked: the segmenter model is not public |
| Convert floor plans | Own raster reader | 0 | – | not built |
| Convert IFC | One storey to native Revit (`ifc.py`) | 5 | real project data (details private) | stairs with landings |
| Convert IFC | All storeys in one model (`merge.py`) | 4 | real project data (details private) | doors on locked families |
| Convert IFC | Openings on the right wall piece, panes left out | 4 | 'cannot cut from wall' 359 -> 36 on the whole building | – |
| Convert IFC | Rooms without `IfcSpace` (cells between the walls) | 4 | real project data (details private); synthetic house exact | areas off where walls overlap |
| Convert IFC | Synthetic IFC example and tests | 4 | `bench/ifc_synth.py`: 3 tests, 22 of 22 checks in Revit | – |
| Revit and MCP (all routes) | End-to-end runner (start, calls, checks, report) | 4 | every example, a real IFC building and real scan storeys (0.5 add-in); all nine examples through pyRevit, 218 of 218 checks (0.7, 20.10.2026) | the real IFC building and the scan storeys again through pyRevit |
| Revit and MCP (all routes) | Unattended runs: failure dialogs answered and logged | 4 | real project data (details private) (0.5 add-in) | in 0.6 the pyRevit agent host answers them; again in Revit |
| Revit and MCP (all routes) | Wall types for every thickness | 4 | real project data (details private) (0.5 add-in); every thickness of the nine examples through pyRevit (0.7) | the whole IFC building again through pyRevit |
| Revit and MCP (all routes) | Door and window types for every size | 4 | every size of the nine examples made in Revit 2025, through the add-in and through pyRevit (Swiss families through the masonry opening; passage families without a leaf never used for a door); size check in every run | fire-rated door families lock their size |
| Revit and MCP (all routes) | Images: a plan per level and a 3D view, JPEG | 4 | every example and the real models (0.5 add-in); every example through pyRevit: a fresh plan per level without the template's view template, cropped, fine detail (0.7) | – |
| Revit and MCP (all routes) | Revit through the pyRevit agent runtime (stages, read back, checks) | 4 | all nine examples in Revit 2025 through `pyrevit mcp`, unattended, 218 of 218 checks (20.10.2026); fixed on the way: Room.Name under IronPython, umlauts in results, a Revit chosen by process id | real project data through pyRevit |
| Revit and MCP (all routes) | Revit API check (`tools/api_check.py`) | 4 | all 136 API names of the Revit module found in Revit 2025.1 | – |
| Revit and MCP (all routes) | Agent team: 9 agents, workflow with gates, phase tool for one model | 3 | three examples built phase by phase in the stand-in, every check passes; the family man's types stage makes every type before the builders | first run in Revit |

## Future functions

| # | Function | Value | Effort | Depends on | Raises |
|---|---|---|---|---|---|
| 1 | Wall detection on densely partitioned real floors | 5 | L | – | scan walls 4 to 5 |
| 2 | A door and a window family with free size in the blank project | 4 | S | template (you) | door sizes 3 to 4 |
| 3 | Room separation lines where the slice route's rooms have no wall (rooms closed in Revit) | 4 | M | – | slice route rooms |
| 4 | Raster PDF into Revit | 4 | S to L | decision: segmenter model, own reader or web app | raster plans 1 to 4 |
| 5 | Stairs with landings (IFC flights, scans) | 3 | L | – | stairs |
| 6 | IFC: wall types by the IFC type name | 3 | M | – | type quality |
| 7 | IFC: slab holes and openings | 3 | M | – | floors |
| 8 | IFC: columns and beams | 3 | M | – | new element classes |
| 9 | IFC: curtain walls with their doors and windows | 3 | L | – | new element class |
| 10 | Door swing from the IFC | 2 | S | – | – |
| 11 | Own raster reader (instead of plan-extract) | 3 | L | decision in 4 | raster plans 0 to 3 |
| 13 | Stairs and ramps in the voids of the slab regions (steps in thin horizontal slices) | 4 | M | – | stairs 4 to 5 |
| 14 | Slab outlines: straight, square edges instead of the 10 cm raster | 3 | S | – | fewer Revit warnings |
| 15 | Modelling guideline, open points: phase "Existing" for every element, a parameter measured / assumed on walls, floors, doors and windows | 3 | S | – | guideline met |
| 12 | Slice route: opening heights (a third slice or the top of each gap), sloped roofs, one wall from its upper and lower face | 3 | M | – | slice route 4 to 5 |

## Reading

Every route reaches Revit natively and passes in a real Revit, since 20.10.2026 through pyRevit (all nine
examples, 218 of 218 checks). real project data (details private) Closing the rooms of the slice route
in Revit (3) and finding the rest of the walls on densely partitioned floors (1) are the main open items.
