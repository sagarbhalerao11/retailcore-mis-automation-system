"""
Data ingestion and cleaning module.

This module is responsible for loading source
datasets, validating schemas, cleaning sales
records, and preparing inventory data for
analytics processing.
"""

import pandas as pd
import logging
import os
from datetime import datetime as dt

log_dir = "logs"

log_file = os.path.join(
    log_dir,
    f"pipeline_{dt.now():%Y-%m-%d}.log"
)

os.makedirs(
    log_dir,
    exist_ok=True
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)

SALES_COLUMNS = [
    "order_id",
    "date",
    "product_id",
    "product_name",
    "category",
    "region",
    "quantity_sold",
    "unit_price",
    "discount_pct",
    "sales_rep"
]

INVENTORY_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "stock_available",
    "reorder_level",
    "last_restocked_date",
    "warehouse_location"
]

RETURNS_COLUMNS = [
    "return_id",
    "order_id",
    "product_id",
    "return_date",
    "return_reason",
    "refund_amount"
]


def validate_columns(
    df,
    expected_columns,
    file_name
):
    """
    Validate that the input DataFrame contains all
    required columns expected by the pipeline.

    Raises:
        ValueError: If any required column is missing.
    """

    missing = (
        set(expected_columns)
        -
        set(df.columns)
    )

    if missing:
        raise ValueError(
            f"{file_name} "
            f"missing columns: "
            f"{missing}"
        )


def load_data(
    input_dir="input"
):
    """
    Load sales, inventory, and returns datasets
    from CSV files and validate their schemas.
    """

    sales = pd.read_csv(
        f"{input_dir}/sales_data.csv"
    )

    inventory = pd.read_csv(
        f"{input_dir}/inventory_data.csv"
    )

    returns = pd.read_csv(
        f"{input_dir}/returns_data.csv"
    )

    validate_columns(
        sales,
        SALES_COLUMNS,
        "sales_data.csv"
    )

    validate_columns(
        inventory,
        INVENTORY_COLUMNS,
        "inventory_data.csv"
    )

    validate_columns(
        returns,
        RETURNS_COLUMNS,
        "returns_data.csv"
    )

    logging.info(
        "Files loaded successfully"
    )

    return (
        sales,
        inventory,
        returns
    )


def clean_sales_data(
    sales
):
    """
    Clean sales data by removing duplicate orders,
    filling missing discount values, removing
    negative quantity records, and converting
    date fields to datetime format.
    """

    original_rows = len(sales)

    duplicates = (
        sales.duplicated(
            subset="order_id"
        ).sum()
    )

    sales = (
        sales
        .drop_duplicates(
            subset="order_id",
            keep="first"
        )
        .copy()
    )

    logging.info(
        f"Removed "
        f"{duplicates} duplicates"
    )

    null_count = (
        sales["discount_pct"]
        .isna()
        .sum()
    )

    sales["discount_pct"] = (
        sales["discount_pct"]
        .fillna(0)
    )

    logging.info(
        f"Filled "
        f"{null_count} "
        f"discount nulls"
    )

    negative_rows = (
        sales["quantity_sold"] < 0
    ).sum()

    sales = sales[
        sales["quantity_sold"] >= 0
    ].copy()

    logging.info(
        f"Removed "
        f"{negative_rows} "
        f"negative quantity rows"
    )

    sales["date"] = pd.to_datetime(
        sales["date"]
    )

    logging.info(
        f"Sales cleaned. "
        f"{original_rows} -> "
        f"{len(sales)} rows"
    )

    return sales


def clean_inventory_data(
    inventory
):
    """
    Calculate inventory reorder flags based on
    available stock and reorder levels.
    """

    inventory[
        "reorder_flag"
    ] = (
        inventory[
            "stock_available"
        ]
        <
        inventory[
            "reorder_level"
        ]
    )

    flagged = (
        inventory[
            "reorder_flag"
        ]
        .sum()
    )

    logging.info(
        f"{flagged} "
        f"products marked "
        f"for reorder"
    )

    return inventory

def process_data():
    """
    Execute the complete data ingestion and
    cleaning workflow and return processed
    sales, inventory, and returns datasets.
    """

    sales, inventory, returns = (
        load_data()
    )

    sales = clean_sales_data(
        sales
    )

    inventory = (
        clean_inventory_data(
            inventory
        )
    )

    return (
        sales,
        inventory,
        returns
    )