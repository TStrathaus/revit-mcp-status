"""Builds index.html from scoring.md (a copy of documentation/scoring.md in the Revit-MCP repository),
open.html from open-tasks.md (a copy of documentation/open-tasks.md: open functions and tasks per sub-project) and
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
    def pane(file, label, alt):
        return (f'<div class="pane"><span class="tag">{label}</span><a href="{html.escape(file)}">'
                f'<img src="{html.escape(file)}" alt="{html.escape(alt)}" loading="lazy"></a></div>')

    def fig(g):                                          # before (the input) and after (Revit) side by side
        tags = g.get("tags") or ["Before: " + g.get("before_label", "input"), "After: Revit"]   # own labels, e.g. two steps
        panes = (pane(g["before"], html.escape(tags[0]), tags[0]) if g.get("before") else "") + \
            pane(g["file"], html.escape(tags[1]), g["title"])
        return (f'<figure class="card shot"><div class="pair{" two" if g.get("before") else ""}">{panes}</div>'
                f'<figcaption><b class="t">{html.escape(g["title"])}</b>{inline(g["text"])}</figcaption></figure>')
    figs = "".join(fig(g) for g in gal)
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
.gallery {{ display:grid; grid-template-columns:1fr; gap:16px; }}
.shot {{ padding:0; margin:0; overflow:hidden; }} .shot img {{ display:block; width:100%; height:auto; background:#fff; }}
.pair {{ display:grid; grid-template-columns:1fr; gap:1px; background:var(--line); align-items:center; }}
.pair.two {{ grid-template-columns:1fr 1fr; }}
.pane {{ position:relative; background:#fff; height:100%; display:flex; align-items:center; }} .pane a {{ display:block; width:100%; }}
.tag {{ position:absolute; top:8px; left:8px; font-size:12px; font-weight:600; padding:2px 8px; border-radius:10px;
  background:rgba(29,29,27,.72); color:#fff; }}
@media (max-width:640px) {{ .pair.two {{ grid-template-columns:1fr; }} }}
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
<p class="sub">Point clouds, 2D plans and IFC storeys to native Revit elements through the pyRevit agent runtime. State {html.escape(state)}.
Open functions and tasks per sub-project: <a href="open.html">open items</a>. How the models are built:
<a href="modeling.html">modelling guideline</a>. What the agent team did and found:
<a href="agents.html">agent scoreboard</a>.</p>
<div class="cards">
  <div class="card"><b>{len(scores)}</b>functions scored</div>
  <div class="card"><b>{sum(1 for s in scores if s >= 4)}</b>pass in a real Revit (score 4 or 5)</div>
  <div class="card"><b>{dist[5]}</b>proven on real project data (score 5)</div>
  <div class="card"><b>{len(fut) - 1}</b>missing features planned</div>
</div>
<h2>Current functions in Revit</h2>
<p class="sub">Before and after for each main function: on the left what the route starts from (point cloud, plan, IFC),
on the right the native Revit model, exported by the unattended Revit test. Synthetic examples only (project data stays private).</p>
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
<p class="sub">Sorted by value, then effort. Value 1 to 5, effort S (hours), M (a day or two), L (more).
By sub-project, with the gaps and the tasks: <a href="open.html">open items</a>.</p>
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
    if (HERE / "open-tasks.md").exists():
        open_page(page.split("<style>", 1)[1].split("</style>", 1)[0])
    if (HERE / "agent-scoreboard.md").exists():
        scoreboard_page(page.split("<style>", 1)[1].split("</style>", 1)[0])


def open_page(style):
    """open.html: one section per sub-project (## heading in open-tasks.md), its intro and its table of open
    items; a Kind column (Function, Gap, Task) becomes a coloured tag."""
    md = (HERE / "open-tasks.md").read_text(encoding="utf-8")
    md = md.split("\n## ", 1)
    head, rest = md[0], ("## " + md[1]) if len(md) > 1 else ""
    title = head.splitlines()[0].lstrip("# ").strip()
    intro = "\n".join(head.splitlines()[1:])
    state = re.search(r"State (\d{1,2}\.\d{1,2}\.\d{4})", head)
    legend = "\n\n".join(p for p in intro.split("\n\n") if p.strip() and not p.strip().startswith("State"))  # not the sources note
    t = tables(rest)
    secs = [b for b in rest.split("\n## ") if b.strip()]
    kinds = ("Function", "Gap", "Task")
    cards, body = [], []
    for b in secs:
        b = b[3:] if b.startswith("## ") else b
        name = b.splitlines()[0].strip()
        rows = t.get(name, [])
        text = "\n".join(l for l in b.splitlines()[1:] if not l.startswith("|"))
        ki = rows[0].index("Kind") if rows and "Kind" in rows[0] else None
        n = {k: sum(1 for r in rows[1:] if ki is not None and r[ki] == k) for k in kinds}
        anchor = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        cards.append(f'<a class="card route" href="#{anchor}"><span class="rn">{html.escape(name)}</span><b>{len(rows) - 1 if rows else 0}</b>'
                     + " ".join(f'<span class="kind k{k.lower()}">{n[k]} {k.lower()}{"s" if n[k] != 1 else ""}</span>' for k in kinds if n[k])
                     + "</a>")
        tbl = ""
        if rows:
            h = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            trs = "".join("<tr>" + "".join(
                (f'<td><span class="kind k{c.lower()}">{html.escape(c)}</span></td>' if i == ki else f"<td>{inline(c)}</td>")
                for i, c in enumerate(r)) + "</tr>" for r in rows[1:])
            tbl = f'<div class="wrap"><table><thead><tr>{h}</tr></thead><tbody>{trs}</tbody></table></div>'
        body.append(f'<h2 id="{anchor}">{html.escape(name)}</h2>{md_body(text)}{tbl}')
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Open items</title>
<meta name="description" content="Open functions, gaps and tasks of Revit-MCP per sub-project: Pointcloud2Revit, IFC2Revit, Plans2Revit and the shared core.">
<style>{style}
main p {{ max-width:820px; }} a {{ color:var(--accent); overflow-wrap:anywhere; }}
.route {{ text-decoration:none; color:var(--fg); display:block; }} .route:hover {{ border-color:var(--accent); }}
.route .rn {{ display:block; font-weight:600; }} .route b {{ margin:2px 0 6px; }}
.kind {{ display:inline-block; font-size:12px; font-weight:600; padding:1px 7px; border-radius:10px; white-space:nowrap; margin:2px 4px 0 0; }}
.kfunction {{ background:color-mix(in srgb,var(--accent) 18%,transparent); color:var(--accent); }}
.kgap {{ background:color-mix(in srgb,var(--s1) 25%,transparent); color:color-mix(in srgb,var(--s1) 70%,var(--fg)); }}
.ktask {{ background:color-mix(in srgb,var(--s4) 22%,transparent); color:color-mix(in srgb,var(--s4) 75%,var(--fg)); }}
</style>
</head>
<body>
<main>
<p class="sub"><a href="index.html">&larr; Revit-MCP status</a></p>
<h1>{html.escape(title)}</h1>
<p class="sub">State {html.escape(state.group(1) if state else "")}. Open functions, known gaps and tasks, one section per sub-project; the order within a section is the order of work.</p>
<div class="cards">{"".join(cards)}</div>
{md_body(legend)}
{"".join(body)}
<footer>Generated from open-tasks.md (documentation/open-tasks.md) by build.py.</footer>
</main>
</body>
</html>
"""
    (HERE / "open.html").write_text(page, encoding="utf-8")
    print(f"open.html: {len(secs)} sections")




def scoreboard_page(style):
    """agents.html from agent-scoreboard.md (documentation/agent-scoreboard.md: actions and findings per agent)."""
    md = (HERE / "agent-scoreboard.md").read_text(encoding="utf-8")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent scoreboard</title>
<meta name="description" content="What the agents of the Revit-MCP modelling team did and found, per agent and project.">
<style>{style}
main p, main li {{ max-width:820px; }} main h2 {{ border-top:1px solid var(--line); padding-top:24px; }}
.tablewrap {{ overflow-x:auto; }}
</style>
</head>
<body>
<main>
<p class="sub"><a href="index.html">&larr; Revit-MCP status</a></p>
{md_body(md)}
<footer>Generated from agent-scoreboard.md (documentation/agent-scoreboard.md) by build.py.</footer>
</main>
</body>
</html>
"""
    (HERE / "agents.html").write_text(page, encoding="utf-8")
    print("agents.html: the agent scoreboard")

if __name__ == "__main__":
    main()
