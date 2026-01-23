import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.hotel_models import Review
from src.services.tripadvisor_api import fetch_reviews_by_location
from src.database.db_setup import init_db, Session

def fetch_and_store_reviews(api_key, location_id):
    init_db()
    session = Session()
    
    try:
        # Fetch reviews
        reviews = fetch_reviews_by_location(api_key, location_id)
        if not reviews:
            print(f"No reviews fetched for location_id {location_id}")
            return
        
        new_reviews = 0
        for review_data in reviews:
            # Check for duplicate
            existing_review = session.query(Review).filter_by(review_id=review_data["id"]).first()
            if existing_review:
                print(f"Skipping duplicate review {review_data['id']} for location_id {location_id}")
                continue
            
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
            
            # Create new review
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
            new_reviews += 1
            print(f"Added review {review.review_id} for location_id {location_id}")
        
        if new_reviews > 0:
            session.commit()
            print(f"Successfully added {new_reviews} new reviews for location_id {location_id}")
        else:
            print(f"No new reviews added for location_id {location_id}")
    
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
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("Error: API_KEY not found in environment variables. Please check your .env file.")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="Fetch reviews for a hotel by location_id.")
    parser.add_argument("location_id", type=int, help="TripAdvisor location ID")
    args = parser.parse_args()
    
    fetch_and_store_reviews(api_key, args.location_id)



