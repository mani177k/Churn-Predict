import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from scripts import data_preprocessing
    print("Import successful")
    print(f"transform_data: {data_preprocessing.transform_data}")
except Exception as e:
    print(f"Import failed: {e}")
