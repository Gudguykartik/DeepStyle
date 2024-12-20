import pandas as pd
import pickle
import os

def load_and_analyze_dataset():
    """
    Load and analyze the fashion dataset
    """
    try:
        # Using absolute path
        dataset_path = 'c:/Users/k/Desktop/Projects/app/frontend/ai_assistant/fashion_dataset_full.pkl'
        
        print(f"Attempting to load dataset from: {dataset_path}")
        
        with open(dataset_path, 'rb') as f:
            data = pickle.load(f)
        
        print("\nRaw data type:", type(data))
        
        # If data is a dictionary, let's see its keys first
        if isinstance(data, dict):
            print("\nDictionary keys:", data.keys())
            # Try to convert the most relevant part to DataFrame
            for key, value in data.items():
                print(f"\nKey: {key}")
                print(f"Type: {type(value)}")
                if isinstance(value, (list, dict)):
                    print(f"Length/Size: {len(value)}")
            return data
        
        # If it's already a DataFrame
        elif isinstance(data, pd.DataFrame):
            print("\nDataset Info:")
            print(data.info())
            print("\nFirst few rows:")
            print(data.head())
            return data
            
        # If it's a list or numpy array
        else:
            print("\nData type not directly compatible with DataFrame")
            print("Data structure:", type(data))
            return data
            
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return None

if __name__ == "__main__":
    data = load_and_analyze_dataset()
