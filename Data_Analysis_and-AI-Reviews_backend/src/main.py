import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.database.db_setup import init_db
from src.services.hotel_service import populate_hotels
from src.controllers.hotel_controller import router as hotel_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(title="Hotel Reviews API")

# Aloow CORS for frontend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include hotel routes
app.include_router(hotel_router, prefix="/hotels")

@app.on_event("startup")
def on_startup():
    init_db()
    if not API_KEY:
        raise RuntimeError("API_KEY non trouvé dans les variables d'environnement.")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY non trouvé dans les variables d'environnement.")
    
    # Populate hotels table after database creation
    try:
        populate_hotels()
    except Exception as e:
        logger.error(f"Échec de la population initiale des hôtels : {str(e)}")
        # Continue startup even if population fails