import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="MarketPulse Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    # Path relative to src/dashboard/app.py
    cities_df = pd.read_csv(os.path.join(base_dir, "../../data/processed/city_market_metrics.csv"))
    orders_df = pd.read_csv(os.path.join(base_dir, "../../data/synthetic/orders.csv"))
    customers_df = pd.read_csv(os.path.join(base_dir, "../../data/synthetic/customers.csv"))
    return cities_df, orders_df, customers_df

try:
    cities, orders, customers = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.title("📊 MarketPulse: Market Entry Decision Engine")
st.markdown("Interactive Dashboard for Bain & Company Portfolio Project")

# --- KPI Metrics ---
st.subheader("Executive Overview")
col1, col2, col3, col4 = st.columns(4)

total_revenue = orders['delivery_fee'].sum() * 10 # Using delivery fee as proxy for simple visualization
total_orders = len(orders)
total_customers = len(customers)

col1.metric("Total Cities Analyzed", len(cities))
col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Est. Proxy Revenue", f"₹{total_revenue:,.0f}")

st.divider()

# --- Visualizations ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("City Attractiveness (Population & eCommerce)")
    # Bar chart for cities
    fig_city = px.bar(
        cities.sort_values('population', ascending=False),
        x='city', 
        y='population',
        color='ecommerce_adoption',
        title="Cities by Population & eCommerce Adoption (%)",
        labels={'population': 'Population', 'city': 'City', 'ecommerce_adoption': 'eCommerce Adop.'},
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_city, use_container_width=True)

with col_right:
    st.subheader("Customer Segmentation Breakdown")
    # Donut chart for segments
    segment_counts = customers['customer_segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    fig_seg = px.pie(
        segment_counts, 
        values='Count', 
        names='Segment', 
        hole=0.4,
        title="Customer Distribution by Segment"
    )
    st.plotly_chart(fig_seg, use_container_width=True)

st.divider()

st.subheader("AI Recommendation Output")
st.info("**Primary Recommendation:** Enter **Bengaluru** first using the Medium Pricing strategy. Expected break-even occurs in Month 18 under the base case. Re-evaluate expansion if CAC exceeds ₹350.")
