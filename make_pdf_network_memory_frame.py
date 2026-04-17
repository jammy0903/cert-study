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
OUT = ROOT / "output/pdf/정보처리기사_실기_4단원_네트워크_암기프레임.pdf"

NANUM_REGULAR = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
NANUM_BOLD = "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
SYMBOL_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SYMBOL_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAGE_W, PAGE_H = landscape(A4)
MARGIN = 8.5 * mm
GAP_X = 4.2 * mm
GAP_Y = 4.2 * mm
CARD_W = (PAGE_W - 2 * MARGIN - 2 * GAP_X) / 3
CARD_H = 65.5 * mm


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("NanumGothic", NANUM_REGULAR))
    pdfmetrics.registerFont(TTFont("NanumGothic-Bold", NANUM_BOLD))
    pdfmetrics.registerFontFamily("NanumGothic", normal="NanumGothic", bold="NanumGothic-Bold")
    pdfmetrics.registerFont(TTFont("DejaVuSans", SYMBOL_REGULAR))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", SYMBOL_BOLD))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="NanumGothic-Bold",
            fontSize=19,
            leading=23,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#11243d"),
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["BodyText"],
            fontName="NanumGothic",
            fontSize=9.1,
            leading=11.4,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#566371"),
        ),
        "card_title": ParagraphStyle(
            "card_title",
            parent=base["Heading2"],
            fontName="NanumGothic-Bold",
            fontSize=10.6,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.white,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="NanumGothic",
            fontSize=7.85,
            leading=9.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#23303d"),
        ),
        "body_bold": ParagraphStyle(
            "body_bold",
            parent=base["BodyText"],
            fontName="NanumGothic-Bold",
            fontSize=7.85,
            leading=9.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#23303d"),
        ),
        "tiny_center": ParagraphStyle(
            "tiny_center",
            parent=base["BodyText"],
            fontName="NanumGothic",
            fontSize=7.1,
            leading=8.4,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#23303d"),
        ),
        "tiny_bold_center": ParagraphStyle(
            "tiny_bold_center",
            parent=base["BodyText"],
            fontName="NanumGothic-Bold",
            fontSize=7.2,
            leading=8.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#23303d"),
        ),
        "tiny_bold": ParagraphStyle(
            "tiny_bold",
            parent=base["BodyText"],
            fontName="NanumGothic-Bold",
            fontSize=7.2,
            leading=8.5,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#23303d"),
        ),
    }


def draw_paragraph(c: canvas.Canvas, text: str, style: ParagraphStyle, x: float, top: float, width: float) -> float:
    para = Paragraph(text, style)
    _, h = para.wrap(width, 1000)
    para.drawOn(c, x, top - h)
    return top - h


def round_box(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill: colors.Color, stroke: colors.Color, radius: float = 8, line: float = 0.9) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(line)
    c.roundRect(x, y, w, h, radius, stroke=1, fill=1)


def draw_header(c: canvas.Canvas, title: str, x: float, y: float, w: float, h: float, header: colors.Color, body: colors.Color, border: colors.Color) -> tuple[float, float, float, float]:
    shadow = colors.Color(0, 0, 0, alpha=0.07)
    c.setFillColor(shadow)
    c.roundRect(x + 1.8, y - 1.8, w, h, 10, stroke=0, fill=1)

    round_box(c, x, y, w, h, body, border, 10, 1.0)
    c.setFillColor(header)
    c.setStrokeColor(header)
    c.roundRect(x, y + h - 14.5 * mm, w, 14.5 * mm, 10, stroke=0, fill=1)
    c.rect(x, y + h - 14.5 * mm, w, 5.5 * mm, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("NanumGothic-Bold", 10.6)
    c.drawString(x + 4.2 * mm, y + h - 9.1 * mm, title)
    return x + 3.5 * mm, y + 3.3 * mm, w - 7 * mm, h - 18.5 * mm


def begin_clip(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    c.saveState()
    path = c.beginPath()
    path.roundRect(x, y, w, h, 6)
    c.clipPath(path, stroke=0, fill=0)


def end_clip(c: canvas.Canvas) -> None:
    c.restoreState()


def chip(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, body: str, fill: str, stroke: str, st: dict[str, ParagraphStyle], title_size: float | None = None) -> None:
    round_box(c, x, y, w, h, colors.HexColor(fill), colors.HexColor(stroke), 7, 0.8)
    c.setFillColor(colors.HexColor("#1f3348"))
    c.setFont("NanumGothic-Bold", title_size or 7.5)
    c.drawCentredString(x + w / 2, y + h - 8.2, title)
    draw_paragraph(c, body, st["tiny_center"], x + 2.2, y + h - 11.5, w - 4.4)


def draw_title_area(c: canvas.Canvas, st: dict[str, ParagraphStyle]) -> float:
    top = PAGE_H - MARGIN
    draw_paragraph(c, "정보처리기사 실기 4단원 네트워크 암기 프레임", st["title"], MARGIN, top, PAGE_W - 2 * MARGIN)
    top -= 8.5 * mm
    draw_paragraph(c, "층, 주소, 라우팅, URL, 전송 프로토콜, HDLC를 한 페이지에 묶은 시각 암기장", st["subtitle"], MARGIN, top, PAGE_W - 2 * MARGIN)
    top -= 6.8 * mm
    round_box(c, MARGIN, top - 8.3 * mm, PAGE_W - 2 * MARGIN, 9.5 * mm, colors.HexColor("#edf4ff"), colors.HexColor("#9fb7de"), 7, 0.8)
    c.setFillColor(colors.HexColor("#173968"))
    c.setFont("NanumGothic-Bold", 9.5)
    c.drawCentredString(PAGE_W / 2, top - 2.4 * mm, "먼저 분류: 계층 / 주소 / 라우팅 / URL / 프로토콜 / HDLC")
    return top - 12.3 * mm


def draw_osi_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    ix, iy, iw, ih = draw_header(c, "1. OSI / 프로토콜 기본", x, y, w, h, colors.HexColor("#2e68c1"), colors.HexColor("#f8fbff"), colors.HexColor("#a8c3ec"))
    begin_clip(c, ix, iy, iw, ih)

    layer_x = ix
    layer_w = 26 * mm
    layer_h = 5.25 * mm
    layer_top = y + h - 21 * mm
    layers = [
        ("7 응용", "#d7ebff"),
        ("6 표현", "#e2f0ff"),
        ("5 세션", "#e9f4ff"),
        ("4 전송", "#eff7ff"),
        ("3 네트워크", "#eef6fd"),
        ("2 데이터링크", "#e3f0fb"),
        ("1 물리", "#d8eaf9"),
    ]
    for idx, (name, fill) in enumerate(layers):
        ly = layer_top - idx * (layer_h + 1.2 * mm)
        round_box(c, layer_x, ly, layer_w, layer_h, colors.HexColor(fill), colors.HexColor("#8fb6de"), 4, 0.7)
        c.setFillColor(colors.HexColor("#173968"))
        c.setFont("NanumGothic-Bold", 7.2)
        c.drawCentredString(layer_x + layer_w / 2, ly + 1.7 * mm, name)

    text_x = ix + 30 * mm
    t = y + h - 21.5 * mm
    bullets = [
        "<b>전송</b> = 종단 간 신뢰성",
        "<b>세션</b> = 연결 설정 / 동기화",
        "<b>표현</b> = 형식 변환 / 암호화 / 압축",
        "<b>응용</b> = 사용자 서비스와 가장 가까움",
    ]
    for b in bullets:
        t = draw_paragraph(c, b, st["body"], text_x, t, iw - 30 * mm)
        t -= 1.0

    box_y = iy + 3.5 * mm
    bw = (iw - 4 * mm) / 3
    chip(c, ix, box_y, bw, 15 * mm, "구문", "Syntax<br/>형식·구조", "#e9f3ff", "#9ec1eb", st)
    chip(c, ix + bw + 2 * mm, box_y, bw, 15 * mm, "의미", "Semantic<br/>각 필드 뜻", "#edf5ff", "#9ec1eb", st)
    chip(c, ix + 2 * (bw + 2 * mm), box_y, bw, 15 * mm, "타이밍", "Timing<br/>순서·속도·시점", "#f1f7ff", "#9ec1eb", st)
    end_clip(c)


def draw_address_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    ix, iy, iw, ih = draw_header(c, "2. 주소 / IP", x, y, w, h, colors.HexColor("#3e8c5a"), colors.HexColor("#f7fdf8"), colors.HexColor("#add7ba"))
    begin_clip(c, ix, iy, iw, ih)

    chip(c, ix, y + h - 27.5 * mm, 25 * mm, 12.5 * mm, "IPv6", "128bit", "#e0f4e7", "#9ed0ac", st, 8.2)
    chip(c, ix + 27 * mm, y + h - 27.5 * mm, 25 * mm, 12.5 * mm, "NAT", "사설 IP<br/>-> 공인 IP", "#e8f7ed", "#9ed0ac", st)
    chip(c, ix + 54 * mm, y + h - 27.5 * mm, 25 * mm, 12.5 * mm, "VPN", "공용망 위<br/>사설망처럼", "#edf9f1", "#9ed0ac", st)

    mid_y = y + h - 45.5 * mm
    round_box(c, ix, mid_y, 35 * mm, 13.5 * mm, colors.HexColor("#e8f7ed"), colors.HexColor("#9ed0ac"), 7, 0.8)
    round_box(c, ix + 42 * mm, mid_y, 35 * mm, 13.5 * mm, colors.HexColor("#edf9f1"), colors.HexColor("#9ed0ac"), 7, 0.8)
    c.setFillColor(colors.HexColor("#1e5d3c"))
    c.setFont("NanumGothic-Bold", 7.7)
    c.drawCentredString(ix + 17.5 * mm, mid_y + 8.2, "ARP")
    c.drawCentredString(ix + 59.5 * mm, mid_y + 8.2, "RARP")
    c.setFont("NanumGothic", 7.1)
    c.drawCentredString(ix + 17.5 * mm, mid_y + 3.0, "IP -> MAC")
    c.drawCentredString(ix + 59.5 * mm, mid_y + 3.0, "MAC -> IP")
    c.setStrokeColor(colors.HexColor("#5ba978"))
    c.setLineWidth(1.0)
    c.line(ix + 35 * mm + 2 * mm, mid_y + 6.7 * mm, ix + 42 * mm - 2 * mm, mid_y + 6.7 * mm)
    c.line(ix + 42 * mm - 5 * mm, mid_y + 6.7 * mm, ix + 42 * mm - 7 * mm, mid_y + 8.7 * mm)
    c.line(ix + 42 * mm - 5 * mm, mid_y + 6.7 * mm, ix + 42 * mm - 7 * mm, mid_y + 4.7 * mm)

    lower_y = iy + 4 * mm
    chip(c, ix, lower_y, 25 * mm, 13.5 * mm, "네트워크 주소", "서브넷 자체", "#e8f7ed", "#9ed0ac", st)
    chip(c, ix + 27 * mm, lower_y, 25 * mm, 13.5 * mm, "브로드캐스트", "전체 호스트", "#edf9f1", "#9ed0ac", st)
    chip(c, ix + 54 * mm, lower_y, 25 * mm, 13.5 * mm, "/26", "사용 가능 62 hosts", "#f2fbf5", "#9ed0ac", st)
    end_clip(c)


def draw_routing_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    ix, iy, iw, ih = draw_header(c, "3. 라우팅 / 교환", x, y, w, h, colors.HexColor("#9a6b1a"), colors.HexColor("#fffaf3"), colors.HexColor("#e0bf88"))
    begin_clip(c, ix, iy, iw, ih)

    top_y = y + h - 28 * mm
    chip(c, ix, top_y, 37 * mm, 13 * mm, "IGP", "AS 내부 라우팅", "#fff0d8", "#e1b676", st, 8.4)
    chip(c, ix + 42 * mm, top_y, 37 * mm, 13 * mm, "EGP", "AS 간 라우팅", "#fff3df", "#e1b676", st, 8.4)
    c.setFillColor(colors.HexColor("#855007"))
    c.setFont("NanumGothic-Bold", 7.1)
    c.drawCentredString(ix + 60.5 * mm, top_y - 3.2, "외부에서 실제 대표 프로토콜 = BGP")

    mid_y = y + h - 47 * mm
    chip(c, ix, mid_y, 25 * mm, 14.5 * mm, "RIP", "홉 수<br/>거리 벡터", "#fff2dc", "#e1b676", st)
    chip(c, ix + 27 * mm, mid_y, 25 * mm, 14.5 * mm, "OSPF", "링크 상태<br/>최단 경로", "#fff6e7", "#e1b676", st)
    chip(c, ix + 54 * mm, mid_y, 25 * mm, 14.5 * mm, "BGP", "AS 간 경로<br/>외부 라우팅", "#fff8ec", "#e1b676", st)

    low_y = iy + 4 * mm
    chip(c, ix, low_y, 25 * mm, 14.5 * mm, "데이터그램", "경로 설정 X", "#fff2dc", "#e1b676", st)
    chip(c, ix + 27 * mm, low_y, 25 * mm, 14.5 * mm, "가상회선", "먼저 경로 설정", "#fff6e7", "#e1b676", st)
    chip(c, ix + 54 * mm, low_y, 25 * mm, 14.5 * mm, "ATM", "고정 길이 셀", "#fff8ec", "#e1b676", st)
    end_clip(c)


def draw_url_web_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    ix, iy, iw, ih = draw_header(c, "4. URL / 웹 기본", x, y, w, h, colors.HexColor("#7b55c7"), colors.HexColor("#faf8ff"), colors.HexColor("#c9b8ea"))
    begin_clip(c, ix, iy, iw, ih)

    url_y = y + h - 28 * mm
    segs = [
        ("scheme", 14 * mm, "#e6dcff"),
        ("authority", 21 * mm, "#eadfff"),
        ("path", 13 * mm, "#efe6ff"),
        ("query", 12 * mm, "#f2ebff"),
        ("fragment", 17 * mm, "#f6f0ff"),
    ]
    sx = ix
    for name, sw, fill in segs:
        round_box(c, sx, url_y, sw, 9 * mm, colors.HexColor(fill), colors.HexColor("#b8a5e5"), 5, 0.8)
        c.setFillColor(colors.HexColor("#4e3487"))
        c.setFont("NanumGothic-Bold", 7.0)
        c.drawCentredString(sx + sw / 2, url_y + 3.0 * mm, name)
        sx += sw + 1.2 * mm

    t = url_y - 2.0 * mm
    lines = [
        "scheme = https://",
        "authority = 호스트명·포트",
        "path = /board/list",
        "query = ? 뒤",
        "fragment = # 뒤",
    ]
    for line in lines:
        t = draw_paragraph(c, line, st["body"], ix, t, iw)
        t -= 0.6

    chip(c, ix, iy + 17 * mm, 24 * mm, 13 * mm, "Hypertext", "링크로 이동하는<br/>텍스트 구조", "#efe8ff", "#b8a5e5", st)
    chip(c, ix + 27 * mm, iy + 17 * mm, 24 * mm, 13 * mm, "HTML", "웹 문서 구조", "#f3edff", "#b8a5e5", st)
    chip(c, ix + 54 * mm, iy + 17 * mm, 24 * mm, 13 * mm, "HTTP", "하이퍼텍스트 통신", "#f7f2ff", "#b8a5e5", st)
    chip(c, ix, iy + 1.5 * mm, 39 * mm, 13.5 * mm, "AJAX", "새로고침 없는 비동기", "#ede5ff", "#b8a5e5", st, 8.0)
    chip(c, ix + 41 * mm, iy + 1.5 * mm, 18 * mm, 13.5 * mm, "JSON", "키-값", "#f3edff", "#b8a5e5", st)
    chip(c, ix + 61 * mm, iy + 1.5 * mm, 18 * mm, 13.5 * mm, "HTTPS", "HTTP + TLS/SSL", "#f8f4ff", "#b8a5e5", st)
    end_clip(c)


def draw_protocol_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    ix, iy, iw, ih = draw_header(c, "5. 전송 / 응용 프로토콜", x, y, w, h, colors.HexColor("#d24d7d"), colors.HexColor("#fff7fb"), colors.HexColor("#e6b1c5"))
    begin_clip(c, ix, iy, iw, ih)

    top_y = y + h - 28 * mm
    chip(c, ix, top_y, 37 * mm, 14 * mm, "TCP", "연결형<br/>신뢰성 O", "#ffe8f0", "#e0a0b8", st, 8.3)
    chip(c, ix + 42 * mm, top_y, 37 * mm, 14 * mm, "UDP", "비연결형<br/>빠르지만 보장 적음", "#fff0f5", "#e0a0b8", st, 8.3)

    mid_y = y + h - 46 * mm
    chip(c, ix, mid_y, 18 * mm, 13 * mm, "FTP", "파일", "#ffeaf1", "#e0a0b8", st)
    chip(c, ix + 20 * mm, mid_y, 18 * mm, 13 * mm, "SMTP", "송신", "#fff1f6", "#e0a0b8", st)
    chip(c, ix + 40 * mm, mid_y, 18 * mm, 13 * mm, "POP3", "내려받기", "#fff5f8", "#e0a0b8", st)
    chip(c, ix + 60 * mm, mid_y, 18 * mm, 13 * mm, "IMAP", "서버 동기화", "#fff8fa", "#e0a0b8", st)

    low_y = iy + 4 * mm
    chip(c, ix, low_y, 24 * mm, 13 * mm, "ICMP", "오류 보고·제어 메시지", "#ffeaf1", "#e0a0b8", st)
    chip(c, ix + 27 * mm, low_y, 24 * mm, 13 * mm, "SSH", "암호화 원격 접속", "#fff1f6", "#e0a0b8", st)
    chip(c, ix + 54 * mm, low_y, 24 * mm, 13 * mm, "L2TP", "2계층 터널링", "#fff7fb", "#e0a0b8", st)
    end_clip(c)


def draw_misc_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, st: dict[str, ParagraphStyle]) -> None:
    ix, iy, iw, ih = draw_header(c, "6. Web Service / HDLC / 기타", x, y, w, h, colors.HexColor("#3e6c89"), colors.HexColor("#f7fbfe"), colors.HexColor("#aecaDA"))
    begin_clip(c, ix, iy, iw, ih)

    top_y = y + h - 27.5 * mm
    chip(c, ix, top_y, 25 * mm, 13 * mm, "WSDL", "설명서", "#e6f2fa", "#9ec2d8", st)
    chip(c, ix + 27 * mm, top_y, 25 * mm, 13 * mm, "SOAP", "XML 호출 메시지", "#edf6fb", "#9ec2d8", st)
    chip(c, ix + 54 * mm, top_y, 25 * mm, 13 * mm, "UDDI", "등록 / 검색", "#f3f9fd", "#9ec2d8", st)

    mid_y = y + h - 45.5 * mm
    chip(c, ix, mid_y, 25 * mm, 13 * mm, "I 프레임", "정보 프레임", "#e6f2fa", "#9ec2d8", st)
    chip(c, ix + 27 * mm, mid_y, 25 * mm, 13 * mm, "S 프레임", "감독 프레임", "#edf6fb", "#9ec2d8", st)
    chip(c, ix + 54 * mm, mid_y, 25 * mm, 13 * mm, "U 프레임", "비번호 프레임", "#f3f9fd", "#9ec2d8", st)

    low_y = iy + 18 * mm
    chip(c, ix, low_y, 25 * mm, 13 * mm, "NRM", "정상응답<br/>허가 후 응답", "#e6f2fa", "#9ec2d8", st)
    chip(c, ix + 27 * mm, low_y, 25 * mm, 13 * mm, "ARM", "비동기응답<br/>선택 응답", "#edf6fb", "#9ec2d8", st)
    chip(c, ix + 54 * mm, low_y, 25 * mm, 13 * mm, "ABM", "비동기균형<br/>양측 대등", "#f3f9fd", "#9ec2d8", st)

    bot_y = iy + 1.5 * mm
    chip(c, ix, bot_y, 25 * mm, 13 * mm, "Ad-hoc", "고정 인프라 없이", "#e6f2fa", "#9ec2d8", st)
    chip(c, ix + 27 * mm, bot_y, 25 * mm, 13 * mm, "I/P/SaaS", "인프라 / 플랫폼 / 소프트웨어", "#edf6fb", "#9ec2d8", st, 7.0)
    chip(c, ix + 54 * mm, bot_y, 25 * mm, 13 * mm, "암기 팁", "문제 단어를 먼저 카드에 꽂기", "#f3f9fd", "#9ec2d8", st)
    end_clip(c)


def build_pdf() -> None:
    register_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    st = styles()
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
    c.setTitle("정보처리기사 실기 4단원 네트워크 암기 프레임")
    c.setAuthor("Codex")

    c.setFillColor(colors.HexColor("#fffdfa"))
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    title_bottom = draw_title_area(c, st)
    row1_y = title_bottom - CARD_H
    row2_y = MARGIN
    x1 = MARGIN
    x2 = MARGIN + CARD_W + GAP_X
    x3 = MARGIN + 2 * (CARD_W + GAP_X)

    draw_osi_card(c, x1, row1_y, CARD_W, CARD_H, st)
    draw_address_card(c, x2, row1_y, CARD_W, CARD_H, st)
    draw_routing_card(c, x3, row1_y, CARD_W, CARD_H, st)
    draw_url_web_card(c, x1, row2_y, CARD_W, CARD_H, st)
    draw_protocol_card(c, x2, row2_y, CARD_W, CARD_H, st)
    draw_misc_card(c, x3, row2_y, CARD_W, CARD_H, st)

    c.setFont("NanumGothic-Bold", 7.8)
    c.setFillColor(colors.HexColor("#637180"))
    c.drawRightString(PAGE_W - MARGIN, 5.6 * mm, "모든 카드 body에 clip 적용: overflow가 옆 카드를 덮지 않음")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build_pdf()
