import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Laptop Price Dashboard", 
                  page_icon="💻",
                  layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("laptop_data.csv")

df = load_data()

# Main title
st.title("💻 Laptop Price Analysis Dashboard")
st.sidebar.header("Filters")

# Sidebar filters
selected_brands = st.sidebar.multiselect(
    "Select Brands",
    options=df['Brand'].unique(),
    default=df['Brand'].unique()[:3]
)

price_range = st.sidebar.slider(
    "Price Range (USD)",
    min_value=int(df['Price_USD'].min()),
    max_value=int(df['Price_USD'].max()),
    value=(int(df['Price_USD'].min()), int(df['Price_USD'].max()))
)

# Filter the dataframe
filtered_df = df[
    (df['Brand'].isin(selected_brands)) &
    (df['Price_USD'] >= price_range[0]) &
    (df['Price_USD'] <= price_range[1])
]

# Create three columns for KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.info("Average Price", icon="💰")
    st.metric(label="USD", value=f"${filtered_df['Price_USD'].mean():,.2f}")

with col2:
    st.info("Total Laptops", icon="🔢")
    st.metric(label="Count", value=len(filtered_df))

with col3:
    st.info("Price Range", icon="📊")
    st.metric(label="USD", value=f"${filtered_df['Price_USD'].max() - filtered_df['Price_USD'].min():,.2f}")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    # Brand vs Average Price
    fig_brand_price = px.bar(
        filtered_df.groupby('Brand')['Price_USD'].mean().reset_index(),
        x='Brand',
        y='Price_USD',
        title='Average Price by Brand',
        labels={'Price_USD': 'Average Price (USD)'}
    )
    st.plotly_chart(fig_brand_price, use_container_width=True)

    # RAM vs Price
    fig_ram_price = px.box(
        filtered_df,
        x='RAM_GB',
        y='Price_USD',
        title='Price Distribution by RAM',
        labels={'RAM_GB': 'RAM (GB)', 'Price_USD': 'Price (USD)'}
    )
    st.plotly_chart(fig_ram_price, use_container_width=True)

with col2:
    # Processor vs Average Price
    fig_processor_price = px.bar(
        filtered_df.groupby('Processor')['Price_USD'].mean().reset_index(),
        x='Price_USD',
        y='Processor',
        title='Average Price by Processor',
        labels={'Price_USD': 'Average Price (USD)'},
        orientation='h'
    )
    st.plotly_chart(fig_processor_price, use_container_width=True)

    # GPU vs Price
    fig_gpu_price = px.box(
        filtered_df,
        x='GPU',
        y='Price_USD',
        title='Price Distribution by GPU',
        labels={'Price_USD': 'Price (USD)'}
    )
    fig_gpu_price.update_xaxes(tickangle=45)
    st.plotly_chart(fig_gpu_price, use_container_width=True)

# Detailed Data View
st.subheader("Detailed Data View")
st.dataframe(
    filtered_df.style.format({'Price_USD': '${:,.2f}', 'Screen_Size': '{:.1f}"'}),
    use_container_width=True
)

