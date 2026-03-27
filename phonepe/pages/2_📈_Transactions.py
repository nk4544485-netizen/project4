import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

st.set_page_config(page_title="Transactions | Quantum Dash", page_icon="📈", layout="wide")

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

st.title("📈 Quantum Transactions")

@st.cache_data
def load_tx_data():
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    if not os.path.exists(db_path): return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)
    except:
        df = pd.DataFrame({
            'year': [2022, 2022, 2023, 2023, 2023],
            'quarter': [1,2,1,2,3],
            'transaction_type': ['Peer-to-Peer', 'Merchant Payments', 'Peer-to-Peer', 'Merchant Payments', 'Recharge'],
            'amount': [5e7, 8e7, 6e7, 1e8, 3e7]
        })
    return df

df = load_tx_data()

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transaction Archetypes")
        fig_donut = px.pie(
            df, values='amount', names='transaction_type', hole=0.5,
            template="plotly_dark", color_discrete_sequence=['#00f2ff', '#39ff14', '#ff00ff']
        )
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col2:
        st.subheader("Time-Series Growth Resonance")
        df_time = df.groupby(['year', 'quarter', 'transaction_type'])['amount'].sum().reset_index()
        df_time['Time'] = df_time['year'].astype(str) + "-Q" + df_time['quarter'].astype(str)
        fig_line = px.line(
            df_time, x='Time', y='amount', color='transaction_type',
            template="plotly_dark", color_discrete_sequence=['#00f2ff', '#39ff14', '#ff00ff']
        )
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)
