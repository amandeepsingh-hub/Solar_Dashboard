"""
Static source data for the Solar Dashboard (3 plants: Bhiwandi, Raliawas,
Surat), transcribed from the underlying Google Sheet ("W&D solar Plant with
monthly Generation reports.xlsx").

`df4` (wide, one row per plant with a column per month) is the single
source of truth. `df2`, `df3`, and most of `df1`'s KPI cards are DERIVED
from `df4` below rather than re-typed as separate literals.
"""

import numpy as np
import pandas as pd

# ============================================================
# DF4 — LOCATION & MONTH-WISE SOLAR PERFORMANCE (WIDE FORMAT)
# ============================================================

df4 = pd.DataFrame({
    "Location": [
        "Bhiwandi (94+56)",
        "Raliawas",
        "Surat Palsana",
    ],

    "Installation Cost": [4923000.0, 2489000.0, 2667000.0],
    "With GST Cost": [5615940.0, 2728084.0, 269759.0],
    "Installed Solar (kW)": [150.0, 70.0, 71.0],
    "Rate per Unit": [21.8, 7.0, 8.5],
    "Total Unit": [534002.0, 140606.0, 71690.0],          # sheet totals (reconciled below)
    "Total Recovery": [2859963.0, 984242.0, 609365.0],    # sheet totals (reconciled below)

    # --------------------------------------------------------
    # Monthly data (Mar 2025 – Oct 2026)
    # --------------------------------------------------------

    "Mar 25 Solar Unit": [2134.0, np.nan, np.nan],
    "Mar 25 Amount Saved": [46479.0, np.nan, np.nan],
    "Mar 25 Performance %": [17.0, np.nan, np.nan],
    "Mar 25 Unit per KW": [3.3, np.nan, np.nan],

    "April 25 Solar Unit": [7243.0, np.nan, np.nan],
    "April 25 Amount Saved": [157753.0, np.nan, np.nan],
    "April 25 Performance %": [60.0, np.nan, np.nan],
    "April 25 Unit per KW": [3.3, np.nan, np.nan],

    "May 25 Solar Unit": [8299.0, np.nan, np.nan],
    "May 25 Amount Saved": [180752.0, np.nan, np.nan],
    "May 25 Performance %": [67.0, np.nan, np.nan],
    "May 25 Unit per KW": [3.3, np.nan, np.nan],

    "June 25 Solar Unit": [7172.0, np.nan, np.nan],
    "June 25 Amount Saved": [156206.0, np.nan, np.nan],
    "June 25 Performance %": [60.0, np.nan, np.nan],
    "June 25 Unit per KW": [3.3, np.nan, np.nan],

    "July 25 Solar Unit": [5564.0, np.nan, np.nan],
    "July 25 Amount Saved": [121184.0, np.nan, np.nan],
    "July 25 Performance %": [45.0, np.nan, np.nan],
    "July 25 Unit per KW": [np.nan, np.nan, np.nan],

    "Aug 25 Solar Unit": [5208.0, np.nan, np.nan],
    "Aug 25 Amount Saved": [113430.0, np.nan, np.nan],
    "Aug 25 Performance %": [0.4, np.nan, np.nan],
    "Aug 25 Unit per KW": [np.nan, np.nan, np.nan],

    "Sep 25 Solar Unit": [4632.0, np.nan, np.nan],
    "Sep 25 Amount Saved": [100885.0, np.nan, np.nan],
    "Sep 25 Performance %": [39.0, np.nan, np.nan],
    "Sep 25 Unit per KW": [3.3, np.nan, np.nan],

    "Oct 25 Solar Unit": [8192.0, np.nan, np.nan],
    "Oct 25 Amount Saved": [178422.0, np.nan, np.nan],
    "Oct 25 Performance %": [66.0, np.nan, np.nan],
    "Oct 25 Unit per KW": [2.6, 3.6, np.nan],

    "Nov 25 Solar Unit": [11251.0, np.nan, np.nan],
    "Nov 25 Amount Saved": [245047.0, np.nan, np.nan],
    "Nov 25 Performance %": [94.0, np.nan, np.nan],
    "Nov 25 Unit per KW": [3.8, np.nan, np.nan],

    "Dec 25 Solar Unit": [8268.0, np.nan, np.nan],
    "Dec 25 Amount Saved": [180077.0, np.nan, np.nan],
    "Dec 25 Performance %": [67.0, np.nan, np.nan],
    "Dec 25 Unit per KW": [2.7, np.nan, np.nan],

    "Jan 26 Solar Unit": [8958.0, 4693.0, np.nan],
    "Jan 26 Amount Saved": [195105.0, 32851.0, np.nan],
    "Jan 26 Performance %": [0.7, 0.5, np.nan],
    "Jan 26 Unit per KW": [2.9, 2.2, np.nan],

    "Feb 26 Solar Unit": [9210.0, 6974.0, np.nan],
    "Feb 26 Amount Saved": [200594.0, 48818.0, np.nan],
    "Feb 26 Performance %": [82.0, 89.0, np.nan],
    "Feb 26 Unit per KW": [3.3, 3.6, np.nan],

    "Mar 26 Solar Unit": [12679.0, 8256.0, np.nan],
    "Mar 26 Amount Saved": [276149.0, 57792.0, np.nan],
    "Mar 26 Performance %": [102.0, 95.0, np.nan],
    "Mar 26 Unit per KW": [4.1, 3.8, np.nan],

    # ------------------------------------------------------------------
    # KNOWN DATA CORRECTION — Bhiwandi, April 2026, Amount Saved
    # ------------------------------------------------------------------
    # Raw sheet entry is 1,924.0; corrected to 10,821 units * Rs.21.8 = 235,897.8
    "Apr 26 Solar Unit": [10821.0, 9856.0, np.nan],
    "Apr 26 Amount Saved": [235897.8, 68992.0, np.nan],
    "Apr 26 Performance %": [90.0, 114.0, np.nan],
    "Apr 26 Unit per KW": [3.6, 4.7, np.nan],

    "May 26 Solar Units": [16707.0, 9534.0, np.nan],
    "May 26 Amount Saved": [363878.0, 66738.0, np.nan],
    "May 26 Performance %": [93.0, 110.0, np.nan],
    "May 26 Unit per KW": [3.6, 4.4, np.nan],

    "June -26 Solar Units": [15706.0, 9230.0, 5531.0],
    "June -26 Amount Saved": [342078.0, 64610.0, 45631.0],
    "June -26 Performance %": [87.0, 106.0, 63.0],
    "June -26 Unit per KW": [3.4, 4.3, 3.0],

    "Jul 26 Solar Units": [8489.0, 7380.0, 3773.0],
    "Jul 26 Amount Saved": [184890.42, 51660.0, 31127.25],
    "Jul 26 Performance %": [46.0, 85.0, 43.0],
    "Jul 26 Unit per KW": [1.8, 3.4, 1.7],

    "Aug 26 Solar Units": [12422.0, 7058.0, 4735.0],
    "Aug 26 Amount Saved": [270551.16, 49406.0, 39063.75],
    "Aug 26 Performance %": [67.0, 81.0, 54.0],
    "Aug 26 Unit per KW": [2.7, 3.3, 2.2],

    "Sep 26 Solar Units": [12931.0, 6742.0, 5305.0],
    "Sep 26 Amount Saved": [281637.18, 47194.0, 43766.25],
    "Sep 26 Performance %": [70.0, 78.0, 60.0],
    "Sep 26 Unit per KW": [2.8, 3.1, 2.4],

    "OCT - 26 Solar Units": [16038.0, 6273.0, 6715.0],
    "OCT - 26 Amount Saved": [349307.6, 43911.0, 55398.75],
    "OCT - 26 Performance %": [86.0, 72.0, 76.0],
    "OCT - 26 Unit per KW": [3.4, 2.9, 3.1],
})

# Normalize location names for consistency
df4["Location"] = df4["Location"].replace({
    "Bhiwandi (94+56)": "Bhiwandi",
    "Surat Palsana": "Surat",
})

# ------------------------------------------------------------------
# Reconcile "Total Unit" and "Total Recovery" with monthly columns.
#
# The Google Sheet's "Total Unit" and "Total Recovery" columns include
# cumulative historical totals accrued prior to the monthly breakdown
# columns (through Sep-26, plus Oct-26 in the sheet's latest totals).
# We preserve the historical pre-tracking baseline and add the sum of
# all tracked monthly columns (including the Apr-26 Bhiwandi fix).
# ------------------------------------------------------------------

_amount_saved_cols = [c for c in df4.columns if "Amount Saved" in c]
_monthly_recovery_sum = df4[_amount_saved_cols].sum(axis=1, skipna=True)

# Pre-tracking recovery offsets (Sheet Total Recovery minus tracked monthly sum using raw Apr-26 value)
_PRE_TRACKING_RECOVERY = pd.Series(
    [
        2859963.0 - (_monthly_recovery_sum.iloc[0] - 235897.8 + 1924.0),  # Bhiwandi historical offset
        984242.0 - _monthly_recovery_sum.iloc[1],                        # Raliawas historical offset
        609365.0 - _monthly_recovery_sum.iloc[2],                        # Surat historical offset
    ],
    index=df4.index,
)
df4["Total Recovery"] = _PRE_TRACKING_RECOVERY + _monthly_recovery_sum

_unit_cols = [c for c in df4.columns if "Solar Unit" in c]
_monthly_unit_sum = df4[_unit_cols].sum(axis=1, skipna=True)

# Pre-tracking unit offsets (Sheet Total Unit minus tracked monthly sum)
_PRE_TRACKING_UNITS = pd.Series(
    [
        534002.0 - _monthly_unit_sum.iloc[0],
        140606.0 - _monthly_unit_sum.iloc[1],
        71690.0 - _monthly_unit_sum.iloc[2],
    ],
    index=df4.index,
)
df4["Total Unit"] = _PRE_TRACKING_UNITS + _monthly_unit_sum

# ============================================================
# DF2 — PLANT-LEVEL INVESTMENT / RECOVERY (derived from df4)
# ============================================================

df2 = pd.DataFrame({
    "Plant": df4["Location"],
    "Investment": df4["Installation Cost"] / 1e5,   # -> Rs. Lakhs
    "Recovery": df4["Total Recovery"] / 1e5,          # -> Rs. Lakhs
}).reset_index(drop=True)
df2["Recovery %"] = df2["Recovery"] / df2["Investment"] * 100

# ============================================================
# DF3 — PLANT CAPACITY & GENERATION (derived from df4)
# ============================================================

df3 = pd.DataFrame({
    "Plant": df4["Location"],
    "Capacity": df4["Installed Solar (kW)"],
    "Total Units": df4["Total Unit"],
    "Total Savings": df4["Total Recovery"] / 1e5,  # -> Rs. Lakhs
}).reset_index(drop=True)

# ============================================================
# DF1 — HEADLINE KPI CARDS (derived from df2 / df3)
# ============================================================

df1 = pd.DataFrame({
    "KPI": [
        "Total Solar Plants",
        "Total Installed Capacity",
        "Total Energy Generated",
        "Total Savings (Recovery)",
        "Total Investment (Without GST)",
        "Overall Recovery Achieved",
    ],
    "Value": [
        str(len(df3)),
        f"{int(df3['Capacity'].sum())} kW",
        f"{int(df3['Total Units'].sum()):,} Units",
        f"₹{df2['Recovery'].sum():.2f} Lakhs",
        f"₹{df2['Investment'].sum() / 100:.2f} Crore",
        f"~{round(df2['Recovery'].sum() / df2['Investment'].sum() * 100)}% of investment",
    ],
})


def _build_monthly(source: pd.DataFrame) -> pd.DataFrame:
    """Reshape df4 from wide (one row per plant, one set of columns per
    month) into a tidy long format: one row per (Location, Month)."""

    month_columns = [
        ("Mar 25", "Mar 25 Solar Unit", "Mar 25 Amount Saved", "Mar 25 Performance %", "Mar 25 Unit per KW"),
        ("Apr 25", "April 25 Solar Unit", "April 25 Amount Saved", "April 25 Performance %", "April 25 Unit per KW"),
        ("May 25", "May 25 Solar Unit", "May 25 Amount Saved", "May 25 Performance %", "May 25 Unit per KW"),
        ("Jun 25", "June 25 Solar Unit", "June 25 Amount Saved", "June 25 Performance %", "June 25 Unit per KW"),
        ("Jul 25", "July 25 Solar Unit", "July 25 Amount Saved", "July 25 Performance %", "July 25 Unit per KW"),
        ("Aug 25", "Aug 25 Solar Unit", "Aug 25 Amount Saved", "Aug 25 Performance %", "Aug 25 Unit per KW"),
        ("Sep 25", "Sep 25 Solar Unit", "Sep 25 Amount Saved", "Sep 25 Performance %", "Sep 25 Unit per KW"),
        ("Oct 25", "Oct 25 Solar Unit", "Oct 25 Amount Saved", "Oct 25 Performance %", "Oct 25 Unit per KW"),
        ("Nov 25", "Nov 25 Solar Unit", "Nov 25 Amount Saved", "Nov 25 Performance %", "Nov 25 Unit per KW"),
        ("Dec 25", "Dec 25 Solar Unit", "Dec 25 Amount Saved", "Dec 25 Performance %", "Dec 25 Unit per KW"),
        ("Jan 26", "Jan 26 Solar Unit", "Jan 26 Amount Saved", "Jan 26 Performance %", "Jan 26 Unit per KW"),
        ("Feb 26", "Feb 26 Solar Unit", "Feb 26 Amount Saved", "Feb 26 Performance %", "Feb 26 Unit per KW"),
        ("Mar 26", "Mar 26 Solar Unit", "Mar 26 Amount Saved", "Mar 26 Performance %", "Mar 26 Unit per KW"),
        ("Apr 26", "Apr 26 Solar Unit", "Apr 26 Amount Saved", "Apr 26 Performance %", "Apr 26 Unit per KW"),
        ("May 26", "May 26 Solar Units", "May 26 Amount Saved", "May 26 Performance %", "May 26 Unit per KW"),
        ("Jun 26", "June -26 Solar Units", "June -26 Amount Saved", "June -26 Performance %", "June -26 Unit per KW"),
        ("Jul 26", "Jul 26 Solar Units", "Jul 26 Amount Saved", "Jul 26 Performance %", "Jul 26 Unit per KW"),
        ("Aug 26", "Aug 26 Solar Units", "Aug 26 Amount Saved", "Aug 26 Performance %", "Aug 26 Unit per KW"),
        ("Sep 26", "Sep 26 Solar Units", "Sep 26 Amount Saved", "Sep 26 Performance %", "Sep 26 Unit per KW"),
        ("Oct 26", "OCT - 26 Solar Units", "OCT - 26 Amount Saved", "OCT - 26 Performance %", "OCT - 26 Unit per KW"),
    ]

    records = []
    for _, row in source.iterrows():
        for month, unit_col, saving_col, performance_col, unit_kw_col in month_columns:
            records.append({
                "Location": row["Location"],
                "Month": month,
                "Solar Units": row[unit_col],
                "Amount Saved": row[saving_col],
                "Performance %": row[performance_col],
                "Unit per KW": row[unit_kw_col],
            })

    monthly = pd.DataFrame(records)
    monthly["Month"] = pd.to_datetime(monthly["Month"], format="%b %y")
    monthly = monthly.sort_values(["Month", "Location"]).reset_index(drop=True)
    return monthly


df_monthly = _build_monthly(df4)
