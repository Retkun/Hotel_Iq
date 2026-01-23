import { Component } from '@angular/core';
import { MaterialModule } from '../../material.module';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [MaterialModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {

}
