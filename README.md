# 🥐 Bakery Sales Analytics Dashboard

A comprehensive analytics dashboard for bakery sales data that provides insights into revenue trends, profitability, and performance metrics across products and cities.

## 📋 Project Overview

This project analyzes bakery sales data to help business owners understand their performance, identify top-selling products, and optimize operations across different cities.

## ✨ Key Features

- **📊 Interactive Dashboard**: Dynamic filters for cities and products
- **🔄 Automated Data Pipeline**: Daily data fetching from PostgreSQL
- **📈 Revenue & Profit Analysis**: Comprehensive financial metrics
- **📤 Report Generation**: Automated Excel/PDF report export
- **📧 Email Delivery**: Scheduled report distribution
- **🔍 Performance Insights**: Identify top performers and areas for improvement

## 🛠 Tech Stack

- **Backend**: PostgreSQL, Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Frontend**: Streamlit
- **Reporting**: OpenPyXL, FPDF

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- Streamlit

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/softdevsakil/bakery-dashboard.git
   cd bakery-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your database credentials and email settings
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
bakery-dashboard/
├── app.py                 # Main Streamlit application
├── data_processor.py      # Data fetching and processing
├── report_generator.py    # Excel/PDF report generation
├── email_sender.py        # Automated email delivery
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── bakery_sales.csv       # Dummy data, if not able to connect database
├── reports/               # Generated PDF & CSV will store here
├── logs/                  # Data generation logs will store here
└── README.md              # Project documentation
```

## 🔧 Configuration

### Database Setup
Configure your PostgreSQL connection in `config.py`:

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'bakery_sales',
    'user': 'your_username',
    'password': 'your_password'
}
```

### Email Configuration
Set up email notifications in the environment variables:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## 📊 Key Insights

### 🏆 Top Performers
- **Highest Revenue City**: Sylhet
- **Most Profitable Product**: Croissant
- **Best Margin Product**: Croissant

### 📈 Performance Metrics
- Total revenue trends over time
- Product-wise profitability analysis
- City-wise performance comparison
- Seasonal sales patterns

### 🎯 Improvement Opportunities
- **Dhaka**: Lowest margins, needs promotional strategies
- **Underperforming Products**: Identify and optimize pricing
- **Seasonal Opportunities**: Capitalize on peak sales periods

## 🌐 Live Demo

Check out the live dashboard:  
**[https://bakery-dashboard.streamlit.app/](https://bakery-dashboard.streamlit.app/)**

## 📱 Usage Guide

### Dashboard Navigation
1. **Overview Tab**: High-level metrics and trends
2. **Product Analysis**: Detailed product performance
3. **City Performance**: Regional sales analysis
4. **Reports**: Generate and download custom reports

### Filter Options
- Select specific cities or products
- Filter by product categories

### Report Generation
- **Excel Reports**: Detailed data with charts
- **PDF Summaries**: Executive summary with key insights
- **Automated Delivery**: Schedule daily/weekly reports

## 🔄 Data Pipeline

1. **Data Extraction**: Automated daily fetch from PostgreSQL
2. **Data Cleaning**: Handle missing values and outliers
3. **Feature Engineering**: Calculate revenue, profit margins
4. **Analysis**: Generate insights and visualizations
5. **Reporting**: Create and distribute reports

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- 📧 Email: softdevsakil@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/softdevsakil/bakery-dashboard/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/softdevsakil/bakery-dashboard/discussions)

## 🙏 Acknowledgments

- Data provided by [Dummy Sales Data from Prime Bread & Bakery](#)
- Icons by [Icon Library](#)
- Built with [Streamlit](https://streamlit.io/)

---

**⭐ If you find this project helpful, please give it a star on GitHub!**