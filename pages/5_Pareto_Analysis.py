import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.subheader("🔍 Key Insights")

st.success("""
• A small percentage of products contribute the majority of total profit.

• The business follows the Pareto Principle (80/20 rule).

• Over-dependence on a few products increases business risk.

• Diversifying profit sources can improve long-term stability.
""")

df = pd.read_csv("data/Nassau Candy Distributor.csv")

st.title("📈 Pareto Analysis")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    errors="coerce"
)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        &
        (filtered_df["Order Date"].dt.date <= end_date)
    ]

division_options = ["All"] + sorted(
    df["Division"].dropna().unique().tolist()
)

selected_division = st.sidebar.selectbox(
    "Select Division",
    division_options
)

if selected_division != "All":
    filtered_df = filtered_df[
        filtered_df["Division"] == selected_division
    ]

filtered_df["Gross Margin %"] = (
    filtered_df["Gross Profit"] /
    filtered_df["Sales"]
) * 100

margin_threshold = st.sidebar.slider(
    "Minimum Margin %",
    0,
    100,
    0
)

filtered_df = filtered_df[
    filtered_df["Gross Margin %"] >= margin_threshold
]

product_search = st.sidebar.text_input(
    "Search Product"
)

if product_search:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(
            product_search,
            case=False,
            na=False
        )
    ]

if filtered_df.empty: #no data check
    st.warning("No records found.")
    st.stop()

pareto = filtered_df.groupby("Product Name")["Gross Profit"].sum().reset_index()

pareto = pareto.sort_values(
        by="Gross Profit",
        ascending=False
    )

pareto["Cumulative Profit"] = pareto["Gross Profit"].cumsum()

pareto["Cumulative %"] = (
        pareto["Cumulative Profit"]
        / pareto["Gross Profit"].sum()
    ) * 100

st.dataframe(pareto)

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
        pareto["Product Name"],
        pareto["Cumulative %"],
        marker="o"
    )

ax.axhline(
        y=80,
        linestyle="--"
    )

plt.xticks(rotation=90)

ax.set_title("Pareto Analysis")

st.pyplot(fig)