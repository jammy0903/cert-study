"""
정보처리기사_실기_출제현황_뜻포함.md → PDF (B&W 프린트 최적화).
docx 버전과 동일한 스타일(●/◐/○ 심볼, 굵기/이탤릭, 회색 음영)을 HTML+CSS로 구성해 weasyprint로 출력.
"""
import re
import html
from pathlib import Path

from weasyprint import HTML, CSS


SRC = Path('/home/jammy/projects/cert-study/정보처리기사_실기_출제현황_뜻포함.md')
OUT = Path('/home/jammy/projects/cert-study/정보처리기사_실기_출제현황_뜻포함_BW.pdf')


CSS_TEXT = """
@page {
    size: A4 landscape;
    margin: 1.5cm 1.8cm;
    @bottom-center { content: counter(page) " / " counter(pages); font-size: 8pt; color: #666; }
}
* { box-sizing: border-box; }
body {
    font-family: "NanumBarunGothic", "Nanum Gothic", "NanumGothic", sans-serif;
    font-size: 10pt;
    color: #000;
    line-height: 1.45;
}
h1.doc-title { font-size: 20pt; font-weight: 700; text-align: center; margin: 0 0 4pt 0; }
p.subtitle { font-size: 11pt; text-align: center; color: #666; margin: 0 0 10pt 0; }

table.legend {
    width: 100%; border-collapse: collapse; margin-bottom: 10pt;
    table-layout: fixed;
}
table.legend td {
    border: 1.5pt solid #555; padding: 8pt 10pt; text-align: center; vertical-align: middle;
    width: 33.3%;
}
table.legend .l-label { font-size: 11pt; display: block; }
table.legend .l-desc { font-size: 8.5pt; color: #666; display: block; margin-top: 2pt; }
table.legend .l-bold   { font-weight: 700; }
table.legend .l-italic { font-style: italic; }

h1.sec { font-size: 15pt; font-weight: 700; margin: 14pt 0 5pt 0;
         border-bottom: 3pt double #000; padding-bottom: 2pt; page-break-after: avoid; }
h2.sub { font-size: 12pt; font-weight: 700; margin: 9pt 0 3pt 0;
         border-bottom: 1pt solid #555; padding-bottom: 1.5pt; page-break-after: avoid; }
h3.sub2{ font-size: 11pt; font-weight: 700; color: #333; margin: 7pt 0 3pt 0; page-break-after: avoid; }

blockquote {
    background: #f5f5f5; border-left: 4pt solid #000;
    margin: 4pt 0; padding: 8pt 12pt; font-size: 10pt; color: #333;
}

p { margin: 2pt 0; }
ul, ol { margin: 2pt 0 4pt 0; padding-left: 18pt; }
li { margin: 1pt 0; }

table.data {
    width: 100%; border-collapse: collapse;
    table-layout: fixed; margin: 3pt 0 6pt 0;
    page-break-inside: auto;
}
table.data thead { display: table-header-group; }
table.data tr { page-break-inside: avoid; }
table.data th {
    background: #222; color: #fff; font-weight: 700;
    font-size: 10pt; padding: 5pt 7pt; text-align: center;
    border: 0.5pt solid #fff;
}
table.data td {
    border: 0.5pt solid #bbb; padding: 3.5pt 7pt;
    font-size: 9.5pt; vertical-align: middle;
}
tr.alt td { background: #f0f0f0; }
tr.hit td { background: #e4e4e4; }
td.status { text-align: center; }

/* 상태별 */
.sym { font-weight: 700; }
.hit  .item-name   { font-weight: 700; }
.hit  .status      { font-weight: 700; }
.weak .item-name   { font-weight: 400; }
.miss .item-name   { font-style: italic; color: #333; }
.miss .status      { font-style: italic; color: #666; }

/* 열폭 프리셋 */
table.cols-2 col:nth-child(1) { width: 23%; }
table.cols-2 col:nth-child(2) { width: 77%; }
table.cols-3 col:nth-child(1) { width: 18%; }
table.cols-3 col:nth-child(2) { width: 23%; }
table.cols-3 col:nth-child(3) { width: 59%; }
table.cols-4 col:nth-child(1) { width: 18%; }
table.cols-4 col:nth-child(2) { width: 23%; }
table.cols-4 col:nth-child(3) { width: 49%; }
table.cols-4 col:nth-child(4) { width: 10%; }
/* 중요도 컬럼 포함된 4열 표 */
table.cols-4.imp col:nth-child(1) { width: 9%; }
table.cols-4.imp col:nth-child(2) { width: 21%; }
table.cols-4.imp col:nth-child(3) { width: 21%; }
table.cols-4.imp col:nth-child(4) { width: 49%; }
td.importance { text-align: center; font-weight: 700; white-space: nowrap; }
"""


# ─── 상태 분류 (docx와 동일) ───
def classify_status(val: str):
    v = val.strip()
    if not v:
        return '', 'none'
    if v == '미출제':
        return '○', 'miss'
    if v.startswith('약출제'):
        return '◐', 'weak'
    return '●', 'hit'


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


# ─── 파서 (make_docx_bw.py와 동일 로직) ───
def parse_md(text):
    lines = text.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith('# '):
            blocks.append(('h1', stripped[2:].strip())); i += 1; continue
        if stripped.startswith('## '):
            blocks.append(('h2', stripped[3:].strip())); i += 1; continue
        if stripped.startswith('### '):
            blocks.append(('h3', stripped[4:].strip())); i += 1; continue
        if re.match(r'^-{3,}$', stripped):
            blocks.append(('hr',)); i += 1; continue
        if stripped.startswith('>'):
            qlines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                qlines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            blocks.append(('quote', qlines)); continue
        if stripped.startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|?\s*:?-+', lines[i + 1]):
            header = [c.strip() for c in stripped.strip('|').split('|')]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if len(cells) < len(header):
                    cells += [''] * (len(header) - len(cells))
                elif len(cells) > len(header):
                    cells = cells[:len(header)]
                rows.append(cells)
                i += 1
            blocks.append(('table', header, rows)); continue
        if re.match(r'^\d+\.\s', stripped):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                items.append(re.sub(r'^\d+\.\s', '', lines[i].strip()))
                i += 1
            blocks.append(('ol', items)); continue
        if stripped.startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            blocks.append(('ul', items)); continue
        blocks.append(('para', stripped)); i += 1
    return blocks


def detect_status_col(headers):
    for i, h in enumerate(headers):
        if h.strip() in ('상태', '출제 이력'):
            return i
    return None


def render_table(headers, rows):
    n = len(headers)
    status_col = detect_status_col(headers)
    has_importance = len(headers) >= 1 and headers[0].strip() == '중요도'
    item_col = 0
    for idx, h in enumerate(headers):
        if h.strip() == '항목':
            item_col = idx
            break

    cls_extra = ' imp' if has_importance else ''
    out = [f'<table class="data cols-{n}{cls_extra}">']
    out.append('<colgroup>' + ''.join('<col/>' for _ in range(n)) + '</colgroup>')
    out.append('<thead><tr>')
    for h in headers:
        out.append(f'<th>{inline_md(h)}</th>')
    out.append('</tr></thead><tbody>')

    for ri, row in enumerate(rows):
        sym, cls = '', 'none'
        if status_col is not None and status_col < len(row):
            sym, cls = classify_status(row[status_col])
        tr_cls = cls if cls in ('hit', 'weak', 'miss') else ('alt' if ri % 2 else '')
        out.append(f'<tr class="{tr_cls}">')
        for ci, cell in enumerate(row):
            content = inline_md(cell)
            if has_importance and ci == 0:
                out.append(f'<td class="importance">{content}</td>')
                continue
            if ci == item_col and sym:
                content = f'<span class="sym">{sym}</span> <span class="item-name">{content}</span>'
                out.append(f'<td>{content}</td>')
                continue
            if ci == status_col:
                out.append(f'<td class="status">{content}</td>')
                continue
            out.append(f'<td>{content}</td>')
        out.append('</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)


def render_list(items, ordered):
    tag = 'ol' if ordered else 'ul'
    parts = [f'<{tag}>']
    for it in items:
        parts.append(f'<li>{inline_md(it)}</li>')
    parts.append(f'</{tag}>')
    return '\n'.join(parts)


def build_html(blocks):
    body = []
    # 타이틀 + 부제
    body.append('<h1 class="doc-title">정보처리기사 실기 출제현황 · 뜻 포함판</h1>')
    body.append('<p class="subtitle">2020~2025 기출 분석 · 2026 쪽집게 전략 포함</p>')
    # 범례
    body.append("""
<table class="legend"><tr>
  <td><span class="l-label l-bold">● 출제됨</span><span class="l-desc">정답 칸에 직접 등장 (굵은 글씨)</span></td>
  <td><span class="l-label">◐ 약출제</span><span class="l-desc">문제/보기/해설에서만 확인 (일반)</span></td>
  <td><span class="l-label l-italic">○ 미출제</span><span class="l-desc">보유 기출 기준 미확인 (기울임)</span></td>
</tr></table>
""")

    skip_first_h1 = True
    for b in blocks:
        kind = b[0]
        if kind == 'h1':
            if skip_first_h1:
                skip_first_h1 = False
                continue
            body.append(f'<h1 class="sec">{inline_md(b[1])}</h1>')
        elif kind == 'h2':
            body.append(f'<h1 class="sec">{inline_md(b[1])}</h1>')
        elif kind == 'h3':
            body.append(f'<h2 class="sub">{inline_md(b[1])}</h2>')
        elif kind == 'hr':
            body.append('<div style="height:4pt;"></div>')
        elif kind == 'quote':
            inner = '<br/>'.join(inline_md(l) for l in b[1] if l)
            body.append(f'<blockquote>{inner}</blockquote>')
        elif kind == 'para':
            body.append(f'<p>{inline_md(b[1])}</p>')
        elif kind == 'ol':
            body.append(render_list(b[1], ordered=True))
        elif kind == 'ul':
            body.append(render_list(b[1], ordered=False))
        elif kind == 'table':
            body.append(render_table(b[1], b[2]))

    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"/>
<title>정보처리기사 실기 출제현황</title></head>
<body>
{''.join(body)}
</body></html>"""


md_text = SRC.read_text(encoding='utf-8')
blocks = parse_md(md_text)
html_str = build_html(blocks)

HTML(string=html_str).write_pdf(OUT, stylesheets=[CSS(string=CSS_TEXT)])
print(f'✔ 저장 완료: {OUT}')
