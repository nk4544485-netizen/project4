import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_db_connection, format_currency, format_count

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
    conn = get_db_connection()
    try:
        df_tx = pd.read_sql("SELECT * FROM top_transaction", conn)
        df_user = pd.read_sql("SELECT * FROM top_user", conn)
        return df_tx, df_user
    except Exception as e:
        st.error(f"Error loading top data: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_tx, df_user = load_top_data()

if not df_tx.empty and not df_user.empty:
    years = sorted(df_tx['year'].unique().tolist())
    quarters = sorted(df_tx['quarter'].unique().tolist())
    
    col_y, col_q = st.columns(2)
    with col_y:
        sel_year = st.selectbox("Year", years, index=len(years)-1)
    with col_q:
        sel_quarter = st.selectbox("Quarter", quarters)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    metric_type = st.radio("Select Metric Stream", ["Transactions", "Users"], horizontal=True)
    entity_level = st.selectbox("Entity Resolution", ["state", "district", "pincode"])

    if metric_type == "Transactions":
        data = df_tx[(df_tx['year'] == sel_year) & (df_tx['quarter'] == sel_quarter) & (df_tx['entity_type'] == entity_level)]
        data = data.groupby('entity_name')['amount'].sum().reset_index().sort_values(by='amount', ascending=False).head(10)
        y_axis = 'amount'
        color = '#00f2ff'
    else:
        data = df_user[(df_user['year'] == sel_year) & (df_user['quarter'] == sel_quarter) & (df_user['entity_type'] == entity_level)]
        data = data.groupby('entity_name')['registered_users'].sum().reset_index().sort_values(by='registered_users', ascending=False).head(10)
        y_axis = 'registered_users'
        color = '#39ff14'

    st.subheader(f"Top 10 {entity_level.capitalize()}s by {metric_type}")
    
    fig = px.bar(
        data, x='entity_name', y=y_axis,
        template="plotly_dark", color_discrete_sequence=[color],
        text_auto='.2s'
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Database unavailable or top tables missing.")
