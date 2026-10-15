# Scoring: current functionality and future functions

State 15.10.2026. Replaces nothing in the research log (its section 12 scores the outside options); this
table scores what this repository does itself. Update it when a score changes, with the evidence.

## Scale

Maturity 0 to 5:

| Score | Meaning |
|---|---|
| 0 | not started |
| 1 | designed only |
| 2 | code exists, not verified |
| 3 | passes the synthetic tests and the benchmark |
| 4 | passes in a real Revit (`scan2revit/tools/revit_e2e.py`) |
| 5 | proven on real project data in Revit |

Future functions: value 1 to 5 (5 = most useful), effort S (hours), M (a day or two), L (more).

## Current functionality

| Area | Function | Score | Evidence | Gap |
|---|---|---|---|---|
| Scan | Levels and storeys from the scan | 3 | benchmark S1 to S10 | not yet in Revit with several storeys |
| Scan | Straight walls (faces, thickness, squaring, joins) | 4 | `curved_bay` 15 of 15 checks in Revit 2025; benchmark faces within 15 mm | no real scan yet |
| Scan | Curved walls | 4 | `curved_bay`: radius 5.0031 m exact in Revit | circular arcs only |
| Scan | Doors and windows from holes in the faces | 4 | `curved_bay`: all hosted, sills to the millimetre | families matched by size only |
| Scan | Door swing and hinge side | 3 | benchmark 8 of 8 | Revit check not run yet |
| Scan | Ghost points (glass, mirrors) | 3 | benchmark S9: 97 % removed | – |
| Scan | Stairs, slab openings | 3 | benchmark S10 | not yet in Revit |
| Scan | Rooms, floor outline | 4 | `curved_bay`: 3 rooms bounded, areas within 3 % | – |
| Scan | E57 reader | 2 | `pye57` installed, code path exists | no real E57 read yet |
| Scan | Large scans (more than 1 GB) | 0 | – | needs a chunked reader |
| 2D plan | DXF and vector PDF | 3 | benchmark P1 to P7, faces exact | not yet in Revit |
| 2D plan | Several storeys, aligned | 3 | benchmark P6, P7 | – |
| 2D plan | Raster plans through plan-extract (`fpx.py`) | 3 | synthetic F1 to F3, plan-extract's test floor | never on a real result |
| 2D plan | plan-extract run locally | 1 | repository cloned | blocked: the segmenter model is not public |
| 2D plan | Own raster reader | 0 | – | not built |
| IFC | One storey to the build plan (`ifc.py`) | 2 | real model, ground floor: 362 walls, 6 curved, 137 doors and windows, 33 floors, 4 flights, 43 rooms; preview checked | Revit run pending |
| IFC | Doors and windows without host link (nearest wall) | 2 | 79 more openings placed | not verified in Revit |
| IFC | Rooms without `IfcSpace` (cells between the walls) | 2 | 43 cells | halls open to curtain walls stay open |
| Revit, MCP | End-to-end runner (start, calls, checks, report) | 4 | `curved_bay`; stops at "not found", a blocked Revit or a taken port | – |
| Revit, MCP | Images: cropped plans and 3D view, JPEG | 3 | checked in Revit as PNG | JPEG export not run yet |
| Revit, MCP | Unattended failure handling (add-in patch) | 2 | built and installed for Revit 2025 | first run pending |
| Revit, MCP | Wall and opening types by size | 3 | used in `curved_bay` | no mapping by IFC type name |
| Revit, MCP | C# snippet compile check | 3 | `tools/snippets/compile_check.py` | – |

## Future functions

| # | Function | Value | Effort | Depends on | Raises |
|---|---|---|---|---|---|
| 1 | IFC storey in Revit, checked against the IFC | 5 | S | add-in confirmed once in Revit | IFC 2 to 4, then 5 |
| 2 | First real scan (small E57) | 5 | S | – | E57 reader 2 to 4 |
| 3 | Chunked E57 reader and survey shift (large scan) | 5 | M | 2 | large scans 0 to 3 |
| 4 | Scan of the same building against the IFC storey: first measured accuracy | 5 | M | 1, 3 | scan walls 4 to 5 |
| 5 | Raster PDF into Revit | 4 | S to L | decision: segmenter model, own reader or web app | raster plans 1 to 4 |
| 6 | All examples in Revit (stairs, slab openings, swings, 2D plans) | 4 | S | – | several 3 to 4 |
| 7 | IFC: all storeys | 4 | S | 1 | – |
| 8 | IFC: wall types by the IFC type name | 3 | M | 1 | type quality |
| 9 | IFC: slab holes and openings | 3 | M | 1 | floors |
| 10 | IFC: columns and beams | 3 | M | 1 | new element classes |
| 11 | IFC: curtain walls with their doors and windows | 3 | L | 1 | new element class |
| 12 | Stairs with landings | 3 | L | – | stairs 3 to 4 |
| 13 | Door swing from the IFC | 2 | S | 1 | – |
| 14 | Own raster reader (instead of plan-extract) | 3 | L | decision in 5 | raster plans 0 to 3 |

## Reading

The core (walls, openings, rooms) works in Revit on synthetic data; nothing is proven on real data yet
(no score 5). Items 1 and 2 are small steps; item 4 gives the project's first measured accuracy.
