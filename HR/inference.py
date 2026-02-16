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
    import os
    
    print("=" * 60)
    print("EMPLOYEE ATTRITION PREDICTION MODEL")
    print("=" * 60)
    
    while True:
        print("\nMENU:")
        print("1. Single Employee Prediction")
        print("2. Batch Prediction from CSV")
        print("3. Model Information")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Single prediction
            print("\n1. SINGLE EMPLOYEE PREDICTION")
            print("-" * 60)
            
            try:
                employee = {}
                
                # Numeric inputs
                employee['MonthlyIncome'] = float(input("Enter Monthly Income: "))
                
                # Department input with validation
                while True:
                    dept = input("Enter Department (Sales/R&D/HR): ").strip()
                    if dept in ['Sales', 'R&D', 'HR']:
                        employee['Department'] = dept
                        break
                    print("Invalid department. Please enter Sales, R&D, or HR.")
                
                employee['EnvironmentSatisfaction'] = float(input("Enter Environment Satisfaction (1-4): "))
                employee['JobSatisfaction'] = float(input("Enter Job Satisfaction (1-4): "))
                employee['StockOptionLevel'] = float(input("Enter Stock Option Level: "))
                employee['WorkLifeBalance'] = float(input("Enter Work Life Balance (1-4): "))
                employee['NumCompaniesWorked'] = float(input("Enter Number of Companies Worked: "))
                employee['YearsInCurrentRole'] = float(input("Enter Years in Current Role: "))
                employee['PercentSalaryHike'] = float(input("Enter Percent Salary Hike: "))
                employee['YearsWithCurrManager'] = float(input("Enter Years with Current Manager: "))
                
                result = predict_single(employee)
                print(f"\nEmployee Data: {employee}")
                print(f"\nPrediction: {result['prediction']}")
                print(f"Probability of Attrition: {result['probability_attrition']:.4f}")
                print(f"Probability of Staying: {result['probability_no_attrition']:.4f}")
            
            except ValueError as e:
                print(f"Error: Invalid input. Please enter valid numbers.")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            # Batch prediction from CSV
            print("\n2. BATCH PREDICTION FROM CSV")
            print("-" * 60)
            
            while True:
                csv_file = input("Enter CSV file path (e.g., sample.csv): ").strip()
                
                if not csv_file:
                    print("Error: File path cannot be empty.")
                    continue
                
                if not os.path.exists(csv_file):
                    print(f"Error: File '{csv_file}' not found.")
                    continue
                
                try:
                    results = predict_batch(csv_file)
                    print(f"\nSuccessfully processed {len(results)} records.")
                    print("\nFirst few records with predictions:")
                    print(results.head())
                    
                    # Option to save results
                    save_option = input("\nSave predictions to CSV? (y/n): ").strip().lower()
                    if save_option == 'y':
                        output_file = input("Enter output file name (default: predictions.csv): ").strip()
                        if not output_file:
                            output_file = "predictions.csv"
                        results.to_csv(output_file, index=False)
                        print(f"Predictions saved to '{output_file}'")
                    break
                
                except ValueError as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error processing file: {e}")
        
        elif choice == '3':
            # Model information
            print("\n3. MODEL INFORMATION")
            print("-" * 60)
            info = get_model_info()
            for key, value in info.items():
                print(f"{key}: {value}")
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")
