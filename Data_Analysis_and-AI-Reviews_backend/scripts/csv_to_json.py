import pandas as pd
import json

def csv_to_json(file_path, output_file="hotels.json"):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Verify expected columns
        expected_columns = ["nom_hotel", "marque"]
        if not all(col in df.columns for col in expected_columns):
            raise ValueError("CSV must contain 'nom_hotel' and 'marque' columns")
        
        # Convert dataframe to list of dictionaries
        data = df[expected_columns].to_dict(orient="records")
        
        # Write to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Successfully converted CSV to JSON. Output saved to {output_file}")
        
        # Print first few records as preview
        print("\nPreview of JSON content (first 3 records):")
        print(json.dumps(data[:3], indent=4, ensure_ascii=False))
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    #CSV file path
    file_path = "../data/hotels.csv"
    csv_to_json(file_path)