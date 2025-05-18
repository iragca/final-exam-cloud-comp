# dashboard.py

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import polars as pl
import streamlit as st
from wordcloud import WordCloud

from src.config import WAREHOUSE_DATABASE_URL
from src.data import Warehouse
from src.utils import format_revenue

st.set_page_config(page_title="Warehouse Dashboard", layout="centered")

# Load warehouse data
WAREHOUSE = Warehouse(WAREHOUSE_DATABASE_URL)


@st.cache_data
def load_data() -> tuple[pl.DataFrame]:
    sales = WAREHOUSE.get_table("sales_details")
    products = WAREHOUSE.get_table("prd_info")
    customers = WAREHOUSE.get_table("cust_info")
    locations = WAREHOUSE.get_table("loc_a101")
    tables = WAREHOUSE.get_table_names()

    return sales, products, customers, locations, tables


sales, products, customers, locations, tables = load_data()

# --- KPIs ---
st.title("Sales Dashboard")
st.markdown("###### A visual report of customer and sales performance")
st.subheader("**Quick Stats**")

total_customers = customers.select("cst_id").n_unique()
total_products = products.select("prd_id").n_unique()
total_orders = sales.select("sls_ord_num").n_unique()
total_revenue = sales.select("sls_sales").sum().item()

formatted_revenue: str = format_revenue(total_revenue)

# Format values
formatted_customers = f"{total_customers:,}"
formatted_products = f"{total_products:,}"
formatted_orders = f"{total_orders:,}"
formatted_revenue = f"₱{format_revenue(total_revenue)}"

# Layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("Total Customers", formatted_customers)

with col2:
    with st.container(border=True):
        st.metric("Products", formatted_products)

with col3:
    with st.container(border=True):
        st.metric("Orders", formatted_orders)

with col4:
    with st.container(border=True):
        st.metric("Revenue", formatted_revenue)


# --- Line chart: Sales over time ---
st.markdown("### **Sales Over Time**")
sales_by_date = (
    sales.group_by("sls_order_dt")
    .agg(pl.sum("sls_sales").alias("total_sales"))
    .sort("sls_order_dt")
    .filter(pl.col("sls_order_dt").is_not_null())
)

if sales_by_date.shape[0] > 0:
    st.line_chart(sales_by_date.to_pandas().set_index("sls_order_dt"))
else:
    st.warning("No sales dates available.")


# --- Gender Distribution Pie Chart ---
st.markdown("### **Customer Gender Distribution**")
gender_counts = (
    customers.group_by("cst_gndr")
    .agg(pl.count("cst_id").alias("count"))
    .filter(pl.col("cst_gndr").is_not_null())
)

if gender_counts.shape[0] > 0:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=gender_counts["cst_gndr"].to_list(),
                values=gender_counts["count"].to_list(),
                hole=0.4,
                textinfo="label+percent",
                textposition="outside",  # Put labels outside the pie slices
                showlegend=True,  # Optional: keeps the legend on the side
                marker=dict(colors=["#060378", "#4c4eb5", "#8181cb"]),
            )
        ]
    )
    fig.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No gender data available.")

# --- Location Word Cloud ---
st.markdown("### **Which Countries Drive the Most Sales?**")
st.caption("Visualizing the geographic footprint of our customers")


if "CNTRY" in locations.columns and locations.height > 0:
    # Count occurrences of each country
    country_counts = (
        locations.filter(pl.col("CNTRY").is_not_null())
        .group_by("CNTRY")
        .agg(pl.count("CNTRY").alias("count"))
        .to_pandas()
    )

    # Create dictionary for word cloud
    country_freq = dict(zip(country_counts["CNTRY"], country_counts["count"]))

    # Generate word cloud
    wc = WordCloud(
        width=800, height=400, background_color="white", colormap="Blues"
    ).generate_from_frequencies(country_freq)

    # Display in Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.warning("No country data available in 'loc_a101'.")

# --- Data explorer ---
st.markdown("### **Explore Warehouse Tables**")
selected_table: str = st.selectbox("Select a table to preview", tables)


@st.cache_data(show_spinner="Loading data...")
def get_table_data(table_name: str) -> pl.DataFrame:
    return WAREHOUSE.get_table(table_name)


if selected_table:
    df: pl.DataFrame = get_table_data(selected_table)
    st.subheader(f"`{selected_table}`")
    st.dataframe(df, use_container_width=True)
