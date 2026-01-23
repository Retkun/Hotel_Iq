import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from src.models.hotel_models import Hotel, Review
from src.services.tripadvisor_api import fetch_reviews_by_location
from src.services.openai_api import analyze_hotel_sentiment
from src.database.db_setup import Session as SessionMaker
from src.schemas.hotel_schemas import HotelResponse, ReviewResponse, AnalysisResponse
import os

# Configure logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[HotelResponse])
def get_all_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    if not hotels:
        raise HTTPException(status_code=404, detail="Aucun hôtel trouvé")
    return hotels

@router.get("/{location_id}", response_model=HotelResponse)
def get_hotel_by_id(location_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter_by(location_id=location_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail=f"L'identifiant {location_id} ne correspond à aucun hôtel dans notre base de données.")
    return hotel

@router.get("/{location_id}/reviews", response_model=List[ReviewResponse])
def get_reviews_for_hotel(location_id: int, db: Session = Depends(get_db)):
    # Verify hotel exists
    hotel = db.query(Hotel).filter_by(location_id=location_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail=f"L'identifiant {location_id} ne correspond à aucun hôtel dans notre base de données.")

    # Fetch reviews from TripAdvisor, passing nom_hotel for validation
    reviews_data = fetch_reviews_by_location(os.getenv("API_KEY"), location_id, hotel.nom_hotel)
    
    # Store new reviews
    new_reviews = 0
    for review_data in reviews_data:
        existing_review = db.query(Review).filter_by(review_id=review_data["id"]).first()
        if existing_review:
            continue
        
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
            username=review_data.get("user", {}).get("username"),
            url=review_data.get("url")
        )
        db.add(review)
        new_reviews += 1
    
    if new_reviews > 0:
        try:
            db.commit()
            logger.info(f"Ajouté {new_reviews} nouveaux avis pour location_id {location_id}")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Échec de l'enregistrement des avis : {str(e)}")
    
    # Return all reviews for the hotel
    reviews = db.query(Review).filter_by(location_id=location_id).all()
    return reviews

@router.get("/{location_id}/analysis", response_model=AnalysisResponse)
def analyze_hotel_reviews(location_id: int, db: Session = Depends(get_db)):
    # Get hotel details
    hotel = db.query(Hotel).filter_by(location_id=location_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail=f"L'identifiant {location_id} ne correspond à aucun hôtel dans notre base de données.")
    
    # Get the last 5 reviews from the database
    last_reviews = (
        db.query(Review)
        .filter_by(location_id=location_id)
        .order_by(Review.published_date.desc())
        .limit(5)
        .all()
    )
    
    if not last_reviews:
        logger.warning(f"Aucun avis trouvé pour location_id {location_id}")
        raise HTTPException(
            status_code=404,
            detail="Aucun avis trouvé pour cet hôtel. Veuillez rafraîchir les avis pour obtenir les derniers."
        )
    
    # Prepare review data for OpenAI 
    review_data = [
        {
            "title": review.title,
            "text": review.text,
            "rating": review.rating,
            "published_date": review.published_date,
            "trip_type": review.trip_type
        }
        for review in last_reviews
    ]
    
    # Call OpenAI API for sentiment analysis
    try:
        analysis = analyze_hotel_sentiment(os.getenv("OPENAI_API_KEY"), hotel.nom_hotel, hotel.marque, review_data)
        return analysis
    except ValueError as e:
        logger.error(f"Erreur de validation pour l'analyse de {hotel.nom_hotel}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse pour {hotel.nom_hotel}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse : {str(e)}")