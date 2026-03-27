import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

st.set_page_config(page_title="User Insights | Quantum Dash", page_icon="👥", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0e1117; color: white; }
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    background: transparent !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 15px !important;
    border: 1px solid #00f2ff !important;
    padding: 20px !important;
}
h1, h2, h3 { color: #00f2ff !important; }
</style>
""", unsafe_allow_html=True)

st.title("👥 User Telemetry & Insights")

@st.cache_data
def load_user_data():
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    if not os.path.exists(db_path): return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM aggregated_user", conn)
    except:
        df = pd.DataFrame({
            'year': [2023, 2023, 2023],
            'quarter': [1,2,3],
            'registered_users': [500000, 600000, 750000],
            'app_opens': [1200000, 1500000, 2000000],
            'brand': ['Xiaomi', 'Samsung', 'Vivo'],
            'count': [200000, 150000, 100000]
        })
    return df

df = load_user_data()

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("App Opens vs Registrations")
        # Sums for simplicity or plot over time
        df_time = df.groupby(['year', 'quarter'])[['app_opens', 'registered_users']].sum().reset_index()
        df_time['Time'] = df_time['year'].astype(str) + "-Q" + df_time['quarter'].astype(str)
        fig_bar = px.bar(
            df_time, x='Time', y=['app_opens', 'registered_users'], barmode='group',
            template="plotly_dark", color_discrete_sequence=['#00f2ff', '#39ff14']
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("Top Hardware Interfaces")
        df_brand = df.groupby('brand')['count'].sum().reset_index().sort_values(by='count', ascending=False).head(10)
        fig_brands = px.bar(
            df_brand, x='brand', y='count',
            template="plotly_dark", color_discrete_sequence=['#ff00ff']
        )
        fig_brands.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_brands, use_container_width=True)
