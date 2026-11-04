"""
Build the NovaMart / Databricks student guide PDF.
Run: python docs/student-guide/build_pdf.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
OUT = ROOT / "Databricks_Student_Project_Guide.pdf"

NAVY = colors.HexColor("#0B3A5B")
TEAL = colors.HexColor("#0F7B8A")
LIGHT = colors.HexColor("#F4F7FA")
ORANGE = colors.HexColor("#D97706")


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    base.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="H1Custom",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            name="H2Custom",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=TEAL,
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            name="BodyCustom",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#1F2937"),
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            name="BulletCustom",
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#1F2937"),
            leftIndent=8,
            spaceAfter=2,
        )
    )
    base.add(
        ParagraphStyle(
            name="Caption",
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#4B5563"),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=10,
        )
    )
    base.add(
        ParagraphStyle(
            name="Footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=colors.HexColor("#6B7280"),
            alignment=TA_CENTER,
        )
    )
    return base


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=10, bulletColor=TEAL) for i in items],
        bulletType="bullet",
        start="•",
    )


def add_image(story, filename, caption, s, width=6.5 * inch):
    path = IMAGES / filename
    if not path.exists():
        story.append(Paragraph(f"[Missing image: {filename}]", s["BodyCustom"]))
        return
    img = Image(str(path))
    img._restrictSize(width, 3.6 * inch)
    story.append(Spacer(1, 6))
    story.append(img)
    story.append(Paragraph(caption, s["Caption"]))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1)
    canvas.line(0.75 * inch, A4[1] - 0.55 * inch, A4[0] - 0.75 * inch, A4[1] - 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(0.75 * inch, A4[1] - 0.45 * inch, "Databricks Student Project Guide")
    canvas.drawRightString(A4[0] - 0.75 * inch, A4[1] - 0.45 * inch, "NovaMart + Gen AI")
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawCentredString(A4[0] / 2, 0.45 * inch, f"Page {doc.page}")
    canvas.line(0.75 * inch, 0.6 * inch, A4[0] - 0.75 * inch, 0.6 * inch)
    canvas.restoreState()


def table(data, col_widths):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#111827")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        title="Databricks Student Project Guide",
        author="Akhil Vydyula Teaching Repo",
    )
    story = []

    # Cover
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("Databricks Student Project Guide", s["CoverTitle"]))
    story.append(Paragraph("Retail Data Warehouse + Generative AI Learning Path", s["CoverSub"]))
    story.append(Paragraph("Public GitHub: github.com/akhilvydyula01/databricks", s["CoverSub"]))
    story.append(
        Paragraph(
            "Workspace: dbc-37e2a2e8-2739.cloud.databricks.com",
            s["CoverSub"],
        )
    )
    story.append(Spacer(1, 0.3 * inch))
    add_image(
        story,
        "diagram_project_map.jpg",
        "Figure 1. Full repository map — Data Warehouse track and Gen AI track.",
        s,
        width=6.3 * inch,
    )
    story.append(
        Paragraph(
            "This guide is designed for classroom teaching and YouTube walkthroughs. "
            "Students should clone the repository into Databricks Repos / Git folders and run notebooks in order.",
            s["BodyCustom"],
        )
    )
    story.append(PageBreak())

    # TOC / overview
    story.append(Paragraph("1. Project Overview", s["H1Custom"]))
    story.append(
        Paragraph(
            "This repository contains two teaching tracks that share one Databricks workspace and one public GitHub repo.",
            s["BodyCustom"],
        )
    )
    story.append(
        table(
            [
                ["Track", "Path", "What students learn"],
                [
                    "Data Warehouse",
                    "notebooks/data_warehouse",
                    "Medallion architecture, star schema, SCD2, quality, SQL analytics",
                ],
                [
                    "Gen AI Basic→Advanced",
                    "notebooks/gen_ai + gen-ai/",
                    "Open-source LLMs, RAG, agents, LoRA, multi-agent patterns",
                ],
                [
                    "Teaching pack",
                    "data-warehouse/",
                    "YouTube scripts, assignment, job JSON, 20-min demo plan",
                ],
            ],
            [1.3 * inch, 1.8 * inch, 3.2 * inch],
        )
    )
    story.append(Spacer(1, 10))
    story.append(Paragraph("1.1 Learning outcomes", s["H2Custom"]))
    story.append(
        bullets(
            [
                "Explain lakehouse and medallion architecture in plain language.",
                "Build Bronze, Silver, and Gold tables for a retail domain (NovaMart).",
                "Design a star schema with facts and dimensions.",
                "Implement SCD Type 2 for changing customer attributes.",
                "Apply data quality gates before analytics.",
                "Optionally explore open-source Gen AI notebooks in the same repo.",
            ],
            s["BulletCustom"],
        )
    )
    story.append(PageBreak())

    # Setup
    story.append(Paragraph("2. How to Open the Project in Databricks", s["H1Custom"]))
    story.append(Paragraph("2.1 One-time setup", s["H2Custom"]))
    story.append(
        bullets(
            [
                "Open your Databricks workspace.",
                "Go to Workspace → Repos / Git folders.",
                "Add repo URL: https://github.com/akhilvydyula01/databricks",
                "Click Pull to sync latest notebooks.",
                "Attach a Databricks Runtime 13+ cluster (ML runtime for Gen AI notebooks).",
            ],
            s["BulletCustom"],
        )
    )
    story.append(Paragraph("2.2 Exact notebook locations", s["H2Custom"]))
    story.append(
        Paragraph(
            "<b>Data Warehouse:</b> Repos → &lt;you&gt; → databricks → notebooks → data_warehouse<br/>"
            "<b>Gen AI:</b> Repos → &lt;you&gt; → databricks → notebooks → gen_ai → basic / intermediate / advanced",
            s["BodyCustom"],
        )
    )
    story.append(Paragraph("2.3 Suggested class schedule", s["H2Custom"]))
    story.append(
        table(
            [
                ["Session", "Focus", "Notebooks"],
                ["Day 1", "Architecture + Bronze/Silver", "00, 01, 02, 03"],
                ["Day 2", "Gold + SCD2 + Quality", "04, 05, 06"],
                ["Day 3", "Analytics + Jobs + Assignment", "07, 08/09 + homework"],
                ["Optional", "Gen AI intro", "gen_ai/basic 01–03"],
            ],
            [1.0 * inch, 2.4 * inch, 2.9 * inch],
        )
    )
    story.append(PageBreak())

    # Medallion
    story.append(Paragraph("3. Data Warehouse Architecture", s["H1Custom"]))
    story.append(
        Paragraph(
            "NovaMart is a fictional retailer. Students ingest customers, products, stores, and orders, "
            "then transform them through Bronze → Silver → Gold.",
            s["BodyCustom"],
        )
    )
    add_image(
        story,
        "diagram_medallion.jpg",
        "Figure 2. Medallion architecture used in this course.",
        s,
    )
    story.append(Paragraph("3.1 Layer responsibilities", s["H2Custom"]))
    story.append(
        table(
            [
                ["Layer", "Purpose", "Example tables"],
                ["Bronze", "Raw landing + lineage", "bronze_orders, bronze_customers"],
                ["Silver", "Trusted cleaned data", "silver_orders, silver_orders_rejected"],
                ["Gold", "BI-ready star schema", "gold_fact_sales, gold_dim_*"],
            ],
            [1.1 * inch, 2.5 * inch, 2.7 * inch],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<b>Teaching tip:</b> Emphasize that Bronze preserves history of what arrived. "
            "Silver creates trust. Gold creates usability for analysts.",
            s["BodyCustom"],
        )
    )
    story.append(PageBreak())

    # Notebook walkthrough
    story.append(Paragraph("4. Notebook Walkthrough (Data Warehouse)", s["H1Custom"]))
    story.append(
        table(
            [
                ["#", "Notebook", "Student takeaway"],
                ["00", "architecture_overview", "Big picture before coding"],
                ["01", "setup_and_sample_data", "Create schema + landing files"],
                ["02", "bronze_ingestion", "Land raw tables with metadata"],
                ["03", "silver_transform", "Cast, dedupe, quarantine bad rows"],
                ["04", "gold_star_schema", "Build dims + fact_sales"],
                ["05", "scd2_customers", "Track customer history over time"],
                ["06", "data_quality", "Fail pipeline on broken rules"],
                ["07", "analytics_sql", "Answer business questions"],
                ["08", "end_to_end_pipeline", "Run full refresh sequence"],
                ["09", "youtube_20min_runner", "Fast demo path for teaching videos"],
            ],
            [0.45 * inch, 1.9 * inch, 3.95 * inch],
        )
    )
    story.append(Spacer(1, 10))
    story.append(Paragraph("4.1 Important demo details baked into sample data", s["H2Custom"]))
    story.append(
        bullets(
            [
                "Order amounts arrive as strings in Bronze (type casting lesson).",
                "Duplicate order_id 5015 exists (dedupe lesson).",
                "One negative amount is rejected into silver_orders_rejected.",
                "Customer 101 later moves Austin → Houston (SCD2 lesson).",
            ],
            s["BulletCustom"],
        )
    )
    story.append(PageBreak())

    # Star schema
    story.append(Paragraph("5. Gold Star Schema Explained", s["H1Custom"]))
    story.append(
        Paragraph(
            "Analysts think in business events (facts) and descriptive context (dimensions). "
            "In this project, the fact grain is one order.",
            s["BodyCustom"],
        )
    )
    add_image(
        story,
        "diagram_star_schema.jpg",
        "Figure 3. NovaMart Gold star schema.",
        s,
    )
    story.append(Paragraph("5.1 Key definitions for exams / interviews", s["H2Custom"]))
    story.append(
        bullets(
            [
                "<b>Fact table:</b> stores measures (quantity, gross_amount) and foreign keys.",
                "<b>Dimension table:</b> stores descriptive attributes (customer city, product category).",
                "<b>Surrogate key:</b> warehouse-generated key (customer_sk) independent of source IDs.",
                "<b>Grain:</b> what one fact row represents — here, one order.",
            ],
            s["BulletCustom"],
        )
    )
    story.append(PageBreak())

    # SCD2
    story.append(Paragraph("6. SCD Type 2 (Customer History)", s["H1Custom"]))
    story.append(
        Paragraph(
            "Slowly Changing Dimensions Type 2 preserve history when attributes change. "
            "Instead of overwriting Austin with Houston, we close the old row and insert a new current row.",
            s["BodyCustom"],
        )
    )
    add_image(
        story,
        "diagram_scd2.jpg",
        "Figure 4. SCD Type 2 example for customer 101.",
        s,
    )
    story.append(
        Paragraph(
            "Columns to memorize: <b>valid_from</b>, <b>valid_to</b>, <b>is_current</b>. "
            "Advanced designs join the dimension version that was valid on the order date.",
            s["BodyCustom"],
        )
    )
    story.append(PageBreak())

    # Quality + analytics
    story.append(Paragraph("7. Data Quality and Analytics", s["H1Custom"]))
    story.append(Paragraph("7.1 Quality gates in notebook 06", s["H2Custom"]))
    story.append(
        bullets(
            [
                "Fact sales_key must be unique.",
                "Quantity and gross_amount must be positive.",
                "No orphan keys to customer/product/store dimensions.",
                "Reject table must capture known bad records.",
            ],
            s["BulletCustom"],
        )
    )
    story.append(Paragraph("7.2 Business questions in notebook 07", s["H2Custom"]))
    story.append(
        bullets(
            [
                "Total revenue and average order value",
                "Revenue by month",
                "Top products by revenue",
                "Store performance and AOV",
                "Customer segment contribution",
            ],
            s["BulletCustom"],
        )
    )
    story.append(Paragraph("7.3 Student assignment highlight", s["H2Custom"]))
    story.append(
        Paragraph(
            "Homework asks students to add a <b>Returns</b> source and build bronze_returns → "
            "silver_returns → gold_fact_returns, then write SQL for refunds by product category. "
            "Full rubric: data-warehouse/STUDENT_ASSIGNMENT.md",
            s["BodyCustom"],
        )
    )
    story.append(PageBreak())

    # Gen AI section
    story.append(Paragraph("8. Gen AI Track (Same Repository)", s["H1Custom"]))
    story.append(
        Paragraph(
            "The same repo includes an open-source Gen AI path so students can continue into LLM apps "
            "without leaving Databricks.",
            s["BodyCustom"],
        )
    )
    story.append(
        table(
            [
                ["Level", "Folder", "Projects"],
                ["Basic", "gen_ai/basic", "Hello LLM, chatbot, tiny RAG"],
                ["Intermediate", "gen_ai/intermediate", "FAISS RAG, tool agent, evaluation"],
                ["Advanced", "gen_ai/advanced", "LoRA fine-tune, multi-agent, production RAG"],
            ],
            [1.2 * inch, 1.8 * inch, 3.3 * inch],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Local Python equivalents live under <b>gen-ai/</b> with requirements.txt for offline practice. "
            "Databricks notebook versions are under <b>notebooks/gen_ai/</b>.",
            s["BodyCustom"],
        )
    )
    story.append(PageBreak())

    # Glossary + resources
    story.append(Paragraph("9. Quick Glossary", s["H1Custom"]))
    story.append(
        table(
            [
                ["Term", "Meaning"],
                ["Lakehouse", "Platform combining data lake storage with warehouse-style analytics"],
                ["Medallion", "Layered data design: Bronze, Silver, Gold"],
                ["Star schema", "Fact table surrounded by dimensions"],
                ["SCD2", "Keep historical versions of dimension attributes"],
                ["Lineage", "Tracking where data came from and when it was ingested"],
                ["Quarantine", "Isolating bad records instead of deleting silently"],
            ],
            [1.4 * inch, 5.0 * inch],
        )
    )
    story.append(Spacer(1, 12))
    story.append(Paragraph("10. Resources", s["H1Custom"]))
    story.append(
        bullets(
            [
                "GitHub repo: https://github.com/akhilvydyula01/databricks",
                "DWH docs: data-warehouse/README.md",
                "YouTube full script: data-warehouse/YOUTUBE_TEACHING_GUIDE.md",
                "20-min demo cut: data-warehouse/YOUTUBE_20MIN_DEMO.md",
                "Voiceover teleprompter: data-warehouse/youtube/",
                "Job setup: data-warehouse/jobs/HOW_TO_CREATE_JOB.md",
            ],
            s["BulletCustom"],
        )
    )
    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            "<b>Instructor note:</b> Print this PDF for students, or share the GitHub docs folder. "
            "For live class, project Figures 2–4 while running notebooks 02, 04, and 05.",
            s["BodyCustom"],
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
