
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="SalesPulse | Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = Path(__file__).parent / "dataset" / "superstore.csv"

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #4f46e5;
    --primary-light: #eef2ff;
    --background: #f7f8fc;
    --surface: #ffffff;
    --heading: #172033;
    --muted: #8490a5;
    --border: #e9edf5;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--background);
}

.block-container {
    max-width: 1500px;
    padding: 2rem 2.5rem 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #171e35;
}

[data-testid="stSidebar"] * {
    color: #e8ecf8;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #aab4ce;
}

[data-testid="stSidebar"] label {
    color: #dce3f5 !important;
    font-weight: 600;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #252e49;
    border: 1px solid #3b4765;
    border-radius: 9px;
}

.sidebar-brand {
    padding: 10px 0 24px;
}

.sidebar-logo {
    background: linear-gradient(135deg, #6366f1, #14b8a6);
    display: inline-flex;
    width: 43px;
    height: 43px;
    border-radius: 13px;
    justify-content: center;
    align-items: center;
    font-size: 22px;
    margin-bottom: 12px;
}

.sidebar-title {
    font-size: 21px;
    font-weight: 800;
    color: white;
}

.sidebar-subtitle {
    font-size: 11px;
    color: #9caaca;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Page header */
.eyebrow {
    color: #6366f1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.main-title {
    font-size: 31px;
    line-height: 1.25;
    font-weight: 800;
    letter-spacing: -1.1px;
    color: var(--heading);
}

.main-subtitle {
    color: var(--muted);
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 24px;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 20px 20px 17px;
    box-shadow: 0 5px 18px rgba(30, 41, 59, 0.035);
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #78859b !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #172033 !important;
    font-size: 27px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 11px;
}

/* Section headings */
.section-heading {
    color: #202b42;
    font-size: 17px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 3px;
}

.section-description {
    color: #929db0;
    font-size: 12px;
    margin-bottom: 13px;
}

/* Chart containers */
[data-testid="stPlotlyChart"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 4px 16px rgba(30, 41, 59, 0.025);
}

/* Table */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

/* Buttons */
.stDownloadButton button {
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 18px;
    font-weight: 650;
}

.stDownloadButton button:hover {
    background: #4338ca;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #9aa4b5;
    font-size: 11px;
    padding-top: 30px;
}

hr {
    border-color: #e9edf5;
}

@media(max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .main-title {
        font-size: 24px;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "Order_ID", "Product", "Category",
        "Region", "Sales", "Profit"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))

    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0)
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0)

    return df


try:
    data = load_data()
except Exception as error:
    st.error(f"Unable to load the sales dataset: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">▥</div>
        <div class="sidebar-title">SalesPulse</div>
        <div class="sidebar-subtitle">Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Dashboard Filters")

    categories = sorted(data["Category"].dropna().unique())
    regions = sorted(data["Region"].dropna().unique())

    selected_categories = st.multiselect(
        "Product Category",
        categories,
        default=categories
    )

    selected_regions = st.multiselect(
        "Sales Region",
        regions,
        default=regions
    )

    st.markdown("---")
    st.markdown("### About")

    st.caption(
        "Analyze sales performance, revenue, "
        "profitability and product contributions."
    )

    st.markdown("---")
    st.caption("DATA SOURCE")
    st.caption("Sample CSV Sales Dataset")


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------
filtered = data[
    data["Category"].isin(selected_categories) &
    data["Region"].isin(selected_regions)
].copy()


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------
st.markdown("""
<div class="eyebrow">BUSINESS INTELLIGENCE</div>
<div class="main-title">Sales Performance Overview</div>
<div class="main-subtitle">
Understand your business performance through clear sales insights and analytics.
</div>
""", unsafe_allow_html=True)

st.divider()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
revenue = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()
products = filtered["Product"].nunique()

profit_margin = (profit / revenue * 100) if revenue else 0
average_order_value = (revenue / orders) if orders else 0


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.markdown(
    '<div class="section-heading">Business Summary</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Key performance indicators for the selected filters</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"₹{revenue:,.0f}")
c2.metric("📈 Total Profit", f"₹{profit:,.0f}")
c3.metric("🛒 Total Orders", f"{orders:,}")
c4.metric("📦 Products Sold", f"{products:,}")

c5, c6 = st.columns(2)

c5.metric("Profit Margin", f"{profit_margin:.1f}%")
c6.metric("Average Order Value", f"₹{average_order_value:,.0f}")


# --------------------------------------------------
# CHART STYLE
# --------------------------------------------------
COLORS = [
    "#4f46e5",
    "#14b8a6",
    "#f59e0b",
    "#8b5cf6",
    "#ec4899"
]

def style_chart(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Inter, sans-serif",
            color="#64748b",
            size=11
        ),
        margin=dict(l=15, r=20, t=25, b=15),
        hoverlabel=dict(
            bgcolor="#172033",
            font_color="white"
        )
    )
    return fig


# --------------------------------------------------
# CHART 1 AND 2
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-heading">Sales Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Understand revenue distribution across categories and regions</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2, gap="large")

with left:

    category_data = (
        filtered.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig1 = px.pie(
        category_data,
        names="Category",
        values="Sales",
        hole=0.62,
        color_discrete_sequence=COLORS
    )

    fig1.update_traces(
        textinfo="percent",
        textposition="inside",
        marker=dict(line=dict(color="white", width=3)),
        hovertemplate="%{label}<br>Revenue: ₹%{value:,.0f}<extra></extra>"
    )

    fig1.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.08,
            x=0.1
        )
    )

    style_chart(fig1)
    st.plotly_chart(fig1, use_container_width=True)

with right:

    region_data = (
        filtered.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=True)
    )

    fig2 = px.bar(
        region_data,
        x="Sales",
        y="Region",
        orientation="h",
        text="Sales",
        color="Sales",
        color_continuous_scale=["#c7d2fe", "#4f46e5"]
    )

    fig2.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig2.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Revenue (₹)",
        yaxis_title="",
        xaxis=dict(showgrid=True, gridcolor="#edf0f6"),
        yaxis=dict(showgrid=False)
    )

    style_chart(fig2)
    st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------
# CHART 3 AND 4
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-heading">Product & Profit Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Compare product revenue and profit contribution</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2, gap="large")

product_data = (
    filtered.groupby("Product", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Sales", ascending=True)
)

with left:

    fig3 = px.bar(
        product_data,
        x="Sales",
        y="Product",
        orientation="h",
        text="Sales",
        color="Sales",
        color_continuous_scale=["#bfdbfe", "#2563eb"]
    )

    fig3.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig3.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Revenue (₹)",
        yaxis_title="",
        xaxis=dict(showgrid=True, gridcolor="#edf0f6"),
        yaxis=dict(showgrid=False)
    )

    style_chart(fig3)
    st.plotly_chart(fig3, use_container_width=True)

with right:

    profit_data = (
        filtered.groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=True)
    )

    fig4 = px.bar(
        profit_data,
        x="Region",
        y="Profit",
        text="Profit",
        color="Profit",
        color_continuous_scale=["#a7f3d0", "#0f9d8a"]
    )

    fig4.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig4.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Region",
        yaxis_title="Profit (₹)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#edf0f6")
    )

    style_chart(fig4)
    st.plotly_chart(fig4, use_container_width=True)


# --------------------------------------------------
# TRANSACTION TABLE
# --------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-heading">Sales Transactions</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">View the records based on your selected filters</div>',
    unsafe_allow_html=True
)

if filtered.empty:
    st.info("No sales records match the selected filters.")
else:
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------
st.markdown("---")

download_col, info_col = st.columns([1, 2])

with download_col:

    st.markdown("### Export Report")

    st.download_button(
        label="⬇ Download Sales Report",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="sales_report.csv",
        mime="text/csv",
        use_container_width=True
    )

with info_col:

    st.markdown("### Report Information")

    st.caption(
        f"Showing {len(filtered)} records from the sample dataset. "
        "The downloaded CSV contains the currently filtered records."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
    SalesPulse Analytics Dashboard · Built with Python, Streamlit, Pandas and Plotly
</div>
""", unsafe_allow_html=True)
