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
    sns.barplot(data=data, x=x_col, y=y_col, hue=x_col, palette='viridis', errorbar=None, ax=ax)
    
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
    
    col1, col2, = st.columns(2)
    
    with col1:
        st.subheader("Average CO Concentration per Month")
        fig = create_bar_chart(
            df, 
            'month', 
            'Average_CO',
            "CO Concentration per Month"
        )
        st.pyplot(fig)
   
    with col2:
        st.subheader("CO Statistics")
        display_pollutant_stats(df, 'Average_CO', 'month') 

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
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average SO2 Concentration per Month")
        fig = create_bar_chart(
            df,
           'month',
            'Average_SO2',
            "SO2 Concentration per Month"
        )
        st.pyplot(fig)
    
    with col2:
        st.subheader("SO2 Statistics")
        display_pollutant_stats(df, 'Average_SO2', 'month')
    
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