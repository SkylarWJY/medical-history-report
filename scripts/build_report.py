#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_report.py — Turn a structured patient JSON into a single self-contained,
mobile-friendly HTML health dashboard (Chinese UI).

Usage:
    python3 build_report.py <patient.json> <output.html>

The input JSON schema is documented in assets/schema.json and demonstrated in
examples/sample_patient.json. Every value in the output comes from the JSON —
this script renders, it does not invent. Keep all clinical content evidence-based
and flag uncertainty in the source data; this report never replaces a doctor.
"""
import json
import sys
import html as _html

LEVEL_BADGE = {
    "green": ("b-green", "d-green"),
    "yellow": ("b-yellow", "d-yellow"),
    "orange": ("b-orange", "d-orange"),
    "red": ("b-red", "d-red"),
    "blue": ("b-blue", "d-green"),
    "gray": ("b-gray", "d-green"),
}
LEVEL_TEXT = {"green": "低", "yellow": "需关注", "orange": "中高", "red": "高", "blue": "改善", "gray": "—"}
TAG_LABEL = {"dx": ("t-dx", "诊断"), "tx": ("t-tx", "治疗"), "img": ("t-img", "影像"),
             "fu": ("t-fu", "随访"), "other": ("t-other", "其他")}
TREND = {"up": ('up', '↑ 增大'), "down": ('down', '↓ 缩小'), "flat": ('flat', '→ 持平'),
         "baseline": ('flat', '基线')}


def esc(x):
    return _html.escape(str(x)) if x is not None else ""


def badge(level, text=None):
    b, d = LEVEL_BADGE.get(level, LEVEL_BADGE["gray"])
    t = text if text is not None else LEVEL_TEXT.get(level, "")
    return f'<span class="badge {b}"><span class="dotr {d}"></span>{esc(t)}</span>'


def get(d, k, default=None):
    return d.get(k, default) if isinstance(d, dict) else default


CSS = """
:root{--bg:#f4f6f9;--card:#fff;--ink:#1f2a37;--muted:#64748b;--line:#e5eaf0;--blue:#2563eb;--blue-d:#1e40af;
--green:#16a34a;--green-bg:#e7f6ec;--yellow:#d97706;--yellow-bg:#fdf3e3;--orange:#ea580c;--orange-bg:#fdeee3;
--red:#dc2626;--red-bg:#fdeaea;--shadow:0 1px 3px rgba(16,24,40,.06),0 1px 2px rgba(16,24,40,.04);--shadow-lg:0 10px 30px rgba(16,24,40,.08);}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Segoe UI",sans-serif;
background:var(--bg);color:var(--ink);line-height:1.7;font-size:15px;-webkit-text-size-adjust:100%}
.wrap{max-width:1140px;margin:0 auto;padding:0 16px 70px}
header.top{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;padding:30px 0 26px;margin-bottom:24px;box-shadow:var(--shadow-lg)}
header.top .wrap{padding-top:0;padding-bottom:0}
.brand{font-size:12.5px;letter-spacing:2px;opacity:.85;margin-bottom:6px}
header.top h1{margin:.1em 0 .25em;font-size:27px;font-weight:800}
header.top .sub{opacity:.92;font-size:14px}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.pill{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);padding:5px 12px;border-radius:999px;font-size:12.5px}
.disclaimer{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:12px;padding:13px 16px;font-size:13px;margin-bottom:24px}
section{margin-bottom:30px}
h2.sec{font-size:20px;font-weight:800;margin:0 0 4px;display:flex;align-items:center;gap:10px}
h2.sec .num{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:9px;background:var(--blue);color:#fff;font-size:14px;font-weight:700;flex:none}
.sec-desc{color:var(--muted);font-size:13px;margin:0 0 14px;padding-left:40px}
.grid{display:grid;gap:14px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}
@media(max-width:820px){.g2,.g3{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:var(--shadow)}
.card h3{margin:0 0 8px;font-size:15.5px;display:flex;align-items:center;gap:8px;justify-content:space-between}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:820px){.stats{grid-template-columns:repeat(2,1fr)}}
.stat{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;text-align:center;box-shadow:var(--shadow)}
.stat .k{font-size:12px;color:var(--muted);margin-bottom:6px}.stat .v{font-size:21px;font-weight:800;line-height:1.2}.stat .note{font-size:11px;color:var(--muted);margin-top:4px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:3px 11px;border-radius:999px;font-size:12px;font-weight:700;white-space:nowrap}
.b-green{background:var(--green-bg);color:#15803d}.b-yellow{background:var(--yellow-bg);color:#b45309}.b-orange{background:var(--orange-bg);color:#c2410c}.b-red{background:var(--red-bg);color:#b91c1c}.b-gray{background:#eef1f5;color:#475569}.b-blue{background:#e6efff;color:#1d4ed8}
.dotr{width:8px;height:8px;border-radius:50%;flex:none}.d-green{background:var(--green)}.d-yellow{background:var(--yellow)}.d-orange{background:var(--orange)}.d-red{background:var(--red)}
.top5 .row{display:flex;gap:13px;align-items:flex-start;padding:15px 0;border-bottom:1px dashed var(--line)}.top5 .row:last-child{border-bottom:none}
.rank{flex:none;width:32px;height:32px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:15px}
.top5 .title{font-weight:700;font-size:15.5px;margin-bottom:3px}.top5 .meta{font-size:13px;color:var(--muted);margin:2px 0}
.top5 .ev{font-size:13px;background:#f8fafc;border-left:3px solid var(--blue);padding:7px 11px;border-radius:6px;margin-top:6px}
.timeline{position:relative;padding-left:28px}
.timeline::before{content:"";position:absolute;left:9px;top:6px;bottom:6px;width:2px;background:linear-gradient(#93c5fd,#bfdbfe)}
.tl{position:relative;margin-bottom:18px}
.tl::before{content:"";position:absolute;left:-25px;top:5px;width:13px;height:13px;border-radius:50%;background:#fff;border:3px solid var(--blue)}
.tl.major::before{border-color:var(--red);width:15px;height:15px;left:-26px}
.tl .yr{font-weight:800;font-size:14.5px;color:var(--blue-d)}
.tl .ev{background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 13px;margin-top:6px;box-shadow:var(--shadow);font-size:13.5px}
.tl .ev .where{font-size:11.5px;color:var(--muted)}
.tag{display:inline-block;font-size:11px;padding:1px 8px;border-radius:6px;margin-right:5px;font-weight:600}
.t-dx{background:#fee2e2;color:#b91c1c}.t-tx{background:#dbeafe;color:#1d4ed8}.t-img{background:#ede9fe;color:#6d28d9}.t-fu{background:#dcfce7;color:#15803d}.t-other{background:#f1f5f9;color:#475569}
table{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}
th,td{padding:9px 11px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f1f5f9;font-weight:700;font-size:12px;color:#334155;white-space:nowrap}
tr:last-child td{border-bottom:none}td.c{text-align:center}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.up{color:var(--red);font-weight:700}.down{color:var(--green);font-weight:700}.flat{color:var(--muted)}
.chart{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px;box-shadow:var(--shadow)}
.bars{display:flex;align-items:flex-end;gap:8px;height:160px;padding:18px 4px 0;border-bottom:2px solid var(--line);position:relative}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.bar .col{width:70%;border-radius:5px 5px 0 0;min-height:3px}.bar .lab{font-size:10px;color:var(--muted);margin-top:6px;text-align:center;line-height:1.25;white-space:pre-line}.bar .val{font-size:10.5px;font-weight:700;margin-bottom:3px}
.refline{position:absolute;left:0;right:0;border-top:2px dashed #f59e0b;font-size:10px;color:#b45309}
.marker-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}@media(max-width:820px){.marker-grid{grid-template-columns:1fr 1fr}}
.mk{background:#fff;border:1px solid var(--line);border-radius:11px;padding:12px;text-align:center;box-shadow:var(--shadow)}.mk .n{font-size:12px;color:var(--muted)}.mk .vv{font-size:19px;font-weight:800;margin:3px 0;color:var(--green)}.mk .rg{font-size:11px;color:#94a3b8}
.note-src{font-size:11.5px;color:#94a3b8;margin-top:8px;font-style:italic}
.change .card{border-top:4px solid}.ch-worse{border-color:var(--red)}.ch-maybe{border-color:var(--orange)}.ch-stable{border-color:var(--green)}.ch-better{border-color:var(--blue)}
.change ul{margin:8px 0 0;padding-left:18px}.change li{margin-bottom:7px;font-size:13px}
.risk-matrix{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}@media(max-width:820px){.risk-matrix{grid-template-columns:1fr}}
.rm{display:flex;align-items:center;gap:12px;padding:11px 13px;border-radius:11px;border:1px solid var(--line);background:#fff;box-shadow:var(--shadow)}.rm .sys{font-weight:700;flex:1}.rm .lv{font-size:12px;color:var(--muted)}
.family{background:linear-gradient(135deg,#eff6ff,#f0f9ff);border:1px solid #bfdbfe;border-radius:16px;padding:8px 22px 18px}
.qa .q{font-weight:700;color:var(--blue-d);margin-top:13px}.qa .a{margin-top:2px;font-size:14.5px}
.action .card{border-left:4px solid var(--blue)}.action .now{border-color:var(--red)}.action .m1{border-color:var(--orange)}.action .m3{border-color:var(--yellow)}.action .lt{border-color:var(--green)}
.action ul{margin:8px 0 0;padding-left:18px;font-size:13px}.action li{margin-bottom:6px}
.checklist{background:#fff;border:1px solid var(--line);border-radius:14px;padding:8px 20px 16px;box-shadow:var(--shadow)}
.checklist .item{display:flex;gap:10px;padding:10px 0;border-bottom:1px dashed var(--line);font-size:13.5px}.checklist .item:last-child{border-bottom:none}
.checklist .box{flex:none;width:18px;height:18px;border:2px solid var(--blue);border-radius:5px;margin-top:3px}
.concl{background:#0f172a;color:#e2e8f0;border-radius:16px;padding:22px 22px}.concl h3{color:#fff;margin-top:0}
.concl .line{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid #1e293b;font-size:14px}.concl .line:last-child{border-bottom:none}
.concl .k{flex:none;width:118px;color:#7dd3fc;font-weight:700}.concl .big{font-size:17px;font-weight:800}
footer{text-align:center;color:var(--muted);font-size:12px;margin-top:36px;padding-top:18px;border-top:1px solid var(--line)}
"""


def render(d):
    p = get(d, "patient", {})
    ov = get(d, "overall", {})
    out = []
    A = out.append

    # header
    pills = "".join(f'<span class="pill">{esc(x)}</span>' for x in get(p, "pills", []))
    A(f'''<header class="top"><div class="wrap">
      <div class="brand">个人健康全景分析 · HEALTH OVERVIEW</div>
      <h1>{esc(get(p,"name","健康全景报告"))}</h1>
      <div class="sub">{esc(get(p,"subtitle",""))}</div>
      <div class="pills">{pills}</div>
    </div></header><div class="wrap">''')

    A('''<div class="disclaimer"><b>重要说明：</b>本报告由 AI 依据病历原文整理，<b>仅用于帮助家属理解病情、与医生沟通，不能替代医生诊断</b>。
      所有判断均应基于病历原文；不确定处需写明"需医生确认"。如遇红色提示请优先就医。</div>''')

    n = 0
    def secnum():
        nonlocal n
        n += 1
        return n

    # 1 overview
    if ov:
        stats = "".join(
            f'<div class="stat"><div class="k">{esc(get(s,"k"))}</div>'
            f'<div class="v" style="color:var(--{get(s,"color","blue") if get(s,"color") in ["green","yellow","orange","red"] else "ink"})">{esc(get(s,"v"))}</div>'
            f'<div class="note">{esc(get(s,"note",""))}</div></div>'
            for s in get(ov, "stats", []))
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>整体健康概览</h2>
          <p class="sec-desc">{esc(get(ov,"risk_note",""))}</p>
          <div class="stats" style="margin-bottom:16px">{stats}</div>
          <div class="grid g3">
            <div class="card"><h3>📌 长期存在</h3><div style="font-size:13px">{esc(get(ov,"long_existing",""))}</div></div>
            <div class="card"><h3>🆕 近期新发/升级</h3><div style="font-size:13px">{esc(get(ov,"new_recent",""))}</div></div>
            <div class="card"><h3>⚠ 优先关注</h3><div style="font-size:13px">{esc(get(ov,"top_risk_hint",""))}</div></div>
          </div></section>''')

    # 2 top issues
    issues = get(d, "top_issues", [])
    if issues:
        rows = []
        colors = {"red": "var(--red)", "orange": "var(--orange)", "yellow": "var(--yellow)", "green": "var(--green)"}
        for it in issues:
            c = colors.get(get(it, "level", "yellow"), "var(--yellow)")
            rows.append(f'''<div class="row"><div class="rank" style="background:{c}">{esc(get(it,"rank",""))}</div>
              <div class="body"><div class="title">{esc(get(it,"title"))} {badge(get(it,"level","yellow"))}</div>
              <div class="meta">为什么重要：{esc(get(it,"why",""))}</div>
              <div class="ev">📄 证据：{esc(get(it,"evidence",""))}</div>
              <div class="meta">建议：{esc(get(it,"advice",""))}</div></div></div>''')
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>当前最需要关注的问题</h2>
          <p class="sec-desc">按优先级排序。</p><div class="card top5">{"".join(rows)}</div></section>''')

    # evolution (病情变化史)
    ev = get(d, "evolution", [])
    if ev:
        trs = "".join(
            f'<tr><td><b>{esc(get(e,"period"))}</b></td><td>{esc(get(e,"diagnosis"))}</td>'
            f'<td class="c">{badge(get(e,"status_level","gray"), get(e,"status"))}</td>'
            f'<td>{esc(get(e,"evidence",""))}</td></tr>' for e in ev)
        A(f'''<section><h2 class="sec"><span class="num" style="background:#7c3aed">史</span>病情变化史 · 诊断演变一览</h2>
          <p class="sec-desc">用一张表看清"诊断 / 状态"如何随时间变化——理解全局最快的一节。</p>
          <div class="scroll"><table><thead><tr><th>时期</th><th>诊断/分期</th><th>病情状态</th><th>关键证据</th></tr></thead>
          <tbody>{trs}</tbody></table></div></section>''')

    # lesion size tracking
    lesions = get(d, "lesions", [])
    if lesions:
        blocks = []
        for L in lesions:
            trs = []
            for r in get(L, "rows", []):
                tc, tt = TREND.get(get(r, "trend", "flat"), ("flat", ""))
                trs.append(f'<tr><td>{esc(get(r,"date"))}</td><td><b>{esc(get(r,"size"))}</b></td>'
                            f'<td>{esc(get(r,"extra",""))}</td><td class="c">{esc(get(r,"suv","—"))}</td>'
                            f'<td>{esc(get(r,"modality",""))}</td><td class="{tc}">{tt}</td></tr>')
            blocks.append(f'''<h3 style="margin:18px 0 8px;font-size:15.5px">{esc(get(L,"name"))} — {esc(get(L,"summary",""))}</h3>
              <div class="scroll"><table><thead><tr><th>日期</th><th>尺寸</th><th>性质/描述</th><th>SUV</th><th>检查</th><th>趋势</th></tr></thead>
              <tbody>{"".join(trs)}</tbody></table></div><p class="note-src">{esc(get(L,"note",""))}</p>''')
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>重点病灶尺寸变化轨迹（核心）</h2>
          <p class="sec-desc">每个病灶的逐次精确尺寸。↑增大 / ↓缩小 / →持平。</p>{"".join(blocks)}</section>''')

    # lab trends + markers
    labs = get(d, "lab_trends", [])
    markers = get(d, "markers", [])
    if labs or markers:
        charts = []
        for lab in labs:
            pts = get(lab, "points", [])
            mx = max([float(get(pt, "value", 0)) for pt in pts] + [1])
            bars = []
            for pt in pts:
                v = float(get(pt, "value", 0))
                h = max(4, int(v / mx * 100))
                col = {"red": "var(--red)", "orange": "var(--orange)", "yellow": "var(--yellow)", "green": "var(--green)"}.get(get(pt, "level", "green"), "var(--blue)")
                bars.append(f'<div class="bar"><div class="val">{esc(get(pt,"value"))}</div>'
                            f'<div class="col" style="height:{h}%;background:{col}"></div>'
                            f'<div class="lab">{esc(get(pt,"label",""))}</div></div>')
            rr = get(lab, "refline_ratio")
            refl = (f'<div class="refline" style="bottom:calc(18px + {1-float(rr)}*(160px - 18px))">{esc(get(lab,"ref",""))}</div>') if rr else ""
            charts.append(f'''<div class="chart"><h3 style="margin:0 0 4px;font-size:15px">{esc(get(lab,"name"))}</h3>
              <div style="font-size:12px;color:var(--muted);margin-bottom:6px">{esc(get(lab,"ref",""))}</div>
              <div class="bars">{refl}{"".join(bars)}</div><p class="note-src">{esc(get(lab,"note",""))}</p></div>''')
        if markers:
            mk = "".join(f'<div class="mk"><div class="n">{esc(get(m,"n"))}</div><div class="vv">{esc(get(m,"v"))}</div><div class="rg">{esc(get(m,"rg",""))}</div></div>' for m in markers)
            charts.append(f'<div class="chart"><h3 style="margin:0 0 10px;font-size:15px">关键化验指标</h3><div class="marker-grid">{mk}</div></div>')
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>关键指标趋势</h2>
          <div class="grid g2">{"".join(charts)}</div></section>''')

    # systems
    systems = get(d, "systems", [])
    if systems:
        cards = "".join(
            f'''<div class="card"><h3><span>{esc(get(s,"name"))}</span>{badge(get(s,"level","gray"))}</h3>
            <div style="font-size:13px"><b>问题：</b>{esc(get(s,"problem",""))}<br><b>趋势：</b>{esc(get(s,"trend",""))}<br><b>建议：</b>{esc(get(s,"advice",""))}</div></div>'''
            for s in systems)
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>按器官系统分类分析</h2>
          <div class="grid g2">{cards}</div></section>''')

    # timeline
    tl = get(d, "timeline", [])
    if tl:
        items = []
        for t in tl:
            evs = []
            for e in get(t, "events", []):
                tc, tlbl = TAG_LABEL.get(get(e, "tag", "other"), ("t-other", "其他"))
                evs.append(f'<div class="ev"><span class="tag {tc}">{tlbl}</span>{esc(get(e,"text"))}<div class="where">📄 {esc(get(e,"where",""))}</div></div>')
            items.append(f'<div class="tl{" major" if get(t,"major") else ""}"><div class="yr">{esc(get(t,"year"))}</div>{"".join(evs)}</div>')
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>疾病发展时间线</h2>
          <div class="timeline">{"".join(items)}</div></section>''')

    # changes
    ch = get(d, "changes", {})
    if ch:
        def ul(items): return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in (items or [])) + "</ul>"
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>病情变好 / 变差 / 稳定总结</h2>
          <div class="grid g2 change">
            <div class="card ch-worse"><h3 style="color:var(--red)">A. 需重视 / 变重</h3>{ul(get(ch,"worse"))}</div>
            <div class="card ch-maybe"><h3 style="color:var(--orange)">B. 待医生确认</h3>{ul(get(ch,"uncertain"))}</div>
            <div class="card ch-stable"><h3 style="color:var(--green)">C. 基本稳定</h3>{ul(get(ch,"stable"))}</div>
            <div class="card ch-better"><h3 style="color:var(--blue)">D. 明显好转</h3>{ul(get(ch,"better"))}</div>
          </div></section>''')

    # risk matrix
    rmx = get(d, "risk_matrix", [])
    if rmx:
        rms = "".join(f'<div class="rm">{badge(get(r,"level","gray"))}<span class="sys">{esc(get(r,"system"))}</span><span class="lv">{esc(get(r,"note",""))}</span></div>' for r in rmx)
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>风险等级矩阵</h2><div class="risk-matrix">{rms}</div></section>''')

    # family qa
    qa = get(d, "family_qa", [])
    if qa:
        body = "".join(f'<div class="q">{esc(get(x,"q"))}</div><div class="a">{esc(get(x,"a"))}</div>' for x in qa)
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>给家属看的解释版（大白话）</h2>
          <div class="family qa">{body}</div></section>''')

    # actions
    ac = get(d, "actions", {})
    if ac:
        def ul(items): return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in (items or [])) + "</ul>"
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>下一步行动建议</h2>
          <div class="grid g2 action">
            <div class="card now"><h3 style="color:var(--red)">🔴 立刻/尽快</h3>{ul(get(ac,"now"))}</div>
            <div class="card m1"><h3 style="color:var(--orange)">🟠 1 个月内</h3>{ul(get(ac,"m1"))}</div>
            <div class="card m3"><h3 style="color:var(--yellow)">🟡 3 个月内</h3>{ul(get(ac,"m3"))}</div>
            <div class="card lt"><h3 style="color:var(--green)">🟢 长期随访</h3>{ul(get(ac,"long"))}</div>
          </div></section>''')

    # doctor questions
    dq = get(d, "doctor_questions", [])
    if dq:
        items = "".join(f'<div class="item"><span class="box"></span><span>{esc(x)}</span></div>' for x in dq)
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>带去医院的"问医生"清单</h2>
          <div class="checklist">{items}</div></section>''')

    # conclusion
    cc = get(d, "conclusion", [])
    if cc:
        lines = "".join(
            f'<div class="line"><span class="k">{esc(get(c,"k"))}</span><span'
            + (' class="big" style="color:#fdba74"' if get(c, "big") else "")
            + f'>{esc(get(c,"v"))}</span></div>' for c in cc)
        A(f'''<section><h2 class="sec"><span class="num">{secnum()}</span>最终结论</h2>
          <div class="concl"><h3>📌 基于证据的克制总结</h3>{lines}</div></section>''')

    A(f'''<footer>{esc(get(d,"sources",""))}<br>本报告由 AI 整理 · 仅供理解病情与医患沟通，<b>不构成医疗诊断，一切以执业医生意见为准</b>。</footer></div>''')
    return "\n".join(out)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 build_report.py <patient.json> <output.html>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    body = render(data)
    title = get(get(data, "patient", {}), "name", "健康全景报告")
    page = (f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>')
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(page)
    print(f"✓ 已生成 {sys.argv[2]}（{len(page)} 字符）")


if __name__ == "__main__":
    main()
