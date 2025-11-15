import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import DataProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Bakery Sales Dashboard",
    page_icon="🍞",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🍰 Bakery Sales Dashboard")
st.markdown("Visualizing daily performance from the bakery sales database or CSV backup.")

# Initialize data processor
@st.cache_resource
def get_data_processor():
    return DataProcessor()

data_processor = get_data_processor()

# --- LOAD DATA ---
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_cached_data():
    data = data_processor.load_data()

    if data.empty:
        st.error("No data available from database or CSV backup")
        return pd.DataFrame()

    # Calculate metrics
    data = data_processor.calculate_metrics(data)
    return data

data = load_cached_data()

if not data.empty:
    # Get summary stats
    summary = data_processor.get_summary_stats(data)

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔍 Filters")

    # City filter
    cities = data["city"].unique()
    selected_cities = st.sidebar.multiselect(
        "Select City",
        options=list(cities),
        default=list(cities)
    )

    # Product filter
    products = data["product"].unique()
    selected_products = st.sidebar.multiselect(
        "Select Product",
        options=list(products),
        default=list(products)
    )

    # Apply filters
    df_filtered = data[
        (data["city"].isin(selected_cities)) &
        (data["product"].isin(selected_products))
        ]

    # --- KPIs ---
    st.header("📊 Key Performance Indicators")

    total_revenue = round(df_filtered["revenue"].sum(), 2)
    total_profit = round(df_filtered["profit"].sum(), 2)
    avg_price = round(df_filtered["unit_price"].mean(), 2)
    profit_margin = round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
    col3.metric("🏷️ Avg. Price", f"${avg_price:.2f}")
    col4.metric("📊 Profit Margin", f"{profit_margin}%")

    st.markdown("---")

    # --- CHARTS ---
    st.header("📈 Performance Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by City")
        if not df_filtered.empty:
            city_rev = df_filtered.groupby("city")["revenue"].sum().reset_index().sort_values("revenue",
                                                                                              ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="city", y="revenue", data=city_rev, palette="magma", ax=ax)
            ax.set_ylabel("Revenue ($)")
            ax.set_xlabel("City")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No data available for selected filters")

    with col2:
        st.subheader("Profit by Product")
        if not df_filtered.empty:
            prod_profit = df_filtered.groupby("product")["profit"].sum().reset_index().sort_values("profit",
                                                                                                   ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="product", y="profit", data=prod_profit, palette="crest", ax=ax)
            ax.set_ylabel("Profit ($)")
            ax.set_xlabel("Product")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No data available for selected filters")

    # Additional charts
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Units Sold by Product")
        if not df_filtered.empty:
            units_sold = df_filtered.groupby("product")["units_sold"].sum().reset_index().sort_values("units_sold",
                                                                                                      ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="product", y="units_sold", data=units_sold, palette="plasma", ax=ax)
            ax.set_ylabel("Units Sold")
            ax.set_xlabel("Product")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No data available for selected filters")

    with col4:
        st.subheader("Top Performing Cities")
        if not df_filtered.empty:
            # Create a simple summary of top cities
            city_summary = df_filtered.groupby("city").agg({
                'revenue': 'sum',
                'profit': 'sum'
            }).reset_index()
            st.dataframe(city_summary.sort_values('revenue', ascending=False), use_container_width=True)
        else:
            st.info("No data available for selected filters")

    st.markdown("---")

    # --- DATA TABLE ---
    st.header("📋 Detailed Sales Data")

    # Show summary statistics
    if summary:
        st.subheader("Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Top City", summary.get('top_city', 'N/A'))
        with col2:
            st.metric("Top Product", summary.get('top_product', 'N/A'))
        with col3:
            st.metric("Total Transactions", summary.get('total_transactions', 0))
        with col4:
            st.metric("Lowest Margin City", summary.get('lowest_margin_city', 'N/A'))

    # Data table
    st.subheader("Raw Data")
    if not df_filtered.empty:
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True
        )

        # Download button for filtered data
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="bakery_sales_filtered.csv",
            mime="text/csv"
        )
    else:
        st.info("No data available for selected filters")

else:
    st.error("""
    ❌ No data available. Please check:

    **Database Connection:**
    - Ensure PostgreSQL is running
    - Check database credentials in `.env` file
    - Verify the 'sales' table exists in your database

    **CSV Backup:**
    - Ensure 'cleaned_bakery_sales.csv' exists in the project directory
    - Or update CSV_BACKUP_PATH in config.py

    **Troubleshooting Steps:**
    1. Check the logs in the 'logs' directory
    2. Verify your database connection settings
    3. Ensure the CSV file is in the correct location
    """)

# --- FOOTER ---
st.markdown("---")
st.caption("👩‍💻 Built by Mohammad Sakil Hossain | Data Analytics Course — Day 21 (Portfolio Project) | Powered by Streamlit 🌐")