import os
import logging
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.hotel_models import Hotel
from src.services.tripadvisor_api import fetch_location_details
from src.utils.file_utils import load_json_file
from src.database.db_setup import Session as SessionMaker

# Configure logging
logger = logging.getLogger(__name__)

# Fallback flag for population without validation
FALLBACK_POPULATION = os.getenv("FALLBACK_POPULATION", "False").lower() == "true"

def populate_hotels():
    """Populate hotels table from hotels.json, validating category and name. Checks existing location_id, stops after two validation failures."""
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../data", "hotels.json")
    
    if not os.path.exists(json_file_path):
        logger.error(f"Fichier JSON '{json_file_path}' introuvable. La table hotels ne sera pas populée.")
        return
    
    hotels_data = load_json_file(json_file_path)
    if not hotels_data:
        logger.warning("Aucune donnée valide trouvée dans hotels.json.")
        return
    
    session = SessionMaker()
    try:
        added_hotels = 0
        skipped_hotels = 0
        failed_validations = 0  # Track validation failures
        
        for hotel_data in hotels_data:
            if not all(key in hotel_data for key in ["nom_hotel", "marque", "location_id"]):
                logger.warning(f"Saut d'hôtel : Champs requis manquants - {hotel_data}")
                skipped_hotels += 1
                continue
            
            # Check if location_id already exists in the database
            existing_hotel = session.query(Hotel).filter_by(location_id=hotel_data["location_id"]).first()
            if existing_hotel:
                logger.info(f"Saut d'hôtel : location_id {hotel_data['location_id']} existe déjà dans la base de données : {existing_hotel.nom_hotel}")
                skipped_hotels += 1
                continue
            
            # Validate category and name via TripAdvisor API, unless fallback is enabled
            if not FALLBACK_POPULATION:
                details = fetch_location_details(os.getenv("API_KEY"), hotel_data["location_id"], hotel_data["nom_hotel"])
                if not details:
                    logger.warning(f"Saut d'hôtel : Validation échouée pour location_id {hotel_data['location_id']} ({hotel_data['nom_hotel']})")
                    skipped_hotels += 1
                    failed_validations += 1
                    # Stop after two validation failures
                    if failed_validations >= 2:
                        logger.error(f"Arrêt de la population : Deux échecs de validation détectés (dernier : location_id {hotel_data['location_id']})")
                        break
                    continue
            else:
                logger.info(f"Validation API sautée pour {hotel_data['nom_hotel']} (FALLBACK_POPULATION activé)")
            
            hotel = Hotel(
                nom_hotel=hotel_data["nom_hotel"],
                marque=hotel_data["marque"],
                location_id=hotel_data["location_id"]
            )
            session.add(hotel)
            added_hotels += 1
            logger.info(f"Ajout de l'hôtel : {hotel.nom_hotel}")
            
            # Add delay to avoid rate limits (except in fallback mode)
            if not FALLBACK_POPULATION:
                time.sleep(0.5)  # 0.5-second delay between API calls
        
        if added_hotels > 0:
            session.commit()
            logger.info(f"Population des hôtels terminée avec succès : {added_hotels} hôtels ajoutés, {skipped_hotels} sautés.")
        else:
            logger.info(f"Aucun nouvel hôtel ajouté : {skipped_hotels} sautés.")
    
    except SQLAlchemyError as e:
        logger.error(f"Erreur de base de données lors de la population des hôtels : {str(e)}")
        session.rollback()
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la population des hôtels : {str(e)}")
        session.rollback()
    finally:
        session.close()