import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { UserResponse } from './user.models';
import { Observable, map } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { ApiPaths, environment } from 'src/environment';

const TOKEN_KEY = 'access';
const REFRESH_KEY = 'refresh';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private _jwtHelperService: JwtHelperService,private _http: HttpClient) { }



  getUser(id: number): Observable<UserResponse> {
    return this._http.get<UserResponse>(`${environment.baseUrl}${ApiPaths.GetUpdateUser}${id}`).pipe(
      map(response => ({
        email: response.email,
        first_name: response.first_name,
        last_name: response.last_name,
        phone_number: response.phone_number,
        avatar: response.avatar,
        id_card: response.id_card,
        cars: response.cars
      }))
    );
  }

  getUserId(): number | null{
    const user = window.sessionStorage.getItem(TOKEN_KEY);
    if(user){
      return this._jwtHelperService.decodeToken(user).user_id;
    }
    return null;
  }
  signOut(): void {
    window.sessionStorage.clear();
  }

  updateUser(id: number,changed: any): Observable<UserResponse>{
    return this._http.patch<UserResponse>(`${environment.baseUrl}${ApiPaths.GetUpdateUser}${id}/`,changed).pipe(
      map(response => ({
        email: response.email,
        first_name: response.first_name,
        last_name: response.last_name,
        phone_number: response.phone_number,
        avatar: response.avatar,
        id_card: response.id_card,
        cars: response.cars
      }))
    );
  }

}
