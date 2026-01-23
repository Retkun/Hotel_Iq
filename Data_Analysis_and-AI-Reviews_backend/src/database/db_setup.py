from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.hotel_models import Base

# Create SQLite database
engine = create_engine("sqlite:///hotels.db", echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)