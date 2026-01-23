# Hotel Reviews Frontend

This **Angular 19** frontend powers the Hotel Reviews API, providing a French-language interface for data analysis and AI-driven insights. It features **Power BI dashboards** for visualizing data analysis results (Colt, Webhelp, and Réservations) and an **AI-powered sentiment analysis** page using a **lightweight Retrieval-Augmented Generation (RAG)** approach to analyze hotel reviews. The frontend interacts with a FastAPI backend (at `http://localhost:8000`) to fetch hotel data and reviews. **All application content, including page names, buttons, and UI text, is in French**.

## Features
- **Power BI Dashboards**: Visualize data analysis results for Colt, Webhelp, and Réservations using embedded Power BI reports.
- **AI-Powered Sentiment Analysis with Lightweight RAG**: Retrieves the last 5 TripAdvisor reviews for a selected hotel and uses the OpenAI API to generate sentiment insights (e.g., positive/negative sentiment, key themes).
- French-language interface with a responsive sidebar for navigation.
- Hotel review management with a table-based UI and review details in a new window.

## Power BI Dashboards
The frontend includes three Power BI dashboards for data analysis:
- **Tableau de Bord Colt** (`/colt-dashboard`): Displays analytical results (e.g., business metrics) visualized with Power BI embedded reports.
- **Tableau de Bord Webhelp** (`/webhelp-dashboard`): Presents data analysis results (e.g., performance metrics) using Power BI.
- **Tableau de Bord Réservations** (`/reservation-dashboard`): Shows reservation-related analytics (e.g., booking trends) via Power BI.

These dashboards use Power BI’s embedded report functionality, requiring authentication or embed tokens configured in the frontend for secure access.

## AI-Powered Sentiment Analysis with Lightweight RAG
The **Avis sur les Hôtels** page (`/hotels`) displays a table of hotels. Clicking the “Voir Avis” button for a hotel opens a new window showing a table of the last 5 TripAdvisor reviews (fetched via the backend’s `/hotels/{location_id}/reviews` endpoint). A button in this window triggers **lightweight RAG-based sentiment analysis**:
- **Retrieval**: The frontend queries the backend to retrieve the last 5 reviews from the SQLite database.
- **Augmentation**: The retrieved review data (title, text, rating, etc.) is sent to the backend’s `/hotels/{location_id}/analysis` endpoint.
- **Generation**: The OpenAI API processes the reviews to generate insights, such as overall sentiment, guest satisfaction trends, or key feedback themes.

This lightweight RAG approach combines database retrieval with OpenAI’s generative capabilities, avoiding complex vector stores or embeddings.

## Pages (in French)
- **Accueil**: The application’s homepage.
- **KPI Overflow** (`/kpi-overflow`): Displays descriptions of Key Performance Indicators (KPIs) and explanations of abbreviations used in the dashboards.
- **Tableau de Bord Colt** (`/colt-dashboard`): Power BI dashboard for Colt data analysis.
- **Tableau de Bord Webhelp** (`/webhelp-dashboard`): Power BI dashboard for Webhelp data analysis.
- **Tableau de Bord Réservations** (`/reservation-dashboard`): Power BI dashboard for reservation data analysis.
- **Avis sur les Hôtels** (`/hotels`): Lists hotels in a table; “Voir Avis” opens a new window with 5 reviews and a button for RAG-based sentiment analysis.

## Project Structure
```
hotel-reviews-frontend/
├── src/
│   ├── app/
│   │   ├── components/      # Angular components for pages and features
│   │   ├── layouts/         # Layout components (e.g., sidebar, header)
│   │   ├── models/          # TypeScript interfaces and models
│   │   ├── pipe/            # Custom Angular pipes
│   │   ├── services/        # Services for API calls and Power BI integration
│   │   ├── assets/          # Static assets (e.g., images, Solar icons)
│   │   ├── main.ts          # Angular bootstrap file
│   │   ├── app.routes.ts    # Application routing configuration
├── node_modules/            # Node dependencies (ignored in .gitignore)
├── angular.json             # Angular configuration
├── package.json             # Frontend dependencies
├── .gitignore               # Git ignore file
└── README.md                # Documentation
```

## Setup

### Prerequisites
- **Node.js** 18+ (compatible with Angular 19)
- **Angular CLI** 19.x (`npm install -g @angular/cli@19`)
- **Backend**: A running FastAPI backend at `http://localhost:8000` (see backend repository for setup).
- **Power BI**: Embed tokens or authentication for Power BI dashboards.

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/medamineharbaoui/Data_Analysis_and_AI-Reviews_frontend.git
   cd Data_Analysis_and_AI-Reviews_frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Configure Power BI**:
   - Add Power BI embed tokens or authentication details in a service (e.g., `src/app/services/powerbi.service.ts`).
   - Ensure your Power BI workspace is accessible and reports are configured for embedding.

4. **Run the Development Server**:
   ```bash
   npm start
   ```
   - Access the frontend at `http://localhost:4200`.
   - Ensure the backend is running for API connectivity.

## Usage
1. Start the backend server
( here is the backend repository link: https://github.com/medamineharbaoui/Data_Analysis_and-AI-Reviews_backend.git ).
2. Run the frontend:
   ```bash
   npm start
   ```
3. Open `http://localhost:4200` in your browser.
4. Navigate to **Avis sur les Hôtels** (`/hotels`), click “Voir Avis” for a hotel, and use the sentiment analysis button to generate RAG-based insights.
5. Access **Tableau de Bord Colt**, **Webhelp**, or **Réservations** to view Power BI dashboards.

### Example Workflow
- Go to `http://localhost:4200/hotels`.
- Click “Voir Avis” for a hotel.
- In the new window, view the 5 latest reviews and click the analysis button to see RAG-based sentiment insights.
- Visit `/colt-dashboard`, `/webhelp-dashboard`, or `/reservation-dashboard` to explore Power BI visualizations.

## Notes
- **Language**: All frontend content (page names, buttons like “Voir Avis,” labels) is in French.
- **Backend Dependency**: Requires the FastAPI backend at `http://localhost:8000` for hotel data, reviews, and RAG-based sentiment analysis.
- **Power BI**: Dashboards require Power BI embed tokens or authentication. Ensure reports are configured in your Power BI workspace.
- **Icons**: Uses Solar icons (e.g., `solar:star-line-duotone`). Install `@iconify/angular` for rendering.
- **CORS**: Backend is configured for `http://localhost:4200`. Update `allow_origins` in the backend if using a different frontend URL.
- **Security**: Store API keys in the backend’s `.env`.

## Extending the App
- Add Chart.js visualizations for review ratings or sentiment trends in **Avis sur les Hôtels**.
- Add authentication for secure access to dashboards and analysis.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.



