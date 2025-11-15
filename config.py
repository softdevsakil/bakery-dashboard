import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'bakery_sales'),
    'user': os.getenv('DB_USER', 'your_username'),
    'password': os.getenv('DB_PASSWORD', 'your_db_pass')
}

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'email_user': os.getenv('EMAIL_USER', 'your_email@gmail.com'),
    'email_password': os.getenv('EMAIL_PASSWORD', 'your_app_password'),
    'to_email': os.getenv('TO_EMAIL', 'to_your_boss@gmail.com')
}

# File Paths
REPORTS_DIR = 'reports'
LOGS_DIR = 'logs'
CSV_BACKUP_PATH = 'bakery_sales.csv'

# Create necessary directories
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)