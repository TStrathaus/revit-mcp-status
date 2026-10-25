# Skills and features from GitHub projects: use, and what contributing would take

State 24.10.2026. **Decision of the user (24.10.2026): use only.** We use GitHub projects as dependencies or as
references; we open no pull requests; our repository stays private as it is. Section 3 keeps the analysis of
contributing for a later decision.

## 1. Sources in use or evaluated

| Project | Licence | How we use it |
|---|---|---|
| pyRevit (pyrevitlabs/pyRevit) | GPL-3.0 | the only way to Revit: `pyrevit mcp`, agent runtime (pyRevit 7) |
| ifcopenshell | LGPL-3.0 | reads IFC in `scan2revit/ifc/` |
| plan-extract (bbl-dres/plan-extract) | MIT | raster plans: its results into Revit (`plans/fpx.py`); the model weights are not published |
| shapely, numpy, scipy, scikit-image, ezdxf, pdfplumber, pypdfium2, pye57, laspy | BSD / MIT / Apache | geometry, readers |
| Skill collections (DDC skills, Bonsai skill package, revit toolkits) | mixed, some without licence | read as references only (research log) |
| Cloud2BIM, manicotti, 3d-data-materials | mixed | methods compared, no code taken |

## 2. Rules for taking a skill or a feature from GitHub

1. **Licence first**: MIT, BSD, Apache: code may be taken with the notice. LGPL: use as a library, do not copy
   code into ours. GPL / AGPL: run as a separate program or library only (pyRevit, PyMuPDF); no code copied into
   scan2revit. No licence: read only, take nothing.
2. **Security check before use**: every skill or script is read in full before it is installed or run: does a
   Markdown file or a hook make Claude execute code, download, install packages or call external services
   (as done for the geopogo skill folder). Skills go into `.claude/skills/` only after that check.
3. **Pinned**: a dependency at a fixed version, a copied file at a commit hash, recorded with its licence in
   `scan2revit/third_party/README.md` (to create when the first file is copied).
4. **Adapted, not trusted**: a taken method gets our tests and the measured result in `scoring.md` before it
   replaces our own; no data from GitHub examples in our tests unless its licence allows it.
5. **No customer data out**: issues, questions or forks never contain project data, names or paths.

## 3. Contributing to the GitHub projects: what it would take (not decided)

**Candidates** (things we fixed or built that would help others):
- pyRevit agent runtime: results too large for the response came back without result and without a path
  (we read them through `get_run`); IronPython `json` failing on umlauts; a relative `workspace` refused with an
  unclear message; Revit chosen by process id when several sessions run.
- plan-extract: an importer of its JSON into native Revit through pyRevit (our `fpx.py`).
- ifcopenshell: none so far.

**What would be necessary**

| Need | Detail |
|---|---|
| Rights | clear whether the work belongs to the user privately or to the employer (the Revit user name is a company account); written permission if the employer holds the rights |
| GitHub account and forks | the user's account; a fork per project; their contribution rules (pyRevit: CONTRIBUTING, code style, Python 2.7 compatibility in the IronPython parts) |
| Issue first | describe the problem with a minimal, synthetic reproduction; agree on the solution with the maintainers |
| Generic code | the contribution cut out of scan2revit: no project paths, no Swiss-template specifics unless optional |
| Tests and docs in their style | their test setup, not ours |
| Licence fit | our code is MIT; contributing to GPL projects puts that part under GPL there (fine, but final) |
| Time | review rounds of days to months; follow-up questions; keeping the PR current with their main branch |

**Benefit**
- Fixes live upstream: fewer local workarounds (the `get_run` reading, the ASCII rules) to maintain.
- Maintainers review the code; others report and fix bugs in it.
- Visibility for the work; feedback from people who use Revit automation daily.
- Influence on the direction of the tools we depend on (pyRevit's agent runtime is new and still changing).

**Downside**
- Time for review cycles, which do not fit project deadlines.
- Disclosure: methods become public (fine for generic fixes, a question for the scan-to-BIM methods).
- Rights questions with the employer must be settled first.
- Commitment: issues and questions about the contributed code come back.
- A rejected or long-pending PR still has to be kept locally.

**A lighter form** (also not decided): bug reports as issues with a synthetic reproduction, no code. Low cost,
most of the benefit for the pyRevit runtime findings.
