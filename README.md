# Revit-MCP status

Public status page of Revit-MCP (point clouds, 2D plans and IFC storeys to native Revit elements):
scoring of the current functionality, the open functions and tasks per sub-project (Pointcloud2Revit,
IFC2Revit, Plans2Revit, shared core) and the modelling guideline.

Pages: https://tstrathaus.github.io/revit-mcp-status/ (index.html), open.html, modeling.html

Update: automatic. In the Revit-MCP repository a commit that changes `documentation/scoring.md`,
`documentation/open-tasks.md` or `scan2revit/skills/modeling/SKILL.md` runs `tools/publish_status.py`
(git hook `tools/hooks/post-commit`): it copies them here as `scoring.md`, `open-tasks.md` and
`modeling.md`, runs `python build.py`, commits and pushes. By hand: `py tools/publish_status.py` there.
