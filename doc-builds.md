# Builds

Every Revit model the pipeline built, with the setup it was built with (scan2revit version and git commit,
Revit, pyRevit, template). A model's file name says the same: `<project>_v<setup>_<info>.rvt`. When the setup
gets better, a project is built again and gets a new file next to the old one; the setup versions are
described on the Versions page. Real projects are anonymous: an alias and the storey instead of their names
and files; their check figures are not on the public site.

13 builds, 2 projects, 11 setups.

| Built | Project | Model file | Setup | Template | Revit / pyRevit | Inputs | Phases | Checks |
|---|---|---|---|---|---|---|---|---|
| 2026-11-25 21:47 | Projekt B | Projekt B, 3. OG | 0.8.0-b2d995a+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 17:24 | Projekt B | Projekt B, 3. OG | 0.8.0-98ee957+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 17:01 | Projekt B | Projekt B, 3. OG | 0.8.0-ebb732c+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 16:33 | Projekt B | Projekt B, 1. OG | 0.8.0-062f41f+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 15:03 | Projekt B | Projekt B | 0.8.0-92475bc+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 13:54 | Projekt B | Projekt B, Ebenen 3 bis 7 | 0.8.0-850672b+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 11:50 | Projekt B | Projekt B | 0.8.0-aec7a5d+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 11:45 | Projekt A | Projekt A | 0.8.0-5bd5c93 | blank_2027.rvt (566e86fe) | 2027 / - | Punktwolke (RCS) | structure, types, loadbearing, fitout, check | real project data (details private) |
| 2026-11-25 11:20 | Projekt B | Projekt B | 0.8.0-aec7a5d | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 10:46 | Projekt B | Projekt B | 0.8.0-c9bf541+dev | blank_2027.rvt (566e86fe) | 2027 / - | Bauplan (plan.json) | e2e | real project data (details private) |
| 2026-11-25 10:46 | Projekt A | Projekt A | 0.8.0-aec7a5d | blank_2027.rvt (566e86fe) | 2027 / - | Punktwolke (RCS) | structure, types, loadbearing, fitout, check | real project data (details private) |
| 2026-10-26 12:46 | Projekt A | Projekt A | 0.7.0-7fc6a03+dev | blank.rvt (5d8ab436) | 2025 / 7.0.0 | Punktwolke (RCS) | - | - |
| 2026-10-26 12:46 | Projekt A | Projekt A | 0.7.0-7fc6a03+dev | blank.rvt (5d8ab436) | 2025 / 7.0.0 | Punktwolke (RCS) | structure, types, loadbearing, fitout, check | real project data (details private) |

## Time per build

Working time of the agents per kind of work, the span from the first step's start to the last step's end,
and the coordination time: the span minus the working time (waiting, hand-overs, gates, decisions). A
build whose steps were not all recorded with their start has no span.

| Built | Model file | Analysis | Point cloud | Plans | Revit | Check | Working | Span | Coordination | By agent |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-25 11:50 | Projekt B | 4 s | - | - | 25 min 35 s | - | 25 min 39 s | 26 min 35 s | 56 s | all Revit agents (runner) 25 min 35 s, structure-man 4 s |
| 2026-11-25 11:45 | Projekt A | 3 s | 3 min 46 s | - | 7 min 13 s | 6 s | 11 min 08 s | 1 h 23 min | 1 h 15 min | point-cloud-man 3 min 46 s, structure-man 2 min 49 s, family-man 1 min 59 s, fit-man 1 min 16 s, loadbearing-man 1 min 12 s, checker 6 s |
| 2026-11-25 10:46 | Projekt A | - | - | - | 5 min 55 s | 8 s | 6 min 03 s | - | - | - 6 min 03 s |
