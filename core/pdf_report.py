"""
pdf_report.py

Professional PDF MIS Report Generator.

Author: Sagar
"""

from datetime import datetime
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Table,
    TableStyle
)

#OUTPUT_DIR = Path("output")
#OUTPUT_DIR.mkdir(exist_ok=True)

LOGO_PATH = "assets/images/company_logo.png"


def get_styles():
    """
    Create custom report styles.
    """

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CompanyTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#1F4E78")
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=24
        )
    )

    styles.add(
        ParagraphStyle(
            name="CenterNormal",
            parent=styles["Normal"],
            alignment=TA_CENTER
        )
    )

    return styles

    
def create_cover_page(
    elements,
    styles
):
    """
    Create report cover page.
    """

    try:
        logo = Image(
            LOGO_PATH,
            width=120,
            height=120
        )
        elements.append(logo)
    except Exception:
        pass

    elements.append(
        Spacer(1, 30)
    )

    elements.append(
        Paragraph(
            "RETAILCORE PVT. LTD.",
            styles["CompanyTitle"]
        )
    )

    elements.append(
        Spacer(1, 25)
    )

    elements.append(
        Paragraph(
            "MANAGEMENT INFORMATION SYSTEM",
            styles["ReportTitle"]
        )
    )

    elements.append(
        Paragraph(
            "EXECUTIVE REPORT",
            styles["ReportTitle"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Sales • Inventory • Returns",
            styles["CenterNormal"]
        )
    )

    elements.append(
        Spacer(1, 100)
    )

    elements.append(
        Paragraph(
            f"Generated On: {datetime.now():%d %B %Y}",
            styles["CenterNormal"]
        )
    )

    elements.append(
        Spacer(1, 150)
    )

    elements.append(
        Paragraph(
            "Confidential Internal Business Document",
            styles["CenterNormal"]
        )
    )

    elements.append(PageBreak())

    
def create_executive_summary(
    elements,
    styles,
    metrics
):
    """
    Executive KPI dashboard.
    """

    sales = metrics["sales"]

    total_revenue = round(
        sales["net_revenue"].sum(),
        2
    )

    top_region = (
        metrics["region_revenue"]
        .iloc[0]["region"]
    )

    stockout_count = len(
        metrics["inventory_health"]
    )

    return_rate = round(
        metrics["return_rate"]
        ["return_rate_pct"]
        .mean(),
        2
    )

    data = [
        ["KPI", "Value"],
        #["Total Revenue", f"₹ {total_revenue:,.2f}"],
        ["Total Revenue", f"Rs. {total_revenue:,.2f}"],
        ["Return Rate", f"{return_rate}%"],
        ["Top Region", top_region],
        ["Stockout Products", stockout_count]
    ]

    table = Table(
        data,
        colWidths=[220, 220]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),
            ("GRID", (0, 0), (-1, -1),
             1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold")
        ])
    )

    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(table)

    elements.append(PageBreak())

    
def create_revenue_analysis(
    elements,
    styles,
    metrics
):
    """
    Revenue analysis section.
    """

    elements.append(
        Paragraph(
            "Revenue Analysis",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    elements.append(
        Paragraph(
            "Weekly Revenue Trend",
            styles["Heading2"]
        )
    )

    elements.append(
        Image(
            "charts/weekly_revenue_trend.png",
            width=450,
            height=250
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Revenue by Region",
            styles["Heading2"]
        )
    )

    elements.append(
        Image(
            "charts/region_revenue.png",
            width=450,
            height=250
        )
    )

    elements.append(
        PageBreak()
    )

    
def create_inventory_analysis(
    elements,
    styles,
    metrics
):
    """
    Inventory risk section.
    """

    inventory = (
        metrics["inventory_health"]
        .copy()
    )

    elements.append(
        Paragraph(
            "Inventory Risk Analysis",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    table_data = [[
        "Product",
        "Stock",
        "Reorder",
        "Revenue Risk"
    ]]

    for _, row in (
        inventory.head(15).iterrows()
    ):

        table_data.append([
            row["product_name"],
            row["stock_available"],
            row["reorder_level"],
            f"₹ {row['estimated_lost_revenue']:,.2f}"
        ])

    table = Table(
        table_data,
        colWidths=[
            220,
            70,
            70,
            120
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#1F4E78"
                )
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )
        ])
    )

    elements.append(
        table
    )

    elements.append(
        PageBreak()
    )

    
def create_returns_analysis(
    elements,
    styles,
    metrics
):
    """
    Returns analysis section.
    """

    elements.append(
        Paragraph(
            "Returns Analysis",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    return_rate = (
        metrics["return_rate"]
    )

    table_data = [[
        "Category",
        "Orders",
        "Returns",
        "Return Rate %"
    ]]

    for _, row in (
        return_rate.iterrows()
    ):

        table_data.append([
            row["category"],
            int(row["orders"]),
            int(row["returns"]),
            round(
                row["return_rate_pct"],
                2
            )
        ])

    table = Table(
        table_data
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#1F4E78"
                )
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )
        ])
    )

    elements.append(
        table
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Top Return Reasons",
            styles["Heading2"]
        )
    )

    reasons = (
        metrics["return_reasons"]
    )

    for _, row in reasons.iterrows():

        elements.append(
            Paragraph(
                f"• {row.iloc[0]}",
                styles["Normal"]
            )
        )

        
def add_page_header_footer(
    canvas,
    doc
):
    """
    Corporate header/footer.
    """

    canvas.saveState()

    canvas.setFillColor(
        colors.HexColor(
            "#1F4E78"
        )
    )

    canvas.rect(
        0,
        810,
        700,
        20,
        fill=1
    )

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(
        colors.grey
    )

    canvas.drawCentredString(
        300,
        20,
        f"RetailCore Pvt. Ltd. | Page {doc.page}"
    )

    canvas.restoreState()

    
def create_product_analysis(
    elements,
    styles,
    metrics
):
    """
    Top and bottom products analysis.
    """

    elements.append(
        Paragraph(
            "Product Performance Analysis",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # Top Products

    elements.append(
        Paragraph(
            "Top 5 Products",
            styles["Heading2"]
        )
    )

    top_products = metrics[
        "top_products"
    ]

    top_data = [[
        "Product",
        "Revenue"
    ]]

    for _, row in top_products.iterrows():

        top_data.append([
            row["product_name"],
            f"Rs. {row['net_revenue']:,.2f}"
        ])

    top_table = Table(
        top_data,
        colWidths=[300, 150]
    )

    top_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,0),
             colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0,0), (-1,0),
             colors.white),
            ("GRID", (0,0), (-1,-1),
             1, colors.black)
        ])
    )

    elements.append(
        top_table
    )

    elements.append(
        Spacer(1, 20)
    )

    # Bottom Products

    elements.append(
        Paragraph(
            "Bottom 5 Products",
            styles["Heading2"]
        )
    )

    bottom_products = metrics[
        "bottom_products"
    ]

    bottom_data = [[
        "Product",
        "Revenue"
    ]]

    for _, row in bottom_products.iterrows():

        bottom_data.append([
            row["product_name"],
            f"Rs. {row['net_revenue']:,.2f}"
        ])

    bottom_table = Table(
        bottom_data,
        colWidths=[300, 150]
    )

    bottom_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,0),
             colors.HexColor("#C0504D")),
            ("TEXTCOLOR", (0,0), (-1,0),
             colors.white),
            ("GRID", (0,0), (-1,-1),
             1, colors.black)
        ])
    )

    elements.append(
        bottom_table
    )

    elements.append(
        PageBreak()
    )

    
def create_business_insights(
    elements,
    styles,
    metrics
):
    """
    Executive business insights.
    """

    elements.append(
        Paragraph(
            "Business Insights",
            styles["Heading1"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    sales = metrics["sales"]

    total_revenue = round(
        sales["net_revenue"].sum(),
        2
    )

    top_region = (
        metrics["region_revenue"]
        .iloc[0]["region"]
    )

    inventory_risk = len(
        metrics["inventory_health"]
    )

    top_return_reason = (
        metrics["return_reasons"]
        .iloc[0, 0]
    )

    insights = [

        f"• Total revenue generated was Rs. {total_revenue:,.2f}.",

        f"• {top_region} region delivered the highest revenue performance.",

        f"• {inventory_risk} products are currently below reorder level.",

        f"• Most common return reason was '{top_return_reason}'.",

        "• Inventory replenishment should be prioritised for high-value products.",

        "• Product performance indicates opportunities for inventory optimisation."

    ]

    for insight in insights:

        elements.append(
            Paragraph(
                insight,
                styles["Normal"]
            )
        )

        elements.append(
            Spacer(1, 8)
        )

    elements.append(
        PageBreak()
    )

    
    
def generate_pdf_report(
    metrics,output_dir
):
    """
    Generate PDF MIS report.
    """

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_dir = Path(output_dir)
    
    print("output_dir:>>>>>",output_dir)

    pdf_file = (
        output_dir /
        f"MIS_Summary_{datetime.now():%Y%m%d}.pdf"
    )

    doc = SimpleDocTemplate(
        str(pdf_file)
    )

    styles = get_styles()

    elements = []

    build_report_sections(
        elements,
        styles,
        metrics
    )

    doc.build(
        elements,
        onFirstPage=add_page_header_footer,
        onLaterPages=add_page_header_footer
    )

    return str(pdf_file)

    
def build_report_sections(
    elements,
    styles,
    metrics
):
    """
    Build all report sections.
    """

    create_cover_page(
        elements,
        styles
    )

    create_executive_summary(
        elements,
        styles,
        metrics
    )

    create_business_insights(
        elements,
        styles,
        metrics
    )


    create_revenue_analysis(
        elements,
        styles,
        metrics
    )

    create_product_analysis(
        elements,
        styles,
        metrics
    )

    create_inventory_analysis(
        elements,
        styles,
        metrics
    )

    create_returns_analysis(
        elements,
        styles,
        metrics
    )