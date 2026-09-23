import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)

# -----------------------------
# CUSTOM DASHBOARD STYLE
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

h2, h3 {
    font-weight: 600 !important;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    font-weight: 600;
}

</style>
""")

st.sidebar.title("🚚 Logistics Analytics")
st.sidebar.caption("Supply Chain Dashboard")

st.sidebar.divider()
DATA_DIR = Path("cleaned_data")

loads = pd.read_csv(DATA_DIR / "loads_clean.csv")
delivery_events = pd.read_csv(DATA_DIR / "delivery_events_clean.csv")
trucks = pd.read_csv(DATA_DIR / "trucks_clean.csv")
drivers = pd.read_csv(DATA_DIR / "drivers_clean.csv")
warehouses = pd.read_csv(DATA_DIR / "warehouses_clean.csv")
maintenance = pd.read_csv(DATA_DIR / "maintenance_clean.csv")
fuel = pd.read_csv(DATA_DIR / "fuel_clean.csv")

st.sidebar.subheader("🔎 Dashboard Filters")
st.sidebar.caption("Use filters to explore specific operational segments")

years = sorted(loads["Load_Year"].dropna().unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + years,
    key="year_filter"
)

if selected_year != "All":
    loads = loads[loads["Load_Year"] == selected_year]


traffic_types = sorted(
    delivery_events["Traffic"].dropna().unique()
)

selected_traffic = st.sidebar.selectbox(
    "Select Traffic",
    ["All"] + traffic_types,
    key="traffic_filter"
)

if selected_traffic != "All":
    delivery_events = delivery_events[
        delivery_events["Traffic"] == selected_traffic
    ]
fuel_types = sorted(
    trucks["Fuel_Type"].dropna().unique()
)

fuel_types = sorted(
    trucks["Fuel_Type"].dropna().unique()
)

selected_fuel = st.sidebar.selectbox(
    "Select Fuel Type",
    ["All"] + fuel_types,
    key="fuel_filter"
)

if selected_fuel != "All":
    trucks = trucks[
        trucks["Fuel_Type"] == selected_fuel
    ]



st.success("All datasets loaded successfully!")

st.subheader("📊 Executive Overview")
st.caption("High-level operational performance at a glance")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Loads", f"{len(loads):,}")

col2.metric(
    "Total Revenue",
    f"₹{loads['Freight_Revenue'].sum():,.0f}"
)

col3.metric(
    "Fuel Cost",
    f"₹{fuel['Fuel_Cost'].sum():,.0f}"
)

col4.metric(
    "Maintenance Cost",
    f"₹{maintenance['Maintenance_Cost'].sum():,.0f}"
)

col5.metric(
    "Avg Delay",
    f"{delivery_events['Delay_Minutes'].mean():.2f} min"
)

# =============================
# DELIVERY PERFORMANCE
# =============================

st.subheader("🚚 Delivery Performance")
st.caption("Analyze delivery delays across traffic conditions and event types")

col1, col2 = st.columns(2)

# Average delay by traffic
with col1:

    delay_by_traffic = (
        delivery_events
        .groupby("Traffic")["Delay_Minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    st.markdown("#### ⏱️ Average Delay by Traffic")

    st.bar_chart(delay_by_traffic)

    st.caption(
        "Average delivery delay across different traffic conditions."
    )


# Average delay by event type
with col2:

    event_delay = (
        delivery_events
        .groupby("Event_Type")["Delay_Minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    st.markdown("#### 📦 Average Delay by Event Type")

    st.bar_chart(event_delay)

    st.caption(
        "Average delay recorded for different delivery events."
    )


# =============================
# FLEET PERFORMANCE
# =============================

st.subheader("🚛 Fleet Performance")
st.caption("Monitor truck types and fuel-type distribution across the fleet")

col1, col2 = st.columns(2)

# Truck type distribution
with col1:

    truck_type_count = (
        trucks["Truck_Type"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.markdown("#### 🚚 Trucks by Type")

    st.bar_chart(truck_type_count)

    st.caption(
        "Distribution of light, medium and heavy trucks in the fleet."
    )


# Fuel type distribution
with col2:

    fuel_type_count = (
        trucks["Fuel_Type"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.markdown("#### ⛽ Trucks by Fuel Type")

    st.bar_chart(fuel_type_count)

    st.caption(
        "Distribution of trucks based on their fuel type."
    )

# =============================
# DRIVER PERFORMANCE
# =============================

st.subheader("👨‍✈️ Driver Performance")
st.caption("Evaluate driver safety performance across different regions")

col1, col2 = st.columns(2)

# Average safety score by region
with col1:

    safety_by_region = (
        drivers
        .groupby("Region")["Safety_Score"]
        .mean()
        .sort_values(ascending=False)
    )

    st.markdown("#### 🛡️ Safety Score by Region")

    st.bar_chart(safety_by_region)

    st.caption(
        "Average driver safety score across different regions."
    )


# Overall safety score
with col2:

    avg_safety = drivers["Safety_Score"].mean()

    st.markdown("#### 📊 Overall Driver Safety")

    st.metric(
        "Average Safety Score",
        f"{avg_safety:.2f} / 100"
    )

    st.write(
        "This metric represents the average safety performance "
        "of all drivers in the dataset."
    )

# =============================
# DRIVER SAFETY DISTRIBUTION
# =============================

st.subheader("🛡️ Driver Safety Distribution")
st.caption("Understand the distribution of drivers by safety performance")

safety_distribution = (
    drivers["Safety_Category"]
    .value_counts()
)

st.markdown("#### 👨‍✈️ Drivers by Safety Category")

st.bar_chart(safety_distribution)

st.caption(
    "Number of drivers classified into Low, Average, Good and Excellent safety categories."
)

# =============================
# WAREHOUSE PERFORMANCE
# =============================

st.subheader("🏭 Warehouse Performance")
st.caption("Analyze warehouse utilization and daily storage costs")

col1, col2 = st.columns(2)

# Top 10 warehouses by utilization
with col1:

    utilization = warehouses.nlargest(
        10, "Utilization_Pct"
    )

    st.markdown("#### 📦 Top 10 Warehouses by Utilization")

    st.bar_chart(
        utilization.set_index("Warehouse_Name")["Utilization_Pct"]
    )

    st.caption(
        "Warehouses with the highest space utilization."
    )


# Top 10 warehouses by storage cost
with col2:

    warehouse_cost = warehouses.nlargest(
        10, "Storage_Cost_Per_Day"
    )

    st.markdown("#### 💰 Top 10 Warehouses by Daily Cost")

    st.bar_chart(
        warehouse_cost.set_index("Warehouse_Name")[
            "Storage_Cost_Per_Day"
        ]
    )

    st.caption(
        "Warehouses with the highest daily storage costs."
    )

# =============================
# WAREHOUSE KPI ANALYSIS
# =============================

st.subheader("📊 Warehouse Capacity Overview")
st.caption("Monitor warehouse capacity and average space utilization")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Warehouses",
        f"{len(warehouses):,}"
    )

with col2:

    avg_capacity = warehouses["Capacity_SQFT"].mean()

    st.metric(
        "Avg Capacity",
        f"{avg_capacity:,.0f} SQFT"
    )

with col3:

    avg_utilization = warehouses["Utilization_Pct"].mean()

    st.metric(
        "Avg Utilization",
        f"{avg_utilization:.2f}%"
    )


# =============================
# COST ANALYSIS
# =============================

st.subheader("💰 Cost Analysis")
st.caption("Track fuel and maintenance costs across operations")

col1, col2 = st.columns(2)

# Fuel cost analysis
with col1:

    fuel_cost = (
        fuel
        .groupby("Fuel_Type")["Fuel_Cost"]
        .sum()
        .sort_values(ascending=False)
    )

    st.markdown("#### ⛽ Fuel Cost by Type")

    st.bar_chart(fuel_cost)

    st.caption(
        "Total fuel expenditure across different fuel types."
    )


# Maintenance cost analysis
with col2:

    maintenance_cost = (
        maintenance
        .groupby("Maintenance_Type")["Maintenance_Cost"]
        .sum()
        .sort_values(ascending=False)
    )

    st.markdown("#### 🔧 Maintenance Cost by Type")

    st.bar_chart(maintenance_cost)

    st.caption(
        "Total maintenance expenditure by maintenance category."
    )

# =============================
# REVENUE ANALYSIS
# =============================

st.subheader("📈 Revenue Analysis")
st.caption("Analyze freight revenue across different years")

col1, col2 = st.columns(2)

# Year-wise revenue
with col1:

    yearly_revenue = (
        loads
        .groupby("Load_Year")["Freight_Revenue"]
        .sum()
        .sort_index()
    )

    st.markdown("#### 💰 Revenue by Year")

    st.line_chart(yearly_revenue)

    st.caption(
        "Total freight revenue generated in each year."
    )


# Average revenue per load
with col2:

    avg_revenue = (
        loads["Freight_Revenue"].mean()
    )

    st.markdown("#### 📦 Average Revenue per Load")

    st.metric(
        "Revenue / Load",
        f"₹{avg_revenue:,.2f}"
    )

    st.write(
        "This shows the average freight revenue generated "
        "per load."
    )

# =============================
# DELIVERY STATUS ANALYSIS
# =============================

st.subheader("📦 Delivery Status Analysis")
st.caption("Understand the current status of logistics loads")

status_count = (
    loads["Status"]
    .value_counts()
    .sort_values(ascending=False)
)

st.markdown("#### 🚚 Load Status Distribution")

st.bar_chart(status_count)

st.caption(
    "Number of loads by their current delivery status."
)


# =============================
# MAINTENANCE ANALYSIS
# =============================

st.subheader("🔧 Maintenance Analysis")
st.caption("Monitor vehicle failures and maintenance downtime")

col1, col2 = st.columns(2)

# Failure analysis
with col1:

    failure_count = (
        maintenance["Failure_Flag"]
        .value_counts()
        .sort_index()
    )

    failure_count.index = [
        "No Failure" if value == 0 else "Failure"
        for value in failure_count.index
    ]

    st.markdown("#### 🚨 Maintenance Failure Status")

    st.bar_chart(failure_count)

    st.caption(
        "Number of maintenance records with and without vehicle failures."
    )


# Average downtime
with col2:

    downtime = (
        maintenance
        .groupby("Maintenance_Type")["Downtime_Hours"]
        .mean()
        .sort_values(ascending=False)
    )

    st.markdown("#### ⏱️ Average Downtime by Maintenance Type")

    st.bar_chart(downtime)

    st.caption(
        "Average vehicle downtime associated with each maintenance type."
    )

# =============================
# DELIVERY TIMELINESS
# =============================

st.subheader("⏱️ Delivery Timeliness")
st.caption("Compare on-time and delayed delivery events")

col1, col2 = st.columns(2)

# Delay status count
with col1:

    delay_status = (
        delivery_events["Delay_Status"]
        .value_counts()
    )

    st.markdown("#### 🚦 On-Time vs Delayed")

    st.bar_chart(delay_status)

    st.caption(
        "Distribution of on-time and delayed delivery events."
    )


# Delay percentage
with col2:

    total_events = len(delivery_events)

    delayed_events = (
        delivery_events["Delay_Status"]
        .eq("Delayed")
        .sum()
    )

    delayed_percentage = (
        delayed_events / total_events * 100
        if total_events > 0 else 0
    )

    on_time_percentage = 100 - delayed_percentage

    st.markdown("#### 📊 Delivery Performance")

    st.metric(
        "Delayed %",
        f"{delayed_percentage:.2f}%"
    )

    st.metric(
        "On-Time %",
        f"{on_time_percentage:.2f}%"
    )


st.divider()

st.subheader("💡 Key Business Insights")
st.caption("Important findings from the logistics data")

st.info("📦 67.66% of delivery events were delayed.")

st.info("⏱️ Average delivery delay was approximately 50.69 minutes.")

st.info("🚛 The fleet contains 4,000 trucks across different truck and fuel types.")

st.info("💰 Fuel and maintenance are major operational cost areas.")

st.info("🔧 Around 18.36% of maintenance records were associated with failures.")
