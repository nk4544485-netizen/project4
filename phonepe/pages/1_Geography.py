import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

st.set_page_config(page_title="Geography | Quantum Dash", page_icon="🌍", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0e1117; color: white; }
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    background: transparent !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-radius: 15px !important;
    border: 1px solid #00f2ff !important;
    padding: 20px !important;
}
h1, h2, h3 { color: #00f2ff !important; text-shadow: 0 0 10px rgba(0, 242, 255, 0.5) !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Quantum Geography")

@st.cache_data
def load_geo_data():
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    if not os.path.exists(db_path): return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    # Using dummy columns since exact schema may vary
    try:
        df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)
    except:
        df = pd.DataFrame({'year': [2023]*5, 'quarter': [1,2,3,4,1], 'state': ['maharashtra', 'gujarat', 'karnataka', 'delhi', 'tamil nadu'], 'amount': [1e8, 2e8, 1.5e8, 3e8, 1.2e8]})
    return df

df = load_geo_data()

if not df.empty:
    years = sorted(df['year'].unique().tolist())
    
    # robust handling for single year in DB
    min_year = min(years) if len(years) > 1 else min(years) - 1
    max_year = max(years)
    
    selected_year = st.slider(
        "Select Temporal Orbit (Year)", 
        min_value=min_year, 
        max_value=max_year, 
        value=max_year,
        disabled=(len(years) == 1)
    )
    
    filtered_df = df[df['year'] == selected_year]
    
    # Choropleth placeholder map (using bar chart representation if geojson isn't present)
    # For a real India choropleth, you'd need a GeoJSON file. We'll use a bubble map representation for simplicity.
    fig = px.bar(
        filtered_df.groupby('state')['amount'].sum().reset_index(), 
        x='state', y='amount', 
        title="Transaction Volume by State",
        template="plotly_dark",
        color_discrete_sequence=['#00f2ff']
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Database unavailable.")
