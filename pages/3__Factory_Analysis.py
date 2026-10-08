import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.subheader("🔍 Key Insights")

st.success("""
• Factory performance varies significantly across product lines.

• Lot's O' Nuts and Wicked Choccy's contribute most of the profit through chocolate products.

• Some factories contribute relatively little to total profitability.

• Factory-level monitoring can help optimize sourcing and production decisions.
""")

df = pd.read_csv("data/Nassau Candy Distributor.csv")

st.title("🏭 Factory Analysis")

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

factory_mapping = pd.DataFrame({
        "Product Name":[
            "Wonka Bar - Nutty Crunch Surprise",
            "Wonka Bar - Fudge Mallows",
            "Wonka Bar -Scrumdiddlyumptious",
            "Wonka Bar - Milk Chocolate",
            "Wonka Bar - Triple Dazzle Caramel",
            "Laffy Taffy",
            "SweeTARTS",
            "Nerds",
            "Fun Dip",
            "Fizzy Lifting Drinks",
            "Everlasting Gobstopper",
            "Hair Toffee",
            "Lickable Wallpaper",
            "Wonka Gum",
            "Kazookles"
        ],
        "Factory":[
            "Lot's O' Nuts",
            "Lot's O' Nuts",
            "Lot's O' Nuts",
            "Wicked Choccy's",
            "Wicked Choccy's",
            "Sugar Shack",
            "Sugar Shack",
            "Sugar Shack",
            "Sugar Shack",
            "Sugar Shack",
            "Secret Factory",
            "The Other Factory",
            "Secret Factory",
            "Secret Factory",
            "The Other Factory"
        ]
    })

df_factory = pd.merge(
        df,
        factory_mapping,
        on="Product Name",
        how="left"
    )

factory_summary = df_factory.groupby("Factory").agg({
        "Sales":"sum",
        "Gross Profit":"sum"
    }).reset_index()

st.dataframe(factory_summary)

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(
    factory_summary["Factory"],
    factory_summary["Gross Profit"]
)

plt.xticks(rotation=45)

st.pyplot(fig)