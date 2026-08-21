"""
Solar Dashboard — main Streamlit entry point.

Single-page layout: headline KPI cards, then the 4 visualizations in tabs.
A sidebar plant filter narrows the first two tabs (Investment Recovery and
Monthly Value Creation); the gauge and environmental-impact tabs always
reflect the full 3-plant portfolio, since they're derived from fixed
headline totals rather than a per-plant breakdown.
"""

import streamlit as st

from modules.data_loader import load_data
from modules.visualizations import render_kpi_header, viz_one, viz_two, viz_three, viz_four

st.set_page_config(
    page_title="Solar Dashboard W & D",
    page_icon="☀️",
    layout="wide",
)

st.title("☀️ Solar Dashboard W & D ")

data = load_data()

render_kpi_header(data)
st.divider()

with st.sidebar:
    st.header("Filters")
    locations = sorted(data["plant_financials"]["Plant"].unique())
    selected_locations = st.multiselect(
        "Plant",
        options=locations,
        default=locations,
        help="Applies to the Investment Recovery and Monthly Value Creation tabs.",
    )

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Investment Recovery",
        "Monthly Value Creation",
        "Recovery Progress",
        "Environmental Impact",
    ]
)

with tab1:
    viz_one(data, selected_locations)

with tab2:
    viz_two(data, selected_locations)

with tab3:
    viz_three(data)
    st.caption("Reflects the full 3-plant portfolio.")

with tab4:
    viz_four(data)
    st.caption("Reflects the full 3-plant portfolio.")
