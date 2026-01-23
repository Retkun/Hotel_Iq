import requests
import json
import time
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the input file.")
        return None

def save_json_file(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved updated JSON to {file_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")

def search_tripadvisor_hotel(api_key, hotel_name, max_retries=3):
    url = "https://api.content.tripadvisor.com/api/v1/location/search"
    headers = {"accept": "application/json"}
    params = {
        "key": api_key,
        "searchQuery": hotel_name,
        "category": "hotels",
        "language": "fr"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "data" in data and data["data"]:
                # Take the first result's location_id
                return data["data"][0]["location_id"]
            print(f"No results found for hotel '{hotel_name}'")
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limit exceeded
                print(f"Rate limit exceeded. Retrying after {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
                continue
            print(f"HTTP error for hotel '{hotel_name}': {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error for hotel '{hotel_name}': {str(e)}")
            return None
    print(f"Failed to fetch data for hotel '{hotel_name}' after {max_retries} attempts.")
    return None

def update_hotels_with_location_id(json_file_path, api_key):
    # Load the JSON file
    hotels = load_json_file(json_file_path)
    if not hotels:
        return
    
    # Process each hotel
    updated_count = 0
    for hotel in hotels:
        if "nom_hotel" not in hotel:
            print(f"Skipping hotel: Missing 'nom_hotel' field")
            continue
        
        hotel_name = hotel["nom_hotel"]
        print(f"Searching for hotel: {hotel_name}")
        
        # Search TripAdvisor for the hotel
        location_id = search_tripadvisor_hotel(api_key, hotel_name)
        
        if location_id:
            hotel["location_id"] = location_id
            updated_count += 1
            print(f"Assigned location_id {location_id} to hotel '{hotel_name}'")
        else:
            print(f"No location_id assigned for hotel '{hotel_name}'")
        
        # Respect API rate limits (e.g., ~5 requests per second)
        time.sleep(0.2)
    
    # Save the updated JSON file
    if updated_count > 0:
        save_json_file(json_file_path, hotels)
        print(f"Updated {updated_count} hotels with location_id")
    else:
        print("No hotels were updated with location_id")


if __name__ == "__main__":
    # JSON file path and TripAdvisor API key
    json_file_path = "../data/hotels.json"
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("Error: API_KEY not found in environment variables.")
    else:
        update_hotels_with_location_id(json_file_path, api_key)