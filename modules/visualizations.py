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


_ENV_IMPACT_TEMPLATE = """
<div class="env-banner">
  <style>
    .env-banner {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      background: linear-gradient(180deg, #f4f9f4 0%, #eef6ee 100%);
      border-radius: 16px;
      padding: 22px 28px 18px;
      box-sizing: border-box;
      width: 100%;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .env-title {
      text-align: center;
      font-size: 22px;
      font-weight: 700;
      color: #263238;
      margin: 0 0 14px;
    }
    .env-row {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      min-height: 190px;
    }
    .env-flow-svg {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      z-index: 0;
      pointer-events: none;
    }
    .env-col { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; }
    .env-col.left { flex: 0 0 22%; }
    .env-col.center { flex: 0 0 34%; }
    .env-col.right { flex: 0 0 34%; }

    /* --- solar panel icon --- */
    .sun { font-size: 30px; line-height: 1; margin-bottom: -6px; filter: drop-shadow(0 0 6px rgba(255,193,7,0.5)); }
    .panel {
      width: 92px; height: 58px;
      background: repeating-linear-gradient(90deg, #2a5d8a 0 20px, #1e4666 20px 22px),
                  repeating-linear-gradient(0deg, #2a5d8a 0 12px, #1e4666 12px 14px);
      border: 3px solid #17324a;
      border-radius: 4px;
      transform: perspective(200px) rotateX(18deg);
      box-shadow: 0 6px 10px rgba(0,0,0,0.12);
    }
    .panel-stand { width: 6px; height: 22px; background: #78909c; margin: 0 auto; }
    .tree-cluster { display: flex; align-items: flex-end; margin-top: 4px; }
    .tree-cluster span { line-height: 1; }
    .cluster-left span:nth-child(1) { font-size: 22px; margin-right: -6px; opacity: 0.85; }
    .cluster-left span:nth-child(2) { font-size: 30px; margin-right: -6px; }
    .cluster-left span:nth-child(3) { font-size: 20px; opacity: 0.85; }

    /* --- stats --- */
    .stat-block { text-align: center; margin-bottom: 14px; }
    .stat-label {
      font-size: 13px; font-weight: 700; letter-spacing: 0.04em;
      color: #37474F; text-transform: uppercase; margin-bottom: 2px;
    }
    .stat-value { font-size: 40px; font-weight: 800; line-height: 1.1; }
    .stat-value.trees { color: #2e7d32; }
    .stat-value.co2 { color: #4a7fa8; font-size: 30px; }

    /* --- forest cluster (right) --- */
    .forest-wrap { position: relative; display: flex; align-items: flex-end; }
    .forest-wrap span.tree { line-height: 1; }
    .forest-wrap span.tree:nth-child(1) { font-size: 26px; margin-right: -8px; opacity: 0.8; }
    .forest-wrap span.tree:nth-child(2) { font-size: 40px; margin-right: -10px; }
    .forest-wrap span.tree:nth-child(3) { font-size: 30px; margin-right: -8px; opacity: 0.9; }
    .forest-wrap span.tree:nth-child(4) { font-size: 44px; margin-right: -8px; }
    .forest-wrap span.tree:nth-child(5) { font-size: 24px; opacity: 0.8; }
    .wildlife { position: absolute; top: -6px; right: 6px; font-size: 15px; opacity: 0.85; }
    .wildlife.deer { top: 6px; right: -8px; font-size: 18px; }
    .co2-clouds { display: flex; gap: 10px; margin-bottom: 2px; }
    .co2-cloud {
      display: flex; align-items: center; gap: 3px;
      font-size: 11px; font-weight: 700; color: #6b7c93;
      background: rgba(255,255,255,0.7); border-radius: 10px; padding: 2px 7px;
      animation: env-float 3.2s ease-in-out infinite;
    }
    .co2-cloud:nth-child(2) { animation-delay: 0.6s; }
    .co2-cloud .arrow { color: #7ea0c2; }
    @keyframes env-float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-4px); }
    }

    /* --- sprout row --- */
    .sprout-row {
      display: flex; justify-content: space-between; padding: 6px 4% 0;
      font-size: 18px; opacity: 0.9;
    }

    /* --- flow text pill --- */
    .flow-pill {
      background: white; border-radius: 999px; padding: 9px 20px;
      margin: 12px auto 6px; max-width: 92%; text-align: center;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      font-size: 13.5px; font-weight: 600; color: #2b2f33;
    }
    .env-footnote { text-align: center; font-size: 11px; color: #90A4AE; margin-top: 2px; }
  </style>

  <div class="env-title">Environmental Impact of Solar Generation</div>

  <div class="env-row">
    <svg class="env-flow-svg" viewBox="0 0 800 190" preserveAspectRatio="none">
      <defs>
        <linearGradient id="flowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#66bb6a" stop-opacity="0.55"/>
          <stop offset="100%" stop-color="#66bb6a" stop-opacity="0.05"/>
        </linearGradient>
      </defs>
      <path d="M110,140 C260,60 300,150 400,110 C500,70 560,140 690,60"
            fill="none" stroke="url(#flowGrad)" stroke-width="10" stroke-linecap="round"/>
    </svg>

    <div class="env-col left">
      <div class="sun">☀️</div>
      <div class="panel"></div>
      <div class="panel-stand"></div>
      <div class="tree-cluster cluster-left">
        <span>🌲</span><span>🌳</span><span>🌲</span>
      </div>
    </div>

    <div class="env-col center">
      <div class="stat-block">
        <div class="stat-label">🌱 Tree Equivalent</div>
        <div class="stat-value trees">__TREE_EQ__</div>
      </div>
      <div class="stat-block" style="margin-bottom:0;">
        <div class="stat-label">CO₂ Emissions Avoided</div>
        <div class="stat-value co2">__CO2__ tCO₂e</div>
      </div>
    </div>

    <div class="env-col right">
      <div class="co2-clouds">
        <div class="co2-cloud">☁️ CO₂ <span class="arrow">↑</span></div>
        <div class="co2-cloud">☁️ CO₂ <span class="arrow">↑</span></div>
      </div>
      <div class="forest-wrap">
        <span class="wildlife">🦉</span>
        <span class="wildlife deer">🦌</span>
        <span class="tree">🌲</span><span class="tree">🌳</span><span class="tree">🌲</span><span class="tree">🌳</span><span class="tree">🌲</span>
      </div>
    </div>
  </div>

  <div class="sprout-row">🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱</div>

  <div class="flow-pill">__UNITS__ solar units generated&nbsp;&nbsp;→&nbsp;&nbsp;__CO2__ tCO₂e avoided&nbsp;&nbsp;→&nbsp;&nbsp;__TREE_EQ__ tree seedlings equivalent</div>
  <div class="env-footnote">Based on CEA v21.0 India grid factor of 0.7117 kg CO₂/kWh &middot; Tree equivalency based on EPA methodology</div>
</div>
"""


def viz_four(data: dict) -> None:
    """Visualization 4 — Environmental Impact of solar generation.

    A flat-illustration banner (solar panel, tree clusters, CO2 cloud
    icons, a connecting flow ribbon, and a sprout row) built from HTML/CSS/
    SVG and rendered via st.iframe, since this is a decorative infographic
    layout rather than a data-scaled chart.
    """
    st.subheader("Environmental Impact")

    total_solar_units = data["total_solar_units"]

    grid_emission_factor = 0.7117  # kg CO2 / kWh — CEA v21.0 India grid average
    co2_per_tree = 0.060  # metric tonnes CO2 / tree seedling over 10 yrs — EPA

    co2_avoided_tonnes = round(total_solar_units * grid_emission_factor / 1000, 1)
    tree_equivalent = round(co2_avoided_tonnes / co2_per_tree)

    html = (
        _ENV_IMPACT_TEMPLATE.replace("__TREE_EQ__", f"{tree_equivalent:,}")
        .replace("__CO2__", f"{co2_avoided_tonnes:,.1f}")
        .replace("__UNITS__", f"{total_solar_units:,.0f}")
    )

    st.iframe(html, height="content")
