import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config for a professional look
st.set_page_config(
    page_title="MarketPulse | Strategic Dashboard", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a professional, consulting-firm aesthetic
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background-color: #f8f9fa;
        color: #2c3e50;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Header styling */
    h1, h2, h3 {
        color: #1a252f;
        font-weight: 600 !important;
    }
    
    /* Metric boxes */
    [data-testid="stMetricValue"] {
        color: #003366; /* Deep corporate navy */
        font-weight: 700;
        font-size: 2.4rem;
    }
    [data-testid="stMetricLabel"] {
        color: #5c6c7c;
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Divider */
    hr {
        border-top: 1px solid #d1d8e0;
        margin: 2rem 0;
    }
    
    /* AI Recommendation box */
    .stAlert {
        background-color: #ffffff;
        border-left: 5px solid #003366;
        color: #1a252f;
        padding: 1.5rem;
        border-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 1.1rem;
    }
    
    /* Top banner */
    .banner {
        background-color: #003366; /* Deep corporate navy */
        color: white;
        padding: 2rem;
        border-radius: 6px;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .banner h1 {
        color: white !important;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 400 !important;
        letter-spacing: 0.02em;
    }
    .banner p {
        margin: 0;
        opacity: 0.85;
        font-size: 1.15rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
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

# Custom Header
st.markdown("""
<div class="banner">
    <h1>MarketPulse</h1>
    <p>Strategic Market Entry & Profitability Decision Engine</p>
</div>
""", unsafe_allow_html=True)

# --- KPI Metrics ---
st.markdown("### Executive Overview")
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

# Professional Chart Styling (Clean, Minimalist)
chart_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2c3e50"),
    margin=dict(t=40, l=0, r=0, b=0),
    title_font=dict(size=18, color="#1a252f", family="Inter, sans-serif")
)

with col_left:
    st.markdown("### Market Size & Digital Adoption")
    fig_city = px.bar(
        cities.sort_values('population', ascending=True),
        x='population', 
        y='city',
        orientation='h',
        color='ecommerce_adoption',
        labels={'population': 'Population', 'city': '', 'ecommerce_adoption': 'eCommerce (%)'},
        color_continuous_scale=['#b3cde0', '#6497b1', '#005b96', '#03396c', '#011f4b'] # Professional corporate blue scale
    )
    fig_city.update_layout(**chart_layout)
    fig_city.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e8ecef', title_text="Population")
    fig_city.update_yaxes(showgrid=False)
    st.plotly_chart(fig_city, use_container_width=True)

with col_right:
    st.markdown("### Customer Segment Distribution")
    segment_counts = customers['customer_segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    # Corporate color palette for donut chart (Navy, Slate, Steel, Gray)
    colors = ['#003366', '#4a6984', '#7c98ab', '#b5c6d3', '#e2e8ed']
    
    fig_seg = go.Figure(data=[go.Pie(
        labels=segment_counts['Segment'],
        values=segment_counts['Count'],
        hole=0.65,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
        textinfo='percent'
    )])
    fig_seg.update_layout(
        **chart_layout,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_seg, use_container_width=True)

st.divider()

st.markdown("### Strategic Recommendation Output")
st.info("**Primary Directive:** Enter **Bengaluru** first using the Medium Pricing strategy. Expected break-even occurs in Month 18 under the base case. Re-evaluate expansion if CAC exceeds ₹350 or organic retention drops below 35%.")
