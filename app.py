import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Nassau Candy Analytics Dashboard",
    layout="wide"
)

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("data/cleaned_nassau_candy_distributor.csv")

# ==============================
# SIDEBAR
# ==============================

page = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Home",
        "Product Analysis",
        "Division Analysis",
        "Factory Analysis",
        "Regional Analysis",
        "Pareto Analysis",
        "Cost Diagnostics"
    ]
)

# ==============================
# HOME PAGE
# ==============================

if page == "Home":

    st.title("🍫 Nassau Candy Analytics Dashboard")
    st.subheader("Product Line Profitability & Margin Performance Analysis")

    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    total_records = len(df)
    avg_margin = (total_profit / total_sales) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Records", total_records)
    col4.metric("Average Margin", f"{avg_margin:.2f}%")

    st.markdown("---")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# ==============================
# PRODUCT ANALYSIS
# ==============================

elif page == "Product Analysis":

    st.title("📦 Product Analysis")

    product_summary = df.groupby("Product Name").agg({
        "Sales":"sum",
        "Gross Profit":"sum",
        "Units":"sum"
    }).reset_index()

    product_summary["Gross Margin %"] = (
        product_summary["Gross Profit"]
        / product_summary["Sales"]
    ) * 100

    st.subheader("Top Products by Profit")

    top_profit = product_summary.sort_values(
        "Gross Profit",
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(
        top_profit["Product Name"],
        top_profit["Gross Profit"]
    )

    plt.xticks(rotation=90)

    st.pyplot(fig)

    st.dataframe(product_summary)

# ==============================
# DIVISION ANALYSIS
# ==============================

elif page == "Division Analysis":

    st.title("🏢 Division Analysis")

    division_summary = df.groupby("Division").agg({
        "Sales":"sum",
        "Gross Profit":"sum",
        "Cost":"sum"
    }).reset_index()

    division_summary["Gross Margin %"] = (
        division_summary["Gross Profit"]
        / division_summary["Sales"]
    ) * 100

    st.dataframe(division_summary)

    fig, ax = plt.subplots()

    ax.bar(
        division_summary["Division"],
        division_summary["Gross Profit"]
    )

    ax.set_title("Profit by Division")

    st.pyplot(fig)

# ==============================
# FACTORY ANALYSIS
# ==============================

elif page == "Factory Analysis":

    st.title("🏭 Factory Analysis")

    st.info(
        "Use the factory mapping dataframe from Notebook 4 and merge it with the dataset."
    )

# ==============================
# REGIONAL ANALYSIS
# ==============================

elif page == "Regional Analysis":

    st.title("🌎 Regional Analysis")

    regional_summary = df.groupby("Region").agg({
        "Sales":"sum",
        "Gross Profit":"sum"
    }).reset_index()

    st.dataframe(regional_summary)

    fig, ax = plt.subplots()

    ax.bar(
        regional_summary["Region"],
        regional_summary["Gross Profit"]
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

# ==============================
# PARETO ANALYSIS
# ==============================

elif page == "Pareto Analysis":

    st.title("📈 Pareto Analysis")

    pareto = df.groupby("Product Name")["Gross Profit"].sum().reset_index()

    pareto = pareto.sort_values(
        "Gross Profit",
        ascending=False
    )

    pareto["Cumulative Profit"] = pareto["Gross Profit"].cumsum()

    pareto["Cumulative %"] = (
        pareto["Cumulative Profit"]
        / pareto["Gross Profit"].sum()
    ) * 100

    st.dataframe(pareto)

    fig, ax = plt.subplots()

    ax.plot(
        pareto["Product Name"],
        pareto["Cumulative %"],
        marker="o"
    )

    plt.xticks(rotation=90)

    ax.axhline(
        y=80,
        linestyle="--"
    )

    st.pyplot(fig)

# ==============================
# COST DIAGNOSTICS
# ==============================

elif page == "Cost Diagnostics":

    st.title("💰 Cost Structure Diagnostics")

    fig, ax = plt.subplots(figsize=(8,6))

    ax.scatter(
        df["Cost"],
        df["Gross Profit"]
    )

    ax.set_xlabel("Cost")
    ax.set_ylabel("Gross Profit")

    st.pyplot(fig)

    st.dataframe(
        df[["Product Name","Sales","Cost","Gross Profit"]]
        .sort_values(
            "Cost",
            ascending=False
        )
        .head(20)
    )

st.subheader("📌 Executive Summary")

st.info("""
This dashboard analyzes product profitability, division performance,
factory contribution, regional trends, profit concentration, and cost
efficiency for Nassau Candy Distributor.

The analysis helps identify high-margin products, profitability risks,
and opportunities for business optimization.
""")  