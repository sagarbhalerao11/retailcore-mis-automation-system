"""
charts.py

Generates charts used in both
Excel and PDF MIS reports.

Author: Sagar
"""

from pathlib import Path
import logging

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# CONSTANTS
# ==========================================================

CHARTS_DIR = Path("charts")
CHARTS_DIR.mkdir(exist_ok=True)


# ==========================================================
# CHART GENERATION FUNCTIONS
# ==========================================================

def generate_weekly_revenue_chart(
    weekly_trend: pd.DataFrame
) -> str:
    """
    Generate weekly revenue trend chart.

    Parameters
    ----------
    weekly_trend : pd.DataFrame
        DataFrame containing:
        date
        net_revenue

    Returns
    -------
    str
        Path to saved chart image.
    """

    try:
        output_path = (
            CHARTS_DIR /
            "weekly_revenue_trend.png"
        )

        plt.figure(figsize=(12, 6))

        plt.plot(
            weekly_trend["date"],
            weekly_trend["net_revenue"],
            marker="o"
        )

        plt.title("Weekly Revenue Trend")
        plt.xlabel("Week")
        plt.ylabel("Net Revenue")
        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        logging.info(
            "Weekly revenue chart created."
        )

        return str(output_path)

    except Exception as exc:
        logging.exception(
            "Failed to generate weekly chart."
        )
        raise exc


def generate_region_revenue_chart(
    region_revenue: pd.DataFrame
) -> str:
    """
    Generate region revenue bar chart.

    Parameters
    ----------
    region_revenue : pd.DataFrame

    Returns
    -------
    str
        Saved chart path.
    """

    try:
        output_path = (
            CHARTS_DIR /
            "region_revenue.png"
        )

        plt.figure(figsize=(10, 6))

        plt.bar(
            region_revenue["region"],
            region_revenue["net_revenue"]
        )

        plt.title(
            "Revenue by Region"
        )

        plt.xlabel("Region")
        plt.ylabel("Net Revenue")

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        logging.info(
            "Region revenue chart created."
        )

        return str(output_path)

    except Exception as exc:
        logging.exception(
            "Failed to generate region chart."
        )
        raise exc


# ==========================================================
# GENERATE ALL CHARTS
# ==========================================================

def generate_all_charts(
    metrics: dict
) -> dict:
    """
    Generate all report charts.

    Parameters
    ----------
    metrics : dict
        Analytics output.

    Returns
    -------
    dict
        Chart file paths.
    """

    return {
        "weekly_trend_chart":
            generate_weekly_revenue_chart(
                metrics["weekly_trend"]
            ),

        "region_revenue_chart":
            generate_region_revenue_chart(
                metrics["region_revenue"]
            )
    }
