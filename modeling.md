---
name: modeling
description: Modelling guideline for as-built Revit models from scans, plans and IFC (scan2revit): what each element is in Revit, how it is typed, placed, named and checked, what is only reported. Use when building, checking or editing a model made with scan2revit, when choosing wall, floor, door or window types, or when a question is "how should this be modelled?".
---

# Modelling guideline: as-built Revit models (scan2revit)

These are the rules a model made with scan2revit follows, and the ones it should follow where the code does not
yet (marked **open**). The workflow (running the pipeline, mapping types, sending the calls) is in
`skills/scan-to-revit/SKILL.md`; this file says what the result must be. **G-0.1** When a project has its own BIM
execution plan (BAP, SIA 2051) or the client's modelling rules, those come first; this guideline fills what
they leave open.

**G-0.2** Data first, then the modelling decision. Before anything is modelled, the available data is analysed
(input reports of the scans, IFC and plans; drawings such as sections and build-up legends; documentation), and
the level of detail per element class is decided from it and recorded (the project manager at gate 1, in
status.md: "Modelling decisions"). The simple form is the default: a slab is **one element of its full
thickness** (finished floor to soffit), a wall one element face to face. A slab is split into the structural slab
and its floor build-up, or a wall into its layers, only where sections, build-up legends or documentation give
that build-up (accepted facts, `documentation/drawings-and-scans.md`), never because a template or a habit offers
it. (User, 25.10.2026.)

Every rule has a stable id (G-1.1, G-2.1, ...: section and number, in bold before the rule). Checks, findings and rule proposals
name the rule by its id; which check tests which rule: section 14. A rule changes only when the user approved
the change (proposals: `documentation/agent-team.md`); a new rule takes the next free number of its section,
a removed rule's id is not used again.

Basis: the BIMForum Level of Development specification (LOD 200: generic elements at the right size and
place), the USIBD Level of Accuracy (LOA: measured and represented accuracy kept apart), SIA 2051 / KBOB (the
level of detail is set per project in the BAP), the SBB rules for building models (an as-built model holds
existing elements only), the Autodesk Revit documentation (constraints, room bounding, location line, shared
coordinates). No published Swiss modelling guideline for as-built models from scans was found; sources at the end.

## 1. Walls and slabs are generic, no construction information inside

- **G-1.1** Every wall and every floor (slab) has a generic type: **one layer, no material, no build-up**. The type
  carries the thickness and nothing else; its name says so: `scan2revit 300 mm`, `scan2revit floor 400 mm`.
- Why: a scanner sees surfaces, not what is behind them; a plan or a scan does not show the build-up. A
  layered type from a template (plaster, brick, insulation) states a construction nobody measured. BIMForum
  LOD 200 is exactly this: a generic assembly at the right size, shape and place. Single-layer components are
  also what modelling guides ask for when the build-up is not known (bimaterial, variant MGPa).
- **G-1.2** The build-up is added later, by the project, when it is known: by swapping the generic type for a project
  type of the same thickness, never by editing the generic one.
- **G-1.3** Doors and windows follow the same idea: generic families with free width and height; no fire rating, no
  hardware, no material.
- **G-1.4** Current: the Revit module (`revit_runtime.py`, run by pyRevit) uses only `scan2revit` wall and floor types
  (one layer, no material) and makes the missing ones (floor types are copied from a floor type, never from a
  foundation slab type, which Revit also files as a floor type); the check "walls and floors generic" fails on
  any wall or floor with a build-up or a material. All nine examples passed it in Revit 2025, through the old
  add-in (0.5) and through pyRevit (0.7, 20.10.2026). Door and window sizes are
  set where the family takes them: Swiss families ("TU ...") through "Angabe Maueröffnungsmaß Breite / Höhe"
  (the masonry opening, what a scan measures), read back from "Breite" / "Höhe ab FBOK"; every door and window
  of the examples gets its size. A door of the plan never gets a passage family (an opening without a leaf,
  e.g. "TU Durchgang": it draws no swing in plan), even where its stock size fits best; a passage of the plan
  gets no element but a room separation line (section 9). The template's door families still carry fire ratings
  in some types (**open**: generic door and window families without them in `blank.rvt`).

## 2. Measured or assumed: say which

- **G-2.1** Every dimension is either measured or assumed, and the model says which. Assumed are today: the thickness
  of a wall seen from one side (`thickness_assumed`), door head, window sill and head in the slice route and
  in 2D plans (`heights_assumed`), slab thickness without a vertical section through it.
- **G-2.2** The accuracy is stated per element class as USIBD LOA: measured accuracy (of the scan) and represented
  accuracy (of the model) apart. Measured on real data so far: real project data (details private); synthetic faces within 1 mm.
- **G-2.3** In Revit: the shared instance parameter `scan2revit source` (group Data) on walls, floors, doors and windows
  says `measured` (taken from the scan, the drawing or the IFC) or `assumed: <what>` (`assumed: thickness`,
  `assumed: head`, `assumed: sill and head`). The last build stage (`existing`) adds it through a shared
  parameter file in the temp folder and restores the user's own shared parameter file setting. The flags stay
  in `plan.json` and `report.md` as well.

## 3. Existing elements only

- **G-3.1** An as-built model holds the building as it is: no demolition, no new construction, no design intent.
- **G-3.2** Every element in the phase "Existing" (Bestand): the stage `existing` sets "Phase Created" of every element
  the tool made to the template's existing phase (by name: Existing, Bestand, Bestehend; else the first phase).
  Rooms keep the phase of the view they were placed in; they are bounded by the existing walls all the same.
- **G-3.3** Not modelled, only reported in the QA: furniture, fittings, MEP, finishes, build-ups, anything the scan
  only shows in part (ghost points, mirrors).

## 4. Levels and storeys

- **G-4.1** One level per floor top (finished floor as scanned), named by its storey (EG, 1OG, ... or as the project
  names them). A gallery (a partial floor with less than 2.2 m headroom) gets a level of its own, `Gallery n`.
- **G-4.2** Every element sits on the level of its storey; nothing hangs on a level of another storey.
- **G-4.3** Elevations: Level 0 at elevation 0 in the local frame; the survey offset carries the height above sea
  (`plan.origin.offset_xyz`). Several storeys from one survey frame (`merge`) keep their measured heights.
- **G-4.4** Floor heights come from the vertical sections (`scan2revit.pointcloud.sections`); the scan's height histogram
  only where no section can be cut. A slab underside (a ceiling with a floor 0.12-0.9 m above it) is never a floor.
  Every check made at a floor height (density, registration) uses these floors. Storeys with steps are separate
  levels or reported (`steps_to` in slabs.json). (Approved by the user 25.10.2026, proposed by the point cloud man.)

## 5. Walls

- **G-5.1** Straight walls on their centreline (location line "Wall Centerline", the same as "Core Centerline" for a
  single-layer generic wall), from face to face as measured. Curved walls as arcs (circular only).
- **G-5.2** Base: the storey level. Top: the underside of the slab above (unconnected height = storey floor to
  ceiling). Walls stop at the slabs; they do not run through them.
- **G-5.3** Corners and junctions: centrelines joined at their crossings; overlapping walls are an error to remove.
- **G-5.4** Room bounding: on (the default) for every wall.
- **G-5.5** A wall seen from one side keeps its seen face; the thickness is assumed (0.30 m unless `--exterior-thickness`)
  until an external scan (facade or drone, same survey frame: `scan2revit.pointcloud.facade`) shows its outer
  face, a door reveal measures it or `--thickness-overrides` sets it. The outer face is the dominant face 8 cm to
  1 m behind the inner one in the storey's height band (0.30-1.60 m); pilaster fronts and window frames are
  smaller peaks. Then the wall is "paired", thickness source "inner face + exterior scan". Not for a storey under a sloping roof or below
  ground (`--no-walls`): the band sees eaves and dormers, or terrain.
- **G-5.6** Orientation: with `--align-north` the model is turned so the walls run along the project axes (project
  north); true north keeps the survey bearing (`plan.origin.rotation_deg`).

## 6. Floors (slabs) and voids

- **G-6.1** One floor per slab region (from a horizontal slice at the level, `scan2revit.pointcloud.sections` / `slice2d --slabs`),
  top of the slab at the level, thickness downwards as measured in the vertical sections (else 0.25 m,
  assumed). Without slab regions the outline comes from the walls or the free space.
- **G-6.2** Voids are openings cut into the floor (`NewOpening`): shafts and stairwells (5 m2 or more with no ceiling of
  the storey below under them), courtyards and atria (over 60 m2). Holes the floor is only hidden in
  (furniture) are not voids.
- **G-6.3** With an external scan the floor outline is the building's outline at the facade (`pointcloud.facade`): the
  vertical facade points around the storey form a ring (windows and doors closed, up to 1.6 m; 2.4 and 3.2 m only where the ring stays open); inside the outer ring is
  slab, also where the inside was not scanned; an enclosed space of 30 m2 or more with no scanned floor and its
  own ring of facade points is a courtyard (a void). Flat things in front of the facade (canopies, terrace
  roofs, sills) are not facade; protrusions under 0.8 m (pilasters) are ironed out; edges near the building
  axes are squared. The edge lies on the outer face of the load-bearing walls: the outline is pulled in by the
  cladding depth, measured as the median distance from the outer face of the walls measured from the external
  scan to the facade outline (cladding, cornices, sills are not slab). A ring that does not hold 90 % of the
  scanned floor is open (missing points, shop fronts, terrain): the scanned outline stays.
- **G-6.4** Without an external scan the outline is simplified from the 10 cm raster (**open**: straight, square edges,
  Revit warns about sketch lines slightly off axis).

## 7. Doors and windows

- **G-7.1** Hosted in their wall, one generic type per size, named `scan2revit <w> x <h>` (a copy of the nearest type
  with width and height set; existing sizes within 50 mm are reused). Sizes under 200 mm are not openings.
- **G-7.2** Width and position as measured; sill and head as measured in the full scan route, given (and flagged) in
  the slice route and in 2D plans.
- **G-7.3** Door swing and hinge side as scanned (the open leaf), drawn (the swing arc) or given in the IFC (single-swing
  doors: the leaf opens towards the door's local +Y axis, the hinge side from the operation type LEFT / RIGHT);
  a closed door in a scan and a double door in an IFC have none: the swing stays the family default and is
  reported.

## 8. Stairs, slab openings, ramps

- **G-8.1** Stairs: one straight run per flight (StairsEditScope), riser count and tread from the scan or plan, width on
  the run, from the lower level to the upper. **Open**: landings, winders, spiral stairs; stairs in the voids
  found by the sections.
- **G-8.2** Ramps and sloped roofs are reported, not built.

## 9. Rooms

- **G-9.1** One room per enclosed area, placed at a point inside it; name and number from the plan or the IFC, else
  `Room <storey>.<n>`; net area to the wall faces. Cells under 1 m2 are slivers, not rooms.
- **G-9.2** A room must be enclosed (Revit: "bounded"). A passage between two rooms (a gap with no wall and no door)
  gets a room separation line across it, 5 cm into the wall ends (plan-extract passages: done). Where walls
  are missing (real scans), rooms come from the free space: at the necks where two such rooms meet (a shared
  boundary up to 2.5 m, straight within 0.3 m: a doorway with no door seen) a room separation line, 0.2 m into
  the walls at its ends. Long or bent shared boundaries are missing walls: no line (it would cut through rooms);
  those rooms are placed but not enclosed (**open**: walls found there, F1).
- **G-9.3** Room stamps of a plan sheet (plans.sheet): every stamp gives a room at its position, also where the walls do
  not close around it (then placed, not enclosed, listed in qa). Name = the stamp's name ("Küche"); the unit
  above it goes to Revit's room parameter "Abteilung" (Department): "Wohnung <n>", "G" = "Allgemein"; number =
  storey.unit.nn ("EG.1.03", counted per storey and unit). On sheets with filled walls every gap in a wall is
  an opening: a door (swing), a window (frame lines) or, without a symbol, a passage with a room separation line.
- **G-9.6** Rooms are shown in every floor plan of their level: a room tag (Raumstempel) at the room's point, of a
  type that shows at least the area (a template type whose name says area / Fläche, else the first loaded), and
  the rooms' interior fill ("Innenfüllung") visible, which Revit draws pale blue on screen (set on the plans' view
  template where they have one, so it holds for every plan of it; Revit leaves it out of prints and image exports,
  and its colour is Revit's own). Room data of the input go into the room: name, number, unit (department), use
  (occupancy) and finishes where the input carries them. (25.10.2026, asked by the user.)

## Not modelled: what a plan carries that is not building

**G-9.4** Left out of the model (machine list: `scan2revit/plans/filters.json`; keep both in step):

| Drawn | How it is recognised | Why left out |
|---|---|---|
| Built-in units, cupboards, kitchen units, shafts | a rectangle with both diagonals (crossed box), up to 3 m, not on a wall | furniture and fit-out, not structure; shafts: **open** (slab openings) |
| WC, washbasin, sink, hob, drain, washing machine | full circles and closed arcs up to 0.45 m radius | sanitary and kitchen equipment |
| Furniture (tables, chairs, beds, sofas) | line work inside a room that pairs into no wall and no opening | not building |
| Text masks behind stamps and labels | white filled rectangles not on a wall | drawing aid |
| Dimensions, levels (+3.40), areas (m2), symbol labels (EL, Dachfenster) | text patterns (`filters.json` "texts") | annotation, not a room name |
| Frame, title block, view numbers | long lines, the box with PLAN-NR / DATUM / scale | sheet, not drawing |
| Small symbols in wall colour outside the building (ticks, markers, a chimney ring) | touching wall pieces together under 1.5 m whose middle lies outside the building outline | not walls; listed in the QA |

**G-9.5** A crossed box on a wall is a window, never a cupboard. A white box on a wall is a window symbol.
A gap with window lines and a swing at one end is a door beside a window (a balcony door): both are placed.


## 10. Coordinates and georeferencing

- **G-10.1** The model stays near Revit's internal origin; the Survey Point carries the large coordinates (LV95 E, N and
  the height): `plan.origin.offset_xyz`. True north: the angle `-rotation_deg` when `--align-north` turned the
  model. Set them in Revit (or tell the user to); never move elements to "fix" coordinates.
- **G-10.2** One coordinate source for all storeys and disciplines (the survey); acquire or publish shared coordinates
  once, link by shared coordinates, check with a control point.

## 11. Naming

| Rule | Element | Name |
|---|---|---|
| **G-11.1** | Level | storey name (EG, 1OG, UG2) or `Level n`; galleries `Gallery n` |
| **G-11.2** | Wall type | `scan2revit <t> mm` (generic, one layer) |
| **G-11.3** | Floor type | `scan2revit floor <t> mm` (generic, one layer) |
| **G-11.4** | Door / window type | `scan2revit <w> x <h>` (copy of the nearest family type, size set) |
| **G-11.5** | Room | name from the plan or IFC, else `Room <storey>.<n>`; number `<storey><nn>` |
| **G-11.6** | Element ids in plan.json | walls `W<storey>-<nn>`, curved walls `A..`, openings `O..`, stairs `S..`, slab openings `V..` |

## 12. Checks a model must pass (tools/revit_e2e.py)

**G-12.1** Levels at the planned elevations; walls (straight and curved) per level and their thicknesses; walls and floors
generic; doors and windows hosted and within 50 mm of their size; window sills; floors per level and their
thicknesses; slab openings cut; stairs (risers, tread, levels); rooms bounded and their areas within 3 %; door
swings to the scanned side; Revit warnings and the failures answered without a transaction rolled back.
Each check names the rule it tests by its id; the whole list, and the rules no check covers yet: section 14.

## 13. Working rules

- **G-13.1** Never move or edit elements that were not created in this run.
- **G-13.2** Revit errors during a stage: an error that offers a resolution is resolved with Revit's default (walls that
  cannot stay joined are unjoined) and listed in the stage notes, instead of rolling back the whole stage; a
  floor whose outline Revit refuses is tried once more with a coarser outline, then left out with a note.
- **G-13.3** Do not create types, levels or coordinates silently in a real project: ask; in test copies the runner does it.
- **G-13.4** Quote accuracy with its source: synthetic results (bench/results.md) are optimistic; real scans carry
  registration error, glass and clutter.

## 14. Rule -> check

The checks of `tools/revit_e2e.py` (also run by `tools/revit_project.py phase check`) by rule; each check's name
starts with the rule's id. "Not checked": no check on the model read back from Revit yet (some are tested
without Revit in `tests/`, or belong to the input side).

| Rule | Check |
|---|---|
| G-0.1 | not checked (the project's BAP) |
| G-0.2 | not checked (gate 1: the modelling decisions in status.md) |
| G-1.1 | walls and floors generic (one layer, no material) |
| G-1.2 | scan2revit wall and floor types not edited into a build-up (also the unused ones) |
| G-1.3 | not checked (door and window families with fire ratings in the template: open) |
| G-1.4 | not checked in Revit (no passage family for a door: unit test) |
| G-2.1 | not checked (the flags in plan.json; in Revit: G-2.3) |
| G-2.2 | not checked (accuracy in the report) |
| G-2.3 | measured / assumed on walls, floors, doors and windows |
| G-3.1 | not checked |
| G-3.2 | every element in one phase, the existing one |
| G-3.3 | not checked (QA of the input) |
| G-4.1 | not checked (level names) |
| G-4.2 | every element on a planned level (walls, floors, doors, windows, rooms) |
| G-4.3 | levels at the planned elevations |
| G-4.4 | not checked (input side: sections) |
| G-5.1 | per level: walls (straight, curved); wall thicknesses; curved wall radius |
| G-5.2 | not checked (wall base and top) |
| G-5.3 | not checked (overlaps show in the Revit warnings) |
| G-5.4 | not checked (room bounding) |
| G-5.5 | not checked (input side) |
| G-5.6 | not checked |
| G-6.1 | per level: floors; floor thicknesses |
| G-6.2 | slab openings cut |
| G-6.3 | not checked (input side: facade) |
| G-6.4 | not checked |
| G-7.1 | per level: doors and windows hosted; in curved walls |
| G-7.2 | per level: doors and windows within 50 mm of their size; window sills |
| G-7.3 | door swings: facing points to the scanned swing side |
| G-8.1 | stair: risers, base and top level |
| G-8.2 | not checked |
| G-9.1 | per level: room areas within 3 % |
| G-9.2 | per level: rooms bounded |
| G-9.3 | per level: room departments (units) |
| G-9.6 | per level: every room tagged in the floor plans |
| G-9.4 | not checked (input side: plans filters) |
| G-9.5 | not checked (input side: plans sheet) |
| G-10.1 | not checked (survey point and true north are set by hand) |
| G-10.2 | not checked |
| G-11.1 | not checked (level names) |
| G-11.2 | wall types named by their thickness |
| G-11.3 | floor types named by their thickness |
| G-11.4 | not checked (a loaded type within 50 mm keeps its own name) |
| G-11.5 | not checked (room names and numbers) |
| G-11.6 | not checked (plan.json) |
| G-12.1 | every check of this table |
| G-13.1 | not checked in Revit (every stage deletes only its own elements: unit test) |
| G-13.2 | every stage committed without error; Revit failures and dialogs handled (no error) |
| G-13.3 | not checked |
| G-13.4 | not checked |

Two checks name no rule: "every planned element was built" and "Revit warnings" (reported, never failed).

## Sources

- BIMForum, Level of Development Specification (2015 reprint): https://bimforum.org/wp-content/uploads/2022/06/BIMForum_LOD_2015_reprint.pdf
- LOD for scan-to-BIM (LOD 200 walls without layers or materials): https://www.designingbuildings.co.uk/wiki/A_Comprehensive_Guide_to_Choose_the_Right_LOD_for_Your_Scan_to_BIM_Projects
- Scanners see surfaces only, LOD 300+ needs other investigation: https://www.geoweeknews.com/articles/vol13no4-why-lod-300-isnt-so-easy/
- USIBD Level of Accuracy (LOA10-50; measured vs represented): https://techture.zohodesk.in/portal/en/kb/articles/loa-level-of-accuracy, https://bimforum.org/event/specifying-reality-capture-with-loa-level-of-accuracy-and-lod-level-of-development/, https://isprs-archives.copernicus.org/articles/XLII-2-W8/45/2017/isprs-archives-XLII-2-W8-45-2017.pdf
- SBB, Regelwerk Bauwerksmodelle (as-built model: existing elements only; SIA 2051 and the BAP set the detail): https://company.sbb.ch/content/dam/internet/corporate/downloads/de/sbb-als-geschaeftspartner/einkauf/bim/regelwerk-bauwerksmodelle.pdf.sbbdownload.pdf
- CHGEOL, Richtlinie Bauwerksmodelle (LOG/LOI per BAP, SIA 2051): https://chgeol.org/wp-content/uploads/2023/09/Richtlinie_Bauwerksmodelle-V3_0.pdf
- KBOB, Empfehlungen zum Umgang mit BIM: https://www.kbob.admin.ch/dam/de/sd-web/DehwSu7MxwmU/20180115_KBOB-Empfehlungen_Umgang_BIM_Publikation_DE.pdf; Anwendung der Methode BIM im Hochbau (Stadt Zürich edition): https://www.stadt-zuerich.ch/content/dam/web/de/planen-bauen/projekte-und-ausschreibungen/dokumente/hochbauvorhaben/vorgaben/bim-pilotprojekte/ahb-standard-bim-kbob.pdf
- bimaterial Modellierleitfaden (single-layer components where the build-up is not given): https://NachhaltigWirtschaften.at/resources/sdz_pdf/bimaterial_modellierleitfaden.pdf
- BLB NRW, Modellanforderungen (every element on its storey's level): https://www.blb.nrw.de/fileadmin/Home/Service/Service_fuer_Auftragnehmer/Standards_Erlasse_Regelungen/BIM/bim-modellanforderungen.pdf
- Autodesk Revit help: wall properties (constraints, room bounding): https://help.autodesk.com/cloudhelp/2023/ENU/Revit-ArchDesign/files/GUID-ED2045E5-90BF-418F-AAD6-3BB1544F34F5.htm; wall location line: https://help.autodesk.com/cloudhelp/2019/ENU/Revit-Model/files/GUID-F26DB6DA-A0EC-424D-B656-3BDF47607F4F.htm; coordinates: https://help.autodesk.com/cloudhelp/2023/ENU/Revit-Model/files/GUID-E67ED082-2556-475B-84A7-4605329F612F.htm
- Project north and true north: https://novedge.com/blogs/design-news/revit-tip-revit-north-alignment-project-north-vs-true-north-best-practices; shared coordinates: https://resources.imaginit.com/building/shared-coordinate-best-practice-part-1; LV95: https://llv.li/en/national-administration/civil-engineering-and-geoinformation-office/official-survey-av-/change-of-reference-frame-to-lv95
