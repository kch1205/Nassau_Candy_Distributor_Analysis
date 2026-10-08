import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.subheader("🔍 Key Insights")

st.success("""
• Some products incur high costs without proportional profit generation.

• Cost-heavy products should be reviewed for pricing adjustments.

• Margin optimization opportunities exist for underperforming products.

• Reducing production costs can significantly improve profitability.
""")

df = pd.read_csv("data/Nassau Candy Distributor.csv")

st.title("💰 Cost Diagnostics")

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

fig, ax = plt.subplots(figsize=(8,6))

ax.scatter(
        df["Cost"],
        df["Gross Profit"]
    )

ax.set_xlabel("Cost")
ax.set_ylabel("Gross Profit")

ax.set_title("Cost vs Gross Profit")

st.pyplot(fig)

high_cost = df.sort_values(
        by="Cost",
        ascending=False
    ).head(20)

st.subheader("Highest Cost Records")

st.dataframe(
        high_cost[
            [
                "Product Name",
                "Sales",
                "Cost",
                "Gross Profit"
            ]
        ]
    )