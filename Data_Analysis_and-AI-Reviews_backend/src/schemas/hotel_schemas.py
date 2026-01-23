from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class HotelResponse(BaseModel):
    nom_hotel: str
    marque: str
    location_id: int

class ReviewResponse(BaseModel):
    id: int
    location_id: int
    review_id: int
    published_date: datetime
    rating: int
    text: str
    title: str
    trip_type: Optional[str]
    travel_date: Optional[datetime]
    helpful_votes: int
    username: Optional[str]
    url: Optional[str]

class AnalysisResponse(BaseModel):
    nom_hotel: str
    marque: str
    note_globale: str
    analyse_des_sentiments: str
    insights: str
    conclusion: str