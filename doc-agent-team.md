# Agent team: a Revit model from scans, IFC or plans

Nine specialised agents (Claude Code subagents, `.claude/agents/`) build one as-built Revit model together,
led by a project manager and run by the workflow `.claude/workflows/build-model.js` (or by hand from the main
session). Approved by the user on 17.10.2026: agent definitions plus a workflow, a separate checker, stairs with
the load-bearing man.

## The team

| Agent | File | Job | Delivers | In Revit |
|---|---|---|---|---|
| Project manager | `project-manager.md` | plans the project, keeps the status board, decides at every gate, asks the user, writes the final report | `status.md`, gate decisions, `report.md` | no |
| Point cloud man | `point-cloud-man.md` | checks scans (format, coordinates, registration, density, coverage), thins, cuts vertical sections and slices, builds the storey plans | input report, `slabs.json`, storey plans | no |
| IFC man | `ifc-man.md` | checks the IFC (schema, units, georeferencing, storeys, counts, quantities), converts storey by storey | input report, storey plans | no |
| Plans man | `plans-man.md` | checks plans (DXF, PDF, raster; scale, units, layers, storeys), picks the route (own reader or plan-extract) | input report, storey plans | no |
| Structure man | `structure-man.md` | merges the storeys into one plan, checks the heights, makes the levels and a floor plan per level, states survey point and true north | `plan.json`, levels in Revit | yes |
| Family man | `family-man.md` | builds and keeps the types: generic walls and floors (one layer, no material), door and window sizes; reports template problems | the types in the model (stage `types`) | yes |
| Load-bearing man | `loadbearing-man.md` | walls (straight and curved), floors, slab openings, stairs; later columns and beams | the structure in Revit | yes |
| Fit man | `fit-man.md` | doors and windows with their swing, room separation lines, rooms; later curtain walls, railings | the fit-out in Revit | yes |
| Checker | `checker.md` | checks the model independently: Revit checks, the modelling guideline, the reference (IFC) | `check.md`, defects per agent | read only |

## Phases and gates

1. **Intake** (project manager): what is to be built, from which data, which reference; names the project
   folder; writes `status.md`.
2. **Input check** (point cloud man, IFC man, plans man; in parallel, only those with data): an input report
   each and the storey plans. **Gate 1** (project manager, the user decides): data quality, coordinates,
   storey names and heights.
3. **Structure** (structure man): `plan.json` of all storeys, levels and plan views in Revit. **Gate 2**:
   levels at the planned heights, against the reference where there is one.
4. **Families** (family man): every type the plan needs, before anything is placed.
5. **Load-bearing** (load-bearing man). **Gate 3**: walls and floors generic, thicknesses, slab openings.
6. **Fit-out** (fit man).
7. **Check** (checker), **report** (project manager). Defects go back to the agent responsible; one round of
   fixes, then the project manager reports what is still open.

At every gate and in the report the project manager reads the project's `scoreboard.md` (below): what each agent
did, the open findings by owner, the check score and what changed since the previous check.

Only one agent works in Revit at a time (one Revit, one model). The input men work in parallel.

Revit is reached through the pyRevit agent runtime (pyRevit 7, `pyrevit mcp`; setup in
`scan2revit/docs/AUTOTEST.md`). A phase is one or more stages of the Revit module
(`scan2revit_build.run(doc, {"stages": [...]})`), each one `run_modify`:

| Phase | Agent | Stages |
|---|---|---|
| structure | structure man | levels |
| types | family man | types (every wall, floor, door and window type the plan needs) |
| loadbearing | load-bearing man | walls, floors, slab openings, stairs |
| fitout | fit man | openings (doors, windows, swings), room separations, rooms, existing (phase, measured / assumed) |
| check | checker | the model read back (`run_query`) and checked, a plan per level and a 3D view |

Every stage deletes its own elements of an earlier run first, so an agent can rerun its phase after a fix.

### Planned: review man (F26, not built yet)

A review man runs the review and correction loop: flagged items from the check, the deviation analysis (run by the
checker, F25) and the fact review, the review page, the person's decisions applied to `plan.json`, the affected
phases rerun, every loop on the scoreboard (`deviation-and-review.md` 5). Until it exists the project manager
runs the loop by hand.

### Planned: drawings first (F17 to F21, not built yet)

Decided on 24.10.2026 (`decisions.md` D-8 to D-10, plan in `drawings-and-scans.md`): when drawings and a scan
of the same building exist, the plans man reads every sheet first into `facts.json` (phase 2a), the drawings are
aligned to the scan frame (2c), a person decides the facts on a review page at gate 1, the builders use the
accepted facts as priors (levels, one-sided wall thickness, slab thickness, opening heights, room names) and the
checker compares drawn with measured. Until these tools exist the phases above stay as they are.

## The project folder

Inputs lie by route in `scan2revit/data/pointcloud|ifc|plans/<name>/` (git-ignored); the team works in `scan2revit/data/projects/<project>/project/`:

| File | Who writes it |
|---|---|
| `status.md` | project manager: plan, phase, gate decisions, open questions; the line `synthetic: yes` for a project from synthetic data only (its scoreboard may be published) |
| `inputs/<agent>.md` | input men: the input report |
| `storeys/<name>/plan.json` | input men: one build plan per storey |
| `plan.json` | structure man: the merged plan of all storeys |
| `model.rvt`, `revit.json`, `log.json`, `workspace/` | `tools/revit_project.py` (a copy of the template `revit_test\blank.rvt`; the runtime's workspace; every stage logged) |
| `check.md`, `check.json`, `check/` | checker (through `revit_project.py phase check`; `check.md` says what changed since the previous check) |
| `scoreboard.json`, `scoreboard.md` | every agent through `tools/scoreboard.py`; every phase of `revit_project.py` adds its own entry |
| `handovers/<agent>.md` | every agent: done, open, files, rule proposals |
| `rule-proposals.md` | project manager: the rule proposals of all handovers and the user's answer to each |
| `report.md` | project manager: the final report |

## Scoreboard

`scan2revit/tools/scoreboard.py` keeps what every agent did and found, per project (`scoreboard.json`, schema
`scan2revit.scoreboard/1`, and `scoreboard.md`):

- `add --project <folder> --agent <name> --phase <phase> --action "<text>" [--finding "<severity>|<owner>|<rule id or ->|<text>" ...]
  [--verdict ready|ready with open points|blocked] [--checks <passed>/<total>] [--minutes N] [--fixed N]`: one entry.
  Severity: defect (the model or a plan is wrong), warning (doubtful, to be looked at), info. Owner: the agent who
  has to act (names as the files in `.claude/agents/`). Rule: the id in the modelling guideline (G-5.1, ...). The
  findings are numbered per project (F1, F2, ...).
- `route --project <folder> --finding F3 --to <agent> --via "gate 3"`: the project manager forwards a finding.
- `fix --project <folder> --finding F3 --how "<what was changed>"`: the agent it was forwarded to marks it fixed.
- `verify --project <folder> --finding F3 --how "<check that passes>"` (or `--failed`): the checker confirms the
  fix, or reopens the finding and sends it back to the project manager.
- `summary --projects scan2revit/data/projects --out documentation/agent-scoreboard.md`: one row per agent over all
  projects and one per project. Published on the status site with the guideline: only projects whose `status.md`
  says `synthetic: yes` are public; the others stay inside `real project data (details private)`.
- Every phase of `revit_project.py` records an entry by itself (structure man, family man, load-bearing man, fit
  man, checker: what was made, checks passed of total, the Revit notes counted); the agents add what the tool
  cannot know: their findings, verdict, minutes.

Owners of failed checks, by the rule's section: 1 and 11 family man; 4 and 10 structure man; 5, 6 and 8
load-bearing man; 2, 3, 7 and 9 fit man (the stage `existing` is the fit man's); wrong input data the input man;
G-13.2 (stage errors) the agent of the stage. `check.md` names the owner of every failed check.

## Findings: who finds what, to whom it goes, how it is fixed

The agents do not contact each other: they run one after the other, and what they find travels on the
scoreboard, in their handovers and in check.md. Every finding takes the same way:

1. **Found**: the agent who sees it files it (`add`, with severity, rule id and the owner it proposes). It goes
   to the project manager.
2. **Forwarded**: at the next gate, or in the fix round after the check, the project manager decides who has to
   act (the proposed owner, another agent, or the user) and forwards it (`route`). Decisions for the user go into
   the gate's questions.
3. **Fixed**: the agent it was forwarded to fixes it within its job (a Revit fix only by rerunning its phase) and
   says how (`fix --how`). Nobody changes tool code or another agent's work during a build: that is a finding
   for the project manager, and code changes go through development with review.
4. **Confirmed**: the checker reruns the check that found it and confirms the fix (`verify`), or reopens it, and
   it goes back to the project manager.

`scoreboard.md` shows the whole way of every finding ("Findings flow": found by, forwarded to, status, fixed by,
how, confirmed by); `documentation/agent-scoreboard.md` (site page agents.html) sums it up per finder and owner
and lists every finding of the synthetic projects. Findings filed before 25.10.2026 have no recorded way: they
went from the checker to the owner it named, in the workflow's fix round.

## Rule proposals

The modelling guideline changes only with the user's approval. An agent that finds a rule wrong, missing or
unclear writes a proposal into its handover under the heading **Rule proposals**: the rule id (or "new, section n"),
the proposed text, the reason with the project evidence. The project manager collects them into
`rule-proposals.md` (one entry each: agent, rule, proposal, reason, the user's answer), asks the user at the next
gate or in the report, and only an approved proposal goes into `scan2revit/skills/modeling/SKILL.md` (with its
row in section 14, and the copy on the status site in step).

## Tools

- `scan2revit/tools/revit_project.py open | phase structure|types|loadbearing|fitout|check | status | close`:
  one model, built phase by phase through `pyrevit mcp`, saved after each phase; `--auto-approve` sets the
  agent policy to "auto" for the call (else Revit asks Keep / Discard per stage).
- Comparison with a reference (checker): `scan2revit.core.compare <plan.json> <reference plan.json>
  [--level-map A=B,...] --out <folder>` compares two plans per level in the survey frame (levels, walls,
  openings, floors, rooms; a verdict per USIBD LOA class, LOA30 by default). `phase check` adds it to `check.md`
  when `status.md` has a line `Reference plan: <path>` (and `Reference levels: 1OG=02,...`) or with `--reference`.
- The phase tool addresses the project's Revit by the process id in `revit.json` (another Revit may be open).
- Revit's own dialogs (the save reminder, "save the changes?") block every pyRevit request. `scan2revit/tools/revit_dialogs.py`
  lists and answers them by UI Automation; the phase tool saves the model after every phase through Revit's Save
  button (a pyRevit run may not save) and `close` answers "save the changes?" with Yes. The save reminder is off in
  this machine's Revit.ini (`[Backups] SaveReminderMinutes=0`, 25.10.2026).
- Before the first Revit work of a session: `py tools/api_check.py` with Revit open (every Revit API name of
  the runtime looked up in the running Revit).
- `scan2revit/tools/scoreboard.py add | fix | summary`: the scoreboard (above).
- `tools/revit_e2e.py` (the examples) and `revit_project.py phase check` (the project) say what changed since the
  previous run: checks gained, lost, still failing (`--compare <older report.json>` for another run).
- The pipeline modules by sub-project (`scan2revit.pointcloud.cli`, `.slices`, `.slice2d`, `.sections`;
  `scan2revit.ifc.storey`; `scan2revit.plans.plan2d`, `.fpx`; `scan2revit.core.merge` for all storeys)
  write a folder with `plan.json` and the Revit module; `tools/revit_e2e.py` runs the examples.

## Rules for every agent

- Follow the modelling guideline `scan2revit/skills/modeling/SKILL.md` (walls and slabs generic, levels,
  naming, coordinates, measured or assumed) and the workflow skill `scan2revit/skills/scan-to-revit/SKILL.md`.
- Never put customer scans, plans or Revit projects into git; work in the project folder only.
- Revit only in the project's copy of the blank project, never in a real project; never change elements
  another agent created; never loosen a check or a tolerance.
- Say what is measured and what is assumed; quote accuracy with its source.
- Record what you did and found with `scan2revit/tools/scoreboard.py add` (one entry per piece of work, every
  finding with its owner and rule id); mark a finding you fixed with `scoreboard.py fix`.
- End with a handover note `handovers/<agent>.md`: what was done, what is open, which files, rule proposals (if
  any), and a one-line verdict (ready / ready with open points / blocked).
- Paths contain a space ("2026 KI"): quote them.
