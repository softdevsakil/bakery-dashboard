import schedule
import time
import subprocess
import logging
import os
from datetime import date
from data_processor import DataProcessor
from report_generator import ReportGenerator
from email_sender import EmailSender

# Configure logging
logging.basicConfig(
    filename="logs/report_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_daily_report():
    """Main function to run the daily report pipeline"""
    logging.info("Daily report execution started")

    try:
        # Initialize components
        data_processor = DataProcessor()
        report_generator = ReportGenerator()
        email_sender = EmailSender()

        # Load and process data
        data = data_processor.load_data()
        if data.empty:
            logging.error("No data available for report generation")
            return

        data = data_processor.calculate_metrics(data)
        summary = data_processor.get_summary_stats(data)

        print("Summary Statistics:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

        # Generate reports
        excel_file = report_generator.generate_excel_report(data, summary)
        pdf_file = report_generator.generate_pdf_report(data, summary)

        # Send email with attachments
        if excel_file or pdf_file:
            email_sender.send_report(excel_file, pdf_file)

        logging.info("Daily report completed successfully")

    except Exception as e:
        logging.error(f"Error in daily report: {e}")
        print(f"Error: {e}")


def main():
    """Main function with scheduler"""
    print("Bakery Analytics System - Daily Report Generator")

    # Create necessary directories
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Run immediately on start
    run_daily_report()

    # Schedule daily execution at 4:30 PM
    schedule.every().day.at("09:00").do(run_daily_report)

    print("Scheduler started. Press Ctrl+C to stop.")
    print("Next report scheduled for 9:00 AM daily.")

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()