import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_db_connection, format_currency, format_count

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
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM map_transaction", conn)
        return df
    except Exception as e:
        st.error(f"Error loading map data: {e}. Attempting to fix...")
        return pd.DataFrame()

df = load_geo_data()

if not df.empty:
    years = sorted(df['year'].unique().tolist())
    quarters = sorted(df['quarter'].unique().tolist())
    
    col_y, col_q = st.columns(2)
    with col_y:
        selected_year = st.selectbox("Temporal Orbit (Year)", years, index=len(years)-1)
    with col_q:
        selected_quarter = st.selectbox("Orbital Phase (Quarter)", quarters)
    
    filtered_df = df[(df['year'] == selected_year) & (df['quarter'] == selected_quarter)]
    
    state_data = filtered_df.groupby('state')['amount'].sum().reset_index()
    
    # India GeoJSON URL
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d1ee30ad47b0a52ba51/raw/e383541619b4412282476ef1047ec059/india_states.geojson"
    
    st.subheader(f"Transaction Density - {selected_year} Q{selected_quarter}")
    
    fig = px.choropleth(
        state_data,
        geojson=geojson_url,
        featureidkey='properties.ST_NM',
        locations='state',
        color='amount',
        color_continuous_scale='Viridis',
        range_color=(0, state_data['amount'].max()),
        hover_name='state',
        title='Total Transaction Amount by State',
        template='plotly_dark'
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0},
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("State-wise Breakdown")
    st.dataframe(state_data.sort_values(by='amount', ascending=False), use_container_width=True)
else:
    st.warning("Database unavailable or map_transaction table missing.")
