import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MaterialModule } from '../../material.module';
import { HotelService } from '../../services/hotel.service';
import { Hotel } from '../../models/hotel';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-hotels',
  templateUrl: './hotels.component.html',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule,
    RouterModule
  ]
})
export class HotelsComponent implements OnInit {
  hotels: Hotel[] = [];
  dataSource: MatTableDataSource<Hotel> = new MatTableDataSource<Hotel>([]);
  searchTerm: string = '';
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private hotelService: HotelService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.loadHotels();
  }

  loadHotels(): void {
    this.hotelService.getHotels().subscribe({
      next: (hotels) => {
        this.hotels = hotels;
        this.dataSource = new MatTableDataSource<Hotel>(hotels);
        this.dataSource.paginator = this.paginator; // Connect paginator to dataSource
        this.filterHotels();
      },
      error: (err) => this.showSnackBar(err, true),
    });
  }

  filterHotels(): void {
    const filterValue = this.searchTerm.trim().toLowerCase();
    this.dataSource.filter = filterValue;
    this.dataSource.filterPredicate = (data: Hotel, filter: string) => {
      return data.nom_hotel.toLowerCase().includes(filter);
    };
  }

  viewAvis(locationId: number): void {
    window.open(`/reviews/${locationId}`, '_blank');
  }

  private showSnackBar(errorOrMessage: any, isError = false): void {
    const message =
      errorOrMessage?.error?.error && typeof errorOrMessage.error.error === 'string'
        ? errorOrMessage.error.error
        : typeof errorOrMessage === 'string'
          ? errorOrMessage
          : 'An unexpected error occurred.';

    this.snackBar.open(message, 'Close', {
      duration: 3000,
      panelClass: isError ? 'snackbar-error' : 'snackbar-success'
    });
  }
}