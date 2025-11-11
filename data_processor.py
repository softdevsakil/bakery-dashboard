# # data_processor.py
# import pandas as pd
# import psycopg2
# from config import DB_CONFIG, CSV_BACKUP_PATH
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class DataProcessor:
#     def __init__(self):
#         self.db_config = DB_CONFIG
#         self.csv_backup_path = CSV_BACKUP_PATH
#
#     def connect_to_db(self):
#         """Establish connection to PostgreSQL database"""
#         try:
#             conn = psycopg2.connect(**self.db_config)
#             return conn
#         except Exception as e:
#             logger.error(f"Database connection failed: {e}")
#             return None
#
#     def load_data_from_db(self):
#         """Load data from PostgreSQL database"""
#         conn = self.connect_to_db()
#         if conn:
#             try:
#                 query = "SELECT * FROM sales"
#                 data = pd.read_sql_query(query, conn)
#                 conn.close()
#                 logger.info("Data loaded successfully from database")
#                 return data
#             except Exception as e:
#                 logger.error(f"Error loading data from database: {e}")
#                 conn.close()
#                 return None
#         return None
#
#     def load_data_from_csv(self):
#         """Load data from CSV backup"""
#         try:
#             data = pd.read_csv(self.csv_backup_path)
#             logger.info("Data loaded successfully from CSV backup")
#             return data
#         except Exception as e:
#             logger.error(f"Error loading data from CSV: {e}")
#             return None
#
#     def load_data(self):
#         """Load data with fallback mechanism"""
#         data = self.load_data_from_db()
#         if data is None or data.empty:
#             data = self.load_data_from_csv()
#         return data or pd.DataFrame()
#
#     def calculate_metrics(self, data):
#         """Calculate revenue and profit metrics"""
#         if data.empty:
#             return data
#
#         data = data.copy()
#         data["revenue"] = data["units_sold"] * data["unit_price"]
#         data["profit"] = (data["unit_price"] - data["cost_per_unit"]) * data["units_sold"]
#
#         return data
#
#     def get_summary_stats(self, data):
#         """Generate summary statistics"""
#         if data.empty:
#             return {}
#
#         summary = {
#             "total_revenue": data["revenue"].sum(),
#             "total_profit": data["profit"].sum(),
#             "avg_unit_price": data["unit_price"].mean(),
#             "top_city": data.groupby("city")["revenue"].sum().idxmax(),
#             "top_product": data.groupby("product")["profit"].sum().idxmax(),
#             "lowest_margin_city": data.groupby("city")["profit"].mean().idxmin(),
#             "total_transactions": len(data)
#         }
#
#         return summary

import pandas as pd
import psycopg2
from config import DB_CONFIG, CSV_BACKUP_PATH
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.db_config = DB_CONFIG
        self.csv_backup_path = CSV_BACKUP_PATH

    def connect_to_db(self):
        """Establish connection to PostgreSQL database"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None

    def load_data_from_db(self):
        """Load data from PostgreSQL database"""
        conn = self.connect_to_db()
        if conn:
            try:
                query = "SELECT * FROM sales"
                data = pd.read_sql_query(query, conn)
                conn.close()
                logger.info("Data loaded successfully from database")
                return data
            except Exception as e:
                logger.error(f"Error loading data from database: {e}")
                if conn:
                    conn.close()
                return None
        return None

    def load_data_from_csv(self):
        """Load data from CSV backup"""
        try:
            data = pd.read_csv(self.csv_backup_path)
            logger.info("Data loaded successfully from CSV backup")
            return data
        except FileNotFoundError:
            logger.warning(f"CSV backup file not found: {self.csv_backup_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading data from CSV: {e}")
            return None

    def load_data(self):
        """Load data with fallback mechanism"""
        # Try database first
        data = self.load_data_from_db()

        # If database fails or returns empty, try CSV
        if data is None or data.empty:
            logger.info("Trying CSV backup...")
            data = self.load_data_from_csv()

        # If both methods fail, return empty DataFrame
        if data is None:
            logger.error("Both database and CSV backup failed to load data")
            return pd.DataFrame()

        return data

    def calculate_metrics(self, data):
        """Calculate revenue and profit metrics"""
        if data.empty:
            return data

        data = data.copy()
        data["revenue"] = data["units_sold"] * data["unit_price"]
        data["profit"] = (data["unit_price"] - data["cost_per_unit"]) * data["units_sold"]

        return data

    def get_summary_stats(self, data):
        """Generate summary statistics"""
        if data.empty:
            return {}

        try:
            # Calculate profit margin per row first
            data_with_margin = data.copy()
            data_with_margin['profit_margin'] = (data_with_margin['profit'] / data_with_margin['revenue']) * 100

            summary = {
                "total_revenue": data["revenue"].sum(),
                "total_profit": data["profit"].sum(),
                "avg_unit_price": data["unit_price"].mean(),
                "top_city": data.groupby("city")["revenue"].sum().idxmax(),
                "top_product": data.groupby("product")["profit"].sum().idxmax(),
                "total_transactions": len(data)
            }

            # Safely calculate lowest margin city
            try:
                city_margins = data_with_margin.groupby("city")["profit_margin"].mean()
                summary["lowest_margin_city"] = city_margins.idxmin()
            except:
                summary["lowest_margin_city"] = "N/A"

            return summary

        except Exception as e:
            logger.error(f"Error calculating summary stats: {e}")
            return {}