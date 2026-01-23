import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Hotel } from '../models/hotel';
import { Review } from '../models/review';
import { ReviewAnalysis } from '../components/reviews/reviews.component';

@Injectable({
  providedIn: 'root'
})
export class HotelService {
  private baseUrl = 'http://localhost:8000/hotels';

  constructor(private http: HttpClient) { }

  getHotels(): Observable<Hotel[]> {
    return this.http.get<Hotel[]>(`${this.baseUrl}/`);
  }

  getHotelById(locationId: number): Observable<Hotel> {
    return this.http.get<Hotel>(`${this.baseUrl}/${locationId}`);
  }

  getReviews(locationId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.baseUrl}/${locationId}/reviews`);
  }

  getHotelAnalysis(locationId: number): Observable<ReviewAnalysis> {
    return this.http.get<ReviewAnalysis>(`${this.baseUrl}/${locationId}/analysis`);
  }
}