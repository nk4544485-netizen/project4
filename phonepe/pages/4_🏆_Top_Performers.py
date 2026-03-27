import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

st.set_page_config(page_title="Top Performers | Quantum Dash", page_icon="🏆", layout="wide")

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

st.title("🏆 Leaderboard Telemetry")

@st.cache_data
def load_top_data():
    db_path = os.path.join(os.getcwd(), 'data', 'phonepe_pulse.db')
    if not os.path.exists(db_path): return pd.DataFrame()
    conn = sqlite3.connect(db_path)
    try:
        # Assuming aggregated_transaction has state and we mock pincode/district for demo
        df = pd.read_sql("SELECT * FROM aggregated_transaction", conn)
    except:
        df = pd.DataFrame({
            'state': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Gujarat'],
            'district': ['Mumbai', 'Bengaluru', 'Chennai', 'New Delhi', 'Ahmedabad'],
            'pincode': ['400001', '560001', '600001', '110001', '380001'],
            'amount': [5e8, 4e8, 3e8, 2.5e8, 2e8]
        })
    return df

df = load_top_data()

if not df.empty:
    entity = st.selectbox("Select Display Matrix", ['Top 10 States', 'Top 10 Districts', 'Top 10 Pincodes'])
    
    if entity == 'Top 10 States':
        col = 'state'
    elif entity == 'Top 10 Districts':
        col = 'district'
    else:
        col = 'pincode'
        
    if col in df.columns:
        df_top = df.groupby(col)['amount'].sum().reset_index().sort_values(by='amount', ascending=False).head(10)
        
        fig = px.bar(
            df_top, x=col, y='amount', title=f"Highest Volume by {col.capitalize()}",
            template="plotly_dark", color_discrete_sequence=['#39ff14']
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"{col} column not found in dataset structure.")
