# Versions of the setup

A model is built with a **setup**: the scan2revit version (`scan2revit/pyproject.toml`), the git commit, the Revit
version, pyRevit, and the template project. The setup's id is `<version>-<commit>` (with `+dev` when changed
files were not committed), and it is part of every model's file name: `<project>_v<setup>_<info>.rvt`. When the
setup gets better, a project is built again and gets a new file next to the old one; the Builds page lists every
build with its setup.

Rules: the version goes up when what a build produces changes (a new element kind, a new route, a changed
modelling rule: minor, 0.x); fixes keep the version and are told apart by the commit. Every version gets a row
here when it is set, with what changed for the models.

| Version | Date | Commit | What changed for the models |
|---|---|---|---|
| 0.8.0 | 26.10.2026 | set with this page | Columns from scans (Revit stage `columns`, rules G-8.3, G-11.7 proposed); stairs from scans with turns and landings (L, U, winders); facts from drawings (`facts.json`) and the review page at gate 1 (the build waits for checked facts); local LLM helper (off by default); RCS point clouds read through Revit; model files named by project, setup and info, the build register. Since 0.7 also: the facade step for external scans (F16), phase Existing and measured / assumed per element (F15), door swings from the IFC (F10), room tags with area and the room fill (G-9.6), rooms closed by separation lines (F3), thin walls in dense scans, Revit dialogs answered, the agent team's scoreboard, rule ids with checks, reference comparison |
| 0.7.0 | 17.10.2026 | a0a1ced | One subpackage per sub-project (pointcloud, ifc, plans, core); open tasks on the status site |
| 0.6.0 | 17.10.2026 | ce9960c | Revit through the pyRevit agent runtime (pyRevit 7); the own MCP fork retired; the agent team on phases as pyRevit stages |
| 0.5.0 | 15.10.2026 | 7cbe41b | plan-extract (BBL) results to native Revit |
| 0.4.1 | 15.10.2026 | 682dc36 | Unattended Revit test |
| 0.4.0 | 15.10.2026 | 8cc8c01 | Stairs, slab openings, multi-storey plans |
| 0.3.0 | 15.10.2026 | b2a4f8f | Openings in curved walls, door swings, glass and mirror ghosts, 2D plans |
| 0.2.0 | 14.10.2026 | e4c12f7 | Doors, windows, reveals, overrides, align north, curved walls |
| 0.1.0 | 14.10.2026 | ce3e966 | Indoor point cloud to native Revit (walls, floors, levels, rooms) |
