import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
def create_bar_chart(data, station_col, value_col, title, color, units="µg/m³"):
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(data[station_col], data[value_col], color=color)
    ax.set_xlabel(f"Average {value_col.replace('_', ' ')} Concentration ({units})")
    ax.set_ylabel("Station")
    ax.set_title(title)
    
    for i, v in enumerate(data[value_col]):
        ax.text(v + (max(data[value_col]) * 0.01), i, f'{v:.2f}', va='center')
    
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

def display_pollutant_stats(data, pollutant_col, station_col):
    highest_idx = data[pollutant_col].idxmax()
    lowest_idx = data[pollutant_col].idxmin()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Highest Concentration",
            f"{data.loc[highest_idx, pollutant_col]:.2f} µg/m³",
            f"Station: {data.loc[highest_idx, station_col]}"
        )
    
    with col2:
        st.metric(
            "Lowest Concentration",
            f"{data.loc[lowest_idx, pollutant_col]:.2f} µg/m³",
            f"Station: {data.loc[lowest_idx, station_col]}"
        )

df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Analysis", ["Overview", "CO Analysis", "SO2 Analysis"])

# Overview Page
if page == "Overview":
    st.header("Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Unique Stations", df['station'].nunique())
    with col3:
        st.metric("Months Covered", df['month'].nunique())
    
    st.subheader("Data Sample")
    st.dataframe(df.head(10))

    st.subheader("Statistical Summary")
    st.dataframe(df[['Average_CO', 'Average_SO2']].describe())

# CO Analysis Page
elif page == "CO Analysis":
    st.header("Carbon Monoxide (CO) Analysis")
    
    # CO by Station
    df_co = df.groupby("station").agg(
        Average_CO=('Average_CO', 'mean')
    ).reset_index().sort_values('Average_CO', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average CO per Station")
        fig = create_bar_chart(
            df_co, 
            'station', 
            'Average_CO',
            "Average CO Concentration by Station",
            'steelblue'
        )
        st.pyplot(fig)
    
    with col2:
        st.subheader("CO Statistics")
        display_pollutant_stats(df_co, 'Average_CO', 'station')
    
    st.subheader("Monthly CO Trend per Station")
    fig = create_line_chart(
        df,
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
    
    # SO2 by Station
    df_so2 = df.groupby("station").agg(
        Average_SO2=('Average_SO2', 'mean')
    ).reset_index().sort_values('Average_SO2', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average SO2 per Station")
        fig = create_bar_chart(
            df_so2,
            'station',
            'Average_SO2',
            "Average SO2 Concentration by Station",
            'coral'
        )
        st.pyplot(fig)
    
    with col2:
        st.subheader("SO2 Statistics")
        display_pollutant_stats(df_so2, 'Average_SO2', 'station')
    
    st.subheader("Monthly SO2 Trend per Station")
    fig = create_line_chart(
        df,
        'month',
        'Average_SO2',
        'station',
        "Monthly SO2 Concentration Trends",
        "Average SO2 Concentration"
    )
    st.pyplot(fig)

st.markdown("---")
st.markdown("**Data Source:** Air Quality Dataset (2013-2017)")