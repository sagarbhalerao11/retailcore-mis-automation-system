import logging

from .analytics import run_analytics
from .charts import generate_all_charts
from .data_generator import save_files
from .ingestion import process_data
from .pdf_report import generate_pdf_report
from .report_generator import generate_excel_report
from .utilities import clean_output_directory


class MISPipeline:
    """
    End-to-end MIS automation pipeline responsible for
    data generation, ingestion, analytics, chart creation,
    report generation, and pipeline orchestration.
    """

    def __init__(self, args):
        self.args = args
        self.input_dir = args.input_dir
        self.output_dir = args.output_dir

    # -------------------------
    # PUBLIC ENTRY POINT
    # -------------------------
    def run(self):
        """
            Execute the complete MIS pipeline workflow.

            The workflow includes data generation, ingestion,
            analytics, chart creation, report generation,
            and summary generation.
        """
        try:
            logging.info("Pipeline started")
            # -------------------------
            # CLEAN OUTPUT (STOP HERE IF TRUE)
            # -------------------------
            if self._clean_output():
                return


            #self._clean_output()
            self._handle_dry_run()

            if self._generate_data_only():
                return

            if not self.args.skip_data_generation:
                self._generate_data()

            sales, inventory, returns = self._load_data()
            metrics = self._run_analytics(sales, inventory, returns)

            if self._analytics_only():
                return

            #self._handle_charts(metrics)

            # -------------------------
            # CHARTS SECTION
            # -------------------------
            if self._should_run_charts():
                self._handle_charts(metrics)

                # if charts_only → STOP HERE
                if self.args.charts_only:
                    logging.info("Charts-only mode completed")
                    return
            
            
            self._handle_reports(metrics)

            self._print_summary(sales, inventory, returns)

            logging.info("Pipeline completed successfully")

        except Exception as exc:
            logging.exception("Pipeline execution failed")
            print(f"\nPipeline failed: {exc}")

    # -------------------------
    # STAGE 1: CLEAN OUTPUT
    # -------------------------
    def _clean_output(self):
        """
        Clean the output directory when the
        clean-output flag is enabled.
        """
        if self.args.clean_output:
            logging.info("Cleaning output directory")
            clean_output_directory(self.output_dir)
            logging.info("Output cleaned. Exiting pipeline.")
            return True

        return False

    # -------------------------
    # STAGE 2: DRY RUN
    # -------------------------
    def _handle_dry_run(self):
        """
        Validate pipeline configuration without
        executing any processing steps.
        """
        if self.args.dry_run:
            logging.info("Dry run successful")
            print("Dry run completed.")
            exit()

    # -------------------------
    # STAGE 3: DATA GENERATION ONLY
    # -------------------------
    def _generate_data_only(self):
        """
        Generate mock datasets and exit without
        running the remaining pipeline stages.
        """
        if self.args.generate_data_only:
            logging.info("Generating mock data only")
            save_files(self.input_dir)
            print("Mock data generated.")
            return True
        return False

    # -------------------------
    # STAGE 4: DATA GENERATION
    # -------------------------
    def _generate_data(self):
        """
        Generate mock sales, inventory,
        and returns datasets.
        """
        logging.info("Generating mock data")
        save_files(self.input_dir)

    # -------------------------
    # STAGE 5: LOAD DATA
    # -------------------------
    def _load_data(self):
        """
        Load and clean source datasets
        from the configured input directory.
        """
        logging.info("Loading data")
        return process_data()

    # -------------------------
    # STAGE 6: ANALYTICS
    # -------------------------
    def _run_analytics(self, sales, inventory, returns):
        """
        Compute all business metrics and
        analytical insights from processed data.
        """
        logging.info("Running analytics")
        return run_analytics(sales, inventory, returns)

    # -------------------------
    # ANALYTICS ONLY MODE
    # -------------------------
    def _analytics_only(self):
        """
        Exit the pipeline after analytics
        processing when analytics-only mode
        is enabled.
        """
        if self.args.analytics_only:
            print("Analytics completed.")
            return True
        return False

    # -------------------------
    # STAGE 7: CHARTS
    # -------------------------
    # -------------------------
    # CHARTS DECISION BLOCK
    # -------------------------
    def _should_run_charts(self) -> bool:
        """
        Determine whether chart generation
        should be executed based on CLI flags.
        """
        # charts_only overrides everything
        if self.args.charts_only:
            return True

        # skip_charts disables charts unless charts_only is set
        if self.args.skip_charts:
            return False

        # default behavior
        return True

    def _handle_charts(self, metrics):
        """
        Generate all visualizations required
        for reports and dashboard display.
        """
        logging.info("Generating charts")
        generate_all_charts(metrics)
        print("Charts generated.")

    # -------------------------
    # STAGE 8: REPORTS
    # -------------------------
    def _handle_reports(self, metrics):
        """
        Generate all configured report outputs,
        including Excel and PDF reports.
        """
        self._excel_report(metrics)
        self._pdf_report(metrics)

    def _excel_report(self, metrics):
        """
        Generate the Excel MIS report
        based on calculated business metrics.
        """
        if self.args.excel_only:
            path = generate_excel_report(metrics, self.output_dir)
            print(f"Excel Report: {path}")
            exit()

        if not self.args.skip_excel:
            logging.info("Generating Excel report")
            path = generate_excel_report(metrics, self.output_dir)
            logging.info("Excel report created: %s", path)

    def _pdf_report(self, metrics):
        """
        Generate the PDF executive summary
        report from analytical results.
        """
        if self.args.pdf_only:
            path = generate_pdf_report(metrics, self.output_dir)
            print(f"PDF Report: {path}")
            exit()

        if not self.args.skip_pdf:
            logging.info("Generating PDF report")
            path = generate_pdf_report(metrics, self.output_dir)
            logging.info("PDF report created: %s", path)

    # -------------------------
    # STAGE 9: SUMMARY
    # -------------------------
    def _print_summary(self, sales, inventory, returns):
        """
        Display a summary of pipeline execution,
        processed records, and completion status.
        """
        print("\n===== PIPELINE SUMMARY =====")
        print(f"Sales Rows      : {len(sales)}")
        print(f"Inventory Rows  : {len(inventory)}")
        print(f"Returns Rows    : {len(returns)}")
        print("Pipeline Status : SUCCESS")
