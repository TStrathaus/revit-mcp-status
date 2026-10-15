"""Builds index.html from scoring.md (a copy of documentation/scoring.md in the Revit-MCP repository).

    python build.py        # then commit and push; GitHub Pages serves index.html

Standard library only. The page shows the scale, the current functionality with its maturity score and
the future functions sorted by value and effort.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
EFFORT_ORDER = {"S": 0, "S to L": 1, "M": 2, "L": 3}


def tables(md):
    """{section heading: [rows as lists of cells]} for every markdown table under a ## heading."""
    out, section, rows = {}, None, None
    for line in md.splitlines():
        if line.startswith("## "):
            section, rows = line[3:].strip(), None
        elif line.startswith("|") and section:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells):
                continue
            if rows is None:
                rows = out.setdefault(section, [])
            rows.append(cells)
        else:
            rows = None if not line.startswith("|") else rows
    return out


def inline(s):
    s = html.escape(s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


def score_cell(v):
    try:
        n = int(v)
    except ValueError:
        return f"<td>{inline(v)}</td>"
    dots = "".join(f'<span class="dot{" on" if k < n else ""}"></span>' for k in range(5))
    return f'<td class="score s{n}"><span class="num">{n}</span><span class="dots" aria-hidden="true">{dots}</span></td>'


def render_table(rows, score_cols=(), cls=""):
    head, body = rows[0], rows[1:]
    h = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = []
    for r in body:
        tds = "".join(score_cell(c) if i in score_cols else f"<td>{inline(c)}</td>" for i, c in enumerate(r))
        trs.append(f"<tr>{tds}</tr>")
    return f'<div class="wrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


def main():
    md = (HERE / "scoring.md").read_text(encoding="utf-8")
    t = tables(md)
    state = re.search(r"State (\d{1,2}\.\d{1,2}\.\d{4})", md)
    state = state.group(1) if state else ""
    cur = t["Current functionality"]
    fut = t["Future functions"]
    scores = [int(r[2]) for r in cur[1:] if r[2].isdigit()]
    dist = {k: scores.count(k) for k in range(6)}
    reading = md.split("## Reading", 1)[1].strip() if "## Reading" in md else ""
    hi = fut[0].index("Value")
    ei = fut[0].index("Effort")
    fut_sorted = [fut[0]] + sorted(fut[1:], key=lambda r: (-int(r[hi]), EFFORT_ORDER.get(r[ei], 9)))
    bars = "".join(
        f'<div class="bar"><span class="lbl">{k}</span><span class="fill s{k}" style="width:{max(dist[k], 0) * 100 / max(len(scores), 1):.1f}%"></span>'
        f'<span class="cnt">{dist[k]}</span></div>' for k in range(6))
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Revit-MCP status</title>
<meta name="description" content="Scoring of the current functionality and the missing features of Revit-MCP (scans, 2D plans and IFC to native Revit).">
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e1da; --card:#ffffff; --accent:#2f5d8a;
  --s0:#c9c7c0; --s1:#d9a05b; --s2:#d6c45a; --s3:#8fbf6a; --s4:#4f9d69; --s5:#2f7a4f; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#171716; --fg:#ecebe6; --muted:#a3a29b;
  --line:#33332f; --card:#1f1f1d; --accent:#8db4dc; --s0:#55544f; }} }}
:root[data-theme="dark"] {{ --bg:#171716; --fg:#ecebe6; --muted:#a3a29b; --line:#33332f; --card:#1f1f1d; --accent:#8db4dc; --s0:#55544f; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:32px 16px 64px; }}
h1 {{ font-size:28px; margin:0 0 4px; }} h2 {{ font-size:20px; margin:40px 0 12px; }}
.sub {{ color:var(--muted); margin:0 0 24px; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 16px; }}
.card b {{ font-size:26px; display:block; }}
.wrap {{ overflow-x:auto; background:var(--card); border:1px solid var(--line); border-radius:10px; }}
table {{ border-collapse:collapse; width:100%; min-width:640px; }}
th, td {{ text-align:left; vertical-align:top; padding:8px 10px; border-bottom:1px solid var(--line); }}
th {{ font-size:13px; color:var(--muted); font-weight:600; position:sticky; top:0; background:var(--card); }}
tbody tr:last-child td {{ border-bottom:0; }}
code {{ font:13px ui-monospace,Consolas,monospace; background:color-mix(in srgb,var(--line) 60%,transparent); padding:0 4px; border-radius:4px; }}
.score {{ white-space:nowrap; }} .num {{ font-weight:700; margin-right:6px; }}
.dot {{ display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:2px; background:var(--s0); opacity:.45; }}
.s1 .dot.on {{ background:var(--s1); opacity:1; }} .s2 .dot.on {{ background:var(--s2); opacity:1; }}
.s3 .dot.on {{ background:var(--s3); opacity:1; }} .s4 .dot.on {{ background:var(--s4); opacity:1; }} .s5 .dot.on {{ background:var(--s5); opacity:1; }}
.bar {{ display:flex; align-items:center; gap:8px; margin:4px 0; }}
.bar .lbl {{ width:16px; color:var(--muted); }} .bar .cnt {{ color:var(--muted); font-size:13px; }}
.bar .fill {{ height:12px; border-radius:6px; min-width:2px; }}
.fill.s0 {{ background:var(--s0); }} .fill.s1 {{ background:var(--s1); }} .fill.s2 {{ background:var(--s2); }}
.fill.s3 {{ background:var(--s3); }} .fill.s4 {{ background:var(--s4); }} .fill.s5 {{ background:var(--s5); }}
footer {{ color:var(--muted); font-size:13px; margin-top:40px; }}
</style>
</head>
<body>
<main>
<h1>Revit-MCP status</h1>
<p class="sub">Point clouds, 2D plans and IFC storeys to native Revit elements through the open Revit MCP. State {html.escape(state)}.</p>
<div class="cards">
  <div class="card"><b>{len(scores)}</b>functions scored</div>
  <div class="card"><b>{sum(1 for s in scores if s >= 4)}</b>pass in a real Revit (score 4 or 5)</div>
  <div class="card"><b>{dist[5]}</b>proven on real project data (score 5)</div>
  <div class="card"><b>{len(fut) - 1}</b>missing features planned</div>
</div>
<h2>Maturity</h2>
<div class="card">{bars}</div>
<h2>Scale</h2>
{render_table(t["Scale"])}
<h2>Current functionality</h2>
{render_table(cur, score_cols=(2,))}
<h2>Missing features</h2>
<p class="sub">Sorted by value, then effort. Value 1 to 5, effort S (hours), M (a day or two), L (more).</p>
{render_table(fut_sorted)}
<h2>Reading</h2>
<p>{inline(reading)}</p>
<footer>Generated from scoring.md by build.py.</footer>
</main>
</body>
</html>
"""
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html: {len(scores)} functions, {len(fut) - 1} future functions")


if __name__ == "__main__":
    main()
