import numpy as np
import pandas as pd
import joblib
from typing import Union, Dict, List

model = joblib.load('/home/averroes/Documents/Fundamental-Data-Analysis-Dicoding/Education Problem/model.pkl')

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


# Example usage
if __name__ == "__main__":
    import os
    
    print("=" * 60)
    print("EMPLOYEE ATTRITION PREDICTION MODEL")
    print("=" * 60)
    
    while True:
        print("\nMENU:")
        print("1. Batch Prediction from CSV")
        print("2. Model Information")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':

            # Batch prediction from CSV
            print("\n1. BATCH PREDICTION FROM CSV")
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
        
        elif choice == '2':
            # Model information
            print("\n3. MODEL INFORMATION")
            print("-" * 60)
            info = get_model_info()
            for key, value in info.items():
                print(f"{key}: {value}")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")
