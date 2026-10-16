"""Builds index.html from scoring.md (a copy of documentation/scoring.md in the Revit-MCP repository) and
modeling.html from modeling.md (a copy of scan2revit/skills/modeling/SKILL.md, the modelling guideline).

    python build.py        # then commit and push; GitHub Pages serves both

Standard library only. The page shows the scale, the current functionality with its maturity score and
the future functions sorted by value and effort.
"""
import html
import json
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
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return re.sub(r'(?<![="])(https?://[^\s,;<)]+)', r'<a href="\1">\1</a>', s)


def md_body(md):
    """A small Markdown subset: ## and ### headings, paragraphs, - lists (indented lines continue an item), tables."""
    out, para, items, table = [], [], [], []

    def flush():
        nonlocal para, items, table
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
        if table:
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table]
            rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            out.append(render_table(rows))
        para, items, table = [], [], []

    for line in md.splitlines():
        if line.startswith("|"):
            if para or items:
                flush()
            table.append(line)
        elif line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            out.append(f"<h{min(level, 3)}>{inline(line.lstrip('#').strip())}</h{min(level, 3)}>")
        elif line.startswith("- "):
            if para or table:
                flush()
            items.append(line[2:].strip())
        elif line.startswith("  ") and items:
            items[-1] += " " + line.strip()
        elif not line.strip():
            flush()
        else:
            if items or table:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


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
    gal = json.loads((HERE / "gallery.json").read_text(encoding="utf-8")) if (HERE / "gallery.json").exists() else []
    figs = "".join(f'<figure class="card shot"><a href="{html.escape(g["file"])}"><img src="{html.escape(g["file"])}" '
                   f'alt="{html.escape(g["title"])}" loading="lazy"></a><figcaption><b class="t">{html.escape(g["title"])}</b>'
                   f'{inline(g["text"])}</figcaption></figure>' for g in gal)
    hi = fut[0].index("Value")
    ei = fut[0].index("Effort")
    fut_sorted = [fut[0]] + sorted(fut[1:], key=lambda r: (-int(r[hi]), EFFORT_ORDER.get(r[ei], 9)))
    meaning = {int(r[0]): r[1] for r in t["Scale"][1:]}
    topics = []                                          # in the order they appear
    for r in cur[1:]:
        if r[0] not in topics:
            topics.append(r[0])

    def stack(rows):
        sc = [int(r[2]) for r in rows if r[2].isdigit()]
        segs = "".join(f'<span class="seg s{k}" style="flex:{sc.count(k)}" title="{sc.count(k)} at level {k}: '
                       f'{html.escape(meaning.get(k, ""))}">{sc.count(k)}</span>' for k in range(6) if sc.count(k))
        avg = sum(sc) / len(sc) if sc else 0
        return f'<div class="stack">{segs}</div><span class="avg">{len(sc)} functions, average {avg:.1f}</span>'

    rows_by = {tp: [r for r in cur[1:] if r[0] == tp] for tp in topics}
    bars = "".join(f'<div class="trow"><span class="tname">{html.escape(tp)}</span>{stack(rows_by[tp])}</div>' for tp in topics)
    bars += f'<div class="trow total"><span class="tname">All functions</span>{stack(cur[1:])}</div>'
    legend = "".join(f'<span class="lg"><span class="sw s{k}"></span><b>{k}</b> {inline(meaning.get(k, ""))}</span>' for k in range(6))
    sections = "".join(f'<h3>{html.escape(tp)}</h3>' + render_table([cur[0][1:]] + [r[1:] for r in rows_by[tp]], score_cols=(1,))
                       for tp in topics)
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
.gallery {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:12px; }}
.shot {{ padding:0; margin:0; overflow:hidden; }} .shot img {{ display:block; width:100%; height:auto; background:#fff; }}
.shot figcaption {{ padding:10px 14px 14px; font-size:14px; }} .shot .t {{ display:block; font-size:15px; margin-bottom:4px; }}
.trow {{ display:grid; grid-template-columns:230px 1fr 170px; gap:10px; align-items:center; margin:8px 0; }}
.trow.total {{ border-top:1px solid var(--line); padding-top:10px; margin-top:12px; font-weight:600; }}
.stack {{ display:flex; height:22px; border-radius:6px; overflow:hidden; background:var(--line); }}
.seg {{ display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#fff; min-width:18px; }}
.seg.s0, .seg.s2 {{ color:#1d1d1b; }}
.seg.s0 {{ background:var(--s0); }} .seg.s1 {{ background:var(--s1); }} .seg.s2 {{ background:var(--s2); }}
.seg.s3 {{ background:var(--s3); }} .seg.s4 {{ background:var(--s4); }} .seg.s5 {{ background:var(--s5); }}
.avg {{ color:var(--muted); font-size:13px; }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 16px; margin-top:12px; font-size:13px; color:var(--muted); }}
.lg {{ display:inline-flex; align-items:center; gap:6px; }} .legend .lg b {{ color:var(--fg); font-size:13px; display:inline; }}
.sw {{ width:12px; height:12px; border-radius:3px; display:inline-block; }}
.sw.s0 {{ background:var(--s0); }} .sw.s1 {{ background:var(--s1); }} .sw.s2 {{ background:var(--s2); }}
.sw.s3 {{ background:var(--s3); }} .sw.s4 {{ background:var(--s4); }} .sw.s5 {{ background:var(--s5); }}
h3 {{ font-size:16px; margin:24px 0 8px; }}
@media (max-width:640px) {{ .trow {{ grid-template-columns:1fr; gap:4px; }} }}
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
<p class="sub">Point clouds, 2D plans and IFC storeys to native Revit elements through the open Revit MCP. State {html.escape(state)}.
How the models are built: <a href="modeling.html">modelling guideline</a>.</p>
<div class="cards">
  <div class="card"><b>{len(scores)}</b>functions scored</div>
  <div class="card"><b>{sum(1 for s in scores if s >= 4)}</b>pass in a real Revit (score 4 or 5)</div>
  <div class="card"><b>{dist[5]}</b>proven on real project data (score 5)</div>
  <div class="card"><b>{len(fut) - 1}</b>missing features planned</div>
</div>
<h2>Current functions in Revit</h2>
<p class="sub">One image per main function, exported by the unattended Revit test from the synthetic examples (project data stays private).</p>
<div class="gallery">{figs}</div>
<h2>Maturity by topic</h2>
<p class="sub">Each function has a maturity level from 0 to 5. A bar shows the functions of one topic: each
coloured segment is one level, the number in it how many functions are at that level. Further right and
darker green is more mature.</p>
<div class="card">{bars}<div class="legend">{legend}</div></div>
<h2>Scale</h2>
{render_table(t["Scale"])}
<h2>Current functionality</h2>
{sections}
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
    if (HERE / "modeling.md").exists():
        gm = (HERE / "modeling.md").read_text(encoding="utf-8")
        gm = re.sub(r"\A---\n.*?\n---\n", "", gm, flags=re.S)          # the skill's front matter
        style = page.split("<style>", 1)[1].split("</style>", 1)[0]
        guide = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modelling guideline</title>
<meta name="description" content="How Revit-MCP builds as-built Revit models from scans, plans and IFC: generic walls and slabs, levels, naming, coordinates, checks.">
<style>{style}
main p, main li {{ max-width:820px; }} main ul {{ padding-left:20px; }} main h2 {{ border-top:1px solid var(--line); padding-top:24px; }}
a {{ color:var(--accent); overflow-wrap:anywhere; }}
</style>
</head>
<body>
<main>
<p class="sub"><a href="index.html">&larr; Revit-MCP status</a></p>
{md_body(gm)}
<footer>Generated from modeling.md (scan2revit/skills/modeling/SKILL.md) by build.py.</footer>
</main>
</body>
</html>
"""
        (HERE / "modeling.html").write_text(guide, encoding="utf-8")
        print("modeling.html: the modelling guideline")


if __name__ == "__main__":
    main()
