import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
    selector: 'app-root',
    standalone: true, // Explicitly adding this for clarity (optional, since it's implied)
    imports: [RouterOutlet],
    templateUrl: './app.component.html'
})
export class AppComponent {
  title = 'Analytics Dashboard';
}