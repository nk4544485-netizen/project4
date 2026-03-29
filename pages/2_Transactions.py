import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_db_connection, format_currency, format_count

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
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM agg_transaction", conn)
        return df
    except Exception as e:
        st.error(f"Error loading transaction data: {e}")
        return pd.DataFrame()

df = load_tx_data()

if not df.empty:
    years = sorted(df['year'].unique().tolist())
    quarters = sorted(df['quarter'].unique().tolist())
    
    col1, col2 = st.columns(2)
    with col1:
        sel_year = st.selectbox("Year", years, index=len(years)-1)
    with col2:
        sel_quarter = st.selectbox("Quarter", quarters)
    
    filtered_df = df[(df['year'] == sel_year) & (df['quarter'] == sel_quarter)]
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Transaction Archetypes")
        fig_donut = px.pie(
            filtered_df, values='amount', names='transaction_type', hole=0.5,
            template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma_r
        )
        fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_b:
        st.subheader("State-wise Pulse")
        state_tx = filtered_df.groupby('state')['amount'].sum().reset_index().sort_values(by='amount', ascending=False).head(10)
        fig_bar = px.bar(
            state_tx, x='amount', y='state', orientation='h',
            template="plotly_dark", color_discrete_sequence=['#00f2ff']
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Temporal Evolution")
    evolution_df = df.groupby(['year', 'quarter'])['amount'].sum().reset_index()
    evolution_df['Time'] = evolution_df['year'].astype(str) + " Q" + evolution_df['quarter'].astype(str)
    fig_line = px.line(
        evolution_df, x='Time', y='amount',
        template="plotly_dark", color_discrete_sequence=['#39ff14']
    )
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("Database unavailable or agg_transaction table missing.")
