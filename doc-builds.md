# Builds

Every Revit model the pipeline built, with the setup it was built with (scan2revit version and git commit,
Revit, pyRevit, template). A model's file name says the same: `<project>_v<setup>_<info>.rvt`. When the setup
gets better, a project is built again and gets a new file next to the old one; the setup versions are
described on the Versions page. Real projects are private: their names and figures are not on the public site.

2 builds, 1 projects, 1 setups.

| Built | Project | Model file | Setup | Template | Revit / pyRevit | Inputs | Phases | Checks |
|---|---|---|---|---|---|---|---|---|
| 2026-10-26 12:46 | real project data (details private) | real project data (details private) | 0.7.0-7fc6a03+dev | blank.rvt (5d8ab436) | 2025 / 7.0.0 | RCS linked | - | - |
| 2026-10-26 12:46 | real project data (details private) | real project data (details private) | 0.7.0-7fc6a03+dev | blank.rvt (5d8ab436) | 2025 / 7.0.0 | RCS read through Revit (house, 2 cm), slice route, 4 storeys | structure, types, loadbearing, fitout, check | real project data (details private) |
