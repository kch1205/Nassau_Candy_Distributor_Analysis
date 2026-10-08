import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.subheader("🔍 Key Insights")

st.success("""
• Chocolate Division generates the highest revenue and profit contribution.

• Other Division contributes significantly lower profit compared to Chocolate.

• Profitability is heavily concentrated within a single division, creating dependency risk.

• Management should continue investing in high-performing divisions while improving margins in weaker divisions.
""")

st.title("🏢 Division Analysis")

df = pd.read_csv("data/Nassau Candy Distributor.csv")

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



division_summary = df.groupby("Division").agg({
    "Sales":"sum",
    "Gross Profit":"sum",
    "Cost":"sum",
    "Units":"sum"
}).reset_index()

division_summary["Gross Margin %"] = (
    division_summary["Gross Profit"]
    / division_summary["Sales"]
) * 100

st.dataframe(division_summary)

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(
    division_summary["Division"],
    division_summary["Gross Profit"]
)

ax.set_title("Profit by Division")

st.pyplot(fig)