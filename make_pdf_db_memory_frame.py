from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path("/home/jammy/projects/cert-study")
OUT = ROOT / "output/pdf/정보처리기사_실기_3단원_DB_암기프레임.pdf"

NANUM_REGULAR = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
NANUM_BOLD = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
SYMBOL_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SYMBOL_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 10 * mm
GAP = 5.5 * mm
CARD_W = (PAGE_W - 2 * MARGIN - GAP) / 2
CARD_H = 75 * mm


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("NanumGothic", NANUM_REGULAR))
    pdfmetrics.registerFont(TTFont("NanumGothic-Bold", NANUM_BOLD))
    pdfmetrics.registerFontFamily(
        "NanumGothic",
        normal="NanumGothic",
        bold="NanumGothic-Bold",
    )
    pdfmetrics.registerFont(TTFont("DejaVuSans", SYMBOL_REGULAR))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", SYMBOL_BOLD))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="NanumGothic-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#13233d"),
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["BodyText"],
            fontName="NanumGothic",
            fontSize=9.4,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#546170"),
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="NanumGothic",
            fontSize=8.8,
            leading=11.2,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#22303c"),
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="NanumGothic",
            fontSize=8.1,
            leading=10,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#22303c"),
        ),
        "card_title": ParagraphStyle(
            "card_title",
            parent=base["Heading2"],
            fontName="NanumGothic-Bold",
            fontSize=11.5,
            leading=13,
            alignment=TA_LEFT,
            textColor=colors.white,
        ),
        "pill": ParagraphStyle(
            "pill",
            parent=base["BodyText"],
            fontName="NanumGothic-Bold",
            fontSize=8.4,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#203040"),
        ),
    }


def draw_paragraph(c: canvas.Canvas, text: str, style: ParagraphStyle, x: float, top: float, width: float) -> float:
    para = Paragraph(text, style)
    _, h = para.wrap(width, 1000)
    para.drawOn(c, x, top - h)
    return top - h


def draw_round_box(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill: colors.Color, stroke: colors.Color, radius: float = 10) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def draw_card(c: canvas.Canvas, title: str, x: float, y: float, w: float, h: float, header: colors.Color, body: colors.Color, border: colors.Color) -> tuple[float, float, float, float]:
    shadow = colors.Color(0, 0, 0, alpha=0.08)
    c.setFillColor(shadow)
    c.setStrokeColor(shadow)
    c.roundRect(x + 2.2, y - 2.2, w, h, 12, stroke=0, fill=1)

    draw_round_box(c, x, y, w, h, body, border, 12)
    c.setFillColor(header)
    c.setStrokeColor(header)
    c.roundRect(x, y + h - 18 * mm, w, 18 * mm, 12, stroke=0, fill=1)
    c.rect(x, y + h - 18 * mm, w, 8 * mm, stroke=0, fill=1)

    c.setFont("NanumGothic-Bold", 11.5)
    c.setFillColor(colors.white)
    c.drawString(x + 5 * mm, y + h - 11.5 * mm, title)

    return x + 4.5 * mm, y + 4.5 * mm, w - 9 * mm, h - 24 * mm


def begin_clip(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    c.saveState()
    path = c.beginPath()
    path.roundRect(x, y, w, h, 7)
    c.clipPath(path, stroke=0, fill=0)


def end_clip(c: canvas.Canvas) -> None:
    c.restoreState()


def draw_chip(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, body: str, fill: str, stroke: str) -> None:
    draw_round_box(c, x, y, w, h, colors.HexColor(fill), colors.HexColor(stroke), 6)
    c.setFillColor(colors.HexColor("#183255"))
    c.setFont("NanumGothic-Bold", 8.0)
    c.drawCentredString(x + w / 2, y + h - 8.6, title)
    c.setFont("NanumGothic", 7.6)
    c.drawCentredString(x + w / 2, y + 4.0, body)


def draw_title_area(c: canvas.Canvas, st: dict[str, ParagraphStyle]) -> float:
    top = PAGE_H - MARGIN
    draw_paragraph(c, "정보처리기사 실기 3단원 DB 암기 프레임", st["title"], MARGIN, top, PAGE_W - 2 * MARGIN)
    top -= 9 * mm
    draw_paragraph(
        c,
        "문제를 보면 먼저 어느 덩어리인지 자르고, 그 다음 답을 붙이게 만드는 1페이지 요약",
        st["subtitle"],
        MARGIN,
        top,
        PAGE_W - 2 * MARGIN,
    )
    top -= 7 * mm

    ribbon_y = top - 8 * mm
    draw_round_box(
        c,
        MARGIN,
        ribbon_y,
        PAGE_W - 2 * MARGIN,
        11 * mm,
        colors.HexColor("#eef4ff"),
        colors.HexColor("#9bb7e0"),
        8,
    )
    c.setFillColor(colors.HexColor("#183b74"))
    c.setFont("NanumGothic-Bold", 10.2)
    c.drawCentredString(
        PAGE_W / 2,
        ribbon_y + 4.1 * mm,
        "먼저 분류: 테이블 구조 -> ERD 그림 -> 연산 -> 트랜잭션",
    )
    return ribbon_y - 4 * mm


def draw_table_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    cx, cy, cw, ch = draw_card(
        c,
        "1. 테이블 자체",
        x,
        y,
        w,
        h,
        colors.HexColor("#2f68c4"),
        colors.HexColor("#f8fbff"),
        colors.HexColor("#9dbce9"),
    )

    begin_clip(c, cx, cy, cw, ch)
    draw_paragraph(c, "<b>행 / 열 / 개수 / 구조</b>를 묻는 문제", st["body"], cx, y + h - 22 * mm, cw)

    chip_y1 = y + h - 40 * mm
    chip_gap = 2.3 * mm
    chip_w = (cw - 2 * chip_gap) / 3
    chip_h = 13.2 * mm
    fills = ["#e7f1ff", "#edf5ff", "#f3f8ff"]
    stroke = "#a9c4e8"
    chips = [
        ("릴레이션", "테이블"),
        ("튜플", "행"),
        ("속성", "열"),
        ("도메인", "값 범위"),
        ("카디널리티", "행 개수"),
        ("차수", "열 개수"),
        ("스키마", "설계도"),
        ("인스턴스", "실데이터"),
        ("식별자", "행 구별 키"),
    ]

    for idx, (title, body) in enumerate(chips):
        row = idx // 3
        col = idx % 3
        px = cx + col * (chip_w + chip_gap)
        py = chip_y1 - row * (chip_h + 2.1 * mm)
        draw_chip(c, px, py, chip_w, chip_h, title, body, fills[col], stroke)

    note_y = cy + 1.8 * mm
    draw_round_box(c, cx, note_y, cw, 9.2 * mm, colors.HexColor("#eef4ff"), colors.HexColor("#abc2e6"), 7)
    c.setFillColor(colors.HexColor("#183b74"))
    c.setFont("NanumGothic-Bold", 7.8)
    c.drawCentredString(cx + cw / 2, note_y + 3.3 * mm, "행=튜플 / 열=속성 / 행 개수=카디널리티 / 열 개수=차수")
    end_clip(c)


def draw_erd_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    cx, cy, cw, ch = draw_card(
        c,
        "2. 그림(ERD)",
        x,
        y,
        w,
        h,
        colors.HexColor("#2f9962"),
        colors.HexColor("#f7fdf9"),
        colors.HexColor("#a9d8bd"),
    )

    chip_w = 39 * mm
    draw_round_box(c, x + w - chip_w - 5 * mm, y + h - 29 * mm, chip_w, 8 * mm, colors.HexColor("#e2f5e8"), colors.HexColor("#9bd0aa"), 7)
    c.setFillColor(colors.HexColor("#1d6b43"))
    c.setFont("NanumGothic-Bold", 8.6)
    c.drawCentredString(x + w - chip_w / 2 - 5 * mm, y + h - 24.1 * mm, "사물 - 사이 - 특징")

    base_y = y + h - 50 * mm
    entity_x = cx + 3 * mm
    entity_y = base_y
    c.setFillColor(colors.HexColor("#dff2e7"))
    c.setStrokeColor(colors.HexColor("#5aa278"))
    c.roundRect(entity_x, entity_y, 30 * mm, 12 * mm, 4, stroke=1, fill=1)
    c.setFont("NanumGothic-Bold", 9)
    c.setFillColor(colors.HexColor("#1f5137"))
    c.drawCentredString(entity_x + 15 * mm, entity_y + 4.2 * mm, "개체")

    diamond_cx = entity_x + 49 * mm
    diamond_cy = entity_y + 6 * mm
    path = c.beginPath()
    path.moveTo(diamond_cx, diamond_cy + 7 * mm)
    path.lineTo(diamond_cx + 12 * mm, diamond_cy)
    path.lineTo(diamond_cx, diamond_cy - 7 * mm)
    path.lineTo(diamond_cx - 12 * mm, diamond_cy)
    path.close()
    c.setFillColor(colors.HexColor("#e7f7ee"))
    c.setStrokeColor(colors.HexColor("#5aa278"))
    c.drawPath(path, stroke=1, fill=1)
    c.setFont("NanumGothic-Bold", 8.8)
    c.setFillColor(colors.HexColor("#1f5137"))
    c.drawCentredString(diamond_cx, diamond_cy - 1.5, "관계")

    oval_x = entity_x + 77 * mm
    oval_y = entity_y + 0.5 * mm
    c.setFillColor(colors.HexColor("#edf9f2"))
    c.setStrokeColor(colors.HexColor("#5aa278"))
    c.ellipse(oval_x, oval_y, oval_x + 32 * mm, oval_y + 11 * mm, stroke=1, fill=1)
    c.setFont("NanumGothic-Bold", 8.8)
    c.setFillColor(colors.HexColor("#1f5137"))
    c.drawCentredString(oval_x + 16 * mm, oval_y + 3.6 * mm, "속성")

    c.setStrokeColor(colors.HexColor("#6eb186"))
    c.setLineWidth(1)
    c.line(entity_x + 30 * mm, entity_y + 6 * mm, diamond_cx - 12 * mm, diamond_cy)
    c.line(diamond_cx + 12 * mm, diamond_cy, oval_x, oval_y + 5.5 * mm)

    text_top = entity_y - 5 * mm
    items = [
        "<b>개체</b> = 관리 대상 그 자체",
        "<b>관계</b> = 개체와 개체 사이 연결",
        "<b>속성</b> = 개체나 관계의 특징",
        "<b>개체집합</b> = 같은 종류 개체들의 모음",
        "<b>관계집합 속성</b> = 관계 자체에 붙는 속성",
        "<b>피터첸 표기법</b> = ERD 기호 체계",
    ]
    for item in items:
        text_top = draw_paragraph(c, item, st["small"], cx, text_top, cw)
        text_top -= 0.7 * mm


def draw_symbol_chip(c: canvas.Canvas, x: float, y: float, w: float, h: float, symbol: str, label: str, hint: str, fill: colors.Color, stroke: colors.Color) -> None:
    draw_round_box(c, x, y, w, h, fill, stroke, 8)
    c.setFillColor(colors.HexColor("#2d3136"))
    c.setFont("DejaVuSans-Bold", 16)
    c.drawCentredString(x + w / 2, y + h - 12.5, symbol)
    c.setFont("NanumGothic-Bold", 8.35)
    c.drawCentredString(x + w / 2, y + h - 24.5, label)
    c.setFont("NanumGothic", 7.8)
    c.drawCentredString(x + w / 2, y + 6.5, hint)


def draw_algebra_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    cx, cy, cw, ch = draw_card(
        c,
        "3. 연산",
        x,
        y,
        w,
        h,
        colors.HexColor("#d07c1d"),
        colors.HexColor("#fffaf4"),
        colors.HexColor("#e9c08e"),
    )

    pill_w = (cw - 4 * mm) / 2
    draw_round_box(c, cx, y + h - 31 * mm, pill_w, 8.5 * mm, colors.HexColor("#ffe8ca"), colors.HexColor("#ebb56d"), 8)
    draw_round_box(c, cx + pill_w + 4 * mm, y + h - 31 * mm, pill_w, 8.5 * mm, colors.HexColor("#fff1da"), colors.HexColor("#ebb56d"), 8)
    c.setFillColor(colors.HexColor("#874d00"))
    c.setFont("NanumGothic-Bold", 8.8)
    c.drawCentredString(cx + pill_w / 2, y + h - 25.8 * mm, "관계대수 = 절차적")
    c.drawCentredString(cx + pill_w + 4 * mm + pill_w / 2, y + h - 25.8 * mm, "관계해석 = 비절차적")

    chip_gap = 3 * mm
    chip_w = (cw - chip_gap * 3) / 4
    chip_h = 18 * mm
    row1_y = y + h - 55 * mm
    row2_y = row1_y - chip_h - 3.2 * mm
    fills = [
        colors.HexColor("#fff1d9"),
        colors.HexColor("#fff3de"),
        colors.HexColor("#fff0d3"),
        colors.HexColor("#fff4e3"),
    ]
    stroke = colors.HexColor("#e0b779")

    chips = [
        ("σ", "선택", "행 뽑기"),
        ("π", "프로젝션", "열 뽑기"),
        ("⋈", "조인", "붙이기"),
        ("×", "카티션", "모든 조합"),
        ("∪", "합집합", "합치기"),
        ("-", "차집합", "빼기"),
        ("÷", "디비전", "모두 만족"),
    ]
    for idx, chip in enumerate(chips[:4]):
        draw_symbol_chip(c, cx + idx * (chip_w + chip_gap), row1_y, chip_w, chip_h, chip[0], chip[1], chip[2], fills[idx % len(fills)], stroke)
    for idx, chip in enumerate(chips[4:]):
        draw_symbol_chip(c, cx + idx * (chip_w + chip_gap), row2_y, chip_w, chip_h, chip[0], chip[1], chip[2], fills[(idx + 1) % len(fills)], stroke)

    note_x = cx + 3 * (chip_w + chip_gap)
    note_w = chip_w
    draw_round_box(c, note_x, row2_y, note_w, chip_h, colors.HexColor("#fff8ec"), colors.HexColor("#edd0a2"), 8)
    draw_paragraph(
        c,
        "<b>기호 문제</b>는<br/>모양까지 같이 외워야 바로 풀린다",
        st["small"],
        note_x + 4,
        row2_y + chip_h - 4,
        note_w - 8,
    )


def draw_transaction_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    cx, cy, cw, ch = draw_card(
        c,
        "4. 트랜잭션",
        x,
        y,
        w,
        h,
        colors.HexColor("#c64a4a"),
        colors.HexColor("#fff8f8"),
        colors.HexColor("#e4afaf"),
    )

    pill_gap = 2.4 * mm
    pill_w = (cw - pill_gap * 3) / 4
    acid_y = y + h - 31 * mm
    acid_h = 10 * mm
    acid = [
        ("A", "Atomicity", "전부 or 0", "#ffe2e2"),
        ("C", "Consistency", "전후 일관", "#ffe8dc"),
        ("I", "Isolation", "간섭 X", "#ffece2"),
        ("D", "Durability", "끝난 결과 남음", "#ffe4e4"),
    ]
    for idx, (abbr, name, memo, color_hex) in enumerate(acid):
        px = cx + idx * (pill_w + pill_gap)
        draw_round_box(c, px, acid_y, pill_w, acid_h, colors.HexColor(color_hex), colors.HexColor("#de9c9c"), 8)
        c.setFillColor(colors.HexColor("#8b2626"))
        c.setFont("NanumGothic-Bold", 8.8)
        c.drawCentredString(px + pill_w / 2, acid_y + 6.2 * mm, f"{abbr}  {name}")
        c.setFont("NanumGothic", 7.3)
        c.drawCentredString(px + pill_w / 2, acid_y + 2.1 * mm, memo)

    box_y = y + 9 * mm
    box_h = 26 * mm
    box_w = (cw - 4 * mm) / 2

    draw_round_box(c, cx, box_y, box_w, box_h, colors.HexColor("#fff0f0"), colors.HexColor("#dfb2b2"), 8)
    draw_round_box(c, cx + box_w + 4 * mm, box_y, box_w, box_h, colors.HexColor("#fff3f3"), colors.HexColor("#dfb2b2"), 8)

    c.setFillColor(colors.HexColor("#8b2626"))
    c.setFont("NanumGothic-Bold", 9.2)
    c.drawString(cx + 4, box_y + box_h - 11, "회복")
    c.drawString(cx + box_w + 4 * mm + 4, box_y + box_h - 11, "병행제어")

    left_items = [
        "Rollback = 이전 상태로 되돌리기",
        "REDO = 커밋된 것 다시 반영",
        "UNDO = 잘못된 것 취소",
        "즉각 갱신 / 지연 갱신",
    ]
    right_items = [
        "Locking = 잠그기",
        "낙관적 검증 = 끝에서 검사",
        "타임스탬프 순서 = 시간표 기준",
        "MVCC = 버전 여러 개 유지",
    ]

    left_top = box_y + box_h - 15
    for item in left_items:
        left_top = draw_paragraph(c, item, st["small"], cx + 4, left_top, box_w - 8)
        left_top -= 1.0

    right_x = cx + box_w + 4 * mm + 4
    right_top = box_y + box_h - 15
    for item in right_items:
        right_top = draw_paragraph(c, item, st["small"], right_x, right_top, box_w - 8)
        right_top -= 1.0


def build_pdf() -> None:
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    st = styles()
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
    c.setTitle("정보처리기사 실기 3단원 DB 암기 프레임")
    c.setAuthor("Codex")

    c.setFillColor(colors.HexColor("#fffdf8"))
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    title_bottom = draw_title_area(c, st)

    row1_y = title_bottom - CARD_H
    row2_y = MARGIN
    col1_x = MARGIN
    col2_x = MARGIN + CARD_W + GAP

    draw_table_card(c, col1_x, row1_y, CARD_W, CARD_H, st)
    draw_erd_card(c, col2_x, row1_y, CARD_W, CARD_H, st)
    draw_algebra_card(c, col1_x, row2_y, CARD_W, CARD_H, st)
    draw_transaction_card(c, col2_x, row2_y, CARD_W, CARD_H, st)

    c.setFont("NanumGothic-Bold", 8.3)
    c.setFillColor(colors.HexColor("#6b7683"))
    c.drawRightString(PAGE_W - MARGIN, 6.5 * mm, "문제를 보면 먼저 어느 카드인지 분류")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build_pdf()
