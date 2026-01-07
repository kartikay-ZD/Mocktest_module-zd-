
import pandas as pd

def analyze_excel(file_path):
    """
    Reads an Excel file and prints the first few rows of each sheet
    to understand its structure.
    """
    try:
        # Read all sheets from the Excel file
        xls = pd.ExcelFile(file_path)
        
        if not xls.sheet_names:
            print("The Excel file is empty or has no sheets.")
            return

        print(f"Found sheets: {xls.sheet_names}\n")

        # Loop through each sheet and print its head
        for sheet_name in xls.sheet_names:
            print(f"--- Analyzing Sheet: '{sheet_name}' ---")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            print(f"Columns: {df.columns.tolist()}")
            print("First 5 rows:")
            print(df.head())
            print("\n" + "="*50 + "\n")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_excel('mock_test.xlsx')
