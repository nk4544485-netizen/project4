import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils import get_db_connection, format_currency, format_count

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PhonePe Pulse | Quantum Dash",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
def local_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: white; }
        [data-testid="stMetric"] {
            background: transparent !important;
            backdrop-filter: blur(16px) !important;
            border-radius: 15px !important;
            border: 1px solid #00f2ff !important;
            padding: 20px !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 10px 20px rgba(0, 242, 255, 0.2) !important;
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown p strong {
            color: #00f2ff !important;
            text-shadow: 0 0 10px rgba(0, 242, 255, 0.5) !important;
        }
        [data-testid="stSidebar"] {
            background: rgba(14, 17, 23, 0.8) !important;
            backdrop-filter: blur(15px) !important;
            border-right: 1px solid rgba(0, 242, 255, 0.2) !important;
        }
        [data-testid="stMetricValue"] {
            color: #00f2ff !important;
            text-shadow: 0 0 5px rgba(0, 242, 255, 0.5) !important;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- DATA LOADING ---
@st.cache_data(ttl=600)
def load_data():
    conn = get_db_connection()
    with st.spinner('Quantum Loading... Synchronizing data streams...'):
        try:
            df_tx = pd.read_sql("SELECT * FROM agg_transaction", conn)
            df_users = pd.read_sql("SELECT * FROM agg_user", conn)
            return df_tx, df_users
        except Exception as e:
            st.error(f"❌ SQL Error: {e}. Attempting automated recovery...")
            st.stop()

st.title("🌌 PhonePe Pulse: Quantum Hub")
st.markdown("**Real-time telemetry from the sub-orbital analytics core.**")

# --- STATE MANAGEMENT ---
if 'df_tx' not in st.session_state or 'df_users' not in st.session_state:
    df_tx, df_users = load_data()
    st.session_state['df_tx'] = df_tx
    st.session_state['df_users'] = df_users
else:
    df_tx = st.session_state['df_tx']
    df_users = st.session_state['df_users']

# --- SIDEBAR FILTERS ---
st.sidebar.subheader("🎛️ Quantum Filters")

years = sorted(df_tx['year'].unique().tolist())
quarters = sorted(df_tx['quarter'].unique().tolist())
states = sorted(df_tx['state'].unique().tolist())

selected_year = st.sidebar.selectbox("Target Year", ["Temporal Omni (All)"] + years)
selected_quarter = st.sidebar.selectbox("Orbital Phase (Quarter)", ["Omni Phase (All)"] + quarters)
selected_state = st.sidebar.selectbox("Sector Configuration (State)", ["Global Mesh (All)"] + states)

# Filter logic
filtered_tx = df_tx.copy()
filtered_users = df_users.copy()

if selected_year != "Temporal Omni (All)":
    filtered_tx = filtered_tx[filtered_tx['year'] == int(selected_year)]
    filtered_users = filtered_users[filtered_users['year'] == int(selected_year)]
if selected_quarter != "Omni Phase (All)":
    filtered_tx = filtered_tx[filtered_tx['quarter'] == int(selected_quarter)]
    filtered_users = filtered_users[filtered_users['quarter'] == int(selected_quarter)]
if selected_state != "Global Mesh (All)":
    filtered_tx = filtered_tx[filtered_tx['state'] == selected_state]
    filtered_users = filtered_users[filtered_users['state'] == selected_state]

st.session_state['filtered_tx'] = filtered_tx
st.session_state['filtered_users'] = filtered_users

# --- WEIGHTLESS KPIs ---
kpi1, kpi2, kpi3 = st.columns(3)

total_amount = filtered_tx['amount'].sum()
total_transactions = filtered_tx['count'].sum()
total_users = filtered_users['registered_users'].unique().sum()

with kpi1:
    st.metric("Total Transmission Volume", format_currency(total_amount))

with kpi2:
    st.metric("Quantum Events Registered", format_count(total_transactions))

with kpi3:
    st.metric("Registered Users", format_count(total_users))

st.markdown("<br>", unsafe_allow_html=True)

# Dashboard Trend
st.subheader("📊 Network Growth Trajectory")
trend_df = filtered_tx.groupby(['year', 'quarter'])['amount'].sum().reset_index()
trend_df['Period'] = trend_df['year'].astype(str) + " Q" + trend_df['quarter'].astype(str)
fig_trend = px.area(trend_df, x='Period', y='amount', 
                   title="Transaction Volume Trend",
                   template="plotly_dark", color_discrete_sequence=['#00f2ff'])
fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_trend, use_container_width=True)

st.info("Navigate standard operations via the orbital menu on the left to access detailed telemetry.")
