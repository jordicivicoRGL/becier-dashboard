from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.platypus import ListFlowable, ListItem
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUTS_BASE = Path(__file__).parent.parent / "outputs"

PRIMARY = HexColor("#1B4F72")
SECONDARY = HexColor("#2E86C1")
LIGHT_GRAY = HexColor("#F2F3F4")
DARK_GRAY = HexColor("#2C3E50")
TEXT_COLOR = HexColor("#1A1A1A")

# Registrar fuentes Unicode (Arial desde Windows Fonts)
_FONTS_DIR = Path("C:/Windows/Fonts")
try:
    pdfmetrics.registerFont(TTFont("Arial", str(_FONTS_DIR / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(_FONTS_DIR / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(_FONTS_DIR / "ariali.ttf")))
    FONT_NORMAL = "Arial"
    FONT_BOLD = "Arial-Bold"
except Exception:
    FONT_NORMAL = FONT_NORMAL
    FONT_BOLD = FONT_BOLD


def _build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ProposalTitle",
        parent=base["Title"],
        fontSize=26,
        fontName=FONT_BOLD,
        textColor=PRIMARY,
        spaceAfter=6,
        spaceBefore=0,
        leading=32
    )

    subtitle_style = ParagraphStyle(
        "ProposalSubtitle",
        parent=base["Normal"],
        fontSize=13,
        fontName=FONT_NORMAL,
        textColor=SECONDARY,
        spaceAfter=4,
        spaceBefore=0
    )

    date_style = ParagraphStyle(
        "ProposalDate",
        parent=base["Normal"],
        fontSize=10,
        fontName=FONT_NORMAL,
        textColor=HexColor("#7F8C8D"),
        spaceAfter=20,
        spaceBefore=0
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=base["Heading2"],
        fontSize=14,
        fontName=FONT_BOLD,
        textColor=PRIMARY,
        spaceAfter=8,
        spaceBefore=16,
        borderPadding=(0, 0, 4, 0)
    )

    body_style = ParagraphStyle(
        "ProposalBody",
        parent=base["Normal"],
        fontSize=10.5,
        fontName=FONT_NORMAL,
        textColor=TEXT_COLOR,
        spaceAfter=6,
        spaceBefore=2,
        leading=16
    )

    bullet_style = ParagraphStyle(
        "BulletItem",
        parent=base["Normal"],
        fontSize=10.5,
        fontName=FONT_NORMAL,
        textColor=TEXT_COLOR,
        spaceAfter=3,
        spaceBefore=1,
        leading=15,
        leftIndent=16,
        bulletIndent=4,
        bulletText="•"
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=base["Normal"],
        fontSize=8,
        fontName=FONT_NORMAL,
        textColor=HexColor("#95A5A6"),
        alignment=1
    )

    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "date": date_style,
        "section": section_style,
        "body": body_style,
        "bullet": bullet_style,
        "footer": footer_style
    }


def _parse_content(content: str, styles: dict) -> list:
    elements = []
    lines = content.strip().split("\n")
    buffer = []

    for line in lines:
        line = line.strip()
        if not line:
            if buffer:
                elements.append(Paragraph(" ".join(buffer), styles["body"]))
                buffer = []
            continue

        if line.startswith("- "):
            if buffer:
                elements.append(Paragraph(" ".join(buffer), styles["body"]))
                buffer = []
            elements.append(Paragraph(line[2:], styles["bullet"]))
        else:
            buffer.append(line)

    if buffer:
        elements.append(Paragraph(" ".join(buffer), styles["body"]))

    return elements


def _build_table(table_data: list, styles: dict) -> list:
    from reportlab.lib import colors

    col_count = max(len(row) for row in table_data)
    page_width = 21 * cm - 6 * cm  # A4 minus margins
    col_widths = [page_width * 0.65] + [page_width * 0.35 / max(col_count - 1, 1)] * max(col_count - 1, 1)

    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["body"],
        fontSize=10,
        leading=14,
        spaceAfter=0,
        spaceBefore=0,
    )
    header_cell_style = ParagraphStyle(
        "TableHeaderCell",
        parent=cell_style,
        fontName=FONT_BOLD,
        textColor=colors.white,
    )

    formatted_rows = []
    for i, row in enumerate(table_data):
        s = header_cell_style if i == 0 else cell_style
        formatted_rows.append([Paragraph(str(cell), s) for cell in row])

    t = Table(formatted_rows, colWidths=col_widths, repeatRows=1)

    row_count = len(formatted_rows)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#F2F3F4")]),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D5D8DC")),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]

    # Bold last row (totals)
    if row_count > 1:
        style_cmds += [
            ("FONTNAME", (0, -1), (-1, -1), FONT_BOLD),
            ("LINEABOVE", (0, -1), (-1, -1), 1.5, PRIMARY),
            ("BACKGROUND", (0, -1), (-1, -1), HexColor("#EAF2FF")),
        ]

    t.setStyle(TableStyle(style_cmds))
    return [t, Spacer(1, 8)]


def create_proposal_pdf(title: str, sections: list, client_name: str = "",
                        filename: str = None, client: str = None) -> dict:
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in " _-" else "" for c in title).strip()
        safe_title = safe_title.replace(" ", "_")[:30]
        filename = f"propuesta_{safe_title}_{timestamp}"

    output_dir = OUTPUTS_BASE / client / "proposals" if client else OUTPUTS_BASE / "proposals"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{filename}.pdf"

    try:
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=3 * cm,
            rightMargin=3 * cm,
            topMargin=3 * cm,
            bottomMargin=3 * cm
        )

        styles = _build_styles()
        story = []

        story.append(Paragraph(title, styles["title"]))

        if client_name:
            story.append(Paragraph(f"Preparado para: {client_name}", styles["subtitle"]))

        date_str = datetime.now().strftime("%d de %B de %Y")
        story.append(Paragraph(date_str, styles["date"]))

        story.append(HRFlowable(
            width="100%",
            thickness=2,
            color=PRIMARY,
            spaceAfter=20,
            spaceBefore=0
        ))

        for section in sections:
            heading = section.get("heading", "")
            content = section.get("content", "")
            table_data = section.get("table", None)

            if heading:
                story.append(Paragraph(heading, styles["section"]))
                story.append(HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=SECONDARY,
                    spaceAfter=8,
                    spaceBefore=0
                ))

            if content:
                story.extend(_parse_content(content, styles))

            if table_data:
                story.extend(_build_table(table_data, styles))

            story.append(Spacer(1, 6))

        story.append(Spacer(1, 30))
        story.append(HRFlowable(
            width="100%",
            thickness=0.5,
            color=HexColor("#BDC3C7"),
            spaceAfter=8,
            spaceBefore=0
        ))
        story.append(Paragraph("© Jordi Civico · Propuesta Confidencial", styles["footer"]))

        doc.build(story)

        return {
            "success": True,
            "filename": f"{filename}.pdf",
            "path": str(output_path),
            "title": title,
            "sections": len(sections),
            "message": f"Propuesta PDF creada correctamente en: {output_path}"
        }

    except Exception as e:
        return {"error": f"Error creando el PDF: {str(e)}"}
