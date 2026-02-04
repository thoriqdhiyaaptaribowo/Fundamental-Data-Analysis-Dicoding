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
    
    pollutant_name = pollutant_col.replace('_', ' ').replace('Average ', '')
    
    with col1:
        st.metric(
            f"Highest {pollutant_name}",
            f"{data.loc[highest_idx, pollutant_col]:.2f} µg/m³",
            f"Month {int(data.loc[highest_idx, month_col])}"
        )
    
    with col2:
        st.metric(
            f"Lowest {pollutant_name}",
            f"{data.loc[lowest_idx, pollutant_col]:.2f} µg/m³",
            f"Month {int(data.loc[lowest_idx, month_col])}"
        )

df = load_data()

# Sidebar navigation and filters
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Analysis", ["Overview", "CO Analysis", "SO2 Analysis", "Conclusion"])

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

    st.subheader("Explanation:")
    st.markdown("""
**Insight:**
- Highest CO concentration occurs in November with 997.79 µg/m³, indicating the worst air pollution when entering winter
- Lowest CO concentration is recorded in May with 696.62 µg/m³, meaning air quality is relatively better in summer
- CO concentration shows a gradual increase from May to November, with acceleration particularly in the last quarter of the year (October-December)
- The seasonal patern also shows that there's a precieved volatility between each station showing that CO emision is sensitive to the variation of fossil fuel emmition
""")

    st.subheader("Implication:")
    st.markdown("""
Dramatic increase of CO concentration during winter reflects serious air quality degradation, triggered by:
- Intensification of fossil fuel use (especially for heating)
- Meteorological conditions that hinder pollutant dispersion (thermal inversion, high humidity, weak winds)
- Concentration differences between stations range from 300-400 µg/m³, indicating significant contribution from local characteristics such as traffic density and industrial activities
""")

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

    st.subheader("Explanation:")
    st.markdown("""
**Insight:**
- SO₂ concentration peaks in January with a value of 15.90 µg/m³, slightly later than CO which peaks in November
- Lowest SO₂ concentration occurs in August at 4.21 µg/m³, reflecting the best air quality period in the year
- SO₂ shows a sharper seasonal pattern compared to CO, with fluctuation reaching 78% between highest and lowest values
- The Patern between each station also shows that SO₂ seasonal patern is less volatile compared to CO seasonal patern suggesting that there's a permanent emmision source that's independent from the average household emision
- SO₂ increase from September to January is related to intensification of fossil fuel use for space heating and increased industrial activity in winter
""")

    st.subheader("Implication:")
    st.markdown(""" 
Sharp SO₂ fluctuation (78% difference) reveals strong dependence on seasonal variations and industrial activity:
- Increased energy consumption is the main driver during winter
- Although all stations show similar seasonal trends, some stations particularly near industrial centers show significantly higher baseline concentration levels throughout the year
- This reflects a combination of global meteorological factors and location-specific emission sources
""")

# Conclusion Page
elif page == "Conclusion":
    st.header("Conclusion")
    
    st.subheader("1. Findings on Average Carbon Monoxide (CO) and Sulfur Dioxide (SO₂) Concentration per Month and it's Implication")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average CO per Station")
        display_pollutant_stats(filtered_df, 'Average_CO', 'month') 
    with col2:
        st.subheader("Average SO₂ per Station")
        display_pollutant_stats(filtered_df, 'Average_SO2', 'month')

    st.markdown("""
**Implication:**
- Both polutant shows an U curve that's consistent with the peak from September to February (winter) and valley in April to August (summer)
- The periode from September to February indentified as critical zone with polutant concentration at it's highest which is a health risk for compromized individual (elderly, children, people with respiratory issue) 
- The increase in pollutant concentrations in winter is caused by the convergence of two factors: 
    1. Intensification of the use of fossil fuels for heating and energy needs, and 
    2. Adverse meteorological conditions that inhibit the spread of pollutants (thermal inversion, high humidity, low wind speed). 
- The strong temporal correlation between the two pollutants indicates the same dominant emission source, namely the combustion of fossil fuels from the transportation and energy sectors.
    """)
    
    st.subheader("2. Findings on the Movement of Carbon Monoxide (CO) and Sulfur Dioxide (SO₂) Concentration of Each Station per Month and it's Implication to the Air Quality Cycle")
    
    st.markdown("""
**Implication:** 
- Universal seasonal patterns demonstrate that regional meteorological factors are the primary determinants of pollutant concentration fluctuations, overriding local variations and specific emission sources.
- The presence of stations with high baseline concentrations suggests the presence of significant local, permanent emission sources (e.g., traffic centers, industrial zones, or topography that discourages dispersion).
- Synchronized CO2 and SO2 movements confirm that mitigation strategies should target common emission sources, focusing on the transportation and energy sectors.
- Variations between stations emphasize that despite universal trends, local characteristics and specific emission sources still play a significant role in determining air quality in each region.
    """)
    
    st.subheader("3. Final Conclution")
    st.markdown("""
This dataset demonstrates that air quality in the study area experiences **extreme and structured seasonal fluctuations**, rather than linear degradation. The winter period (September-February) consistently constitutes a critical zone with double the concentration of pollutants compared to summer. While global fluctuations are driven by regional meteorological factors, differences between stations indicate a significant role for local emission sources.
    """)
    
    st.subheader("4. Policy Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
**Seasonal Management:**
-> Implement stricter control protocols specifically in September-February with industrial emission restrictions, traffic restrictions, and increased monitoring.

**Station-Based Intervention**
-> Identify and manage local emission sources at stations with consistently high concentrations through environmental audits and more specific regulations. 

**Public Communication**
-> Develop an educational campaigns on respiratory health risks with special emphasis on the winter period and vulnerable groups
        """)
    
    with col2:
        st.markdown("""
**Early Warning System**
-> Develop an early warning system that use the seasonal cycle to give a public alert during critical periods

**Further Research**
-> In-depth investigation of the correlation between local meteorological characteristics (temperature, humidity, wind speed, pressure) with pollutant concentrations to improve prediction accuracy
        """)

st.markdown("---")
st.markdown("**Data Source:** Air Quality Dataset (2013-2017)")