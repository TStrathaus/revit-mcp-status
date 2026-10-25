# Agent scoreboard

State 25.10.2026. What the agents of the modelling team did and found, over all projects (`scan2revit/tools/scoreboard.py summary`; per project `scoreboard.md` in its folder). The team, its phases and gates: `documentation/agent-team.md`; the rules a finding refers to: the modelling guideline (rule ids G-n.m).

- **Actions**: entries the agent recorded (every phase of `revit_project.py` records one by itself).
- **Findings**: what the agent filed (defect, warning, info), each with the agent who owns it and the rule; **defects found**: the findings of severity defect.
- **Fixed**: defects the agent owned and fixed (plus fixes it reported without a finding); **open**: its own defects and warnings still open.
- **Blocked verdicts**: handovers that ended blocked. **Mean check score**: checks passed of the checks of each entry, averaged (checker: the model checks; builders: their stages without error).
- Projects from real data count in the private copy only; the public tables hold the synthetic projects.

## Agents (synthetic projects)

| Agent | Projects | Actions | Findings | Defects found | Fixed | Open | Blocked verdicts | Mean check score |
|---|---|---|---|---|---|---|---|---|
| project-manager | 1 | 5 | 13 | 1 | 0 | 13 | 0 | – |
| point-cloud-man | 1 | 1 | 5 | 0 | 0 | 0 | 0 | – |
| ifc-man | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – |
| plans-man | 0 | 0 | 0 | 0 | 0 | 0 | 0 | – |
| structure-man | 1 | 4 | 7 | 1 | 1 | 2 | 0 | 100 % |
| family-man | 1 | 4 | 8 | 0 | 0 | 1 | 0 | 100 % |
| loadbearing-man | 1 | 4 | 7 | 0 | 1 | 1 | 0 | 100 % |
| fit-man | 1 | 6 | 9 | 0 | 0 | 1 | 0 | 100 % |
| checker | 1 | 4 | 11 | 3 | 0 | 0 | 0 | 100 % |

## Findings flow (synthetic projects)

Who found what and who acted on it. Every finding goes to the project manager, who forwards it to the agent who has to act; that agent fixes it and says how; the checker confirms the fix. The agents do not contact each other: the scoreboard, the handovers and check.md carry the findings, the project manager forwards them at the gates and in the fix round.

| Found by | Acted on by | Findings | Fixed | Confirmed by the checker |
|---|---|---|---|---|
| project-manager | project-manager | 12 | 4 | 0 |
| family-man | family-man | 5 | 1 | 0 |
| point-cloud-man | point-cloud-man | 4 | 1 | 0 |
| structure-man | project-manager | 4 | 0 | 0 |
| loadbearing-man | loadbearing-man | 4 | 1 | 0 |
| fit-man | fit-man | 4 | 1 | 0 |
| structure-man | structure-man | 3 | 2 | 0 |
| checker | structure-man | 3 | 2 | 0 |
| checker | project-manager | 3 | 1 | 0 |
| family-man | project-manager | 2 | 0 | 0 |
| loadbearing-man | project-manager | 2 | 0 | 0 |
| fit-man | family-man | 2 | 1 | 0 |
| fit-man | project-manager | 2 | 1 | 0 |
| checker | loadbearing-man | 2 | 1 | 0 |
| checker | fit-man | 2 | 1 | 0 |
| point-cloud-man | structure-man | 1 | 1 | 0 |
| project-manager | loadbearing-man | 1 | 0 | 0 |
| checker | family-man | 1 | 1 | 0 |
| loadbearing-man | fit-man | 1 | 1 | 0 |
| family-man | fit-man | 1 | 1 | 0 |
| fit-man | structure-man | 1 | 0 | 0 |

### synthetic-two-storey

| Id | Severity | Rule | Way | Status | Fixed by | How | Confirmed by | Finding |
|---|---|---|---|---|---|---|---|---|
| F1 | warning | G-4.1 | project-manager → project-manager (owner named by the finder) | fixed | project-manager | – | – | Storey names to confirm by the user at gate 1: EG/1OG or Level 0/Level 1 (blocks the structure phase) |
| F2 | warning | G-10.1 | project-manager → project-manager (owner named by the finder) | fixed | project-manager | – | – | Coordinates to confirm at gate 1: survey point = scan offset and true north from the 12 deg rotation, or keep the scan orientation (blocks the structure phase) |
| F3 | info | – | project-manager → project-manager (owner named by the finder) | open | – | – | – | No reference plan: the checker runs without the reference comparison; storey heights known only by construction (0.00 / 3.00 m local) |
| F4 | warning | G-4.4 | point-cloud-man → point-cloud-man (owner named by the finder) | fixed | point-cloud-man | – | – | Input report (scan2revit.core.inputs): histogram floors are 450.01 and 452.75; 452.75 is the S00 ceiling, not the S01 floor (453.005, sections right); density, registration and floor layer of 'floor 452.75' are measured on the ceiling |
| F5 | info | G-2.1 | point-cloud-man → point-cloud-man (owner named by the finder) | open | – | – | – | Assumed: 3 exterior walls per storey at 300 mm (seen from inside only, no facade scan) and the S00 floor slab 0.25 m; S01 slab 0.25 m measured in the sections |
| F6 | warning | G-5.6 | point-cloud-man → structure-man (owner named by the finder) | fixed | structure-man | – | – | Storey plans in the scan orientation (walls about 12 deg off the grid, rotation_deg 0): merge refuses --align-north plans, so turning to project north (gate 1, F2) must be decided for the merged plan |
| F7 | info | G-3.3 | point-cloud-man → point-cloud-man (owner named by the finder) | open | – | – | – | Wall faces behind furniture assumed, not checked for openings: 0.95 m of the entrance wall (W0-06) and 0.85 m of a long exterior wall per storey |
| F8 | info | – | point-cloud-man → point-cloud-man (owner named by the finder) | open | – | – | – | scan2revit.pointcloud.thin reads E57 only: the PLY was thinned with an inline 2 cm voxel script; slices --rest grid clouds gave a wrong S01 floor in the full route, height crops used instead |
| F9 | warning | G-2.1 | project-manager → project-manager (owner named by the finder) | fixed | project-manager | – | – | User to accept the assumed values before the structure phase: 3 exterior walls per storey at 300 mm, S00 floor slab 0.25 m (F5) |
| F10 | info | – | project-manager → project-manager (owner named by the finder) | fixed | project-manager | – | – | Rule proposals G-4.4 and G-6.1 (point-cloud-man) put to the user in rule-proposals.md; not in the guideline until approved |
| F11 | defect | G-13.2 | structure-man → project-manager (owner named by the finder) | open | – | – | – | revit_project.py phase does not save the model: doc.Save() inside run_modify is refused by Revit ('Operation is not permitted when there is any open transaction phase started by API client'), log.json saved false; model.rvt on disk is still the blank copy, the levels exist only in the open Revit pid 32780 (tool defect, save has to happen outside run_modify) |
| F12 | warning | G-4.1 | structure-man → structure-man (owner named by the finder) | fixed | structure-man | – | – | Levels EG / 1OG are the template's levels 'EG- OK FFB' (0.00) and 'OG 1- OK FFB' (3.00), reused at the same elevation by the levels stage; no level is named EG or 1OG in Revit; 16 other template levels (UG 1, OG 2-4, OK RFB, UK RD, Fundamentplatte) and their views stay in the model; plan views EG- OK FFB / OG 1- OK FFB exist |
| F13 | info | G-10.1 | structure-man → structure-man (owner named by the finder) | fixed | structure-man | – | – | Survey point to set (not set in Revit, shared coordinates still 0/0/0): E 2599998.000, N 1200000.000, height 450.000; true north 0 deg (scan orientation kept, rotation_deg 0) |
| F14 | info | – | structure-man → structure-man (owner named by the finder) | open | – | – | – | tools/api_check.py reports DB.SpecTypeId.String as missing: a nested class, found in Revit 2025 as SpecTypeId+String.Text; false alarm of the checker's dotted lookup |
| F15 | warning | G-1.3 | family-man → family-man (owner named by the finder) | fixed | family-man | – | – | Door 900 x 2100 (6 doors, EG and 1OG) reuses the template type 'ML - 885 x 2135 EI 30' (TU DF 1 - Rahmenstock flaechenbuendig): fire rating EI 30 and no scan2revit name; the doors will be 885 x 2135 instead of 900 x 2095 measured (-15 / +40 mm). The 50 mm reuse of G-7.1 overrides G-1.3; tool revit_runtime.TypeCache.opening reuses any type within OPENING_TOL_MM |
| F16 | warning | G-1.3 | family-man → family-man (owner named by the finder) | open | – | – | – | Nearest families copied are not generic: door 1000 x 2200 from 'TU DF 1 - Fluchttuere Endausgang' (escape door, exit hardware), window 1600 x 1290 from 'FE 2 tlg - 1 Nurglasecke-konfigurierbar' (all-glass corner window), 1000 x 1290 from 'FE Oeffnung - Rechteckig', 1200 x 1290 from 'FE 1 tlg - DrehKipp': three different window families for one kind of window. Template needs one generic door and one generic window family with free width / height and no fire rating (G-1.4 open) |
| F17 | info | – | family-man → project-manager (owner named by the finder) | open | – | – | – | stage_types returns no notes: the 'type made: ... (copy of ...)' notes of the type cache are not passed to log.json, and the log key 'wall 299 mm' names the 300 mm type (5 mm rounding); tool revit_runtime.stage_types |
| F18 | info | G-13.2 | family-man → project-manager (owner named by the finder) | open | – | – | – | phase types again saved false (F11): the types exist only in the open Revit pid 32780 |
| F19 | warning | G-5.1 | loadbearing-man → loadbearing-man (owner named by the finder) | fixed | loadbearing-man | – | – | Walls carry Location Line 'Finish Face: Interior' (WALL_KEY_REF_PARAM 3, the template default) although Wall.Create placed them on the centreline; G-5.1 asks for Wall Centerline. Geometry is right now, but a later type swap of another thickness (G-1.2) or an edit grows the wall from the interior face. Tool revit_runtime.stage_walls should set WALL_KEY_REF_PARAM to 0 after Wall.Create |
| F20 | warning | G-6.1 | loadbearing-man → project-manager (owner named by the finder) | open | – | – | – | No slab or roof over 1OG: the sections found a top ceiling ('roof or top ceiling', 456.755 m, 2.75 m above 1OG) but plan.json has no element for it; the 1OG walls end at 5.75 m under nothing. The guideline does not say how the top ceiling is modelled (rule proposal) |
| F21 | info | G-13.2 | loadbearing-man → project-manager (owner named by the finder) | open | – | – | – | phase loadbearing again saved false (F11): walls and floors exist only in the open Revit pid 32780 |
| F22 | info | G-2.1 | loadbearing-man → loadbearing-man (owner named by the finder) | open | – | – | – | Assumed in this phase: 6 exterior walls at 300 mm (W0-03/04/05, W1-03/04/05, seen from inside), EG slab 0.25 m; W0-06 / W1-06 298.5 / 299 mm from the door reveal placed with the 300 mm type (5 mm snap); flags stay in plan.json, the parameter scan2revit source comes with the stage existing (fit man) |
| F23 | info | – | loadbearing-man → loadbearing-man (owner named by the finder) | open | – | – | – | No columns, beams, stairs or slab openings in the input (plan has none, sections found no void) |
| F24 | warning | G-13.2 | project-manager → project-manager (owner named by the finder) | open | – | – | – | Question to the user: F11 the model is not saved (model.rvt on disk is the blank copy; levels, types, walls, floors only in Revit pid 32780). Save it by hand in that Revit (File > Save) now, or wait for the tool fix (save outside run_modify)? Blocks the report, not the fit-out |
| F25 | warning | G-7.1 | project-manager → project-manager (owner named by the finder) | open | – | – | – | Question to the user: approve the family man's two G-7.1 proposals (reuse within 50 mm only for scan2revit or generic types; copy only from plain families) before the fit-out? If not, 6 doors 900 x 2100 are placed with 'ML - 885 x 2135 EI 30' (F15) and the copies stay from escape / glass-corner families (F16); a generic door and window family in blank.rvt is the user's template decision |
| F26 | warning | G-4.1 | project-manager → project-manager (owner named by the finder) | open | – | – | – | Question to the user: approve the structure man's G-4.1 addition (rename the reused template levels to EG / 1OG, delete the 16 unused template levels and their views)? Until then the levels are 'EG- OK FFB' / 'OG 1- OK FFB' (F12) |
| F27 | info | G-5.1 | project-manager → project-manager (owner named by the finder) | open | – | – | – | Question to the user: approve the load-bearing man's G-5.1 addition (Location Line = Wall Centerline, read back by the check) and the new G-6.5 (flat top slab over the highest storey, 0.25 m assumed and flagged, or only reported; F20) |
| F28 | info | – | project-manager → loadbearing-man (owner named by the finder) | open | – | – | – | F20 and the G-6.5 reason quote the top ceiling at 456.755 m; sections/slabs.json has 455.755 m (local 56.755 + origin 399), 5.755 m local, 2.75 m above 1OG: correct the handover |
| F29 | warning | G-9.1 | fit-man → fit-man (owner named by the finder) | fixed | fit-man | – | – | All 6 rooms have the Revit default upper limit (level + 2.438 m, 8 ft): the clear height is 2.75 m (floor to slab underside); room volumes are 0.31 m too low. Tool revit_runtime.stage_rooms sets no LimitOffset (ROOM_UPPER_OFFSET); rule proposal G-9.1 |
| F30 | warning | G-7.1 | fit-man → family-man (owner named by the finder) | fixed | family-man | – | – | F15 in the model: the 6 doors measured 900 x 2095 are placed as 'ML - 885 x 2135 EI 30' (head 2.135 m in Revit, -15 / +40 mm, fire rating EI 30 nobody measured); the 2 entrance doors 1003 x 2196 as the escape-door copy 'scan2revit 1000 x 2200'. Waits for the user's answer to F25 |
| F31 | info | G-3.2 | fit-man → family-man (owner named by the finder) | open | – | – | – | The template has a single phase 'Phase 01', no Existing / Bestand: the stage existing used it as fallback (6 elements changed, 24 already in it); an as-built template should carry an existing phase |
| F32 | info | G-7.3 | fit-man → fit-man (owner named by the finder) | open | – | – | – | Hinge side: all 8 doors have the hinge at -HandOrientation, consistent over the 6 flipped and 2 unflipped doors, but the family convention of 'TU DF 1' is not checked visually; the checker should look at one plan view |
| F33 | info | G-13.2 | fit-man → fit-man (owner named by the finder) | open | – | – | – | phase fitout saved false again (F11): openings, rooms and the source parameter exist only in Revit pid 32780 |
| F34 | warning | G-13.2 | fit-man → project-manager (owner named by the finder) | fixed | fit-man | – | – | Gate 3 asked for the F19 fix round (phase loadbearing rerun) before the fit-out; it had not run (loadbearing last 10:02:18, F19 open) when the fit-out was placed at 10:08:55. A rerun of phase loadbearing deletes the 12 walls and with them the 16 hosted doors and windows (and unbounds the rooms): after it, rerun phase fitout |
| F35 | defect | G-5.1 | checker → loadbearing-man (owner named by the finder) | fixed | loadbearing-man | – | – | not checked by phase check (read back by the checker): all 12 walls have Location Line 'Finish Face: Interior' (WALL_KEY_REF_PARAM 3), not Wall Centerline; F19 still open, the gate 3 fix round (rerun phase loadbearing) was not run (log: loadbearing only 10:02:18); after the fix the fit-out must be rerun (F34) |
| F36 | defect | G-4.1 | checker → structure-man (owner named by the finder) | fixed | structure-man | – | – | not checked by phase check (G-4.1, G-11.1): levels in Revit are 'EG- OK FFB' and 'OG 1- OK FFB', not EG / 1OG as decided at gate 1; 16 unused template levels and 14 template plan views (Vorplanung, Entwurf, Behoerde, Ausfuehrung, Lageplan) stay; consequence: phase check exported no plan per level (no view named EG / 1OG), only plan_3d.jpeg (F12, F26) |
| F37 | defect | G-13.2 | checker → project-manager (owner named by the finder) | open | – | – | – | model.rvt on disk is still the blank copy (09:54): every phase saved false, the open model in Revit pid 32780 is modified and unsaved; the checked model exists only in memory (tool defect F11 / F24, save outside run_modify) |
| F38 | warning | G-1.3 | checker → family-man (owner named by the finder) | fixed | family-man | – | – | doors and windows not generic: 6 doors as template type 'ML - 885 x 2135 EI 30' (fire rating EI 30, 885 x 2135 vs 900 x 2095 measured, within the 50 mm of G-7.2 so the check passes), 2 entrance doors copied from the escape door family, windows from three different families (visible in plan_3d.jpeg); no check covers G-1.3 (F15, F16, F25) |
| F39 | warning | G-10.1 | checker → structure-man (owner named by the finder) | fixed | structure-man | – | – | shared coordinates still 0 / 0 / 0, angle 0: survey point E 2599998.000 N 1200000.000 H 450.000 not set in Revit and the user not yet told to set it (F13) |
| F40 | warning | – | checker → fit-man (owner named by the finder) | fixed | fit-man | – | – | all 6 rooms: upper limit own level + 2.438 m (Revit default), clear height 2.75 m; volumes 71.0 / 89.9 / 54.5 m3 per storey about 11 % low; no rule says the room height (F29, fit man's G-9.1 proposal) |
| F41 | warning | G-6.1 | checker → loadbearing-man (owner named by the finder) | open | – | – | – | plan_3d.jpeg: no slab over 1OG, the 1OG walls end open at 5.75 m although the sections found the top ceiling (455.755 m); waits for the user's answer on G-6.5 (F20, F27) |
| F42 | warning | G-11.5 | checker → fit-man (owner named by the finder) | open | – | – | – | room names 'Room 0.1' ... 'Room 1.3' and numbers 001 / 101 use the storey index, not the storey name EG / 1OG; G-11.5 does not say which (rule proposal) |
| F43 | warning | – | checker → project-manager (owner named by the finder) | fixed | project-manager | – | – | status.md 'Reference plan: none (no IFC ...)' is read by revit_project.py as a path: check.md says 'Reference plan not found' instead of no reference; the reference comparison is n/a for this project (no IFC), not a pass; write 'Reference plan: none' alone or fix _status_value |
| F44 | warning | G-13.2 | loadbearing-man → fit-man (owner named by the finder) | fixed | fit-man | – | – | After the loadbearing rerun (10:17:49) the model has 0 doors and 0 windows: the 16 hosted openings went with the old walls; rerun phase fitout now (F34), then phase check |
| F45 | info | G-6.1 | loadbearing-man → loadbearing-man (owner named by the finder) | open | – | – | – | F41/F20 stay open: no slab over 1OG (top ceiling 455.755 m in sections/slabs.json, 2.75 m above 1OG); waits for the user's answer on G-6.5 (F27); nothing to build until then |
| F46 | warning | G-4.1 | structure-man → project-manager (owner named by the finder) | open | – | – | – | 16 template levels (UG 1, OG 2-4, OK RFB, UK RD, Fundamentplatte) and their plan views (also the Vorplanung/Entwurf/Behoerde/Ausfuehrung plans of EG and 1OG) remain; deleting them waits on the user's answer to the G-4.1 addition (F26, rule proposal 3) |
| F47 | info | G-10.1 | structure-man → project-manager (owner named by the finder) | open | – | – | – | phase structure again saved false (F11): renamed levels and survey point exist only in Revit pid 32780 |
| F48 | warning | G-4.1 | structure-man → project-manager (owner named by the finder) | open | – | – | – | revit_e2e.check has no row for level names (G-4.1/G-11.1) or the survey point (G-10.1): section 14 says not checked, so a row needs the guideline changed first (rule proposal); until then the checker reads them back by query |
| F49 | warning | G-1.3 | family-man → fit-man (owner named by the finder) | fixed | fit-man | – | – | 0 doors and 0 windows in the model (F44): rerun phase fitout so the openings take the new types, then phase check |
| F50 | info | G-7.1 | family-man → family-man (owner named by the finder) | open | – | – | – | Door 900 x 2100 reuses the plain template type 'ML - 885 x 2135' within 50 mm (-15 / +35 mm, no scan2revit name, as G-7.1 allows); reuse only of scan2revit types waits for proposal 5 (F25) |
| F51 | info | G-1.3 | family-man → family-man (owner named by the finder) | open | – | – | – | Window 1600 x 1290 is a copy of the single-leaf 'FE 1 tlg - DrehKipp' (one family per kind); the template still has no generic door or window family (F16, G-1.4) |
| F52 | info | – | family-man → family-man (owner named by the finder) | open | – | – | – | The type cache's notes (type made / deleted) still do not reach log.json (F17); the read-back query shows them |
| F53 | info | G-9.1 | fit-man → fit-man (owner named by the finder) | open | – | – | – | Read-back: IronPython reads Room.UpperLimit as None although ROOM_UPPER_LEVEL holds the base level; read_model uses Room.UnboundedHeight (2.75 m read on all 6 rooms) |
| F54 | warning | G-11.5 | fit-man → structure-man (owner named by the finder) | open | – | – | – | F42 not the fit man's: the names 'Room <i>.<n>' and numbers '<i><nn>' come from pointcloud/plan.py (index si) and core/merge.py (replace 'Room 0.' by 'Room <k>.'); stage_rooms takes name and number from the plan (G-9.1). Fix in the merge, or keep the index, after the user decides on the G-11.5 proposal; then rerun phase fitout |
| F55 | warning | G-13.2 | fit-man → project-manager (owner named by the finder) | open | – | – | – | Phase fitout saved False again (F11/F33): the rooms at 2.75 m exist only in Revit pid 32780; phase check must run before Revit is closed |
| F56 | warning | G-13.2 | checker → project-manager (owner named by the finder) | open | – | – | – | Revit pid 32780 shows the modal dialog 'Projekt seit Laengerem nicht gespeichert' (save reminder): every pyRevit request is refused (revit_busy), the checker's read-back query of the door and window families was refused; the user has to answer it (Save also ends F37/F11); no agent closes it |
| F57 | warning | G-4.1 | checker → structure-man (owner named by the finder) | open | – | – | – | plan_EG.jpeg / plan_1OG.jpeg: the renamed template floor plans EG / 1OG are not cropped to the building (it fills about a tenth of the image, lower left), and the EG plan still shows the template's text note 'BIM mit Revit ...'; the plan image per level is useless for review until the view is cropped and the template annotation removed |
| F58 | defect | G-13.2 | project-manager → project-manager (owner named by the finder) | open | – | – | – | revit_project.py close: taskkill sent to Revit pid 32780, which stays open (save dialog); model.rvt on disk is still the blank copy of 09:54 although the check passed 39 of 39 in memory; the tool prints 'every phase saved the model' while log.json has saved False for every phase (cmd_close should read the saved flags and say so; the save itself is F11) |
| F59 | warning | – | project-manager → project-manager (owner named by the finder) | open | – | – | – | Question to the user: the tool behaviour of rule proposals 3 (level renaming, survey point), 4 (Location Line), 8 (room upper limit) and 13 (door and window types) is already committed in f11e2f1, with its check rows, before the rules were approved; keep it and approve the rules, or revert the parts that are rejected? |
| F60 | warning | – | project-manager → project-manager (owner named by the finder) | open | – | – | – | Question to the user: rule proposals 3 to 13 (rule-proposals.md) wait for an answer; none is in the guideline |

## Projects

| Project | Agents | Actions | Findings | Defects | Fixed | Open | Last check | Last verdict |
|---|---|---|---|---|---|---|---|---|
| synthetic-two-storey | 7 | 28 | 60 | 5 | 2 | 18 | 39/39 | ready with open points |
