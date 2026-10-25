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

## Projects

| Project | Agents | Actions | Findings | Defects | Fixed | Open | Last check | Last verdict |
|---|---|---|---|---|---|---|---|---|
| synthetic-two-storey | 7 | 28 | 60 | 5 | 2 | 18 | 39/39 | ready with open points |
