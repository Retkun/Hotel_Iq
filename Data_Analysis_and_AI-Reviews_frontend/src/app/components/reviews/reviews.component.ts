import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from '../../material.module';
import { HotelService } from '../../services/hotel.service';
import { Review } from '../../models/review';
import { Hotel } from '../../models/hotel';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RouterModule } from '@angular/router';
import { NewlineToBrPipe } from '../../pipe/newline-to-br.pipe';
import { MarkdownPipe } from '../../pipe/markdown.pipe';

export interface ReviewAnalysis {
  nom_hotel: string;
  marque: string;
  note_globale: string;
  analyse_des_sentiments: string;
  insights: string;
  conclusion: string;
}

@Component({
  selector: 'app-reviews',
  templateUrl: './reviews.component.html',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule, 
    RouterModule,
   // NewlineToBrPipe,
    MarkdownPipe
  ]
})
export class ReviewsComponent implements OnInit {
  @Input() locationId!: number;
  reviews: Review[] = [];
  hotel: Hotel | null = null;
  isLoading: boolean = false;
  errorMessage: string | null = null;
  displayedColumns: string[] = ['titre', 'note', 'commentaire', 'date_publication', 'type_voyage', 'lien'];
  showFullText: number | null = null;
  analysis: ReviewAnalysis | null = null;
  isAnalysisLoading: boolean = false;

  constructor(
    private hotelService: HotelService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.reviews = [];
    if (this.locationId) {
      this.loadHotel();
      this.loadReviews();
    } else {
      this.errorMessage = 'Aucun identifiant d\'hôtel fourni';
      this.showSnackBar(this.errorMessage, true);
    }
  }

  loadHotel(): void {
    this.isLoading = true;
    this.hotelService.getHotelById(this.locationId).subscribe({
      next: (hotel) => {
        console.log('Hôtel reçu:', hotel);
        this.hotel = hotel;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Erreur lors du chargement de l\'hôtel:', err);
        this.isLoading = false;
        this.errorMessage = 'Échec du chargement de l\'hôtel: ' + (err.message || 'Erreur inconnue');
        this.showSnackBar(this.errorMessage, true);
      }
    });
  }

  loadReviews(): void {
    this.isLoading = true;
    this.errorMessage = null;
    this.hotelService.getReviews(this.locationId).subscribe({
      next: (reviews) => {
        console.log('Avis reçus:', reviews);
        this.reviews = reviews || [];
        this.isLoading = false;
        if (this.reviews.length === 0) {
          this.showSnackBar('Aucun avis trouvé pour cet hôtel', false);
        }
      },
      error: (err) => {
        console.error('Erreur lors du chargement des avis:', err);
        this.reviews = [];
        this.isLoading = false;
        this.errorMessage = 'Échec du chargement des avis: ' + (err.message || 'Erreur inconnue');
        this.showSnackBar(this.errorMessage, true);
      }
    });
  }

  loadAnalysis(): void {
    this.isAnalysisLoading = true;
    this.errorMessage = null;
    this.hotelService.getHotelAnalysis(this.locationId).subscribe({
      next: (analysis) => {
        console.log('Analyse reçue:', analysis);
        this.analysis = analysis;
        this.isAnalysisLoading = false;
        this.showSnackBar('Analyse générée avec succès', false);
      },
      error: (err) => {
        console.error('Erreur lors du chargement de l\'analyse:', err);
        this.isAnalysisLoading = false;
        this.errorMessage = 'Échec du chargement de l\'analyse: ' + (err.message || 'Erreur inconnue');
        this.showSnackBar(this.errorMessage, true);
      }
    });
  }

  toggleFullText(reviewId: number): void {
    this.showFullText = this.showFullText === reviewId ? null : reviewId;
  }

  private showSnackBar(errorOrMessage: any, isError = false): void {
    const message =
      errorOrMessage?.error?.error && typeof errorOrMessage.error.error === 'string'
        ? errorOrMessage.error.error
        : typeof errorOrMessage === 'string'
          ? errorOrMessage
          : 'Une erreur inattendue s\'est produite.';

    this.snackBar.open(message, 'Fermer', {
      duration: 3000,
      panelClass: isError ? 'snackbar-error' : 'snackbar-success'
    });
  }
}