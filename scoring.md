# Scoring: current functionality and future functions

State 16.10.2026. Section 12 of the research log scores the outside options; this table scores what this
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
| Convert point clouds | Levels and storeys from the scan | 5 | real hotel, 9 storeys in Revit: every floor within 2.1 cm of the IFC storey (one, under a sloped roof, +6.6 cm) | – |
| Convert point clouds | Straight walls (faces, thickness, squaring, joins) | 4 | all scan examples in Revit; real storeys against their IFC: 42-69 % of the wall length on an IFC wall, median axis distance 1-30 cm | real floors: a tenth of the walls found, often joined too long (the slice route finds far more) |
| Convert point clouds | Curved walls | 4 | `curved_bay`: radius exact in Revit | circular arcs only |
| Convert point clouds | Doors and windows from holes in the faces | 4 | scan examples in Revit: all hosted, sills to the millimetre | few found on real floors |
| Convert point clouds | Door swing and hinge side | 4 | door facing checks pass in Revit | – |
| Convert point clouds | Ghost points (glass, mirrors) | 3 | benchmark S9: 97 % removed | – |
| Convert point clouds | Stairs, slab openings | 4 | three stair examples in Revit, 16 risers, tread right | straight runs only |
| Convert point clouds | Rooms, floor outline | 4 | scan examples: rooms bounded, areas within 3 %; slivers under 1 m2 left out | – |
| Convert point clouds | E57 reader (real scans, in blocks) | 4 | real hotel: 9 files, 2.5 billion points, 68 GB, storeys built in Revit | – |
| Convert point clouds | Large scans: thinning to 2 cm | 4 | 2.5 billion -> 290 M points in about 10 minutes | – |
| Convert point clouds | Slice-weighted storeys (walls 0.3-0.7 m, windows 1.1-1.3 m) | 4 | real storeys in Revit; one storey 10 M -> 2.7 M points, 591 s -> 112 s | 8-9 M points still take 10-18 GB |
| Convert point clouds | Slice route: walls, doors, windows, rooms, floor from two 20 cm slices (`slice2d`) | 4 | synthetic (bench SL1-SL5): all walls (faces within 1 mm), doors with swing, windows, rooms; example 15 of 16 checks in Revit. Real hotel, 9 storeys: 14-70 s and under 1.1 GB each; guest floors 39-49 % of the IFC wall length found (full route 19-35 %), 90-93 % of it on IFC walls (51-69 %), rooms 26-54 % one to one with the IFC (0-5 %); a real storey in Revit 14 of 17 checks | rooms not closed in Revit where walls are missing; opening heights given, not measured; sloped roofs (6OG) |
| Convert point clouds | Slabs and levels from vertical sections (`sections`), refined where neighbours differ | 3 | synthetic: floors exact, slab thickness within 2 cm, gallery found, beds and a ramp no level; real hotel: 3 sections per direction, refined at half distance where suspicious, none closer than 3 m: 22 sections, 1 minute, 10 of the 11 scanned IFC levels without given heights (within 1.2 cm, attic +7.6 cm), slabs 0.40-0.42 m; floors and slab thickness go into the slice route | the gallery (IFC 01) is missed at 3 m spacing; some slab thicknesses from few pairs; galleries not built as their own Revit level yet |
| Convert point clouds | Slab regions per floor from horizontal slices: outlines, voids (shafts, stairwells, courtyards), galleries | 4 | synthetic: floor regions, a stairwell void, a hidden floor filled, the gallery; hotel: 87-100 % of each region on the IFC floor, 63-80 % of the IFC floor covered; 3OG in Revit: floor from the region (0.40 m) and 4 voids cut | outlines from a 10 cm raster (Revit sketch warnings); voids under 5 m2 not cut; stairs in the voids not read |
| Convert point clouds | Storeys merged in the survey frame, vertical check | 4 | real hotel: 9 storeys in one Revit model, floors checked against the IFC | – |
| Convert floor plans | DXF and vector PDF | 4 | plan examples in Revit, all checks | – |
| Convert floor plans | Several storeys, aligned | 4 | two-storey PDF in Revit, stair and void right | – |
| Convert floor plans | Raster plans through plan-extract (`fpx.py`) | 4 | plan-extract examples in Revit | one room the walls do not close; never on a real result |
| Convert floor plans | plan-extract run locally | 1 | repository cloned | blocked: the segmenter model is not public |
| Convert floor plans | Own raster reader | 0 | – | not built |
| Convert IFC | One storey to native Revit (`ifc.py`) | 5 | real ground floor: 28 of 34 checks; walls on the IFC axis, all thicknesses, all windows hosted | stairs with landings |
| Convert IFC | All storeys in one model (`merge.py`) | 4 | real hotel, 12 levels: 4274 of 4278 walls, 153 floors, 29 stairs, 798 of 841 doors, 366 of 370 windows; 161 of 212 checks | doors on locked families |
| Convert IFC | Openings on the right wall piece, panes left out | 4 | 'cannot cut from wall' 359 -> 36 on the whole building | – |
| Convert IFC | Rooms without `IfcSpace` (cells between the walls) | 4 | real storey: 42 of 43 rooms bounded; synthetic house exact | areas off where walls overlap |
| Convert IFC | Synthetic IFC example and tests | 4 | `bench/ifc_synth.py`: 3 tests, 22 of 22 checks in Revit | – |
| Revit and MCP (all routes) | End-to-end runner (start, calls, checks, report) | 4 | every example, a real IFC building and real scan storeys | – |
| Revit and MCP (all routes) | Unattended runs: failure dialogs answered and logged | 4 | whole IFC building: 6772 Revit failures answered, none blocked, none rolled back | – |
| Revit and MCP (all routes) | Wall types for every thickness | 4 | 58 thicknesses created for the whole IFC building, every thickness check passes | – |
| Revit and MCP (all routes) | Door and window types for every size | 3 | 137 sizes created, windows at their size; size check in every run | fire-rated door families lock their size |
| Revit and MCP (all routes) | Images: new plan per level and 3D view, JPEG | 4 | every example and the real models | – |
| Revit and MCP (all routes) | C# snippet compile check | 3 | `tools/snippets/compile_check.py`, Revit 2025 or 2026 | – |

## Future functions

| # | Function | Value | Effort | Depends on | Raises |
|---|---|---|---|---|---|
| 1 | Wall detection on densely partitioned real floors (hotel rooms) | 5 | L | – | scan walls 4 to 5 |
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

Every route reaches Revit natively and passes in a real Revit. The real data of one building now gives
measured results: an IFC storey and the whole IFC building in Revit, and nine scanned storeys within 2 cm
of the IFC in height. The full scan route's wall detection is exact on synthetic data but finds only a
tenth of the walls of a densely partitioned hotel floor. The slice route reads the same floors from two
20 cm slices in under a minute and a gigabyte, finds four to five tenths of the IFC walls with nine
tenths of what it finds on them, and the first rooms that match the IFC; closing those rooms in Revit
(3) and the rest of the walls (1) are the main open items.
