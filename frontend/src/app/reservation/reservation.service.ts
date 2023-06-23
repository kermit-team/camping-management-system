import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { PlotResponse, ReservationCreateResponse, ReservationResponse } from './reservation.models';
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
  createReservation(reservation_data: any): Observable<ReservationCreateResponse>{
    return this._http.post<ReservationCreateResponse>(`${environment.baseUrl}${ApiPaths.Reservations}`,reservation_data)
  }
  getUserReservations(user_id: number): Observable<ReservationResponse[]>{
    const bodyString = JSON.stringify(user_id);
    const params = new HttpParams().set('user_id',bodyString);
    return this._http.get<ReservationResponse[]>(`${environment.baseUrl}${ApiPaths.Reservations}`,{params});
  }
}
