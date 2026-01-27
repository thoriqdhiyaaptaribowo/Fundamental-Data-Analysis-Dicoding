import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Air Quality Data Analysis Dashboard",
    layout="wide"
)

st.title("Air Quality Data Analysis Dashboard")
st.markdown("---")

@st.cache_data
def load_data():
    data = pd.read_csv("Dashboard/main_data.csv")
    return data

# Chart creation functions
def create_bar_chart(data, x_col, y_col, title, units="µg/m³"):
    """Create a bar chart similar to notebook style - by month with hue"""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=data, x=x_col, y=y_col, color='darkblue', errorbar=None, ax=ax)
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f') # type: ignore
    
    ax.set_xlabel(x_col.capitalize())
    ax.set_ylabel(f"{y_col.replace('_', ' ')} Concentration ({units})")
    ax.set_title(title)
    ax.legend([])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_line_chart(df, x_col, y_col, hue_col, title, ylabel, units="µg/m³"):
    """Create a line chart for monthly trends"""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for station in df[hue_col].unique():
        station_data = df[df[hue_col] == station].sort_values(x_col)
        ax.plot(station_data[x_col], station_data[y_col], marker='o', label=station)
    
    ax.set_xlabel(x_col.capitalize())
    ax.set_ylabel(f"{ylabel} ({units})")
    ax.set_title(title)
    ax.set_xticks(range(1, 13))
    ax.grid(True, alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    return fig

def display_pollutant_stats(data, pollutant_col, month_col):
    highest_idx = data[pollutant_col].idxmax()
    lowest_idx = data[pollutant_col].idxmin()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Highest Concentration",
            f"{data.loc[highest_idx, pollutant_col]:.2f} µg/m³",
            f"Month: {data.loc[highest_idx, month_col]}"
        )
    
    with col2:
        st.metric(
            "Lowest Concentration",
            f"{data.loc[lowest_idx, pollutant_col]:.2f} µg/m³",
            f"Month: {data.loc[lowest_idx, month_col]}"
        )

df = load_data()

# Sidebar navigation and filters
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Analysis", ["Overview", "CO Analysis", "SO2 Analysis"])

# Dynamic Filtering
st.sidebar.markdown("---")
st.sidebar.title("Filters")

# Initialize session state for filters
if 'filters' not in st.session_state:
    st.session_state.filters = {
        'stations': [],
        'months': []
    }

# Station filter
all_stations = sorted(df['station'].unique().tolist())
selected_stations = st.sidebar.multiselect(
    "Select Stations:",
    all_stations,
    default=all_stations,
    key="station_filter"
)

# Month range filter
month_range = st.sidebar.slider(
    "Select Month Range:",
    min_value=int(df['month'].min()),
    max_value=int(df['month'].max()),
    value=(int(df['month'].min()), int(df['month'].max())),
    key="month_filter"
)

# Apply filters
filtered_df = df[
    (df['station'].isin(selected_stations)) &
    (df['month'] >= month_range[0]) &
    (df['month'] <= month_range[1])
]

# Display filter status
if len(filtered_df) == 0:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# Show active filters
with st.sidebar.expander("Active Filters"):
    st.write(f"**Stations:** {len(selected_stations)} selected")
    st.write(f"**Months:** {month_range[0]} - {month_range[1]}")
    st.write(f"**Rows:** {len(filtered_df)} / {len(df)}")
    
    if st.button("Reset Filters"):
        st.session_state.station_filter = all_stations
        st.session_state.month_filter = (int(df['month'].min()), int(df['month'].max()))
        st.rerun()

# Overview Page
if page == "Overview":
    st.header("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Unique Stations", filtered_df['station'].nunique())
    with col3:
        st.metric("Months Covered", filtered_df['month'].nunique())
    with col4:
        st.metric("Filtered From", f"{len(df)} total")
    
    st.subheader("Data Sample")
    st.dataframe(filtered_df.head(10))

    st.subheader("Statistical Summary")
    st.dataframe(filtered_df[['Average_CO', 'Average_SO2']].describe())

# CO Analysis Page
elif page == "CO Analysis":
    st.header("Carbon Monoxide (CO) Analysis")
    
    col1, col2, = st.columns(2)
    
    with col1:
        st.subheader("Average CO Concentration per Month")
        fig = create_bar_chart(
            filtered_df, 
            'month', 
            'Average_CO',
            "CO Concentration per Month"
        )
        st.pyplot(fig)
   
    with col2:
        st.subheader("CO Statistics")
        display_pollutant_stats(filtered_df, 'Average_CO', 'month') 

    st.subheader("Monthly CO Trend per Station")
    fig = create_line_chart(
        filtered_df,
        'month',
        'Average_CO',
        'station',
        "Monthly CO Concentration Trends",
        "Average CO Concentration"
    )
    st.pyplot(fig)

# SO2 Analysis Page
elif page == "SO2 Analysis":
    st.header("Sulfur Dioxide (SO2) Analysis")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average SO2 Concentration per Month")
        fig = create_bar_chart(
            filtered_df,
           'month',
            'Average_SO2',
            "SO2 Concentration per Month"
        )
        st.pyplot(fig)
    
    with col2:
        st.subheader("SO2 Statistics")
        display_pollutant_stats(filtered_df, 'Average_SO2', 'month')
    
    st.subheader("Monthly SO2 Trend per Station")
    fig = create_line_chart(
        filtered_df,
        'month',
        'Average_SO2',
        'station',
        "Monthly SO2 Concentration Trends",
        "Average SO2 Concentration"
    )
    st.pyplot(fig)

st.markdown("---")
st.markdown("**Data Source:** Air Quality Dataset (2013-2017)")