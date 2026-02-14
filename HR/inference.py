import numpy as np
import pandas as pd
import joblib
from typing import Union, Dict, List

model = joblib.load('model.pkl')
encoder = joblib.load('encoder.pkl')

FEATURE_COLUMNS = [
    'MonthlyIncome', 
    'Department', 
    'EnvironmentSatisfaction',
    'JobSatisfaction', 
    'StockOptionLevel', 
    'WorkLifeBalance',
    'NumCompaniesWorked', 
    'YearsInCurrentRole', 
    'PercentSalaryHike',
    'YearsWithCurrManager'
]

DEPARTMENT_MAPPING = {
    'Sales': 0,
    'R&D': 1,
    'HR': 2
}


def preprocess_input(data: pd.DataFrame) -> pd.DataFrame:
    data_copy = data.copy()
    
    if 'Department' in data_copy.columns and data_copy['Department'].dtype == 'object':
        data_copy['Department'] = data_copy['Department'].map(DEPARTMENT_MAPPING)
    
    for col in FEATURE_COLUMNS:
        if col not in data_copy.columns:
            raise ValueError(f"Missing required column: {col}")
    
    data_copy = data_copy[FEATURE_COLUMNS]
    
    return data_copy


def predict_single(sample: Dict) -> Dict:

    df = pd.DataFrame([sample])
    df_processed = preprocess_input(df)
    
    prediction = model.predict(df_processed)[0]
    probability = model.predict_proba(df_processed)[0]
    
    return {
        'prediction': 'Yes' if prediction == 1 else 'No',
        'prediction_value': int(prediction),
        'probability_no_attrition': float(probability[0]),
        'probability_attrition': float(probability[1])
    }


def predict_batch(data: Union[str, pd.DataFrame]) -> pd.DataFrame:

    if isinstance(data, str):
        df = pd.read_csv(data)
    else:
        df = data.copy()
    
    df_processed = preprocess_input(df)
    
    predictions = model.predict(df_processed)
    probabilities = model.predict_proba(df_processed)
    
    result_df = df.copy()
    result_df['Prediction'] = ['Yes' if p == 1 else 'No' for p in predictions]
    result_df['Probability_No_Attrition'] = probabilities[:, 0]
    result_df['Probability_Attrition'] = probabilities[:, 1]
    
    return result_df


def get_model_info() -> Dict:
    return {
        'model_type': type(model).__name__,
        'n_estimators': model.n_estimators,
        'feature_columns': FEATURE_COLUMNS,
        'categorical_features': ['Department'],
        'target': 'Attrition (Yes/No)'
    }


# Example usage
if __name__ == "__main__":
    
    print("=" * 60)
    print("EMPLOYEE ATTRITION PREDICTION MODEL")
    print("=" * 60)
    
    # Example 1: Single prediction
    print("\n1. SINGLE EMPLOYEE PREDICTION")
    print("-" * 60)
    
    employee = {
        'MonthlyIncome': 5000,
        'Department': 'Sales',
        'EnvironmentSatisfaction': 3,
        'JobSatisfaction': 2,
        'StockOptionLevel': 1,
        'WorkLifeBalance': 2,
        'NumCompaniesWorked': 2,
        'YearsInCurrentRole': 5,
        'PercentSalaryHike': 13,
        'YearsWithCurrManager': 3
    }
    
    result = predict_single(employee)
    print(f"Employee Data: {employee}")
    print(f"\nPrediction: {result['prediction']}")
    print(f"Probability of Attrition: {result['probability_attrition']:.4f}")
    print(f"Probability of Staying: {result['probability_no_attrition']:.4f}")
    
    # Example 2: Batch prediction from CSV
    print("\n\n2. BATCH PREDICTION FROM CSV")
    print("-" * 60)
    print("To predict multiple employees, use:")
    print("results = predict_batch('input_file.csv')")
    print("results.to_csv('predictions.csv', index=False)")
    
    # Example 3: Model information
    print("\n\n3. MODEL INFORMATION")
    print("-" * 60)
    info = get_model_info()
    for key, value in info.items():
        print(f"{key}: {value}")
