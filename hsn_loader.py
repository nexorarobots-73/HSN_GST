import pandas as pd
import os
import sys

def load_hsn_codes():
    try:
        # Get the correct path whether running as script or executable
        if getattr(sys, 'frozen', False):
            # Running as executable
            base_path = sys._MEIPASS
            file_path = os.path.join(base_path, "HSN_SAC.xlsx")
        else:
            # Running as script
            file_path = "HSN_SAC.xlsx"
            
        # Try to load the Excel file
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            codes = df['HSN_CD'].astype(str).tolist()
            return codes, df.set_index('HSN_CD')['HSN_Description'].to_dict()
        else:
            raise FileNotFoundError(f"Excel file not found at: {file_path}")
    except Exception as e:
        print(f"Error loading HSN data: {e}")
        # Return sample data as fallback
        sample_codes = ['0101', '0102', '0201', '0202', '0301']
        sample_map = {
            '0101': 'Live horses',
            '0102': 'Live bovine animals',
            '0201': 'Meat of bovine animals, fresh',
            '0202': 'Meat of bovine animals, frozen',
            '0301': 'Live fish'
        }
        return sample_codes, sample_map