# Local LLM in scan2revit: plan

State 24.10.2026, plan. The machine: the Revit laptop (i7-13700HX, 64 GB RAM, RTX 2000 Ada 8 GB), LM Studio with
Qwen3.6-35B-A3B Q4_K_M and its vision projector, OpenAI-compatible server on `http://localhost:1234/v1`; setup in the
user's note `lmstudio-lokales-llm-setup.md`, outside this repository (speed figures there are estimates, not
measured). The
same machine runs Revit and the point cloud pipeline.

## 1. Role

An optional helper at the few points where text or images must be interpreted. The geometry, the Revit runtime,
the checks and the comparisons stay deterministic code. The development work and the agent team stay with
Claude (long contexts, tool loops, Revit API knowledge).

| Use | Where | Model | Priority |
|---|---|---|---|
| Classify and parse text blocks the rules cannot place: room stamps, labels (T 90/210, BRH 90), level marks, sheet titles | facts readers (`drawings-and-scans.md` rows 2, 6, 14, 17) | Qwen3-VL-8B (in VRAM) | 1 |
| Parse build-up texts into layers and thicknesses | row 8, 9 (F23) | Qwen3.6-35B-A3B, reasoning on | 2 |
| Read room schedules and door / window lists from tables | row 18, 28 | 35B | 3 |
| Raster sheets: read stamps, scale and level marks from scans (F4) | rows 1, 6, 17 | 35B with vision | 4 |
| Visual first look at previews and Revit images of real projects (missing storey, open outline, mirrored plan) | input check, checker | 35B with vision | 5 |
| Classify IFC type names into wall / door classes (F6) | IFC route | 8B | 6 |
| Short texts: input report summary (A1), scoreboard summary (S1), draft rule proposals (R1) | reports | 8B | 7 |

Not for: feature development, code review, Revit scripting, geometry, numbers that feed a decision, gate
decisions. Reason: 16k-32k practical context, 20-30 tokens/s estimated, and the known weakness on multi-step
numbers (the setup document's own warning).

## 2. How it is built in

- One module `scan2revit/core/llm.py`: `ask(task, text_or_image, schema)` against the local server with a JSON
  schema (`response_format`), temperature 0.1; settings in `~/.scan2revit/llm.json` (endpoint, model per task,
  enabled); disabled by default.
- Every answer is validated by code (schema, units, plausibility: thickness 0.005-1.0 m, levels rising,
  number formats) before it becomes a fact; an invalid answer is dropped and logged.
- An LLM result is always a **proposed** fact with `method` `LLM-text` or `LLM-vision` and confidence at most 0.6;
  it is never accepted automatically (review page, `drawings-and-scans.md` section 4).
- Cache per project: `llm_cache/` keyed by the hash of task, prompt version and input; reruns cost nothing.
- Fallback: server down or disabled -> the rule result alone (as today), noted in the qa.
- Never inside the Revit runtime, never during a running Revit build or a scan step on the same machine
  (memory: model 21 GB plus context, Revit with a large model 3-4 GB, scan steps 10-18 GB on 64 GB).

## 3. Steps

1. Measure on this machine (setup document 6.2): tokens/s and time to first answer for the 8B and the 35B,
   text and image. Without these figures no throughput claim.
2. Pilot on the A60 / A61 sheets: every text block the rules leave unclassified, LLM answer vs a person's answer;
   measure precision per task. Decision D-7 (go / no go per task) on these figures.
3. Build `core/llm.py` with cache, validation and fallback; tests with a fake server.
4. Wire in task by task in the order of section 1, each with its measured precision in `scoring.md`.

## 4. Benefit and limits

Benefit: customer drawings and images stay on the machine; no cost per call; works offline; helps exactly where
rules are brittle (free text on plans). Limits: slower than the cloud, small context, weaker at numbers and
multi-step reasoning, shares memory and GPU with Revit; every answer needs a check by code and, for facts, by a
person.
