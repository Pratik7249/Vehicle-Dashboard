import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.tseries.offsets import DateOffset
import numpy as np

def create_sample_data():
    """Creates a sample registrations.csv file for the app to run."""
    dates = pd.to_datetime(pd.date_range(start="2022-01-01", end="2025-08-15", freq="MS"))
    data = []
    manufacturers = {
        "Car": ["Toyota", "Ford", "Honda"],
        "Motorcycle": ["Harley-Davidson", "Yamaha", "Ducati"],
        "Truck": ["Volvo", "Scania", "MAN"]
    }
    base_registrations = {
        "Toyota": 2000, "Ford": 1800, "Honda": 2200,
        "Harley-Davidson": 800, "Yamaha": 1200, "Ducati": 500,
        "Volvo": 1500, "Scania": 1300, "MAN": 1400
    }

    for date in dates:
        for category, mfrs in manufacturers.items():
            for mfr in mfrs:
                month_factor = 1 + np.sin((date.month - 1) * (2 * np.pi / 12)) * 0.2
                noise = np.random.uniform(0.9, 1.1)
                registrations = int(base_registrations[mfr] * month_factor * noise)
                
                yoy_growth = np.random.uniform(-5, 15)
                qoq_growth = np.random.uniform(-10, 10)
                
                data.append([date, category, mfr, registrations, yoy_growth, qoq_growth])
    
    df = pd.DataFrame(data, columns=["Date", "Category", "Manufacturer", "Registrations", "YoY Growth %", "QoQ Growth %"])
    df.to_csv("registrations.csv", index=False)
    print("Sample 'registrations.csv' created.")

try:
    df = pd.read_csv("registrations.csv", parse_dates=["Date"])
except FileNotFoundError:
    create_sample_data()
    df = pd.read_csv("registrations.csv", parse_dates=["Date"])

st.set_page_config(layout="wide")
st.sidebar.header("Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) != 2:
    st.sidebar.warning("You must select a start and end date.")
    st.stop()

start_date, end_date = date_range
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

all_categories = sorted(df["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "Vehicle Category",
    all_categories,
    default=all_categories
)

all_manufacturers = sorted(df[df["Category"].isin(selected_categories)]["Manufacturer"].unique())
selected_manufacturers = st.sidebar.multiselect(
    "Manufacturer",
    all_manufacturers,
    default=all_manufacturers
)

mask = (
    (df["Date"] >= start_date) & (df["Date"] <= end_date) &
    (df["Category"].isin(selected_categories)) &
    (df["Manufacturer"].isin(selected_manufacturers))
)
filtered_df = df[mask].copy()

st.title("📊 Vehicle Registrations – Investor Dashboard")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
else:
   
    total_registrations = filtered_df['Registrations'].sum()

    prev_year_start = start_date - DateOffset(years=1)
    prev_year_end = end_date - DateOffset(years=1)
    prev_year_mask = (
        (df["Date"] >= prev_year_start) & (df["Date"] <= prev_year_end) &
        (df["Category"].isin(selected_categories)) &
        (df["Manufacturer"].isin(selected_manufacturers))
    )
    prev_year_total = df[prev_year_mask]['Registrations'].sum()
    
    yoy_growth = 0.0
    if prev_year_total > 0:
        yoy_growth = ((total_registrations - prev_year_total) / prev_year_total) * 100

    prev_qtr_start = start_date - DateOffset(months=3)
    prev_qtr_end = end_date - DateOffset(months=3)
    prev_qtr_mask = (
        (df["Date"] >= prev_qtr_start) & (df["Date"] <= prev_qtr_end) &
        (df["Category"].isin(selected_categories)) &
        (df["Manufacturer"].isin(selected_manufacturers))
    )
    prev_qtr_total = df[prev_qtr_mask]['Registrations'].sum()

    qoq_growth = 0.0
    if prev_qtr_total > 0:
        qoq_growth = ((total_registrations - prev_qtr_total) / prev_qtr_total) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registrations", f"{total_registrations:,.0f}")
    col2.metric(
        "YoY Growth %",
        f"{yoy_growth:.2f}%",
        f"vs. {prev_year_total:,.0f} (Prev. Year)"
    )
    col3.metric(
        "QoQ Growth %",
        f"{qoq_growth:.2f}%",
        f"vs. {prev_qtr_total:,.0f} (Prev. Quarter)"
    )

    st.markdown("---")

   
    trend_data = filtered_df.set_index('Date').groupby('Category')['Registrations'].resample('MS').sum().reset_index()
    
    fig1 = px.line(
        trend_data,
        x="Date",
        y="Registrations",
        color="Category",
        title="Vehicle Registrations Trend (Monthly)",
        labels={"Registrations": "Total Monthly Registrations"}
    )
    fig1.update_layout(legend_title_text='Category')
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")

    
    manufacturer_summary = filtered_df.groupby(['Manufacturer', 'Category'], as_index=False)['Registrations'].sum()
    
    fig2 = px.bar(
        manufacturer_summary.sort_values('Registrations', ascending=False),
        x="Manufacturer",
        y="Registrations",
        color="Category",
        title="Total Registrations by Manufacturer",
        labels={"Registrations": "Total Registrations"},
        barmode="group"
    )
    fig2.update_layout(legend_title_text='Category')

    st.plotly_chart(fig2, use_container_width=True)
