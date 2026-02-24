import os
import io
import pandas as pd
import streamlit as st
import joblib
from typing import Union, Dict, List


model = joblib.load('Education Problem/model.pkl')

FEATURE_COLUMNS = ['Marital_status',
                   'Course',
                   'Daytime_evening_attendance',
                   'Admission_grade',
                   'Displaced',
                   'Educational_special_needs',
                   'Debtor',
                   'Tuition_fees_up_to_date',
                   'Scholarship_holder',
                   'Unemployment_rate',
                   'Inflation_rate',
                   'GDP']


def preprocess_input(data: pd.DataFrame) -> pd.DataFrame:
    data_copy = data.copy()
    
    for col in FEATURE_COLUMNS:
        if col not in data_copy.columns:
            raise ValueError(f"Missing required column: {col}")
    
    data_copy = data_copy[FEATURE_COLUMNS]
    
    return data_copy

def predict_batch(data: Union[str, pd.DataFrame]) -> pd.DataFrame:

    if isinstance(data, str):
        df = pd.read_csv(data)
    else:
        df = data.copy()
    
    df_processed = preprocess_input(df)
    
    predictions = model.predict(df_processed)
    probabilities = model.predict_proba(df_processed)
    
    result_df = df.copy()
    result_df['Prediction'] = ['Yes' if p == 0 else 'No' for p in predictions]
    result_df['Probability_Dropout'] = probabilities[:, 0]
    result_df['Probability_No_Dropout'] = probabilities[:, 1]
    
    return result_df


def get_model_info() -> Dict:
    return {
        'model_type': type(model).__name__,
        'n_estimators': model.n_estimators,
        'feature_columns': FEATURE_COLUMNS,
        'categorical_features': ['Department'],
        'target': 'Attrition (Yes/No)'
    }


st.set_page_config(page_title="Attrition Prediction", layout="wide")

st.title("Student Dropout Prediction")

col1, col2 = st.columns([3, 1])

with col2:
    st.header("Options")
    use_sample = st.checkbox("Use sample CSV")
    show_model_info = st.button("Show model info")

uploaded_file = None
if use_sample:
    sample_path = os.path.join(os.path.dirname(__file__), "sample.csv")
    if os.path.exists(sample_path):
        uploaded_file = open(sample_path, "rb")
    else:
        st.warning("Sample file not found in app folder.")

if uploaded_file is None:
    uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    try:
        if hasattr(uploaded_file, "read"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_csv(str(uploaded_file))

        st.subheader("Input Preview")
        st.dataframe(df.head())

        if st.button("Run predictions"):
            try:
                results = predict_batch(df)
                st.success(f"Processed {len(results)} records")
                st.subheader("Predictions")
                st.dataframe(results)

                csv = results.to_csv(index=False).encode("utf-8")
                st.download_button("Download predictions as CSV", data=csv, file_name="predictions.csv", mime="text/csv")

            except Exception as e:
                st.error(f"Prediction error: {e}")

    except Exception as e:
        st.error(f"Error reading CSV: {e}")

if show_model_info:
    try:
        info = get_model_info()
        st.subheader("Model Information")
        st.json(info)
    except Exception as e:
        st.error(f"Error loading model info: {e}")

st.markdown("---")
