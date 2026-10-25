# Deviation analysis, review and correction, meshing, browser viewer

State 25.10.2026, plan; nothing of it is built yet. Started from the analysis of a Scan-to-BIM tool that combines
a model proposal with deviation analysis and correction in the browser (`decisions.md` D-22 to D-25). Features:
`open-tasks.md` F25 to F28; sloped elements stay F12.

## 1. Deviation analysis: the built model against the scan (F25)

Today the checker compares the model with the plan (Revit checks) and the plan with a reference plan (V2,
`core/compare.py`). Nothing yet says how far the built faces lie from the scanned surfaces. The deviation
analysis does that per element, in both directions (the literature calls it macro and micro: the whole model
against the cloud and back, and each element's face against the cloud).

### 1.1 Which points the model is verified against (the key decision)

A deviation is only meaningful if the points describe the element's surface, were not themselves used to place
the element, and are dense enough. The selection rules, in order:

| # | Rule | Why |
|---|---|---|
| P1 | **Held-out points.** Verify against points the element was not fitted on: the slice route fits on two 20 cm slices, so verify on the cloud outside these bands (e.g. 1.0-1.1 m and 1.8-2.0 m); the full route: split by scan position or by a height band held back | a face checked against its own fitting points always looks good |
| P2 | **Independent scans first.** Where they exist: another scan position, the external scan (drone, facade, F16), survey control points (total station) as the strongest check | an independent source tests registration and fitting together |
| P3 | **Points of the element's surface only.** Within a search band of the face (start ±0.10 m along the normal), inside the face's extent less 0.05 m at edges and openings, normals agreeing within 15 degrees ("oriented" deviation) | edges, reveals and neighbouring elements otherwise count as error |
| P4 | **Clutter out.** Points the classifier marks as furniture, people, ghost points (glass, mirrors), cables; points of rooms' contents below 2 m near walls with furniture | clutter in front of a wall is not a wall error |
| P5 | **Thinned evenly.** 2 cm voxels before statistics | dense areas near a scanner position must not dominate |
| P6 | **Enough evidence or no verdict.** At least 200 points and 30 % of the face area covered, else "not verifiable" (occluded), listed with the coverage (A4) | occlusion is its own result, not a pass and not a fail |
| P7 | **The visible face only.** A wall seen from one side is verified on that face; its other face only against an external scan; its assumed thickness is never "verified" | assumed values stay assumed |
| P8 | **Noise baseline.** Per storey the spread of points on a large plane (the input report's registration and floor layer) is the floor of what can be shown | a 5 mm deviation on a 9 mm noisy scan says nothing |

### 1.2 Items of the task

1. Point selection P1-P8 as a module (`core/deviation.py`): held-out bands, element search bands, normals,
   clutter mask from the classifier, voxel thinning, coverage threshold.
2. Element faces from the plan (walls: both faces from axis and thickness; arcs; floors: top and soffit;
   openings: jambs, head, sill) and, later, from the Revit read-back.
3. Per element: signed deviation median, mean, 95 %, max; share within the LOA class (LOA30 15 mm, LOA20 50 mm);
   points used; coverage; verdict (pass, fail, not verifiable).
4. Model to scan: points far from every modelled face (more than 0.15 m) clustered into candidates for missed
   elements (a wall, a column, a stair) or clutter, as a list and an image.
5. Signed bias per element class (all walls 8 mm behind the scan: plaster or a systematic offset) separated from
   scatter.
6. Images per storey: scan points coloured by deviation over the plan (blue behind, red in front, grey not
   verifiable), and one 3D view; JPEG.
7. Into the model: the parameter `scan2revit source` gets the verified LOA (`measured, LOA30 verified`); a
   failed element becomes a finding for its owner on the scoreboard.
8. Checker step: `phase check` runs it when a scan is in the project; check.md gets "Deviation from the scan";
   rule ids for the new checks (G-2.x).
9. Tests on the synthetic scans (known truth: deviations of a shifted wall must be found) and a measurement on a
   real storey (private figures).
10. Guideline: what a verified element is (section 2), the thresholds, rule proposal to the user.

## 2. Review and correction as one loop (F26)

The model is a proposal; a person reviews what the checks and the deviation analysis flag, and corrects it; the
corrections go back into the plan, and the stages run again. One loop per round:

1. **Flag**: elements failing a check or the deviation analysis, missed-element candidates, not verifiable
   elements, conflicts of drawing facts (F18), ordered by impact.
2. **Show**: the review page (local, the same server as F18): per item the plan view with the scan slice, the
   element and its deviation colours, and in the browser viewer (F27) the 3D context.
3. **Decide** per item: accept, move (drag the face or enter the offset), change thickness, delete, add (draw a
   missed wall on the scan), mark as clutter, mark as not verifiable.
4. **Apply**: decisions written as edits to `plan.json` (with `edited_by`, the old value kept), the affected
   stages rerun (walls, openings, rooms of that level), the check and the deviation analysis run again.
5. **Record**: every decision on the scoreboard (the person's actions), loops counted per element and per phase
   (the features page shows them).

Stop when no blocking item is open or the user closes the round. The edits never touch the input files; they are
part of the project.

## 3. Meshing: why and when (research, D-24)

A mesh is a surface of triangles made from the points (Poisson, greedy triangulation, marching cubes, as in the
open-source PCL library).

**When it helps**
- Irregular and organic geometry (vaults, ornaments, rock, damaged surfaces, heritage): a mesh is the step between
  points and an object; heritage (HBIM) workflows segment, mesh, refine, then convert.
- Size and handling: a mesh is 10 to 100 times smaller than its cloud (vendor figures), which makes browser
  viewing and sharing of large scans practical.
- Deviation display: comparing and showing a model on a mesh of the scan is lighter than on the raw cloud.
- Classification on surfaces: segmenting planar patches of a mesh into walls, floors, pipes.

**When it does not**
- Planar building elements (walls, slabs, openings) are found and measured directly in the points, as scan2revit
  does; a mesh adds smoothing and its own error (studies report mesh-to-reference distances of 2 to 14 mm for
  SLAM scans) without adding information.
- A mesh cannot go into BIM as it is: it must be converted into parametric objects anyway (or linked as an
  unintelligent object), which is what our routes do from the points.

**Who uses it**
- Pointfuse: point cloud to a segmented, classified mesh, published to Revit (reported to be in Autodesk ReCap
  Pro 2026 through Pointfuse technology; that report is not confirmed).
- Cintoo: every scan position as a compressed mesh in the cloud, BIM against scan with issues as BCF.
- Heritage and research workflows (HBIM), the ODA Scan-to-BIM SDK (PCL algorithms).
- Without a mesh, on the points: EdgeWise (Revit-native walls, pipes, ducts), Aurivus (neural segmentation,
  Revit plugin), PointCab Origins (sections and vectorisation to Revit), and the analysed tool for model
  generation with a mesh preparation step.

**For scan2revit** (recommendation D-24): no meshing in the modelling routes. Possibly later (a) for the browser
viewer, to show large scans light, and (b) for elements that are not planar (vaults, sloped and curved roofs,
F12) as a reference surface for the deviation analysis.

## 4. Browser viewer with That Open Company (ifc.js) (F27)

That Open Company (formerly IFC.js) publishes open-source libraries to read, show and edit IFC in the browser
(`@thatopen/components`, `web-ifc`). Use: a local viewer for the review loop (F26) and the fact review (F18):
the model as IFC (exported from Revit or from `plan.json`), the scan as thinned points or slices, deviation
colours, element selection that opens the review card. Before use: licence and security check
(`github-sources.md`; the libraries are published under the MIT licence according to their repositories, to be
confirmed and pinned), runs on localhost only, no customer data leaves the machine.

## 5. Agents (planned roles, added when the tools exist)

| Role | Job | Why a role of its own |
|---|---|---|
| Deviation work stays with the **checker** | runs the deviation analysis, files failed elements as findings for their owners | the checker is independent and read-only; deviations are checks |
| **Review man** (new, planned) | prepares the review round (F26): collects flagged items from the check, the deviation analysis and the fact review, serves the review page, applies the person's decisions to `plan.json`, sends the affected agents to rerun their phases, records the loop on the scoreboard | the loop has its own state (open items, decisions, reruns) and must not be done by the builders who made the elements or by the checker who must stay independent |

The review man's agent file is written with F26; until then the project manager runs the loop by hand.
