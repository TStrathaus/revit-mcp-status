# Scoring: current functionality and future functions

State 15.10.2026, evening. Section 12 of the research log scores the outside options; this table scores
what this repository does itself. Update it when a score changes, with the evidence.

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

| Area | Function | Score | Evidence | Gap |
|---|---|---|---|---|
| Scan | Levels and storeys from the scan | 4 | two-storey examples in Revit 2025, all levels right | – |
| Scan | Straight walls (faces, thickness, squaring, joins) | 4 | all scan examples in Revit; real storey against its IFC: 52 % of the wall length on an IFC wall, axis median 60 mm, thickness median -7 mm | real storey not yet in Revit; false walls across clutter |
| Scan | Curved walls | 4 | `curved_bay`: radius exact in Revit | circular arcs only |
| Scan | Doors and windows from holes in the faces | 4 | scan examples in Revit: all hosted, sills to the millimetre | families matched by size only |
| Scan | Door swing and hinge side | 4 | door facing checks pass in Revit | – |
| Scan | Ghost points (glass, mirrors) | 3 | benchmark S9: 97 % removed | – |
| Scan | Stairs, slab openings | 4 | three stair examples 71 of 71 checks in Revit (16 risers, tread right) | straight runs only |
| Scan | Rooms, floor outline | 4 | scan examples: rooms bounded, areas within 3 % | – |
| Scan | E57 reader (real scans, in blocks) | 3 | real hotel: 9 files, 2.5 billion points, 68 GB read in about 10 minutes | – |
| Scan | Large scans: thinning to 2 cm | 3 | 2.5 billion -> 290 M points, one measured point per voxel | – |
| Scan | Slice-weighted storeys (walls 0.3-0.7 m, windows 1.1-1.3 m) | 3 | real storey: 10 M -> 2.7 M points, 591 s -> 112 s, more walls and openings found | storeys of 9 M points still take minutes and 10 GB |
| Scan | Storeys merged in the survey frame, vertical check | 3 | real hotel: 8 floors within 2 cm of the IFC storeys (one +8 cm), slab 0.40-0.44 m on every floor | not yet in Revit |
| 2D plan | DXF and vector PDF | 4 | plan examples in Revit, all checks | – |
| 2D plan | Several storeys, aligned | 4 | two-storey PDF in Revit, stair and void right | – |
| 2D plan | Raster plans through plan-extract (`fpx.py`) | 4 | plan-extract examples in Revit | one example: a room the walls do not close; never on a real result |
| 2D plan | plan-extract run locally | 1 | repository cloned | blocked: the segmenter model is not public |
| 2D plan | Own raster reader | 0 | – | not built |
| IFC | One storey to native Revit (`ifc.py`) | 4 | real model, ground floor: 362 walls, 6 curved, 137 doors and windows, 33 floors; 26 of 32 checks in Revit | stairs with landings, one door on an overlapping shaft wall |
| IFC | Doors and windows without host link (nearest wall) | 4 | 82 of 83 doors, 54 of 54 windows hosted in Revit | – |
| IFC | Rooms without `IfcSpace` (cells between the walls) | 4 | 42 of 43 rooms bounded in Revit | 4 room areas off by overlapping walls |
| Revit, MCP | End-to-end runner (start, calls, checks, report) | 4 | every example and a real IFC storey; stops at "not found", a blocked Revit or a taken port | – |
| Revit, MCP | Unattended runs: failure dialogs answered and logged | 4 | real IFC storey: 695 warnings handled, none blocked, none rolled back | – |
| Revit, MCP | Wall types for every thickness | 4 | 36 types created for a real storey, thickness check passes | – |
| Revit, MCP | Images: new plan per level and 3D view, JPEG | 4 | checked on every example and a real storey | – |
| Revit, MCP | C# snippet compile check | 3 | `tools/snippets/compile_check.py`, Revit 2025 or 2026 | – |

## Future functions

| # | Function | Value | Effort | Depends on | Raises |
|---|---|---|---|---|---|
| 1 | Real scan storeys in Revit, one model per floor and all floors in one | 5 | S | storey runs | scan walls 4 to 5 |
| 2 | Accuracy table: every scanned storey against its IFC storey | 5 | S | 1 | scan 4 to 5 |
| 3 | Door and window types for every size (like the wall types) | 4 | M | – | opening quality |
| 4 | Fewer false walls on real scans (clutter, built-ins) | 4 | M | 2 | scan walls |
| 5 | Raster PDF into Revit | 4 | S to L | decision: segmenter model, own reader or web app | raster plans 1 to 4 |
| 6 | IFC: all storeys | 4 | S | – | – |
| 7 | Stairs with landings (IFC flights, scans) | 3 | L | – | stairs 4 to 5 |
| 8 | IFC: wall types by the IFC type name | 3 | M | – | type quality |
| 9 | IFC: slab holes and openings | 3 | M | – | floors |
| 10 | IFC: columns and beams | 3 | M | – | new element classes |
| 11 | IFC: curtain walls with their doors and windows | 3 | L | – | new element class |
| 12 | A synthetic IFC example (public image, tests without project data) | 2 | S | – | IFC tests |
| 13 | Door swing from the IFC | 2 | S | – | – |
| 14 | Own raster reader (instead of plan-extract) | 3 | L | decision in 5 | raster plans 0 to 3 |

## Reading

Scans, plans, plan-extract results and IFC storeys all reach Revit natively, and every route passes its
checks in a real Revit on synthetic data. The real data of one building (IFC and 2.5 billion scan points)
already gives two measured results: the scans sit within 2 cm of the IFC storeys in height, and walls found
in a scan lie a median 60 mm from the IFC walls. Nothing scores 5 yet: the real scan storeys still have to
go through Revit and be measured storey by storey (items 1 and 2).
