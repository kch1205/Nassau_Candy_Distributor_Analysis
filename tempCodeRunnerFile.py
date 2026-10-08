import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nassau Candy Analytics Dashboard",
    layout="wide"
)

st.title("🍫 Nassau Candy Analytics Dashboard")

st.markdown("""
### Product Line Profitability & Margin Performance Analysis

Analyze:

- Product Performance
- Division Performance
- Factory Performance
- Regional Performance
- Pareto Analysis
- Cost Diagnostics
""")

df = pd.read_csv("data/cleaned_nassau_candy_distributor.csv")

total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
total_records = len(df)
total_products = df["Product Name"].nunique()

avg_margin = (total_profit / total_sales) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("Total Profit", f"${total_profit:,.2f}")

with col3:
    st.metric("Total Records", total_records)

with col4:
    st.metric("Average Margin", f"{avg_margin:.2f}%")

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(df.head())
