# Major decisions for development

State 24.10.2026. Decided ones with date; open ones with the options and a recommendation. Details in the
linked documents.

## Decided

| # | Decision | Date | Where |
|---|---|---|---|
| D-1 | Revit only through the pyRevit agent runtime; no own add-in or MCP server | earlier (0.6) | `CLAUDE.md`, research log |
| D-2 | Walls and slabs generic (one layer, no material); only reported what a scan cannot see | earlier | `SKILL.md` |
| D-3 | Public status site: synthetic data only; real figures in private markers | earlier | `tools/publish_status.py` |
| D-8 | 2D drawings first, as the prior; the scan wins on geometry, drawings on what a scan cannot see; conflicts to a person | 24.10.2026 | `drawings-and-scans.md` |
| D-9 | Extracted information as facts in `facts.json` per project (source, method, confidence, status) | 24.10.2026 | `drawings-and-scans.md` 3 |
| D-10 | Facts verified by a person on a local review page at gate 1 | 24.10.2026 | `drawings-and-scans.md` 4 |
| D-11 | GitHub projects: use only, no pull requests; our repository stays private | 24.10.2026 | `github-sources.md` |
| D-12 | Test data: the user's real files, no generated test data | earlier | project memory |
| D-13 | Agent team with scoreboard (per project, summary, site), rule ids with checks, rule proposals approved by the user | 24.10.2026 | `agent-team.md` (after the merge) |

## Open

| # | Question | Options | Recommendation |
|---|---|---|---|
| D-4 | A third value "drawn" in `scan2revit source` | (a) measured / drawn / assumed; (b) drawn counts as assumed | (a): a verified drawing is better than a default, but not a measurement |
| D-5 (decided 25.10.2026, rule G-0.2: one element by default, split only where the data gives the build-up) | Floor and wall build-ups from drawings in Revit | (a) keep generic one-layer types, build-up as type data (text parameter); (b) layered types from accepted build-ups; (c) both, layered only on request | (a) now: D-2 holds, nothing claimed that nobody measured; (b) later per project |
| D-6 | Conflict tolerances drawn vs measured | the start values in `drawings-and-scans.md` 3, or per LOA class | start values, tuned on the first real project with drawings and scan |
| D-7 | Local LLM: go / no go per task | after the measurement and pilot (`local-llm.md` 3) | decide per task on measured precision |
| D-14 | Alignment of drawings to the scan | (a) automatic 2D fit of wall axes, person confirms; (b) person picks 3 points | (a) with (b) as fallback |
| D-15 | Review page technique | (a) local Python server (writes `facts.json` directly); (b) static page exporting a decisions file | (a): one step, nothing leaves the machine |
| D-16 | May a drawing replace a measurement where the scan's coverage is poor (A4) | (a) never, only fill gaps; (b) below a coverage threshold, flagged | (a) |
| D-17 | Bug reports to pyRevit for the runtime findings (no code) | yes / no | yes, low cost; needs the user's go (D-11 covers pull requests) |
| D-18 | Knee walls under a sloping roof on plan sheets (drawn as a band about 1.1 m deep) | (a) as now: a 1.0 m wall as thick as the band, centred on it, thickness and height flagged assumed; (b) a wall of assumed thickness (0.25 m) at the band's inner face; (c) not modelled, only reported | (b): the band is the roof zone, not the wall |
| D-19 | IFC pre-check leaves out wall pieces that lie inside other pieces within their height range (duplicates, linings) | (a) leave them out and list them (as now); (b) only report | (a): they add nothing to the model and caused refused walls; the list stays in qa |
| D-20 | Door and window type names (rule G-11.4) | (a) the runtime keeps reusing a loaded type within 50 mm under its own name, the rule says so; (b) always a type named `scan2revit <w> x <h>` | (a) with the size in a parameter: template families stay recognisable |
| D-21 | Limits of the input reports (density warn under 200 / fail under 50 points per m2, floor spread warn over 5 cm, coverage warn under 0.8 / fail under 0.5, IFC shares warn under 0.9) | confirm, or other values | confirm as start values, revisit after the next real scan |
| D-22 | Points the deviation analysis verifies against | rules P1-P8 in `deviation-and-review.md` 1.1 (held-out points, independent scans first, element surface with normals, clutter out, thinning, minimum evidence, visible face, noise baseline), or fewer | all eight; thresholds tuned on the synthetic scans, then one real storey |
| D-23 | Review loop: who applies a person's corrections | (a) a review man agent (planned); (b) the project manager | (a): the loop has its own state; builders and checker stay out of it |
| D-24 | Meshing | (a) none in the modelling routes, maybe for the viewer and non-planar references; (b) a mesh step before modelling | (a) |
| D-25 | Browser viewer technique | (a) That Open Company libraries (IFC) plus a point layer; (b) Potree for points only; (c) no viewer, images only | (a), after the licence check |
