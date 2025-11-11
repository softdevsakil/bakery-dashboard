import smtplib
from email.message import EmailMessage
from email.utils import formatdate
import os
from datetime import date
from config import EMAIL_CONFIG
import logging

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.email_config = EMAIL_CONFIG

    def send_report(self, excel_file_path=None, pdf_file_path=None):
        """Send daily report via email with attachments"""
        today = date.today().strftime("%Y-%m-%d")

        try:
            msg = EmailMessage()
            msg["Subject"] = f"Daily Bakery Sales Report - {today}"
            msg["From"] = self.email_config['email_user']
            msg["To"] = self.email_config['to_email']
            msg["Date"] = formatdate(localtime=True)

            # Email body
            body = """
            Hello,

            Please find attached the daily bakery sales report.

            Key highlights:
            • Revenue and profit analysis
            • Top performing products and cities
            • Detailed transaction data

            Best regards,
            Bakery Analytics System
            """

            msg.set_content(body)

            # Attach Excel file
            if excel_file_path and os.path.exists(excel_file_path):
                with open(excel_file_path, "rb") as f:
                    file_data = f.read()
                    msg.add_attachment(
                        file_data,
                        maintype="application",
                        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename=os.path.basename(excel_file_path)
                    )

            # Attach PDF file
            if pdf_file_path and os.path.exists(pdf_file_path):
                with open(pdf_file_path, "rb") as f:
                    file_data = f.read()
                    msg.add_attachment(
                        file_data,
                        maintype="application",
                        subtype="pdf",
                        filename=os.path.basename(pdf_file_path)
                    )

            # Send email
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as smtp:
                smtp.starttls()
                smtp.login(self.email_config['email_user'], self.email_config['email_password'])
                smtp.send_message(msg)

            logger.info("Report emailed successfully!")
            print("Report emailed successfully!")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            print(f"Error sending email: {e}")
            return False