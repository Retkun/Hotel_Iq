from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "hotels"
    nom_hotel = Column(String, primary_key=True)
    marque = Column(String, nullable=False)
    location_id = Column(Integer, nullable=False)
    reviews = relationship("Review", back_populates="hotel")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("hotels.location_id"), nullable=False)
    review_id = Column(Integer, nullable=False, unique=True)
    published_date = Column(DateTime, nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    trip_type = Column(String, nullable=True)
    travel_date = Column(Date, nullable=True)
    helpful_votes = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    url = Column(String, nullable=True)   
    hotel = relationship("Hotel", back_populates="reviews")

# Index for faster duplicate checks
Index("idx_review_id", Review.review_id)