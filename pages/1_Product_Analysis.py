import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.subheader("🔍 Key Insights")

st.success("""
• The Wonka chocolate product line dominates both revenue and profit.

• A small number of products contribute the majority of total profit.

• Several products generate low sales and low profit, making them candidates for portfolio review.

• High-margin products should receive greater promotional focus.
""")

st.title("📦 Product Profitability Analysis")


df = pd.read_csv("data/cleaned_nassau_candy_distributor.csv")

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
     
product_summary = filtered_df.groupby("Product Name").agg({
    "Sales": "sum",
    "Gross Profit": "sum",
    "Units": "sum"
}).reset_index()


product_summary["Gross Margin %"] = (
    product_summary["Gross Profit"] /
    product_summary["Sales"]
) * 100

product_summary["Profit Per Unit"] = (
    product_summary["Gross Profit"] /
    product_summary["Units"]
)

st.subheader("Top 10 Products by Sales")

top_sales = product_summary.sort_values(
    "Sales",
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(top_sales["Product Name"], top_sales["Sales"])
plt.xticks(rotation=90)
st.pyplot(fig)

st.subheader("Top 10 Products by Profit")

top_profit = product_summary.sort_values(
    "Gross Profit",
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(top_profit["Product Name"], top_profit["Gross Profit"])
plt.xticks(rotation=90)
st.pyplot(fig)

st.subheader("Product Performance Table")

st.dataframe(
    product_summary.sort_values(
        "Gross Profit",
        ascending=False
    )
)

page = st.sidebar.radio(
    "Select Analysis",
    ["Product Analysis", "Division Analysis", "Factory Analysis", "Regional Analysis", "Pareto Analysis", "Cost Diagnostics"]
)

df["Gross Margin %"] = (
    df["Gross Profit"] / df["Sales"]
) * 100

volatility = df.groupby("Product Name")["Gross Margin %"].std()

st.subheader("Margin Volatility")

st.dataframe(
    volatility.sort_values(ascending=False)
    .reset_index()
    .rename(columns={"Gross Margin %":"Margin Volatility"})
)

