
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Ghana Petroleum Intelligence Dashboard",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main app background */
    .stApp {
        background-color: #f1f5f9;
    }

    /* Main content container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* KPI metric cards */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-size: 15px;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 700;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 12px;
        padding: 10px 18px;
        border: 1px solid #e2e8f0;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0f172a;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Charts */
    .js-plotly-plot {
        border-radius: 16px;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA
# =========================================================

DATA_PATH = Path("data/processed/ghana_petroleum_analytics.csv")

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df["year"] = df["year"].astype(int)

    return df.sort_values("year")

df = load_data()

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_money(value):

    if value >= 1e9:
        return f"${value / 1e9:.2f}B"

    return f"${value / 1e6:.1f}M"

def format_barrels(value):

    return f"{value / 1e6:.1f}M"

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Dashboard Controls")

min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
].copy()

st.sidebar.markdown("---")

st.sidebar.caption(
    "Data Sources: PIAC Annual Reports and Brent crude oil price data."
)

# =========================================================
# HEADER
# =========================================================

header_html = """
<div style='
padding:34px;
border-radius:22px;
background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 55%,#0369a1 100%);
margin-bottom:30px;
box-shadow:0 10px 30px rgba(15,23,42,0.15);
'>

<h1 style='
color:white;
margin-bottom:12px;
font-size:44px;
font-weight:700;
'>
Ghana Petroleum Intelligence Dashboard
</h1>

<p style='
color:#dbeafe;
font-size:18px;
margin-bottom:0px;
max-width:900px;
line-height:1.6;
'>
Interactive analysis of Ghana’s petroleum production,
petroleum revenues, Brent crude oil prices,
and revenue efficiency trends from 2011–2025.
</p>

</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# =========================================================
# KPI SECTION
# =========================================================

total_revenue = filtered_df["petroleum_revenue_usd"].sum()

total_production = filtered_df["total_production_barrels"].sum()

avg_revenue_per_barrel = (
    filtered_df["revenue_per_barrel"].mean()
)

avg_brent_price = (
    filtered_df["brent_price_usd"].mean()
)

peak_revenue_year = filtered_df.loc[
    filtered_df["petroleum_revenue_usd"].idxmax(),
    "year"
]

peak_production_year = filtered_df.loc[
    filtered_df["total_production_barrels"].idxmax(),
    "year"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Petroleum Revenue",
    format_money(total_revenue)
)

col2.metric(
    "Total Oil Production",
    format_barrels(total_production)
)

col3.metric(
    "Avg Revenue per Barrel",
    f"${avg_revenue_per_barrel:.2f}"
)

col4.metric(
    "Avg Brent Price",
    f"${avg_brent_price:.2f}"
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Executive Overview",
        "Revenue Analysis",
        "Production Analysis",
        "Revenue Efficiency",
        "Data Explorer"
    ]
)

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

with tab1:

    st.subheader("Executive Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.info(
            f"""
            Peak petroleum revenue occurred in {int(peak_revenue_year)}
            with total receipts of
            {format_money(filtered_df['petroleum_revenue_usd'].max())}.
            """
        )

    with summary_col2:

        st.info(
            f"""
            Peak oil production occurred in {int(peak_production_year)}
            with production of
            {format_barrels(filtered_df['total_production_barrels'].max())}
            barrels.
            """
        )

    overview_df = filtered_df.copy()

    overview_df["revenue_millions"] = (
        overview_df["petroleum_revenue_usd"] / 1e6
    )

    overview_df["production_million_barrels"] = (
        overview_df["total_production_barrels"] / 1e6
    )

    fig_overview = px.line(
        overview_df,
        x="year",
        y=[
            "revenue_millions",
            "production_million_barrels"
        ],
        markers=True,
        title="Revenue and Production Trends",
        template="plotly_white"
    )

    fig_overview.update_layout(
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(
        fig_overview,
        use_container_width=True
    )

# =========================================================
# REVENUE ANALYSIS
# =========================================================

with tab2:

    st.subheader("Petroleum Revenue Analysis")

    revenue_df = filtered_df.copy()

    revenue_df["revenue_millions"] = (
        revenue_df["petroleum_revenue_usd"] / 1e6
    )

    fig_revenue = px.bar(
        revenue_df,
        x="year",
        y="revenue_millions",
        text="revenue_millions",
        title="Annual Petroleum Revenue",
        template="plotly_white"
    )

    fig_revenue.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside"
    )

    fig_revenue.update_layout(height=500)

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

# =========================================================
# PRODUCTION ANALYSIS
# =========================================================

with tab3:

    st.subheader("Oil Production Analysis")

    production_df = filtered_df.copy()

    production_df["production_million_barrels"] = (
        production_df["total_production_barrels"] / 1e6
    )

    fig_production = px.bar(
        production_df,
        x="year",
        y="production_million_barrels",
        text="production_million_barrels",
        title="Annual Oil Production",
        template="plotly_white"
    )

    fig_production.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig_production.update_layout(height=500)

    st.plotly_chart(
        fig_production,
        use_container_width=True
    )

# =========================================================
# REVENUE EFFICIENCY
# =========================================================

with tab4:

    st.subheader("Revenue Efficiency Analysis")

    fig_efficiency = px.line(
        filtered_df,
        x="year",
        y="revenue_per_barrel",
        markers=True,
        title="Revenue Earned per Barrel",
        template="plotly_white"
    )

    fig_efficiency.update_layout(
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(
        fig_efficiency,
        use_container_width=True
    )

    comparison_df = filtered_df[
        [
            "year",
            "revenue_per_barrel",
            "brent_price_usd"
        ]
    ].melt(
        id_vars="year",
        var_name="metric",
        value_name="usd"
    )

    comparison_df["metric"] = comparison_df["metric"].replace(
        {
            "revenue_per_barrel":
            "Revenue per Barrel",

            "brent_price_usd":
            "Brent Crude Price"
        }
    )

    fig_compare = px.line(
        comparison_df,
        x="year",
        y="usd",
        color="metric",
        markers=True,
        title="Brent Price vs Revenue per Barrel",
        template="plotly_white"
    )

    fig_compare.update_layout(
        hovermode="x unified",
        height=500
    )

    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )

# =========================================================
# DATA EXPLORER
# =========================================================

with tab5:

    st.subheader("Dataset Explorer")

    display_df = filtered_df.copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv = display_df.to_csv(index=False)

    st.download_button(
        label="Download Filtered Dataset",
        data=csv,
        file_name="ghana_petroleum_filtered.csv",
        mime="text/csv"
    )

