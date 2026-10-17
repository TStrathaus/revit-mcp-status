---
name: modeling
description: Modelling guideline for as-built Revit models from scans, plans and IFC (scan2revit): what each element is in Revit, how it is typed, placed, named and checked, what is only reported. Use when building, checking or editing a model made with scan2revit, when choosing wall, floor, door or window types, or when a question is "how should this be modelled?".
---

# Modelling guideline: as-built Revit models (scan2revit)

These are the rules a model made with scan2revit follows, and the ones it should follow where the code does not
yet (marked **open**). The workflow (running the pipeline, mapping types, sending the calls) is in
`skills/scan-to-revit/SKILL.md`; this file says what the result must be. When a project has its own BIM
execution plan (BAP, SIA 2051) or the client's modelling rules, those come first; this guideline fills what
they leave open.

Basis: the BIMForum Level of Development specification (LOD 200: generic elements at the right size and
place), the USIBD Level of Accuracy (LOA: measured and represented accuracy kept apart), SIA 2051 / KBOB (the
level of detail is set per project in the BAP), the SBB rules for building models (an as-built model holds
existing elements only), the Autodesk Revit documentation (constraints, room bounding, location line, shared
coordinates). No published Swiss modelling guideline for as-built models from scans was found; sources at the end.

## 1. Walls and slabs are generic, no construction information inside

- Every wall and every floor (slab) has a generic type: **one layer, no material, no build-up**. The type
  carries the thickness and nothing else; its name says so: `scan2revit 300 mm`, `scan2revit floor 400 mm`.
- Why: a scanner sees surfaces, not what is behind them; a plan or a scan does not show the build-up. A
  layered type from a template (plaster, brick, insulation) states a construction nobody measured. BIMForum
  LOD 200 is exactly this: a generic assembly at the right size, shape and place. Single-layer components are
  also what modelling guides ask for when the build-up is not known (bimaterial, variant MGPa).
- The build-up is added later, by the project, when it is known: by swapping the generic type for a project
  type of the same thickness, never by editing the generic one.
- Doors and windows follow the same idea: generic families with free width and height; no fire rating, no
  hardware, no material.
- Current: the Revit module (`revit_runtime.py`, run by pyRevit) uses only `scan2revit` wall and floor types
  (one layer, no material) and makes the missing ones (floor types are copied from a floor type, never from a
  foundation slab type, which Revit also files as a floor type); the check "walls and floors generic" fails on
  any wall or floor with a build-up or a material. All nine examples passed it in Revit 2025 (scan2revit 0.5,
  through the old add-in; the pyRevit route passes it against the Revit API stand-in). Door and window sizes are
  set where the family takes them: Swiss families ("TU ...") through "Angabe Maueröffnungsmaß Breite / Höhe"
  (the masonry opening, what a scan measures), read back from "Breite" / "Höhe ab FBOK"; every door and window
  of the examples gets its size. The template's door families still carry fire ratings in some types
  (**open**: generic door and window families without them in `blank.rvt`).

## 2. Measured or assumed: say which

- Every dimension is either measured or assumed, and the model says which. Assumed are today: the thickness
  of a wall seen from one side (`thickness_assumed`), door head, window sill and head in the slice route and
  in 2D plans (`heights_assumed`), slab thickness without a vertical section through it.
- The accuracy is stated per element class as USIBD LOA: measured accuracy (of the scan) and represented
  accuracy (of the model) apart. Measured on real data so far: floor heights within 2 cm of the IFC, wall
  axes 6-9 cm (median) from the IFC on guest floors; synthetic faces within 1 mm.
- Current: the flags are in `plan.json` and `report.md`, not in Revit (**open**: a shared parameter
  `scan2revit source` = measured / assumed on walls, floors, doors and windows).

## 3. Existing elements only

- An as-built model holds the building as it is: no demolition, no new construction, no design intent.
- Recommended: every element in the phase "Existing" (Bestand). **Open**: the calls create elements in the
  view's phase; set "Phase Created" to the existing phase in the template or after loading.
- Not modelled, only reported in the QA: furniture, fittings, MEP, finishes, build-ups, anything the scan
  only shows in part (ghost points, mirrors).

## 4. Levels and storeys

- One level per floor top (finished floor as scanned), named by its storey (EG, 1OG, ... or as the project
  names them). A gallery (a partial floor with less than 2.2 m headroom) gets a level of its own, `Gallery n`.
- Every element sits on the level of its storey; nothing hangs on a level of another storey.
- Elevations: Level 0 at elevation 0 in the local frame; the survey offset carries the height above sea
  (`plan.origin.offset_xyz`). Several storeys from one survey frame (`merge`) keep their measured heights.
- Floor heights come from the vertical sections (`scan2revit.pointcloud.sections`) or from the scan's height histogram;
  storeys with steps are separate levels or reported (`steps_to` in slabs.json).

## 5. Walls

- Straight walls on their centreline (location line "Wall Centerline", the same as "Core Centerline" for a
  single-layer generic wall), from face to face as measured. Curved walls as arcs (circular only).
- Base: the storey level. Top: the underside of the slab above (unconnected height = storey floor to
  ceiling). Walls stop at the slabs; they do not run through them.
- Corners and junctions: centrelines joined at their crossings; overlapping walls are an error to remove.
- Room bounding: on (the default) for every wall.
- A wall seen from one side keeps its seen face; the thickness is assumed (0.30 m unless `--exterior-thickness`)
  until a door reveal measures it or `--thickness-overrides` sets it.
- Orientation: with `--align-north` the model is turned so the walls run along the project axes (project
  north); true north keeps the survey bearing (`plan.origin.rotation_deg`).

## 6. Floors (slabs) and voids

- One floor per slab region (from a horizontal slice at the level, `scan2revit.pointcloud.sections` / `slice2d --slabs`),
  top of the slab at the level, thickness downwards as measured in the vertical sections (else 0.25 m,
  assumed). Without slab regions the outline comes from the walls or the free space.
- Voids are openings cut into the floor (`NewOpening`): shafts and stairwells (5 m2 or more with no ceiling of
  the storey below under them), courtyards and atria (over 60 m2). Holes the floor is only hidden in
  (furniture) are not voids.
- The floor outline is simplified (one point per 10 cm raster corner today; **open**: straight, square edges,
  Revit warns about sketch lines slightly off axis).

## 7. Doors and windows

- Hosted in their wall, one generic type per size, named `scan2revit <w> x <h>` (a copy of the nearest type
  with width and height set; existing sizes within 50 mm are reused). Sizes under 200 mm are not openings.
- Width and position as measured; sill and head as measured in the full scan route, given (and flagged) in
  the slice route and in 2D plans.
- Door swing and hinge side as scanned (the open leaf) or drawn (the swing arc); a closed door has no leaf:
  its swing stays the family default and is reported.

## 8. Stairs, slab openings, ramps

- Stairs: one straight run per flight (StairsEditScope), riser count and tread from the scan or plan, width on
  the run, from the lower level to the upper. **Open**: landings, winders, spiral stairs; stairs in the voids
  found by the sections.
- Ramps and sloped roofs are reported, not built.

## 9. Rooms

- One room per enclosed area, placed at a point inside it; name and number from the plan or the IFC, else
  `Room <storey>.<n>`; net area to the wall faces. Cells under 1 m2 are slivers, not rooms.
- A room must be enclosed (Revit: "bounded"). A passage between two rooms (a gap with no wall and no door)
  gets a room separation line across it, 5 cm into the wall ends (plan-extract passages: done). Where walls
  are missing (real scans), rooms come from the free space and are placed but not enclosed (**open**: room
  separation lines along the free-space boundaries where no wall was found).

## 10. Coordinates and georeferencing

- The model stays near Revit's internal origin; the Survey Point carries the large coordinates (LV95 E, N and
  the height): `plan.origin.offset_xyz`. True north: the angle `-rotation_deg` when `--align-north` turned the
  model. Set them in Revit (or tell the user to); never move elements to "fix" coordinates.
- One coordinate source for all storeys and disciplines (the survey); acquire or publish shared coordinates
  once, link by shared coordinates, check with a control point.

## 11. Naming

| Element | Name |
|---|---|
| Level | storey name (EG, 1OG, UG2) or `Level n`; galleries `Gallery n` |
| Wall type | `scan2revit <t> mm` (generic, one layer) |
| Floor type | `scan2revit floor <t> mm` (generic, one layer) |
| Door / window type | `scan2revit <w> x <h>` (copy of the nearest family type, size set) |
| Room | name from the plan or IFC, else `Room <storey>.<n>`; number `<storey><nn>` |
| Element ids in plan.json | walls `W<storey>-<nn>`, curved walls `A..`, openings `O..`, stairs `S..`, slab openings `V..` |

## 12. Checks a model must pass (tools/revit_e2e.py)

Levels at the planned elevations; walls (straight and curved) per level and their thicknesses; walls and floors
generic; doors and windows hosted and within 50 mm of their size; window sills; floors per level and their
thicknesses; slab openings cut; stairs (risers, tread, levels); rooms bounded and their areas within 3 %; door
swings to the scanned side; Revit warnings and the failures answered without a transaction rolled back.

## 13. Working rules

- Never move or edit elements that were not created in this run.
- Do not create types, levels or coordinates silently in a real project: ask; in test copies the runner does it.
- Quote accuracy with its source: synthetic results (bench/results.md) are optimistic; real scans carry
  registration error, glass and clutter.

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
