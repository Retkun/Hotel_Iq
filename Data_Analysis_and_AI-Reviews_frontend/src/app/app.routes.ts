import { Routes } from '@angular/router';
import { FullComponent } from './layouts/full/full.component';
import { HotelsComponent } from './components/hotels/hotels.component';
import { ReviewsComponent } from './components/reviews/reviews.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ColtDashboardComponent } from './components/colt-dashboard/colt-dashboard.component';
import { WebhelpDashboardComponent } from './components/webhelp-dashboard/webhelp-dashboard.component';
import { ReservationDashboardComponent } from './components/reservation-dashboard/reservation-dashboard.component';

export const routes: Routes = [
  {
    path: '',
    component: FullComponent,
    children: [
      {
        path: '',
        redirectTo: 'kpi-overflow',
        pathMatch: 'full',
      },
      {
        path: 'hotels',
        component: HotelsComponent,
      },
      {
        path: 'reviews/:locationId',
        component: ReviewsComponent,
      },
      {
        path: 'kpi-overflow',
        component: DashboardComponent,
      },
      {
        path: 'colt-dashboard',
        component: ColtDashboardComponent,
      },
      {
        path: 'webhelp-dashboard',
        component: WebhelpDashboardComponent,
      },
      {
        path: 'reservation-dashboard',
        component: ReservationDashboardComponent,
      },
      {
        path: '**',
        redirectTo: 'kpi-overflow',
      },
    ],
  }
];
