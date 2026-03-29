import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_db_connection, format_currency, format_count

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
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM agg_user", conn)
        return df
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        return pd.DataFrame()

df = load_user_data()

if not df.empty:
    years = sorted(df['year'].unique().tolist())
    quarters = sorted(df['quarter'].unique().tolist())
    
    col_y, col_q = st.columns(2)
    with col_y:
        sel_year = st.selectbox("Year Filter", years, index=len(years)-1)
    with col_q:
        sel_quarter = st.selectbox("Quarter Filter", quarters)
    
    filtered_df = df[(df['year'] == sel_year) & (df['quarter'] == sel_quarter)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("User Interface (Brands)")
        brand_data = filtered_df.groupby('brand')['brand_count'].sum().reset_index()
        fig_brand = px.pie(
            brand_data, values='brand_count', names='brand',
            template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_brand.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_brand, use_container_width=True)
        
    with col2:
        st.subheader("Regional User Density")
        state_users = filtered_df.groupby('state')['registered_users'].max().reset_index().sort_values(by='registered_users', ascending=False).head(10)
        fig_state = px.bar(
            state_users, x='registered_users', y='state', orientation='h',
            template="plotly_dark", color_discrete_sequence=['#39ff14']
        )
        fig_state.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_state, use_container_width=True)

    st.subheader("User Base Expansion")
    growth_df = df.groupby(['year', 'quarter'])['registered_users'].sum().reset_index()
    growth_df['Time'] = growth_df['year'].astype(str) + " Q" + growth_df['quarter'].astype(str)
    fig_growth = px.bar(
        growth_df, x='Time', y='registered_users',
        template="plotly_dark", color_discrete_sequence=['#00f2ff']
    )
    fig_growth.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_growth, use_container_width=True)
else:
    st.warning("Database unavailable or agg_user table missing.")
