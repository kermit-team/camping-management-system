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

  getAllAvailablePlots(date_from: string, date_to: string): Observable<PlotResponse[]>{
    return this._http.post<PlotResponse[]>(`${environment.baseUrl}${ApiPaths.GetAvailablePlots}`,{date_from,date_to});
  }
}
