import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config for a clean, reliable look
st.set_page_config(
    page_title="MarketPulse | Strategic Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove the complex custom CSS to prevent dark-mode/light-mode clashes
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    cities_df = pd.read_csv(os.path.join(base_dir, "../../data/processed/city_market_metrics.csv"))
    orders_df = pd.read_csv(os.path.join(base_dir, "../../data/synthetic/orders.csv"))
    customers_df = pd.read_csv(os.path.join(base_dir, "../../data/synthetic/customers.csv"))
    return cities_df, orders_df, customers_df

try:
    cities, orders, customers = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Header
st.title("MarketPulse Strategic Dashboard")
st.markdown("**Market Entry & Profitability Decision Engine**")
st.divider()

# --- KPI Metrics ---
st.subheader("Executive Overview")
col1, col2, col3, col4 = st.columns(4)

total_revenue = orders['delivery_fee'].sum() * 10 
total_orders = len(orders)
total_customers = len(customers)

col1.metric("Total Markets Analyzed", len(cities))
col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Est. Base Revenue", f"₹{total_revenue:,.0f}")

st.divider()

# --- Visualizations ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Market Size & Digital Adoption")
    # Using robust, high-contrast plotly defaults
    fig_city = px.bar(
        cities.sort_values('population', ascending=True),
        x='population', 
        y='city',
        orientation='h',
        color='ecommerce_adoption',
        labels={'population': 'Population', 'city': 'City', 'ecommerce_adoption': 'eCommerce (%)'},
        color_continuous_scale='Blues',
        text_auto='.2s'
    )
    # Enforcing a white template so colors don't clash with dark mode
    fig_city.update_layout(template="plotly_white", margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig_city, use_container_width=True)

with col_right:
    st.subheader("Customer Segment Distribution")
    segment_counts = customers['customer_segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    # High-contrast categorical colors
    fig_seg = px.pie(
        segment_counts,
        names='Segment',
        values='Count',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    # Placing text inside the chart so it is always visible
    fig_seg.update_traces(textposition='inside', textinfo='percent+label')
    fig_seg.update_layout(template="plotly_white", showlegend=False, margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig_seg, use_container_width=True)

st.divider()

# --- Recommendation ---
st.subheader("Strategic Recommendation Output")
st.success("""
**Primary Directive:** Enter **Bengaluru** first using the Medium Pricing strategy. 
* Expected break-even occurs in Month 18 under the base case. 
* Re-evaluate expansion if CAC exceeds ₹350 or organic retention drops below 35%.
""")
