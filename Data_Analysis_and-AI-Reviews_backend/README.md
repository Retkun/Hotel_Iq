# AI-Powered Hotel Reviews API

This Python application fetches hotel reviews from the TripAdvisor API, stores them in a SQLite database using SQLAlchemy ORM, and provides a FastAPI web interface to query hotels, reviews, and perform **AI-powered sentiment analysis** using the OpenAI API. It processes a JSON file containing hotel data (`nom_hotel`, `marque`, `location_id`) to populate `hotels` and `reviews` tables. The app supports a frontend at `http://localhost:4200` (e.g., Angular) for user interaction.

## Features
- **AI-Powered Sentiment Analysis**: Analyze the sentiment of the last 5 hotel reviews using OpenAI’s API, providing insights into guest experiences.
- Fetch and store hotel reviews from TripAdvisor API.
- RESTful API to retrieve hotel details and reviews.
- CORS-enabled for frontend integration.
- Automatic database initialization and hotel data population on startup.

## AI-Powered Sentiment Analysis
The app uses the OpenAI API to perform sentiment analysis on the most recent 5 reviews for a given hotel, retrieved from the SQLite database. The `GET /hotels/{location_id}/analysis` endpoint processes review data (title, text, rating, etc.) and returns AI-generated insights, such as overall sentiment, key themes, or guest satisfaction trends. This feature enhances decision-making for users by summarizing review sentiments intelligently.

*Note*: This is not a Retrieval-Augmented Generation (RAG) system but a direct integration with OpenAI’s API for sentiment analysis. Review data is queried from the database before being sent to the OpenAI API.

## Project Structure
```
hotel_reviews_app/
├── src/
│   ├── controllers/          # FastAPI route handlers
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas for API validation
│   ├── services/            # API clients (TripAdvisor, OpenAI)
│   ├── utils/               # File handling utilities
│   ├── database/            # Database setup
├── scripts/                 # Scripts for manual data population
├── data/                    # Input JSON file (hotels.json)
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## Setup

### Prerequisites
- Python 3.8+
- SQLite (included with Python)
- TripAdvisor API key
- OpenAI API key (required for sentiment analysis)
- (Optional) Frontend running at `http://localhost:4200` (e.g., Angular)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/medamineharbaoui/Data_Analysis_and-AI-Reviews_backend.git
   cd Data_Analysis_and_AI-Reviews_backend
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment**:
   - Create a `.env` file in the root directory:
     ```env
     API_KEY=your_tripadvisor_api_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Replace placeholders with your TripAdvisor and OpenAI API keys.

4. **Prepare Input JSON**:
   - Place your `hotels.json` file in the `data/` directory with the structure:
     ```json
     [
         {
             "nom_hotel": "Hotel Paris",
             "marque": "Hilton",
             "location_id": 123456
         },
         ...
     ]
     ```

## Usage

### Run the FastAPI Server
Start the FastAPI server to initialize the database, populate hotels, and serve API endpoints:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
- Access the API at `http://localhost:8000`.
- Explore endpoints via the interactive Swagger UI at `http://localhost:8000/docs`.
- The frontend (if set up) can connect to `http://localhost:4200` with CORS enabled.

### Manual Database Population
Optionally, populate the database manually (e.g., for testing or updates):
```bash
python scripts/populate_database.py
```
This will:
- Create a SQLite database (`hotels.db`) in the project root.
- Load `data/hotels.json` and populate the `hotels` table.
- Fetch up to 5 reviews per hotel from the TripAdvisor API.
- Store reviews in the `reviews` table.

### API Endpoints
- **GET `/hotels/`**: Retrieve a list of all hotels.
  - Response: List of hotels with `nom_hotel`, `marque`, `location_id`.
- **GET `/hotels/{location_id}`**: Retrieve details for a specific hotel by `location_id`.
  - Response: Hotel details or 404 if not found.
- **GET `/hotels/{location_id}/reviews`**: Fetch and store reviews for a hotel from TripAdvisor API.
  - Response: List of reviews for the specified `location_id`.
- **GET `/hotels/{location_id}/analysis`**: Perform AI-powered sentiment analysis on the last 5 reviews using OpenAI API.
  - Response: Sentiment analysis results (e.g., positive/negative sentiment, key themes) or 404 if no reviews exist.


## Notes
- **AI Usage**: The sentiment analysis endpoint (`/hotels/{location_id}/analysis`) requires a valid `OPENAI_API_KEY`. Ensure sufficient API credits for OpenAI usage.
- **API Limits**: The app fetches up to 5 reviews per hotel from TripAdvisor. Check API quota (~1900 calls for 380 hotels).
- **Rate Limits**: A 0.2-second delay in `populate_database.py` prevents 429 errors. Adjust if needed.
- **Database**: Uses SQLite (`hotels.db`). For production, consider PostgreSQL/MySQL by modifying `db_setup.py`.
- **Security**: Keep `.env` out of version control (add to `.gitignore`).
- **Logging**: The API logs startup events, errors, and info (e.g., new reviews added) for debugging.
- **Frontend**: CORS is configured for `http://localhost:4200`. Update `allow_origins` in `main.py` for other frontend URLs.

## Extending the App
- Implement data visualization in the frontend (e.g., charts for review ratings or sentiment trends).
- Add authentication to secure API endpoints.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.


