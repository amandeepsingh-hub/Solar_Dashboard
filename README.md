# Solar Dashboard

A Streamlit dashboard for a 3-plant solar portfolio (Bhiwandi, Raliawas,
Surat): headline KPI cards plus 4 visualizations laid out as tabs on a
single page, with a sidebar plant filter.

## Project structure

```
Solar_Dashboard/
├── app.py                     # Main entry point — run this with streamlit
├── requirements.txt
├── .streamlit/
│   └── config.toml            # Theme / server settings
├── modules/
│   ├── raw_data.py            # Source tables (df1..df4) + monthly reshape
│   ├── data_loader.py         # load_data() — the single data entry point
│   └── visualizations.py      # viz_one..viz_four + render_kpi_header
├── data/                      # Drop a real data export here when you have one
└── assets/                    # Logos, images, etc. (optional)
```

## Setup

```bash
cd Solar_Dashboard
python -m venv .venv
.venv\Scripts\activate        # on Windows
pip install -r requirements.txt
streamlit run app.py
```

## What's in it

- **KPI header** — the 6 headline cards (plants, capacity, energy generated,
  savings, investment, recovery %) from `raw_data.df1`.
- **Tab 1 — Investment Recovery** — stacked horizontal bar of recovered vs.
  remaining investment per plant.
- **Tab 2 — Monthly Value Creation** — monthly savings (bars) and solar
  generation (line) across the portfolio, Mar 2025–Sep 2026.
- **Tab 3 — Recovery Progress** — a gauge showing overall recovery % against
  total investment (portfolio-wide, not filterable).
- **Tab 4 — Environmental Impact** — CO₂ avoided and tree-equivalent, derived
  from total units generated (portfolio-wide, not filterable).

The sidebar plant filter narrows tabs 1 and 2 only — tabs 3 and 4 are driven
by the fixed KPI totals rather than a per-plant breakdown.

## Data

Right now `modules/raw_data.py` holds the source tables as static Python
dataframes (transcribed from the original records) — there's no external
file to load yet. When a live export (CSV, DB, API) is available:

1. Either point `modules/raw_data.py` at that source, or read it directly in
   `modules/data_loader.py::load_data()` — the rest of the app only depends
   on the dict shape `load_data()` returns, documented in that file's
   docstring.
2. If it's a file, drop it in `data/`.

## Note on Tab 2's dual axis

Tab 2 plots two series on two different y-scales (₹ savings on the left,
units generated on the right). That's a deliberate call to preserve the
original chart design, but it's worth knowing dual-axis charts can be read
as one series tracking the other when they're just independently scaled —
if that becomes confusing in practice, an easy alternative is splitting it
into two single-axis charts (or indexing both series to a common base, e.g.
% of their own average).
