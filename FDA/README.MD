# Air Quality Data Analysis Dashboard

## Instalation Guide
Run following command on your terminal
```
conda create -n dashboard python 3.13.9
conda activate dashboard
pip install -r requirement.txt
```
## Run Streamlit App
Run the following command on your terminal
```
streamlit run Dashboard.py
```
---
## Dashboard Guide
### Dataset Overview
- Contain the overview and data sample

### CO Analysis
- Contains the charts for average CO (Carbon Monoxide) concentration per month and monhly CO trend per station.
- The statistic also contain the highest and lowest CO concentration as well as the month.

### SO2 Analysis
- Contains the charts for average SO2 (Sulfur Dioxide) concentration per month and monthly SO2 trend per station.
- The statistic also contain the highest and lowest SO2 concentration as well as the month.

### Filters
- Contain the station selection and the range of month
- User can select which station to be displayed (Default is all of them) and the time range in month (default is 12 month)