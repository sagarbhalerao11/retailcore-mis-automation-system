"""
Utility functions used throughout the
RetailCore MIS Automation System.

This module provides validation,
logging configuration, directory
management, and filesystem helper
functions.
"""

import os
import shutil
from pathlib import Path
import logging
from datetime import datetime as dt
import argparse

# --------------------------------------------------
# Validation
# --------------------------------------------------
            
def validate_schedule_time(
    schedule_time: str
) -> None:
    """
    Validate that the provided schedule time
    follows the HH:MM 24-hour format.

    Raises:
        argparse.ArgumentTypeError:
            If the time format is invalid.
    """
    logging.debug(
        "Schedule time received: %s",
        schedule_time
    )
    try:
        dt.strptime(
            schedule_time,
            "%H:%M"
        )
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Invalid time format. "
            "Use HH:MM."
        ) from exc

        
# --------------------------------------------------
# Logging
# --------------------------------------------------

def configure_logging(verbose: bool) -> None:
    """
    Configure application logging with either
    INFO or DEBUG level based on the verbose flag.
    """
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


# --------------------------------------------------
# Filesystem helpers
# --------------------------------------------------

def ensure_directories(*paths: str) -> None:
    """
    Create one or more directories if they do
    not already exist.
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)

def clean_output_directory(
    output_dir: str
) -> None:
    """
    Remove all files and subdirectories from
    the specified output directory.
    """

    path = Path(output_dir)

    if not path.exists():
        return

    for item in path.iterdir():

        try:

            if item.is_file():
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)

        except Exception as exc:

            logging.warning(
                "Failed removing %s : %s",
                item,
                exc
            )

            
def validate_columns(
    df,
    required_columns
):
    """
    Verify that a DataFrame contains all
    required columns.

    Raises:
        ValueError:
            If one or more required columns
            are missing.
    """

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

