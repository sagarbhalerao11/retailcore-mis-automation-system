from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="RetailCore MIS Dashboard",
    layout="wide"
)


@st.cache_data
def load_report(uploaded_file):

    excel_file = pd.ExcelFile(
        uploaded_file,
        engine="openpyxl"
    )

    summary = pd.read_excel(
        excel_file,
        sheet_name="Executive Summary",
        header=None
    )

    sales_analysis = pd.read_excel(
        excel_file,
        sheet_name="Sales Analysis"
    )

    inventory = pd.read_excel(
        excel_file,
        sheet_name="Inventory Alerts"
    )

    returns = pd.read_excel(
        excel_file,
        sheet_name="Returns Deep Dive"
    )

    return (
        summary,
        sales_analysis,
        inventory,
        returns
    )


# ==================================================
# HEADER
# ==================================================

st.title(
    "RetailCore MIS Dashboard"
)

st.sidebar.title(
    "Report Selection"
)

uploaded_file = st.sidebar.file_uploader(
    "Select MIS Excel Report",
    type=["xlsx"]
)

if uploaded_file is None:

    st.info(
        "Please select MIS_Report.xlsx using Browse Files."
    )

    st.stop()

st.sidebar.success(
    "File Selected Successfully"
)

st.sidebar.write(
    f"**File Name:** {uploaded_file.name}"
)

st.sidebar.write(
    f"**File Size:** {round(uploaded_file.size / 1024, 2)} KB"
)

try:

    (
        summary_df,
        sales_df,
        inventory_df,
        returns_df
    ) = load_report(
        uploaded_file
    )

except Exception as error:

    st.error(
        f"Failed to load report.\n\n{error}"
    )

    st.stop()


# ==================================================
# KPI SECTION
# ==================================================

try:

    total_revenue = (
        summary_df.iloc[5, 1]
    )

    return_rate = (
        summary_df.iloc[6, 1]
    )

    top_region = (
        summary_df.iloc[7, 1]
    )

    stockout_products = (
        summary_df.iloc[8, 1]
    )

except Exception as error:

    st.error(
        f"Unable to read KPI data.\n\n{error}"
    )

    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

with col2:

    st.metric(
        "Return Rate %",
        return_rate
    )

with col3:

    st.metric(
        "Top Region",
        str(top_region)
    )

with col4:

    st.metric(
        "Stockout Products",
        stockout_products
    )

st.divider()


# ==================================================
# CHARTS
# ==================================================

st.subheader(
    "Generated Charts"
)

chart_col1, chart_col2 = st.columns(2)

weekly_chart = (
    Path("charts")
    /
    "weekly_revenue_trend.png"
)

region_chart = (
    Path("charts")
    /
    "region_revenue.png"
)

with chart_col1:

    st.subheader(
        "Weekly Revenue Trend"
    )

    if weekly_chart.exists():

        st.image(
            str(weekly_chart),
            use_container_width=True
        )

    else:

        st.warning(
            "weekly_revenue_trend.png not found"
        )

with chart_col2:

    st.subheader(
        "Region Revenue"
    )

    if region_chart.exists():

        st.image(
            str(region_chart),
            use_container_width=True
        )

    else:

        st.warning(
            "region_revenue.png not found"
        )

st.divider()


# ==================================================
# SALES ANALYSIS
# ==================================================

st.subheader(
    "Sales Analysis"
)

st.dataframe(
    sales_df,
    use_container_width=True
)

st.divider()


# ==================================================
# INVENTORY ALERTS
# ==================================================

st.subheader(
    "Inventory Alerts"
)

filtered_inventory = (
    inventory_df.copy()
)

if (
    "category"
    in inventory_df.columns
):

    categories = sorted(
        inventory_df[
            "category"
        ]
        .dropna()
        .unique()
    )

    selected_category = st.selectbox(
        "Filter By Category",
        ["All"] +
        list(categories)
    )

    if (
        selected_category
        !=
        "All"
    ):

        filtered_inventory = (
            filtered_inventory[
                filtered_inventory[
                    "category"
                ]
                ==
                selected_category
            ]
        )

st.dataframe(
    filtered_inventory,
    use_container_width=True
)

st.write(
    f"Total Records: {len(filtered_inventory)}"
)

st.divider()


# ==================================================
# RETURNS ANALYSIS
# ==================================================

st.subheader(
    "Returns Analysis"
)

st.dataframe(
    returns_df,
    use_container_width=True
)

st.write(
    f"Total Categories: {len(returns_df)}"
)

st.divider()


# ==================================================
# FOOTER
# ==================================================

st.success(
    "Dashboard loaded successfully."
)