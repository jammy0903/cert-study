#!/usr/bin/env python3
"""
TOPCIT 레슨 뷰어 생성기
JSON(topcit_json_v2) → 모바일 반응형 HTML (과목별 인덱스 + 풀스크린 레슨)
- 카드 뷰: 챕터/섹션 그룹 + 검색 + 챕터 탭 필터 + 우선순위 필터
- 카드 클릭 → 레슨 모드 (학습 페이지 + 완료 페이지)
- 키보드 ←/→/Esc + 모바일 스와이프 + 진도바
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).parent
JSON_DIR = ROOT / "topcit_json_v2"
OUT_DIR = ROOT / "topcit_lesson"

SUBJECTS = [
    {"id": "01", "title": "소프트웨어 개발",                 "emoji": "💻", "main": "#2563eb", "sub": "#1d4ed8"},
    {"id": "02", "title": "데이터 이해와 활용",              "emoji": "📊", "main": "#0e9488", "sub": "#115e59"},
    {"id": "03", "title": "시스템 아키텍처",                 "emoji": "🏗️", "main": "#7c3aed", "sub": "#5b21b6"},
    {"id": "04", "title": "정보보안",                        "emoji": "🔒", "main": "#dc2626", "sub": "#991b1b"},
    {"id": "05", "title": "IT 비즈니스와 윤리",              "emoji": "💼", "main": "#b45309", "sub": "#78350f"},
    {"id": "06", "title": "테크니컬 커뮤니케이션·PM",         "emoji": "📝", "main": "#475569", "sub": "#1e293b"},
]

PRIORITY_META = {
    1: {"label": "최우선", "color": "#dc2626", "emoji": "🔴"},
    2: {"label": "중요",   "color": "#d97706", "emoji": "🟡"},
    3: {"label": "보통",   "color": "#16a34a", "emoji": "🟢"},
    4: {"label": "보조",   "color": "#9ca3af", "emoji": "⚪"},
}


def load_json(subj_id: str) -> dict | None:
    path = JSON_DIR / f"topcit_{subj_id}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def concept_to_lesson(con: dict) -> dict:
    return {
        "title":       con.get("title", ""),
        "keywords":    con.get("keywords", []),
        "summary":     con.get("summary", ""),
        "background":  con.get("background", ""),
        "explanation": con.get("explanation", ""),
        "why":         con.get("why", ""),
        "term_focus":  con.get("term_focus", []),
        "connections": con.get("connections", []),
        "types":       con.get("types"),
        "mnemonic":    con.get("mnemonic", ""),
        "trap":        con.get("trap", ""),
        "table":       con.get("table", []),
        "sources":     con.get("sources", []),
        "priority":    con.get("priority"),
    }


def card_html(con: dict, idx: int) -> str:
    title = esc(con.get("title", ""))
    preview_src = con.get("background") or con.get("explanation") or ""
    preview = (preview_src[:50] + "…") if len(preview_src) > 50 else preview_src
    badges = ""
    prio = con.get("priority")
    if prio in PRIORITY_META:
        meta = PRIORITY_META[prio]
        badges += f'<span class="b-prio b-prio-{prio}" title="{meta["label"]}">{meta["emoji"]} P{prio}</span>'
    if con.get("mnemonic"):
        badges += '<span class="b-mn" title="암기 포인트">🧠</span>'
    prio_attr = f' data-prio="{prio}"' if prio else ' data-prio=""'
    return (
        f'<div class="card"{prio_attr} onclick="startLesson({idx})">'
        f'<div class="card-badges">{badges}</div>'
        f'<div class="card-title">{title}</div>'
        f'<div class="card-preview">{esc(preview)}</div>'
        f'<div class="card-cta">레슨 시작 →</div>'
        f'</div>'
    )


def subject_page(subj: dict, data: dict) -> str:
    chapters = data["chapters"]
    total = sum(len(s["concepts"]) for ch in chapters for s in ch["sections"])

    lessons = []
    con_idx_map = {}
    for ci, ch in enumerate(chapters):
        for si, sec in enumerate(ch["sections"]):
            for ki, con in enumerate(sec["concepts"]):
                con_idx_map[(ci, si, ki)] = len(lessons)
                lessons.append(concept_to_lesson(con))

    sections_html = ""
    for ci, ch in enumerate(chapters):
        for si, sec in enumerate(ch["sections"]):
            cards = "".join(
                card_html(con, con_idx_map[(ci, si, ki)])
                for ki, con in enumerate(sec["concepts"])
            )
            sections_html += (
                f'<div class="section-group" data-chapter="{ci}">'
                f'<div class="section-label">{esc(ch["title"])} · {esc(sec["title"])}</div>'
                f'<div class="card-grid">{cards}</div>'
                f'</div>'
            )

    tab_html = '<button class="tab active" onclick="filterTab(this,\'all\')">전체</button>'
    for i, ch in enumerate(chapters):
        tab_html += f'<button class="tab" onclick="filterTab(this,\'{i}\')">{esc(ch["title"][:18])}</button>'

    prio_html = '<button class="pchip active" data-prio="all" onclick="filterPrio(this)">전체</button>'
    for p in (1, 2, 3, 4):
        meta = PRIORITY_META[p]
        prio_html += (
            f'<button class="pchip" data-prio="{p}" onclick="filterPrio(this)" '
            f'style="--pc:{meta["color"]}">{meta["emoji"]} P{p} {meta["label"]}</button>'
        )

    main, sub = subj["main"], subj["sub"]

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>TOPCIT {subj["id"]} {subj["title"]}</title>
<style>
:root{{--font-sans:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,sans-serif;--font-serif:"NanumMyeongjo","Nanum Myeongjo","Batang","Apple SD Gothic Neo",serif}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{overflow-x:hidden}}
body{{font-family:var(--font-sans);background:#f7f8fb;color:#1f2937;min-height:100vh}}

.header{{background:{main};color:#fff;padding:.85rem 1.25rem;display:flex;align-items:center;gap:.75rem;position:sticky;top:0;z-index:20;box-shadow:0 2px 10px rgba(0,0,0,.15)}}
.header-back{{color:#fff;text-decoration:none;font-size:1.2rem;opacity:.85}}
.header h1{{font-size:1rem;font-weight:800;flex:1;font-family:var(--font-serif)}}
.header-cnt{{font-size:.75rem;opacity:.8;white-space:nowrap}}

.search-wrap{{padding:.7rem 1.25rem .3rem}}
.search{{width:100%;padding:.6rem 1rem;border:2px solid #e2e8f0;border-radius:2rem;font-size:.88rem;outline:none;background:#fff;transition:border .2s}}
.search:focus{{border-color:{main}}}

.tabs{{display:flex;gap:.35rem;padding:.4rem 1.25rem .3rem;overflow-x:auto;scrollbar-width:none}}
.tabs::-webkit-scrollbar{{display:none}}
.tab{{flex-shrink:0;padding:.32rem .8rem;border-radius:2rem;border:1.5px solid {main};background:#fff;color:{main};font-size:.74rem;font-weight:700;cursor:pointer;white-space:nowrap;transition:all .15s;font-family:inherit}}
.tab.active,.tab:hover{{background:{main};color:#fff}}

.prio-bar{{display:flex;gap:.3rem;padding:.2rem 1.25rem .6rem;overflow-x:auto;scrollbar-width:none}}
.prio-bar::-webkit-scrollbar{{display:none}}
.pchip{{flex-shrink:0;padding:.28rem .7rem;border-radius:2rem;border:1.5px solid #e5e7eb;background:#fff;color:#475569;font-size:.72rem;font-weight:700;cursor:pointer;white-space:nowrap;transition:all .15s;font-family:inherit}}
.pchip:hover{{border-color:var(--pc,#9ca3af);color:#111827}}
.pchip.active{{background:var(--pc,{main});border-color:var(--pc,{main});color:#fff}}
.pchip[data-prio="all"].active{{background:{main};border-color:{main};color:#fff}}

.section-group{{padding:.3rem 1.25rem .8rem}}
.section-group.hidden{{display:none}}
.section-label{{font-size:.72rem;font-weight:800;color:{sub};letter-spacing:.04em;padding:.4rem 0 .35rem;border-bottom:2px solid {main}33;margin-bottom:.55rem;font-family:var(--font-serif)}}
.card-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.55rem}}
@media(min-width:540px){{.card-grid{{grid-template-columns:repeat(3,1fr)}}}}
@media(min-width:900px){{.card-grid{{grid-template-columns:repeat(4,1fr)}}}}
@media(min-width:1200px){{.card-grid{{grid-template-columns:repeat(5,1fr)}}}}
.card{{background:#fff;border-radius:.7rem;padding:.85rem .8rem .65rem;cursor:pointer;border:1.5px solid #e5e7eb;transition:all .18s;box-shadow:0 1px 3px rgba(0,0,0,.04);position:relative;display:flex;flex-direction:column;gap:.35rem;min-height:9rem}}
.card:hover{{border-color:{main};box-shadow:0 4px 14px {main}33;transform:translateY(-2px)}}
.card-badges{{position:absolute;top:.45rem;right:.5rem;display:flex;gap:.2rem;font-size:.64rem}}
.card-badges span{{padding:.1rem .42rem;border-radius:.4rem;font-weight:700;line-height:1.4;white-space:nowrap}}
.b-prio-1{{background:#fee2e2;color:#991b1b}}
.b-prio-2{{background:#fef3c7;color:#92400e}}
.b-prio-3{{background:#dcfce7;color:#166534}}
.b-prio-4{{background:#f1f5f9;color:#475569}}
.b-mn{{background:#ede9fe;color:#5b21b6}}
.card-title{{font-size:.86rem;font-weight:700;color:#111827;line-height:1.35;padding-right:4.5rem;font-family:var(--font-serif)}}
.card-preview{{font-size:.7rem;color:#6b7280;line-height:1.5;flex:1}}
.card-cta{{font-size:.68rem;color:{main};font-weight:700;text-align:right;margin-top:.25rem}}
.card.hidden-card{{display:none!important}}

/* ───────── 레슨 모드 (풀스크린) ───────── */
.lesson{{display:none;position:fixed;inset:0;background:#f7f8fb;z-index:1000;flex-direction:column}}
.lesson.show{{display:flex}}
.l-head{{background:{main};color:#fff;padding:.7rem 1rem;display:flex;align-items:center;gap:.7rem;flex-shrink:0}}
.l-back{{background:none;border:none;color:#fff;font-size:1.3rem;cursor:pointer;padding:0;line-height:1;opacity:.9}}
.l-title{{flex:1;font-size:.92rem;font-weight:800;font-family:var(--font-serif);line-height:1.3;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.l-page-ind{{font-size:.78rem;font-weight:700;background:rgba(0,0,0,.18);padding:.18rem .55rem;border-radius:1rem;flex-shrink:0}}
.l-progress{{height:4px;background:rgba(0,0,0,.15);flex-shrink:0}}
.l-progress-bar{{height:100%;background:#fff;width:0%;transition:width .3s ease}}
.l-body{{flex:1;overflow-y:auto;padding:1.2rem 1.25rem 5rem;display:flex;flex-direction:column;gap:1rem;align-items:center}}
.l-page{{width:100%;max-width:680px;animation:slideIn .25s ease}}
@keyframes slideIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}

.l-page-title{{font-size:1.5rem;font-weight:800;color:{sub};margin-bottom:.5rem;font-family:var(--font-serif);line-height:1.3}}
.l-page-meta{{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.85rem}}
.l-page-meta .chip{{padding:.18rem .55rem;border-radius:1rem;font-size:.7rem;font-weight:700}}
.chip-prio-1{{background:#fee2e2;color:#991b1b}}
.chip-prio-2{{background:#fef3c7;color:#92400e}}
.chip-prio-3{{background:#dcfce7;color:#166534}}
.chip-prio-4{{background:#f1f5f9;color:#475569}}
.l-page-kw{{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:1.2rem}}
.l-page-kw span{{background:{main}22;color:{sub};border:1px solid {main}55;border-radius:1rem;padding:.18rem .65rem;font-size:.72rem;font-weight:700}}

.sec{{border-radius:.7rem;padding:1rem 1.1rem;line-height:1.65;margin-bottom:.85rem}}
.sec-summary{{background:{main}11;border-left:5px solid {main};font-size:.95rem;color:#111827;font-weight:600}}
.sec-bg{{background:#fef7ec;border-left:5px solid #d97706}}
.sec-expl{{background:#eef2ff;border-left:5px solid #4f46e5}}
.sec-why{{background:#ecfdf5;border-left:5px solid #059669}}
.sec-term{{background:#faf5ff;border-left:5px solid #7c3aed}}
.sec-link{{background:#fff7ed;border-left:5px solid #c2410c}}
.sec-mn{{background:linear-gradient(145deg,#fffef5 0%,#fff7d6 56%,{main}20 100%);color:#1f2937;font-weight:600;border:1.5px solid {main}33;border-left:5px solid {main};box-shadow:0 10px 26px {main}14}}
.sec-trap{{background:#fff1f2;border:1.5px solid #fda4af;border-left:5px solid #e11d48;color:#881337}}
.sec-src{{background:#fff;border:1.5px solid #e5e7eb;border-left:5px solid #475569}}
.sec-types{{background:#f0f9ff;border:1.5px solid #bae6fd;border-left:5px solid #0284c7}}
.sec-types .sec-label{{color:#075985}}
.types-caption{{font-size:.8rem;color:#334155;margin-bottom:.6rem;line-height:1.55}}
.types-list{{display:flex;flex-direction:column;gap:.55rem;counter-reset:tc}}
.type-item{{display:grid;grid-template-columns:2rem 1fr;gap:.55rem;align-items:start;background:#fff;border:1px solid #e0f2fe;border-radius:.7rem;padding:.7rem .78rem;counter-increment:tc;position:relative}}
.type-item::before{{content:counter(tc);display:inline-flex;align-items:center;justify-content:center;width:1.7rem;height:1.7rem;border-radius:.5rem;background:{main}16;color:{sub};font-size:.8rem;font-weight:800;line-height:1}}
.type-body{{min-width:0}}
.type-head{{display:flex;flex-wrap:wrap;gap:.35rem;align-items:center;margin-bottom:.2rem}}
.type-name{{font-size:.92rem;font-weight:800;color:#0f172a;font-family:var(--font-serif)}}
.type-en{{font-size:.72rem;color:#64748b;font-weight:700}}
.type-tier{{display:inline-flex;align-items:center;padding:.08rem .42rem;border-radius:999px;font-size:.62rem;font-weight:800;letter-spacing:.04em}}
.tier-strong{{background:#fee2e2;color:#991b1b}}
.tier-mid{{background:#fef3c7;color:#92400e}}
.tier-weak{{background:#dcfce7;color:#166534}}
.type-note{{font-size:.86rem;line-height:1.68;color:#334155;word-break:keep-all}}
.types-scale{{display:flex;align-items:center;gap:.45rem;margin-top:.65rem;padding:.5rem .7rem;background:rgba(255,255,255,.7);border:1px dashed #bae6fd;border-radius:.6rem;font-size:.72rem;color:#475569;font-weight:700}}
.types-scale .scale-arrow{{flex:1;height:6px;border-radius:999px;background:linear-gradient(90deg,#16a34a,#d97706,#dc2626)}}
.types-scale.reverse .scale-arrow{{background:linear-gradient(90deg,#dc2626,#d97706,#16a34a)}}
.sec-label{{font-size:.7rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.5rem}}
.sec-bg .sec-label{{color:#92400e}}
.sec-expl .sec-label{{color:#3730a3}}
.sec-why .sec-label{{color:#065f46}}
.sec-term .sec-label{{color:#5b21b6}}
.sec-link .sec-label{{color:#9a3412}}
.sec-mn .sec-label{{color:{sub}}}
.sec-trap .sec-label{{color:#9f1239}}
.sec-summary .sec-label{{color:{main}}}
.sec-src .sec-label{{color:#334155}}
.sec p{{font-size:.92rem;line-height:1.7}}
.sec-mn p{{font-size:.98rem}}
.fact-list{{display:flex;flex-direction:column;gap:.65rem}}
.fact-item{{background:rgba(255,255,255,.85);border:1px solid rgba(0,0,0,.06);border-radius:.85rem;padding:.78rem .85rem}}
.fact-term{{font-size:.86rem;font-weight:800;color:#111827;margin-bottom:.22rem}}
.fact-note{{font-size:.9rem;line-height:1.72;color:#374151;word-break:keep-all}}
.fact-link-label{{display:inline-flex;align-items:center;padding:.12rem .45rem;border-radius:999px;background:{main}14;color:{sub};font-size:.64rem;font-weight:800;letter-spacing:.04em;margin-bottom:.38rem}}
.src-list{{display:flex;flex-direction:column;gap:.5rem}}
.src-link{{display:flex;align-items:flex-start;gap:.45rem;text-decoration:none;color:#111827;background:#f9fafb;border:1px solid #e5e7eb;border-radius:.8rem;padding:.72rem .82rem;transition:border-color .15s,transform .15s}}
.src-link:hover{{border-color:{main};transform:translateY(-1px)}}
.src-bullet{{flex-shrink:0;color:{main};font-weight:800}}
.src-text{{font-size:.85rem;line-height:1.55}}
.src-host{{display:block;font-size:.72rem;color:#6b7280;margin-top:.1rem}}
.mn-list{{display:flex;flex-direction:column;gap:.55rem}}
.mn-line{{display:flex;align-items:flex-start;gap:.72rem;background:rgba(255,255,255,.82);border:1px solid {main}22;border-radius:.9rem;padding:.72rem .8rem .68rem;box-shadow:0 4px 12px rgba(0,0,0,.04)}}
.mn-picto{{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;width:1.6rem;height:1.6rem;border-radius:.45rem;background:{main}16;border:1px solid {main}26;font-size:.76rem;font-weight:800;line-height:1;color:{sub}}}
.mn-main{{display:flex;flex-direction:column;gap:.28rem;min-width:0}}
.mn-tag{{display:inline-flex;align-items:center;width:fit-content;padding:.12rem .45rem;border-radius:999px;background:{main}18;color:{sub};font-size:.64rem;font-weight:800;letter-spacing:.05em}}
.mn-text{{font-size:.95rem;line-height:1.76;color:#1f2937;word-break:keep-all}}
.mn-text strong{{color:{main};font-weight:800}}

.ctable{{width:100%;border-collapse:collapse;font-size:.82rem;background:#fff;border-radius:.5rem;overflow:hidden;margin-top:.4rem}}
.ctable th{{background:{main};color:#fff;padding:.55rem .65rem;text-align:left;font-weight:700;font-size:.78rem}}
.ctable td{{padding:.55rem .65rem;border-top:1px solid #e5e7eb;vertical-align:top;line-height:1.55}}
.ctable tr:nth-child(even) td{{background:#f9fafb}}

.done-page{{text-align:center;padding:2.5rem 1rem}}
.done-emoji{{font-size:4.5rem;margin-bottom:1rem;animation:pop .4s ease}}
@keyframes pop{{from{{transform:scale(0)}}80%{{transform:scale(1.2)}}to{{transform:scale(1)}}}}
.done-title{{font-size:1.5rem;font-weight:800;color:{sub};margin-bottom:.5rem;font-family:var(--font-serif)}}
.done-sub{{font-size:.95rem;color:#6b7280;margin-bottom:2rem}}
.done-actions{{display:flex;flex-direction:column;gap:.6rem;max-width:300px;margin:0 auto}}
.done-btn{{padding:.85rem 1.4rem;border-radius:.7rem;font-size:.95rem;font-weight:700;cursor:pointer;border:none;font-family:inherit;transition:all .15s}}
.done-btn-primary{{background:{main};color:#fff}}
.done-btn-primary:hover{{transform:translateY(-2px);box-shadow:0 4px 14px {main}55}}
.done-btn-sub{{background:#fff;color:{main};border:1.5px solid {main}}}
.done-btn-sub:hover{{background:{main}11}}

.l-foot{{position:fixed;bottom:0;left:0;right:0;background:#fff;padding:.7rem 1rem;display:flex;gap:.5rem;border-top:1px solid #e5e7eb;z-index:1010}}
.l-nav-btn{{flex:1;padding:.7rem;border-radius:.55rem;border:1.5px solid {main};background:#fff;color:{main};font-size:.88rem;font-weight:700;cursor:pointer;font-family:inherit;transition:all .15s}}
.l-nav-btn:hover:not(:disabled){{background:{main}11}}
.l-nav-btn:disabled{{opacity:.35;cursor:not-allowed}}
.l-nav-btn.primary{{background:{main};color:#fff;border-color:{main}}}
.l-nav-btn.primary:hover:not(:disabled){{background:{sub};border-color:{sub}}}
</style>
</head>
<body>

<div class="header">
  <a href="../" class="header-back">←</a>
  <span style="font-size:1.2rem">{subj["emoji"]}</span>
  <h1>{subj["id"]} &nbsp;{subj["title"]}</h1>
  <span class="header-cnt">{total}개 개념</span>
</div>

<div class="search-wrap">
  <input class="search" type="text" placeholder="🔍  개념 검색..." oninput="applyFilters()">
</div>

<div class="tabs" id="tab-bar">{tab_html}</div>
<div class="prio-bar">{prio_html}</div>

<div id="card-content">{sections_html}</div>

<!-- ── 레슨 모드 ── -->
<div class="lesson" id="lesson">
  <div class="l-head">
    <button class="l-back" onclick="exitLesson()">←</button>
    <div class="l-title" id="l-title"></div>
    <div class="l-page-ind" id="l-page-ind">1 / 1</div>
  </div>
  <div class="l-progress"><div class="l-progress-bar" id="l-progress-bar"></div></div>
  <div class="l-body" id="l-body"></div>
  <div class="l-foot">
    <button class="l-nav-btn" id="l-prev" onclick="prevPage()">← 이전</button>
    <button class="l-nav-btn primary" id="l-next" onclick="nextPage()">다음 →</button>
  </div>
</div>

<script>
const LESSONS = {json.dumps(lessons, ensure_ascii=False)};
const PRIO_LABEL = {{1:'최우선', 2:'중요', 3:'보통', 4:'보조'}};
let curTab = 'all';
let curPrio = 'all';
let curLessonIdx = -1;
let curPage = 0;
let pages = [];

function filterTab(btn, ch) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  curTab = ch;
  applyFilters();
}}

function filterPrio(btn) {{
  document.querySelectorAll('.pchip').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  curPrio = btn.dataset.prio;
  applyFilters();
}}

function applyFilters() {{
  const q = document.querySelector('.search').value.toLowerCase();
  document.querySelectorAll('.section-group').forEach(grp => {{
    const chOk = curTab === 'all' || grp.dataset.chapter === curTab;
    grp.classList.toggle('hidden', !chOk);
    if (chOk) {{
      let any = false;
      grp.querySelectorAll('.card').forEach(c => {{
        const qOk = !q || c.textContent.toLowerCase().includes(q);
        const pOk = curPrio === 'all' || c.dataset.prio === curPrio;
        const show = qOk && pOk;
        c.classList.toggle('hidden-card', !show);
        if (show) any = true;
      }});
      if (q || curPrio !== 'all') grp.classList.toggle('hidden', !any);
    }}
  }});
}}

function escHtml(str) {{
  return (str || '').replace(/[&<>"]/g, ch => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }})[ch]);
}}

function splitMnemonic(text) {{
  return (text || '')
    .replace(/\\r\\n/g, '\\n')
    .replace(/\\s+\\/\\s+/g, '\\n')
    .replace(/\\s+vs\\.\\s+/gi, '\\n')
    .replace(/\\s+→\\s+/g, ' → ')
    .replace(/\\s+↔\\s+/g, ' ↔ ')
    .replace(/\\.\\s+/g, '.\\n')
    .replace(/다\\.\\s+/g, '다.\\n')
    .replace(/됨\\.\\s+/g, '됨.\\n')
    .split(/\\n+/)
    .map(line => line.trim())
    .filter(Boolean);
}}

function mnemonicIcon(tag, text) {{
  if (tag) return '◈';
  if (text.includes('↔') || text.includes('=')) return '⇄';
  if (text.includes('→')) return '→';
  return '•';
}}

function renderParagraph(text) {{
  return escHtml(text || '').replace(/\\n/g, '<br>');
}}

function renderFactSection(label, secClass, items) {{
  if (!items || !items.length) return '';
  const html = items.map(item => `
    <div class="fact-item">
      ${{item.label ? `<div class="fact-link-label">${{escHtml(item.label)}}</div>` : ''}}
      <div class="fact-term">${{escHtml(item.term || '')}}</div>
      <div class="fact-note">${{renderParagraph(item.note || '')}}</div>
    </div>`).join('');
  return `<div class="sec ${{secClass}}"><div class="sec-label">${{label}}</div><div class="fact-list">${{html}}</div></div>`;
}}

function renderTypesSection(types) {{
  if (!types) return '';
  const items = Array.isArray(types) ? types : (types.items || []);
  if (!items.length) return '';
  const caption = !Array.isArray(types) && types.caption ? types.caption : '';
  const scale = !Array.isArray(types) ? (types.scale || '') : '';
  const scaleLabels = {{
    'strong-to-weak': ['강함','약함','reverse'],
    'weak-to-strong': ['약함','강함',''],
  }};
  const tierClass = {{
    'strong': 'tier-strong',
    'mid': 'tier-mid',
    'weak': 'tier-weak',
  }};
  const tierLabel = {{
    'strong': '강함',
    'mid': '중간',
    'weak': '약함',
  }};
  const rows = items.map(it => {{
    const tierCls = it.tier && tierClass[it.tier] ? tierClass[it.tier] : '';
    const tierLbl = it.tier && tierLabel[it.tier] ? tierLabel[it.tier] : (it.tier || '');
    return `
      <div class="type-item">
        <div class="type-body">
          <div class="type-head">
            <span class="type-name">${{escHtml(it.name || '')}}</span>
            ${{it.en ? `<span class="type-en">${{escHtml(it.en)}}</span>` : ''}}
            ${{tierCls ? `<span class="type-tier ${{tierCls}}">${{escHtml(tierLbl)}}</span>` : ''}}
          </div>
          <div class="type-note">${{renderParagraph(it.note || '')}}</div>
        </div>
      </div>`;
  }}).join('');
  let scaleHtml = '';
  if (scale && scaleLabels[scale]) {{
    const [L, R, rev] = scaleLabels[scale];
    scaleHtml = `<div class="types-scale ${{rev}}"><span>${{L}}</span><span class="scale-arrow"></span><span>${{R}}</span></div>`;
  }}
  return `<div class="sec sec-types">
    <div class="sec-label">🗂️ 유형</div>
    ${{caption ? `<div class="types-caption">${{renderParagraph(caption)}}</div>` : ''}}
    <div class="types-list">${{rows}}</div>
    ${{scaleHtml}}
  </div>`;
}}

function renderSourceSection(sources) {{
  if (!sources || !sources.length) return '';
  const html = sources.map(src => {{
    const hasUrl = !!src.url;
    let host = '';
    if (hasUrl) {{
      try {{ host = new URL(src.url).hostname.replace(/^www\\./, ''); }} catch (_err) {{ host = ''; }}
    }}
    const inner = `
        <span class="src-bullet">↗</span>
        <span class="src-text">
          ${{escHtml(src.title || src.url || '')}}
          ${{src.note ? `<span class="src-host">${{escHtml(src.note)}}</span>` : ''}}
          ${{!src.note && host ? `<span class="src-host">${{escHtml(host)}}</span>` : ''}}
        </span>`;
    if (hasUrl) {{
      return `<a class="src-link" href="${{escHtml(src.url)}}" target="_blank" rel="noreferrer">${{inner}}</a>`;
    }}
    return `<div class="src-link">${{inner}}</div>`;
  }}).join('');
  return `<div class="sec sec-src"><div class="sec-label">🔗 출처</div><div class="src-list">${{html}}</div></div>`;
}}

function renderMnemonic(text) {{
  const lines = splitMnemonic(text);
  if (!lines.length) return '';
  const html = lines.map(line => {{
    const m = line.match(/^【([^】]+)】\\s*(.*)$/);
    const tag = m ? m[1].trim() : '';
    const body = (m ? m[2] : line).trim();
    const safeBody = escHtml(body).replace(/'([^']+)'/g, '<strong>$1</strong>');
    return `
      <div class="mn-line">
        <span class="mn-picto">${{mnemonicIcon(tag, body)}}</span>
        <div class="mn-main">
          ${{tag ? `<span class="mn-tag">${{escHtml(tag)}}</span>` : ''}}
          <div class="mn-text">${{safeBody}}</div>
        </div>
      </div>`;
  }}).join('');
  return `<div class="sec sec-mn"><div class="sec-label">🧠 5초 암기</div><div class="mn-list">${{html}}</div></div>`;
}}

function buildPages(lesson) {{
  return [
    {{ type: 'learn', data: lesson }},
    {{ type: 'done',  data: lesson }},
  ];
}}

function renderPage() {{
  const body = document.getElementById('l-body');
  const page = pages[curPage];
  body.innerHTML = '';
  body.scrollTop = 0;

  const wrap = document.createElement('div');
  wrap.className = 'l-page';

  if (page.type === 'learn') {{
    const d = page.data;
    let h = '';
    h += `<h1 class="l-page-title">${{escHtml(d.title)}}</h1>`;
    const metaBits = [];
    if (d.priority && PRIO_LABEL[d.priority]) {{
      metaBits.push(`<span class="chip chip-prio-${{d.priority}}">P${{d.priority}} · ${{PRIO_LABEL[d.priority]}}</span>`);
    }}
    if (metaBits.length) h += `<div class="l-page-meta">${{metaBits.join('')}}</div>`;
    if (d.keywords && d.keywords.length) {{
      h += `<div class="l-page-kw">${{d.keywords.map(k => `<span>★ ${{escHtml(k)}}</span>`).join('')}}</div>`;
    }}
    if (d.summary)     h += `<div class="sec sec-summary"><div class="sec-label">📌 한 줄 요약</div><p>${{renderParagraph(d.summary)}}</p></div>`;
    if (d.background)  h += `<div class="sec sec-bg"><div class="sec-label">📜 배경·맥락</div><p>${{renderParagraph(d.background)}}</p></div>`;
    if (d.explanation) h += `<div class="sec sec-expl"><div class="sec-label">📖 핵심 설명</div><p>${{renderParagraph(d.explanation)}}</p></div>`;
    if (d.types)       h += renderTypesSection(d.types);
    if (d.why)         h += `<div class="sec sec-why"><div class="sec-label">🔍 왜 이렇게 됐나</div><p>${{renderParagraph(d.why)}}</p></div>`;
    if (d.term_focus && d.term_focus.length)   h += renderFactSection('🈶 용어·한자 풀이', 'sec-term', d.term_focus);
    if (d.connections && d.connections.length) h += renderFactSection('🧭 앞뒤 흐름 연결', 'sec-link', d.connections);
    if (d.mnemonic)    h += renderMnemonic(d.mnemonic);
    if (d.trap)        h += `<div class="sec sec-trap"><div class="sec-label">⚠️ 시험 함정</div><p>${{renderParagraph(d.trap)}}</p></div>`;
    if (d.table && d.table.length) {{
      const cols = Object.keys(d.table[0]);
      const head = cols.map(c => `<th>${{escHtml(c)}}</th>`).join('');
      const rows = d.table.map(r => '<tr>' + cols.map(c => `<td>${{escHtml(r[c] || '')}}</td>`).join('') + '</tr>').join('');
      h += `<div class="sec sec-summary" style="padding:0;background:transparent;border:none">
        <div class="sec-label" style="padding-left:.3rem;color:#6b7280;margin-bottom:.5rem">📊 정리표</div>
        <table class="ctable"><thead><tr>${{head}}</tr></thead><tbody>${{rows}}</tbody></table>
      </div>`;
    }}
    if (d.sources && d.sources.length) h += renderSourceSection(d.sources);
    wrap.innerHTML = h;
  }}
  else if (page.type === 'done') {{
    const d = page.data;
    const hasNext = curLessonIdx + 1 < LESSONS.length;
    wrap.innerHTML = `
      <div class="done-page">
        <div class="done-emoji">🎉</div>
        <div class="done-title">레슨 완료!</div>
        <div class="done-sub">${{escHtml(d.title)}}</div>
        <div class="done-actions">
          ${{hasNext ? '<button class="done-btn done-btn-primary" onclick="startLesson(' + (curLessonIdx + 1) + ')">다음 개념 →</button>' : ''}}
          <button class="done-btn done-btn-sub" onclick="exitLesson()">목록으로 돌아가기</button>
        </div>
      </div>`;
  }}

  body.appendChild(wrap);

  document.getElementById('l-page-ind').textContent = `${{curPage + 1}} / ${{pages.length}}`;
  document.getElementById('l-progress-bar').style.width = `${{((curPage + 1) / pages.length) * 100}}%`;
  document.getElementById('l-prev').disabled = curPage === 0;
  document.getElementById('l-next').disabled = curPage === pages.length - 1;
  document.getElementById('l-next').textContent = curPage === pages.length - 2 ? '완료 🎉' : '다음 →';
}}

function startLesson(idx) {{
  if (idx < 0 || idx >= LESSONS.length) return;
  curLessonIdx = idx;
  curPage = 0;
  pages = buildPages(LESSONS[idx]);
  document.getElementById('l-title').textContent = LESSONS[idx].title;
  document.getElementById('lesson').classList.add('show');
  document.body.style.overflow = 'hidden';
  renderPage();
}}

function exitLesson() {{
  document.getElementById('lesson').classList.remove('show');
  document.body.style.overflow = '';
  curLessonIdx = -1;
}}

function nextPage() {{ if (curPage < pages.length - 1) {{ curPage++; renderPage(); }} }}
function prevPage() {{ if (curPage > 0) {{ curPage--; renderPage(); }} }}

document.addEventListener('keydown', e => {{
  if (curLessonIdx < 0) return;
  if (e.key === 'ArrowLeft')  prevPage();
  if (e.key === 'ArrowRight') nextPage();
  if (e.key === 'Escape')     exitLesson();
}});
</script>
</body>
</html>'''


def index_page(stats: dict[str, int]) -> str:
    cards = ""
    for subj in SUBJECTS:
        cnt = stats.get(subj["id"], 0)
        status = f'{cnt}개 개념' if cnt else '준비 중'
        klass = '' if cnt else 'pending'
        href = f'./{subj["id"]}/' if cnt else '#'
        cards += (
            f'<a href="{href}" class="subj-card {klass}" '
            f'style="--main:{subj["main"]};--sub:{subj["sub"]}">'
            f'<div class="subj-emoji">{subj["emoji"]}</div>'
            f'<div class="subj-num">{subj["id"]}</div>'
            f'<div class="subj-title">{subj["title"]}</div>'
            f'<div class="subj-status">{status}</div>'
            f'</a>'
        )
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TOPCIT 레슨</title>
<style>
:root{{--font-sans:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,sans-serif;--font-serif:"NanumMyeongjo","Nanum Myeongjo","Batang","Apple SD Gothic Neo",serif}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font-sans);background:#f7f8fb;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:2.5rem 1.25rem;color:#1f2937}}
h1{{font-size:1.6rem;font-weight:800;margin-bottom:.4rem;font-family:var(--font-serif);text-align:center}}
.sub{{color:#6b7280;font-size:.88rem;margin-bottom:2rem;text-align:center}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.85rem;width:100%;max-width:780px}}
@media(min-width:600px){{.grid{{grid-template-columns:repeat(3,1fr)}}}}
.subj-card{{background:#fff;border-radius:.85rem;padding:1.3rem 1rem;text-decoration:none;border:2px solid var(--main);transition:all .18s;display:flex;flex-direction:column;gap:.2rem;position:relative;overflow:hidden;color:inherit}}
.subj-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:var(--main)}}
.subj-card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,.12)}}
.subj-card.pending{{opacity:.45;cursor:not-allowed;border-color:#bbb;pointer-events:none}}
.subj-card.pending::before{{background:#bbb}}
.subj-emoji{{font-size:1.8rem;margin-bottom:.15rem}}
.subj-num{{font-size:.7rem;font-weight:800;color:var(--sub);letter-spacing:.07em}}
.subj-title{{font-size:.95rem;font-weight:800;line-height:1.35;font-family:var(--font-serif)}}
.subj-status{{font-size:.7rem;color:#6b7280;margin-top:.3rem}}
.subj-card:not(.pending) .subj-status{{color:var(--main);font-weight:700}}
.back{{margin-bottom:1.5rem;font-size:.85rem;color:#6b7280;text-decoration:none}}
.back:hover{{color:#111827}}
.footer{{margin-top:3rem;font-size:.75rem;color:#9ca3af;text-align:center;line-height:1.6}}
</style>
</head>
<body>
<a href="../" class="back">← 메인으로</a>
<h1>📘 TOPCIT 레슨</h1>
<p class="sub">6과목 개념 학습 — 카드 → 풀스크린 레슨</p>
<div class="grid">{cards}</div>
<div class="footer">총 {sum(stats.values())}개 개념</div>
</body>
</html>'''


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== TOPCIT 레슨 뷰어 생성 ===\n")
    stats = {}
    for subj in SUBJECTS:
        data = load_json(subj["id"])
        if data is None:
            print(f"[스킵] {subj['id']} {subj['title']} — JSON 없음")
            continue
        out_dir = OUT_DIR / subj["id"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(subject_page(subj, data), encoding="utf-8")
        cnt = sum(len(s["concepts"]) for ch in data["chapters"] for s in ch["sections"])
        stats[subj["id"]] = cnt
        print(f"✓ {subj['id']}/index.html  ({cnt}개 개념)")

    (OUT_DIR / "index.html").write_text(index_page(stats), encoding="utf-8")
    print(f"\n✓ index.html  (총 {sum(stats.values())}개 개념)")
    print(f"\n출력: {OUT_DIR}")
