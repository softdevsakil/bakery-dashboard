# report_generator.py
import pandas as pd
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from datetime import date
import os
from config import REPORTS_DIR


class ReportGenerator:
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_excel_report(self, data, summary):
        """Generate Excel report with raw data and summary"""
        today = date.today().strftime("%Y-%m-%d")
        filename = f"{self.reports_dir}/daily_sales_report_{today}.xlsx"

        try:
            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                # Raw data sheet
                data.to_excel(writer, sheet_name="Raw_Data", index=False)

                # Summary sheet
                summary_df = pd.DataFrame([summary])
                summary_df.to_excel(writer, sheet_name="Summary", index=False)

                # Analytics sheet with key metrics
                analytics_data = {
                    'Metric': ['Total Revenue', 'Total Profit', 'Average Unit Price', 'Top City', 'Top Product'],
                    'Value': [
                        f"${summary.get('total_revenue', 0):.2f}",
                        f"${summary.get('total_profit', 0):.2f}",
                        f"${summary.get('avg_unit_price', 0):.2f}",
                        summary.get('top_city', 'N/A'),
                        summary.get('top_product', 'N/A')
                    ]
                }
                pd.DataFrame(analytics_data).to_excel(writer, sheet_name="Analytics", index=False)

            print(f"Excel report saved as {filename}")
            return filename
        except Exception as e:
            print(f"Error generating Excel report: {e}")
            return None

    def generate_pdf_report(self, data, summary):
        """Generate PDF report with formatted content"""
        today = date.today().strftime("%Y-%m-%d")
        filename = f"{self.reports_dir}/daily_sales_report_{today}.pdf"

        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title = Paragraph("Daily Bakery Sales Report", styles["Title"])
            story.append(title)
            story.append(Spacer(1, 12))

            # Date
            date_para = Paragraph(f"Date: {today}", styles["Normal"])
            story.append(date_para)
            story.append(Spacer(1, 12))

            # Summary section
            summary_title = Paragraph("Key Performance Indicators", styles["Heading2"])
            story.append(summary_title)
            story.append(Spacer(1, 6))

            # Summary table
            summary_data = [
                ['Metric', 'Value'],
                ['Total Revenue', f"${summary.get('total_revenue', 0):.2f}"],
                ['Total Profit', f"${summary.get('total_profit', 0):.2f}"],
                ['Average Unit Price', f"${summary.get('avg_unit_price', 0):.2f}"],
                ['Top Performing City', summary.get('top_city', 'N/A')],
                ['Most Profitable Product', summary.get('top_product', 'N/A')],
                ['Total Transactions', str(summary.get('total_transactions', 0))]
            ]

            table = Table(summary_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(table)
            story.append(Spacer(1, 12))

            # Insights section
            insights_title = Paragraph("Business Insights", styles["Heading2"])
            story.append(insights_title)
            story.append(Spacer(1, 6))

            insights = [
                f"• {summary.get('top_city', 'N/A')} generates the highest revenue",
                f"• {summary.get('top_product', 'N/A')} is the most profitable product",
                f"• Consider promotions in {summary.get('lowest_margin_city', 'N/A')} to improve margins"
            ]

            for insight in insights:
                story.append(Paragraph(insight, styles["Normal"]))
                story.append(Spacer(1, 3))

            doc.build(story)
            print(f"PDF report saved as {filename}")
            return filename

        except Exception as e:
            print(f"Error generating PDF report: {e}")
            return None