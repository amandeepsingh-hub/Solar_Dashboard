"""
Visualization functions for the Solar Dashboard — the 4 charts, adapted
from the provided Plotly code to render inside Streamlit (st.plotly_chart
instead of fig.show()) with layout tweaks so labels/annotations never
clip or overlap:

  viz_one   -- Investment Recovery by Solar Plant (stacked horizontal bar)
  viz_two   -- Monthly Solar Value Creation (bars + line, dual axis)
  viz_three -- Investment Recovery Progress (gauge)
  viz_four  -- Environmental Impact (CO2 avoided / tree equivalent)

Each function takes the `data` dict returned by modules.data_loader.load_data().
viz_one / viz_two also take an optional `selected_locations` list to filter
by plant; viz_three / viz_four always reflect the full portfolio (they're
derived from the fixed KPI totals, not a per-plant breakdown).
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

PLANT_COLORS = {
    "Bhiwandi": "#4F81BD",
    "Raliawas": "#A7ADB4",
    "Surat": "#D6A84F",
}


def render_kpi_header(data: dict) -> None:
    """Headline KPI cards (from df1), shown above the tabs.

    Laid out 3-per-row (instead of all 6 squeezed into one row) so the
    longer labels and values have room to render in full rather than
    getting truncated or wrapped awkwardly. The two longest labels are
    also shortened, with the trimmed detail moved into a hover tooltip.
    """
    kpi = data["kpi"]

    label_overrides = {
        "Total Savings (Recovery)": ("Total Savings", "Recovery amount to date"),
        "Total Investment (Without GST)": ("Total Investment", "Excludes GST"),
        "Overall Recovery Achieved": ("Recovery Achieved", "Overall, as a % of total investment"),
    }

    kpi_rows = [kpi.iloc[i : i + 3] for i in range(0, len(kpi), 3)]
    for kpi_row in kpi_rows:
        cols = st.columns(len(kpi_row))
        for col, (_, row) in zip(cols, kpi_row.iterrows()):
            label, help_text = label_overrides.get(row["KPI"], (row["KPI"], None))
            col.metric(label, row["Value"], help=help_text)


def viz_one(data: dict, selected_locations=None) -> None:
    """Visualization 1 — Investment Recovery by Solar Plant."""
    st.subheader("Investment Recovery by Solar Plant")

    df_recovery = data["plant_financials"].rename(columns={"Plant": "Location"}).copy()

    for col in ("Investment", "Recovery", "Recovery %"):
        df_recovery[col] = (
            df_recovery[col]
            .astype(str)
            .str.replace("₹", "", regex=False)
            .str.replace("Lakh", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df_recovery[col] = pd.to_numeric(df_recovery[col], errors="coerce")

    df_recovery = df_recovery.rename(
        columns={"Investment": "Investment (₹ Lakhs)", "Recovery": "Recovery (₹ Lakhs)"}
    )
    df_recovery["Unrecovered (₹ Lakhs)"] = (
        df_recovery["Investment (₹ Lakhs)"] - df_recovery["Recovery (₹ Lakhs)"]
    ).clip(lower=0)

    if selected_locations is not None:
        df_recovery = df_recovery[df_recovery["Location"].isin(selected_locations)]

    if df_recovery.empty:
        st.info("Select at least one plant in the sidebar to see this chart.")
        return

    df_recovery = df_recovery.sort_values("Recovery %", ascending=True).reset_index(drop=True)

    max_investment = df_recovery["Investment (₹ Lakhs)"].max()
    axis_max = max_investment * 1.4  # headroom so "% recovered" labels never clip

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=df_recovery["Location"],
            x=df_recovery["Unrecovered (₹ Lakhs)"],
            name="Investment Yet to Recover",
            orientation="h",
            marker=dict(color="#E6E9ED"),
            hovertemplate="<b>%{y}</b><br>Yet to Recover: <b>₹%{x:.2f} Lakhs</b><extra></extra>",
        )
    )

    for _, row in df_recovery.iterrows():
        fig.add_trace(
            go.Bar(
                y=[row["Location"]],
                x=[row["Recovery (₹ Lakhs)"]],
                name=row["Location"],
                orientation="h",
                marker=dict(color=PLANT_COLORS.get(row["Location"], "#4F81BD")),
                hovertemplate=(
                    "<b>%{y}</b><br>Recovered: <b>₹%{x:.2f} Lakhs</b><br>"
                    f"Recovery: <b>{row['Recovery %']:.1f}%</b><extra></extra>"
                ),
            )
        )

    for _, row in df_recovery.iterrows():
        fig.add_annotation(
            x=row["Investment (₹ Lakhs)"] + axis_max * 0.02,
            y=row["Location"],
            text=f"<b>{row['Recovery %']:.1f}% recovered</b>",
            showarrow=False,
            xanchor="left",
            font=dict(size=13, color="#37474F"),
        )
        fig.add_annotation(
            x=row["Investment (₹ Lakhs)"],
            y=row["Location"],
            text=f"₹{row['Investment (₹ Lakhs)']:.2f} L",
            showarrow=False,
            xanchor="right",
            xshift=-6,
            font=dict(size=11, color="#263238"),
        )

    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        height=460,
        title=dict(
            text=(
                "<b>Investment Recovery by Solar Plant</b>"
                "<br><sup>Recovered capital vs. remaining investment</sup>"
            ),
            x=0.02,
            xanchor="left",
            font=dict(size=22, color="#263238"),
        ),
        xaxis=dict(
            title=dict(text="<b>Investment Value (₹ Lakhs)</b>", font=dict(size=14, color="#37474F")),
            range=[0, axis_max],
            showgrid=True,
            gridcolor="rgba(100,110,120,0.10)",
            zeroline=False,
            showline=True,
            linecolor="#D0D5DA",
            tickfont=dict(size=11, color="#59636E"),
        ),
        yaxis=dict(
            title=dict(text="<b>Solar Plant</b>", font=dict(size=14, color="#37474F")),
            showgrid=False,
            tickfont=dict(size=13, color="#263238"),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, font=dict(size=11)),
        bargap=0.35,
        plot_bgcolor="#FBFCFD",
        paper_bgcolor="white",
        margin=dict(l=100, r=40, t=110, b=60),
    )

    st.plotly_chart(fig, width="stretch")


def viz_two(data: dict, selected_locations=None) -> None:
    """Visualization 2 — Monthly Solar Value Creation (portfolio level)."""
    st.subheader("Monthly Solar Value Creation")

    df_value = data["monthly"].copy()
    df_value["Solar Units"] = pd.to_numeric(df_value["Solar Units"], errors="coerce")
    df_value["Amount Saved"] = pd.to_numeric(df_value["Amount Saved"], errors="coerce")
    df_value = df_value.dropna(subset=["Month", "Solar Units", "Amount Saved"])

    if selected_locations is not None:
        df_value = df_value[df_value["Location"].isin(selected_locations)]

    if df_value.empty:
        st.info("Select at least one plant in the sidebar to see this chart.")
        return

    portfolio = (
        df_value.groupby("Month", as_index=False)
        .agg(Solar_Units=("Solar Units", "sum"), Amount_Saved=("Amount Saved", "sum"))
        .sort_values("Month")
        .reset_index(drop=True)
    )
    portfolio["Savings_Lakhs"] = portfolio["Amount_Saved"] / 100_000

    total_savings = portfolio["Amount_Saved"].sum() / 100_000
    total_units = portfolio["Solar_Units"].sum()

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Total Savings", f"₹{total_savings:.2f} L")
    metric_col2.metric("Total Solar Units", f"{total_units:,.0f}")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=portfolio["Month"],
            y=portfolio["Savings_Lakhs"],
            name="Monthly Savings",
            marker=dict(color="#5B8DB8"),
            text=[f"₹{v:.1f}L" for v in portfolio["Savings_Lakhs"]],
            textposition="outside",
            textfont=dict(size=10, color="#37474F"),
            cliponaxis=False,
            customdata=portfolio[["Solar_Units"]].values,
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>Monthly Savings: <b>₹%{y:.2f} Lakhs</b><br>"
                "Solar Generation: <b>%{customdata[0]:,.0f} Units</b><extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=portfolio["Month"],
            y=portfolio["Solar_Units"],
            name="Solar Generation",
            mode="lines+markers",
            yaxis="y2",
            line=dict(color="#D2A84C", width=4),
            marker=dict(size=7, color="#D2A84C", line=dict(color="white", width=2)),
            hovertemplate="<b>%{x|%b %Y}</b><br>Solar Generation: <b>%{y:,.0f} Units</b><extra></extra>",
        )
    )

    # Headroom on both y-axes so bar text ("outside") and line markers never
    # clip against the top of the plot or the legend.
    savings_max = portfolio["Savings_Lakhs"].max()
    units_max = portfolio["Solar_Units"].max()

    fig.update_layout(
        template="plotly_white",
        height=520,
        title=dict(
            text=(
                "<b>Monthly Solar Value Creation</b>"
                "<br><sup>Portfolio-wide energy generation translated into financial savings</sup>"
            ),
            x=0.02,
            xanchor="left",
            font=dict(size=22, color="#263238"),
        ),
        yaxis=dict(
            title=dict(text="<b>Monthly Savings (₹ Lakhs)</b>", font=dict(size=14, color="#37474F")),
            range=[0, savings_max * 1.25],
            showgrid=True,
            gridcolor="rgba(100,110,120,0.10)",
            zeroline=False,
            tickfont=dict(size=11, color="#59636E"),
        ),
        yaxis2=dict(
            title=dict(text="<b>Solar Generation (Units)</b>", font=dict(size=14, color="#A57E27")),
            range=[0, units_max * 1.25],
            overlaying="y",
            side="right",
            showgrid=False,
            tickformat=",",
            tickfont=dict(size=11, color="#A57E27"),
        ),
        xaxis=dict(
            title=dict(text="<b>Month</b>", font=dict(size=14, color="#37474F")),
            tickformat="%b %Y",
            tickangle=-45,
            showgrid=False,
            showline=True,
            linecolor="#D0D5DA",
            tickfont=dict(size=11, color="#59636E"),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=12)),
        plot_bgcolor="#FBFCFD",
        paper_bgcolor="white",
        margin=dict(l=90, r=90, t=100, b=90),
    )

    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Two scales share this chart (savings on the left, units on the right) — "
        "read them as two independent series indexed to the same months, not as one ratio."
    )


def viz_three(data: dict) -> None:
    """Visualization 3 — Investment Recovery Progress (gauge)."""
    st.subheader("Investment Recovery Progress")

    investment = data["total_investment_lakhs"]
    recovery = data["total_recovery_lakhs"]
    remaining = max(investment - recovery, 0)
    recovery_pct = (recovery / investment) * 100 if investment else 0

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=recovery_pct,
            number=dict(suffix="%", font=dict(size=44, color="#3E5F78")),
            title=dict(
                text=(
                    "<b>Investment Recovery</b>"
                    "<br><span style='font-size:12px'>Progress toward full investment recovery</span>"
                ),
                font=dict(size=18, color="#263238"),
            ),
            gauge=dict(
                shape="angular",
                axis=dict(range=[0, 100], tickwidth=1, tickcolor="#B0BEC5", tickfont=dict(size=11, color="#607D8B")),
                bar=dict(color="#6F9E78", thickness=0.30),
                bgcolor="#EEF2F3",
                borderwidth=0,
                steps=[
                    dict(range=[0, 25], color="#F1F3F4"),
                    dict(range=[25, 50], color="#E7ECE8"),
                    dict(range=[50, 75], color="#DDE7DF"),
                    dict(range=[75, 100], color="#D3E1D5"),
                ],
                threshold=dict(line=dict(color="#A67C32", width=4), thickness=0.80, value=50),
            ),
            domain=dict(x=[0.15, 0.85], y=[0.32, 0.95]),
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=480,
        title=dict(
            text=(
                "<b>Solar Investment Recovery Progress</b><br>"
                f"<sup>₹{recovery:.2f} Lakhs recovered against ₹{investment / 100:.2f} Crore investment</sup>"
            ),
            x=0.02,
            xanchor="left",
            font=dict(size=22, color="#263238"),
        ),
        annotations=[
            dict(
                x=0.22,
                y=0.10,
                xref="paper",
                yref="paper",
                text=f"<b>₹{recovery:.2f} L</b><br><span style='font-size:11px'>Recovered</span>",
                showarrow=False,
                align="center",
                font=dict(size=19, color="#5F8A68"),
            ),
            dict(
                x=0.78,
                y=0.10,
                xref="paper",
                yref="paper",
                text=(
                    f"<b>₹{remaining:.2f} L</b>"
                    "<br><span style='font-size:11px'>Remaining to Recover</span>"
                ),
                showarrow=False,
                align="center",
                font=dict(size=19, color="#8B6B3E"),
            ),
        ],
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=50, r=50, t=110, b=40),
    )

    st.plotly_chart(fig, width="stretch")


def viz_four(data: dict) -> None:
    """Visualization 4 — Environmental Impact of solar generation."""
    st.subheader("Environmental Impact")

    total_solar_units = data["total_solar_units"]

    grid_emission_factor = 0.7117  # kg CO2 / kWh — CEA v21.0 India grid average
    co2_per_tree = 0.060  # metric tonnes CO2 / tree seedling over 10 yrs — EPA

    co2_avoided_tonnes = round(total_solar_units * grid_emission_factor / 1000, 1)
    tree_equivalent = round(co2_avoided_tonnes / co2_per_tree)

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=tree_equivalent,
            number=dict(valueformat=",d", font=dict(size=64, color="#557A62")),
            title=dict(text="<b>🌱 Tree Equivalent</b>", font=dict(size=19, color="#37474F")),
            domain=dict(x=[0, 1], y=[0.50, 1]),
        )
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=co2_avoided_tonnes,
            number=dict(valueformat=",.1f", suffix=" tCO₂e", font=dict(size=34, color="#6689A8")),
            title=dict(text="<b>CO₂ Emissions Avoided</b>", font=dict(size=15, color="#607D8B")),
            domain=dict(x=[0, 1], y=[0.18, 0.48]),
        )
    )

    fig.add_annotation(
        x=0.5,
        y=0.06,
        xref="paper",
        yref="paper",
        text=(
            f"<b>{total_solar_units:,.0f} solar units generated</b> → "
            f"<b>{co2_avoided_tonnes:,.1f} tCO₂e avoided</b> → "
            f"<b>{tree_equivalent:,.0f} tree seedlings equivalent</b>"
        ),
        showarrow=False,
        font=dict(size=13, color="#455A64"),
        align="center",
    )

    fig.update_layout(
        height=480,
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=40, r=40, t=90, b=70),
        title=dict(
            text="<b>Environmental Impact of Solar Generation</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=21, color="#263238"),
        ),
    )

    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Based on CEA v21.0 India grid factor of 0.7117 kg CO₂/kWh · "
        "Tree equivalency based on EPA methodology"
    )
