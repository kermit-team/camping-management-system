import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PlotResponse } from './reservation.models';
import { Observable } from 'rxjs';
import { ApiPaths, environment } from 'src/environment';

@Injectable({
  providedIn: 'root'
})
export class ReservationService {

  constructor(private _http: HttpClient) { }

  getAllAvailablePlots(): Observable<PlotResponse[]>{
    return this._http.get<PlotResponse[]>(`${environment.baseUrl}${ApiPaths.GetPlots}`);
  }
}
