import os
import sys
from sqlalchemy.exc import SQLAlchemyError

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.hotel_models import Hotel
from src.utils.file_utils import load_json_file
from src.database.db_setup import init_db, Session

def populate_hotels(json_file_path):
    init_db()
    session = Session()
    
    if not os.path.exists(json_file_path):
        print(f"Error: JSON file '{json_file_path}' does not exist.")
        return
    
    hotels_data = load_json_file(json_file_path)
    if not hotels_data:
        return
    
    try:
        for hotel_data in hotels_data:
            if not all(key in hotel_data for key in ["nom_hotel", "marque", "location_id"]):
                print(f"Skipping hotel: Missing required fields - {hotel_data}")
                continue
            
            existing_hotel = session.query(Hotel).filter_by(nom_hotel=hotel_data["nom_hotel"]).first()
            if not existing_hotel:
                hotel = Hotel(
                    nom_hotel=hotel_data["nom_hotel"],
                    marque=hotel_data["marque"],
                    location_id=hotel_data["location_id"]
                )
                session.add(hotel)
                print(f"Added hotel: {hotel.nom_hotel}")
        
        session.commit()
        print("Hotels population completed successfully.")
    
    except SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        session.rollback()
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    json_file_path = os.path.join(project_root, "data", "hotels.json")
    populate_hotels(json_file_path)