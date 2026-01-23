export interface Review {
  id: number;
  location_id: number;
  review_id: number;
  published_date: string;
  rating: number;
  text: string;
  title: string;
  trip_type: string | null;
  travel_date: string | null;
  helpful_votes: number;
  username: string;
  url: string;
}