"""
scheduler.py
Handles scheduled execution of MIS pipeline.
"""

import time
import schedule
import logging
from datetime import datetime as dt

from core.pipeline import MISPipeline


def start_scheduler(args) -> None:
    """
    Start daily scheduled pipeline execution.
    """

    # validate again for safety (optional but good practice)
    try:
        dt.strptime(args.schedule_time, "%H:%M")
    except ValueError:
        raise ValueError(
            "Invalid schedule time. Use HH:MM format."
        )

    def job():
        logging.info("Scheduled pipeline started")
        MISPipeline(args).run()
        logging.info("Scheduled pipeline finished")

    schedule.every().day.at(args.schedule_time).do(job)

    print(f"Pipeline scheduled daily at {args.schedule_time}")

    while True:
        schedule.run_pending()
        time.sleep(60)