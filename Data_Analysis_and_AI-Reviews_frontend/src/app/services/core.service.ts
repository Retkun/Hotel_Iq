import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AppSettings, defaults } from '../config';





@Injectable({
  providedIn: 'root',
})
export class CoreService {
  private optionsSignal = signal<AppSettings>(defaults);


  constructor(private http: HttpClient) {}

  getOptions() {
    return this.optionsSignal();
  }

  setOptions(options: Partial<AppSettings>) {
    this.optionsSignal.update((current) => ({
      ...current,
      ...options,
    }));
  }



}
