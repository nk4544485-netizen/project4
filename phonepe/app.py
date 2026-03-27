import streamlit as st
import os
import sqlite3
import pandas as pd
import time
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PhonePe Pulse | Quantum Dash",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS: GLASSMORPHISM & NEON ACCENTS ---
def local_css():
    st.markdown("""
        <style>
        /* Deep space-black background */
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        
        /* Remove hard edges & add glassmorphism to metric containers */
        [data-testid="stMetric"] {
            background: transparent !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border-radius: 15px !important;
            border: 1px solid #00f2ff !important;
            padding: 20px !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        }

        /* Hover-lift animation */
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 10px 20px rgba(0, 242, 255, 0.2) !important;
        }

        /* Neon Titles */
        h1, h2, h3, h4, h5, h6, .stMarkdown p strong {
            color: #00f2ff !important;
            text-shadow: 0 0 10px rgba(0, 242, 255, 0.5) !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: rgba(14, 17, 23, 0.8) !important;
            backdrop-filter: blur(15px) !important;
            border-right: 1px solid rgba(0, 242, 255, 0.2) !important;
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #00f2ff !important;
            text-shadow: 0 0 5px rgba(0, 242, 255, 0.5) !important;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- DB CONNECTION & QUANTUM LOADING ---
@st.cache_resource
def get_db_connection():
    # 1. Finds the 'data' folder inside your GitHub repo automatically
    # This works on your PC and on Streamlit Cloud
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    
    # 2. Check if the file actually exists to prevent crashing
    if not os.path.exists(db_path):
        st.error(f"🛰️ Database not found at: {db_path}. Ensure your 'data' folder is pushed to GitHub!")
        st.stop()
        
    return sqlite3.connect(db_path, check_same_thread=False)

@st.cache_data(ttl=600)
def load_data():
    conn = get_db_connection()
    with st.spinner('Quantum Loading... Synchronizing data streams...'):
        time.sleep(1.0) # Simulate quantum processing time
        # 3. Use the EXACT table names from your SQLite DB
        # If your tables are named differently, change 'aggregated_transaction' below
        try:
            df_tx = pd.read_sql("SELECT * FROM aggregated_transaction", conn)
            df_users = pd.read_sql("SELECT * FROM aggregated_user", conn)
            return df_tx, df_users
        except Exception as e:
            st.error(f"❌ SQL Error: {e}. Check if table names match your DB!")
            st.stop()

st.title("🌌 PhonePe Pulse: Quantum Hub")
st.markdown("**Welcome to the sub-orbital analytics core. All systems nominal.**")

# --- STATE MANAGEMENT ---
if 'df_tx' not in st.session_state or 'df_users' not in st.session_state:
    df_tx, df_users = load_data()
    st.session_state['df_tx'] = df_tx
    st.session_state['df_users'] = df_users
else:
    df_tx = st.session_state['df_tx']
    df_users = st.session_state['df_users']

df = df_tx  # Fallback to df_tx for existing UI filters

# --- FORMATTING UTILS ---
def format_currency(val):
    return f"₹ {val / 10000000:.2f} Cr" if val >= 10000000 else f"₹ {val:,.2f}"

def format_count(val):
    return f"{val / 1000000:.2f} M" if val >= 1000000 else f"{val:,}"

# --- SIDEBAR FILTERS ---
st.sidebar.subheader("🎛️ Quantum Filters")

if not df.empty:
    years = sorted(df['year'].unique().tolist())
    quarters = sorted(df['quarter'].unique().tolist())
    states = sorted(df['state'].unique().tolist())
else:
    years, quarters, states = [2023], [1, 2, 3, 4], ["All"]

selected_year = st.sidebar.selectbox("Target Year", ["Temporal Omni (All)"] + years)
selected_quarter = st.sidebar.selectbox("Orbital Phase (Quarter)", ["Omni Phase (All)"] + quarters)
selected_state = st.sidebar.selectbox("Sector Configuration (State)", ["Global Mesh (All)"] + states)

# Filter logic
filtered_df = df.copy()
if selected_year != "Temporal Omni (All)":
    filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
if selected_quarter != "Omni Phase (All)":
    filtered_df = filtered_df[filtered_df['quarter'] == int(selected_quarter)]
if selected_state != "Global Mesh (All)":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]

# Session State for filtering across pages (optional, but good for multi-page apps)
st.session_state['filtered_data'] = filtered_df
st.session_state['theme_color'] = '#00f2ff' # Neon Cyan

# --- WEIGHTLESS KPIs ---
kpi1, kpi2, kpi3 = st.columns(3)

total_amount = filtered_df['amount'].sum() if not filtered_df.empty else 0
total_transactions = filtered_df['count'].sum() if not filtered_df.empty else 0
avg_txn = (total_amount / total_transactions) if total_transactions > 0 else 0

with kpi1:
    st.metric("Total Transmission Volume", format_currency(total_amount))

with kpi2:
    st.metric("Quantum Events Registered", format_count(total_transactions))

with kpi3:
    st.metric("Avg Event Amplitude", format_currency(avg_txn))

st.markdown("<br><hr style='border: 1px solid rgba(0, 242, 255, 0.2);'>", unsafe_allow_html=True)
st.info("Navigate standard operations via the orbital menu on the left to access detailed telemetry (Choropleth, Sunbursts, etc.).")
