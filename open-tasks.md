# Open functions and tasks

State 24.10.2026, scan2revit 0.7.0. All nine examples pass in Revit through pyRevit; the whole real IFC building builds unattended. One table per sub-project, then what all three share. Plans and decisions: `drawings-and-scans.md`, `local-llm.md`, `github-sources.md`, `decisions.md`. Sources: the gaps
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
| Function | A4 Scan coverage per storey: share of every wall and of the outline seen, coverage image | 4 | M | done (24.10.2026, `pointcloud/coverage.py`) real project data (details private); open: external scans not counted, arc walls not checked, write the share back into plan.json |
| Function | F1 Wall detection on densely partitioned real floors: real project data (details private) | 5 | L | build on the slice route real project data (details private) |
| Function | F16 External parts of the point cloud (`pointcloud/facade.py`): exterior walls measured, slab outline from the facade ring (closed stepwise), edge on the walls' outer face, courtyards as voids | 5 | M | done (24.10.2026), in Revit with the stacked storeys; open: rings where no facade is seen, storeys under the roof and below ground |
| Function | F3 Room separation lines where the slice route's rooms have no wall | 4 | M | at the necks done (short straight shared boundaries); in Revit the rooms still do not close where walls are missing real project data (details private): needs F1 |
| Function | F13 Stairs and ramps in the voids of the slab regions (steps in thin horizontal slices) | 4 | M | – |
| Function | F12 Slice route: measured opening heights, sloped roofs, one wall from its upper and lower face | 3 | M | a third slice or the top of each gap |
| Function | F14 Slab outlines with straight, square edges instead of the 10 cm raster (fewer Revit warnings) | 3 | S | done with F16 where an external scan closes the ring; without one still the 10 cm raster |
| Gap | Galleries: missed at 3 m section spacing, not built as their own Revit level yet | 3 | M | – |
| Gap | Doors and windows: few found on real floors | 3 | M | after F1 |
| Gap | Stairs: straight runs only; curved walls: circular arcs only | 2 | L | stairs with landings: F5 |
| Gap | Memory: large real storeys still take much memory on the full route real project data (details private) | 2 | M | slice route by default |
| Gap | Slab voids under 5 m2 are not cut | 2 | S | – |

## IFC2Revit

IFC storeys to native Revit elements, all storeys in one model. Code `scan2revit/ifc/` and `core/merge.py`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Function | A3 IFC pre-check: what Revit will refuse (degenerate arcs, short pieces, duplicates), fixed where safe, reported | 4 | S | done (24.10.2026, `ifc/precheck.py`, in the storey route; pieces stacked by base offset, which the Revit side now applies) real project data (details private); open: a few doors Revit refuses with very narrow jambs, partitions under 40 mm reported only |
| Task | Revit test of the whole real IFC building through pyRevit (0.7) | 5 | S | done (24.10.2026) real project data (details private) |
| Gap | IFC: a few walls and their openings Revit refuses ("Wand kann nicht erstellt werden"), doors in curved walls | 3 | M | real project data (details private); read the refused wall's geometry |
| Gap | Doors on locked (fire-rated) families keep their size real project data (details private) | 4 | S | F2 (a door family with free size) |
| Function | F5 Stairs with landings (IFC flights; also for scans) | 3 | L | – |
| Function | F6 Wall types by the IFC type name | 3 | M | – |
| Function | F7 Slab holes and openings from the IFC | 3 | M | done (24.10.2026): IfcOpeningElement in slabs and inner loops of slab outlines real project data (details private); in Revit: next run of the whole building |
| Function | F8 Columns and beams | 3 | M | – |
| Function | F9 Curtain walls with their doors and windows | 3 | L | – |
| Gap | Rooms without `IfcSpace`: areas off where walls overlap | 2 | M | – |
| Function | F10 Door swing from the IFC: single-swing doors from the placement (opens towards local +Y) and the operation type (hinge side) | 2 | S | done (24.10.2026) real project data (details private); double doors without swing |

## Plans2Revit

2D plans to Revit: DXF and vector PDF, raster plans through plan-extract results. Code `scan2revit/plans/`.

| Kind | Item | Value | Effort | Next step |
|---|---|---|---|---|
| Gap | Knee walls under a sloping roof built as wide as the drawn band (thickness and height flagged assumed) | 3 | S | decision D-18 |
| Function | Plan sheets with several storeys (`plans/sheet.py`): drawings split, storey labels, ordered bottom first, aligned | 5 | M | done on one real CAD sheet (four storeys); a test needs example sheets from the user |
| Function | Orientation and scale from the sheet: scale from the title block ("1 : 100") done; turning a sheet whose text is not upright not built yet | 5 | S | a turned sheet as example |
| Function | Rooms with the data of their stamps: name, unit (Revit "Abteilung"), number storey.unit.nn; a room at every stamp | 5 | M | done; in Revit on a real sheet, every check passes (23.10.2026) |
| Function | Clutter filter: built-in units, sanitary, text masks, annotation; list in the modelling guideline, machine list `plans/filters.json` | 4 | M | done; furniture only implicitly (no wall pairs) |
| Function | Walls drawn as filled areas in vector PDFs: wall rectangles, openings where the rendered wall colour is absent, swings from chains of short lines | 4 | S | done |
| Gap | Rooms on a real sheet not all closed by walls: real project data (details private) after the corner joins, stub and jog fixes and knee walls (24.10.2026) | 3 | S | the open balcony is correct as drawn; in Revit: next run |
| Gap | Plan sheets: small symbols drawn in wall colour outside the building became wall stubs; a door beside a window in one gap got only the window | 3 | S | done (24.10.2026): loose groups under 1.5 m outside the outline left out and listed; a window gap with a swing at one end split into door and window |
| Function | Storey heights from the elevations sheet (levels and heights instead of the assumed storey height) | 4 | M | built (24.10.2026, `plans/sheet.py --elevations`): level marks of vector elevations or sections; real project data (details private), needs a vector sheet with level texts |
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
| Function | F17 Facts from drawings: catalogue of 29 information types from plans, sections, elevations, build-up legends, schedules, site plans into `facts.json` per project (`drawings-and-scans.md`) | 5 | L | the types half built first (scale, storeys, levels, walls, openings, swings, stamps), then sections and labels |
| Function | F18 Review page: a person accepts, corrects or rejects every fact at gate 1, crops of the drawing beside each value | 5 | M | after F17; decision D-15 (local server) |
| Function | F19 Drawings aligned to the scan frame per storey (2D fit of wall axes, person confirms) | 5 | M | needs drawings and a scan of the same building from the user; D-14 |
| Function | F20 Drawn facts as priors in modelling: levels, thickness of one-sided walls, slab thickness, opening heights, room names on scan rooms, drawn walls as hypotheses for the slice route | 5 | L | after F18, F19; D-4, D-16 |
| Function | F21 Checker: drawn vs measured for every accepted fact, unused facts listed | 4 | M | after F20 |
| Function | F22 Local LLM helper (`local-llm.md`): text classification, build-up parsing, raster reading; always proposed facts, checked by code | 3 | M | measure speed on this machine, pilot on the plan sheets; D-7 |
| Function | F23 Build-ups (floor, wall, roof) parsed into layers and thicknesses; slab thickness from them | 4 | M | with F17; D-5 (generic types stay) |
| Task | F24 Agent team phases updated for drawings first (phase 2a, alignment 2c, review at gate 1, drawn vs measured in the check) | 4 | S | planned phases described in `agent-team.md` (24.10.2026); the agent files follow with F17 to F21 |
| Task | GitHub sources: licence and security check before any skill or code is taken; pinned and listed (`github-sources.md`) | 3 | S | rule in place; `third_party/README.md` with the first copied file |
| Function | S1 Agent scoreboard: actions, findings, defects found and fixed, gate verdicts and check scores per agent and project, summed up over projects | 5 | M | done (24.10.2026, `tools/scoreboard.py`; every phase records its entry; summary `documentation/agent-scoreboard.md`, site page agents.html); first real use: the team's next test build |
| Function | V1 Rule ids in the modelling guideline, each rule with its Revit check; R2 table rule -> check | 4 | M | done (24.10.2026): ids G-0.1 to G-13.4, checks prefixed with their id, new checks G-1.2, G-4.2, G-11.2, G-11.3, table in section 14; open: checks for G-5.2 (wall base and top), G-5.4 (room bounding), G-11.1, G-11.5 (names); decision D-20 for G-11.4 |
| Function | R1 Rule proposals: agents propose guideline changes in their handover, the project manager collects them, the user approves | 4 | S | done (24.10.2026): handover section, `rule-proposals.md`, approval by the user |
| Function | V2 Comparison with a reference (an IFC of the same building) as a standard checker step, LOA tolerances | 4 | M | done (24.10.2026, `core/compare.py`, in `phase check`) real project data (details private); open: arcs, stairs, opening heights; IFC linings as walls (`--min-thickness`) |
| Function | V3 Each Revit run compared with the previous one: checks gained, lost, still failing | 3 | S | done (24.10.2026): e2e runs and project checks say what changed since the last run |
| Function | A1 Machine-readable input reports for every route (verdict per item) | 4 | M | done (24.10.2026, `core/inputs.py`: pointcloud, ifc with the pre-check, plans); limits are start values (D-21) |
| Task | Unattended runs: check that the pyRevit agent host answers Revit's failure dialogs like the old add-in | 4 | S | done (24.10.2026) real project data (details private) |
| Function | F2 A door and a window family with free size in the blank project (the template) | 4 | S | **you**: load the families into the template |
| Task | Agent team: first model built in Revit, phase by phase with its gates | 4 | M | the synthetic project first, then a real building |
| Function | F15 Modelling guideline: phase "Existing" for every element, a parameter measured / assumed on walls, floors, doors and windows | 3 | S | done (24.10.2026): stage `existing`, shared parameter `scan2revit source`; checked by the runner |
