import pandas as pd

def read_csv_info(file_path, num_rows=5):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Get column names
        columns = df.columns.tolist()
        
        # Print column names
        print("\nColumn Names:")
        print("-" * 30)
        for col in columns:
            print(col)
        
        # Print first few rows
        print(f"\nFirst {num_rows} rows of the CSV:")
        print("-" * 30)
        print(df.head(num_rows))
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    #  CSV file path
    file_path = "../data/hotels.csv"
    read_csv_info(file_path)