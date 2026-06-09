"""
main.py

RetailCore MIS Automation System
Main application entry point.
"""
from __future__ import annotations

import argparse
import logging

from core.pipeline import MISPipeline

from core.pipeline import MISPipeline
from core.scheduler import start_scheduler
from core.utilities import (
    validate_schedule_time,
    configure_logging,
    ensure_directories
)


VERSION = "1.0.0"

# --------------------------------------------------
# CLI
# --------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """
    Create CLI parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "RetailCore MIS Automation "
            "System"
        )
    )

    parser.add_argument(
        "--input-dir",
        default="input",
        help="Input directory path"
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory path"
    )

    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run daily scheduler"
    )

    parser.add_argument(
        "--schedule-time",
        default="08:00",
        help=(
            "Schedule time in HH:MM "
            "(default: 08:00)"
        )
    )

    parser.add_argument(
        "--generate-data-only",
        action="store_true",
        help="Generate mock data only"
    )

    parser.add_argument(
        "--analytics-only",
        action="store_true",
        help="Run analytics only"
    )

    parser.add_argument(
        "--charts-only",
        action="store_true",
        help="Generate charts only"
    )

    parser.add_argument(
        "--excel-only",
        action="store_true",
        help="Generate Excel report only"
    )

    parser.add_argument(
        "--pdf-only",
        action="store_true",
        help="Generate PDF report only"
    )

    parser.add_argument(
        "--skip-data-generation",
        action="store_true",
        help="Skip data generation"
    )

    parser.add_argument(
        "--skip-charts",
        action="store_true",
        help="Skip chart generation"
    )

    parser.add_argument(
        "--skip-excel",
        action="store_true",
        help="Skip Excel generation"
    )

    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="Skip PDF generation"
    )

    parser.add_argument(
        "--clean-output",
        action="store_true",
        help="Clean output directory"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate pipeline only"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=(
            f"RetailCore MIS "
            f"Automation System "
            f"v{VERSION}"
        )
    )

    return parser


# --------------------------------------------------
# Main
# --------------------------------------------------

def main() -> None:
    """
    Application entry point.
    """

    parser = build_parser()

    args = parser.parse_args()

    validate_schedule_time(
        args.schedule_time
    )

    configure_logging(
        args.verbose
    )

    ensure_directories(args.input_dir, args.output_dir)

    print(
        f"Input Directory  : {args.input_dir}"
    )

    print(
        f"Output Directory : {args.output_dir}"
    )

    logging.info(
        "Input Directory: %s",
        args.input_dir
    )

    logging.info(
        "Output Directory: %s",
        args.output_dir
    )

    if args.schedule:
        start_scheduler(args)
    else:
        MISPipeline(args).run()

if __name__ == "__main__":
    main()
