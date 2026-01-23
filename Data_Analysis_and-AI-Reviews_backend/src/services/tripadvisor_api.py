import requests
import time
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache file path
CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "../data", "hotel_details_cache.json")

def load_cache():
    """Load cached hotel details from file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur lors du chargement du cache : {str(e)}")
            return {}
    return {}

def save_cache(cache):
    """Save hotel details to cache file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement du cache : {str(e)}")

def fetch_location_details(api_key: str, location_id: int, nom_hotel: str, max_retries: int = 3) -> dict:
    """Fetch location details to validate category and name, using cache."""
    try:
        location_id = int(location_id)  # Ensure location_id is an integer
        if location_id <= 0:
            logger.error(f"Identifiant de localisation invalide : {location_id}. Doit être un entier positif.")
            return {}
    except (TypeError, ValueError):
        logger.error(f"Identifiant de localisation non numérique : {location_id}")
        return {}

    # Check cache
    cache = load_cache()
    cache_key = str(location_id)
    if cache_key in cache:
        logger.info(f"Utilisation du cache pour location_id {location_id}")
        data = cache[cache_key]
        
        # Validate cached data
        category = data.get("category", {}).get("name", "").lower()
        if category != "hotel":
            logger.warning(f"Localisation {location_id} n'est pas un hôtel (catégorie : {category})")
            return {}

        api_name = data.get("name", "").lower()
        nom_hotel_lower = nom_hotel.lower()
        if not (nom_hotel_lower in api_name or api_name in nom_hotel_lower or
                any(word in api_name for word in nom_hotel_lower.split())):
            logger.warning(f"Nom de l'hôtel ne correspond pas pour location_id {location_id}. Attendu : {nom_hotel}, Trouvé : {data.get('name')}")
            return {}

        return data

    # API call if not in cache
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details"
    headers = {"accept": "application/json"}
    params = {
        "key": api_key,
        "language": "fr"
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Log raw response for debugging
            logger.debug(f"Réponse API pour location_id {location_id} : {data}")

            # Check category
            category = data.get("category", {}).get("name", "").lower()
            if category != "hotel":
                logger.warning(f"Localisation {location_id} n'est pas un hôtel (catégorie : {category})")
                return {}

            # Check name (case-insensitive, lenient match)
            api_name = data.get("name", "").lower()
            nom_hotel_lower = nom_hotel.lower()
            if not (nom_hotel_lower in api_name or api_name in nom_hotel_lower or
                    any(word in api_name for word in nom_hotel_lower.split())):
                logger.warning(f"Nom de l'hôtel ne correspond pas pour location_id {location_id}. Attendu : {nom_hotel}, Trouvé : {data.get('name')}")
                return {}

            # Cache the result
            cache[cache_key] = data
            save_cache(cache)
            return data

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logger.info(f"Limite de taux dépassée. Nouvelle tentative après {2 ** attempt} secondes...")
                time.sleep(2 ** attempt)
                continue
            logger.error(f"Erreur HTTP pour location_id {location_id} : {str(e)}")
            return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de requête pour location_id {location_id} : {str(e)}")
            return {}
    
    logger.error(f"Échec de la récupération des détails pour location_id {location_id} après {max_retries} tentatives.")
    return {}

def fetch_reviews(api_key: str, location_id: int, max_retries: int = 3, limit: int = 5) -> list:
    """Legacy function for bulk fetching (kept for compatibility)."""
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews"
    headers = {"accept": "application/json"}
    params = {
        "key": api_key,
        "language": "fr",
        "limit": limit
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "data" in data and data["data"]:
                return data["data"]
            logger.info(f"Aucun avis trouvé pour location_id {location_id}")
            return []
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logger.info(f"Limite de taux dépassée. Nouvelle tentative après {2 ** attempt} secondes...")
                time.sleep(2 ** attempt)
                continue
            logger.error(f"Erreur HTTP pour location_id {location_id} : {str(e)}")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur de requête pour location_id {location_id} : {str(e)}")
            return []
    
    logger.error(f"Échec de la récupération des avis pour location_id {location_id} après {max_retries} tentatives.")
    return []

def fetch_reviews_by_location(api_key: str, location_id: int, nom_hotel: str = "", max_retries: int = 3, limit: int = 5) -> list:
    """Fetch reviews for a single location_id after validating it's a hotel."""
    try:
        location_id = int(location_id)
        if location_id <= 0:
            logger.error(f"Identifiant de localisation invalide : {location_id}. Doit être un entier positif.")
            return []
    except (TypeError, ValueError):
        logger.error(f"Identifiant de localisation non numérique : {location_id}")
        return []
    
    # Validate location is a hotel if nom_hotel is provided
    if nom_hotel:
        details = fetch_location_details(api_key, location_id, nom_hotel, max_retries)
        if not details:
            logger.error(f"Validation échouée pour location_id {location_id}. Aucun avis ne sera récupéré.")
            return []
    
    return fetch_reviews(api_key, location_id, max_retries, limit)