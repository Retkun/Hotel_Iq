import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import time

# Add project root to sys.path to ensure src/ is found
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.hotel_models import Hotel, Review
from src.services.tripadvisor_api import fetch_reviews
from src.utils.file_utils import load_json_file
from src.database.db_setup import init_db, Session

def populate_database(json_file_path, api_key):
    # Initialize database
    init_db()
    session = Session()
    
    # Verify JSON file path
    if not os.path.exists(json_file_path):
        print(f"Error: JSON file '{json_file_path}' does not exist. Please place hotels.json in the data/ directory.")
        return
    
    # Load JSON file
    hotels_data = load_json_file(json_file_path)
    if not hotels_data:
        return
    
    try:
        # Process hotels
        for hotel_data in hotels_data:
            if not all(key in hotel_data for key in ["nom_hotel", "marque", "location_id"]):
                print(f"Skipping hotel: Missing required fields - {hotel_data}")
                continue
            
            # Check if hotel exists
            existing_hotel = session.query(Hotel).filter_by(nom_hotel=hotel_data["nom_hotel"]).first()
            if not existing_hotel:
                hotel = Hotel(
                    nom_hotel=hotel_data["nom_hotel"],
                    marque=hotel_data["marque"],
                    location_id=hotel_data["location_id"]
                )
                session.add(hotel)
                print(f"Added hotel: {hotel.nom_hotel}")
            
            # Fetch reviews
            reviews = fetch_reviews(api_key, hotel_data["location_id"])
            for review_data in reviews:
                # Parse dates
                try:
                    published_date = datetime.strptime(review_data["published_date"], "%Y-%m-%dT%H:%M:%S%z")
                except (ValueError, KeyError):
                    published_date = datetime.now()
                
                travel_date = None
                if review_data.get("travel_date"):
                    try:
                        travel_date = datetime.strptime(review_data["travel_date"], "%Y-%m").date()
                    except ValueError:
                        pass
                
                # Check if review exists
                existing_review = session.query(Review).filter_by(review_id=review_data["id"]).first()
                if not existing_review:
                    review = Review(
                        location_id=review_data["location_id"],
                        review_id=review_data["id"],
                        published_date=published_date,
                        rating=review_data["rating"],
                        text=review_data["text"],
                        title=review_data["title"],
                        trip_type=review_data.get("trip_type"),
                        travel_date=travel_date,
                        helpful_votes=review_data.get("helpful_votes", 0),
                        username=review_data.get("user", {}).get("username")
                    )
                    session.add(review)
                    print(f"Added review {review.review_id} for hotel {hotel_data['nom_hotel']}")
            
            # Respect API rate limits ( less than 5 requests per second)
            time.sleep(0.5)
        
        # Commit changes
        session.commit()
        print("Database population completed successfully.")
    
    except SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        session.rollback()
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    load_dotenv()
    json_file_path = os.path.join(project_root, "data", "hotels.json")
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("Error: API_KEY not found in environment variables. Please check your .env file.")
    else:
        populate_database(json_file_path, api_key)