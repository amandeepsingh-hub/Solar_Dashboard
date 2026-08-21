"""
Data loading / preparation for the Solar Dashboard.

`load_data()` is the single entry point app.py and visualizations.py use.
Today it's backed by the static tables in `modules/raw_data.py`. Once a
live data source (CSV export, database, API) is available, either update
`raw_data.py` to read from it, or point this function at it directly —
everything downstream keys off the dict shape returned here, so nothing
else needs to change.
"""

import streamlit as st

from modules import raw_data


@st.cache_data
def load_data() -> dict:
    """Return every dataframe / derived value the dashboard needs.

    Keys:
      kpi                   -- df1, the 6 headline KPI cards (display only)
      plant_financials      -- df2, per-plant Investment / Recovery
      plant_capacity        -- df3, per-plant capacity & generation
      monthly               -- df_monthly, tidy long format (Location, Month, ...)
      total_investment_lakhs, total_recovery_lakhs, total_solar_units
                            -- portfolio-wide totals, summed directly from
                               df2 / df3 (the numeric source), not parsed
                               back out of the rounded KPI display strings
    """
    kpi = raw_data.df1.copy()
    plant_financials = raw_data.df2.copy()
    plant_capacity = raw_data.df3.copy()
    monthly = raw_data.df_monthly.copy()

    return {
        "kpi": kpi,
        "plant_financials": plant_financials,
        "plant_capacity": plant_capacity,
        "monthly": monthly,
        "total_investment_lakhs": plant_financials["Investment"].sum(),
        "total_recovery_lakhs": plant_financials["Recovery"].sum(),
        "total_solar_units": plant_capacity["Total Units"].sum(),
    }
