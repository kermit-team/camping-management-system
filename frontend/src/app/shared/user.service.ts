import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { FullUserResponse, Groups, UserResponse } from './user.models';
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

  getAllUsers(): Observable<FullUserResponse[]> {
    return this._http
      .get<FullUserResponse[]>(`${environment.baseUrl}${ApiPaths.GetAllUsers}`);
  }

  getAllGroups(): Observable<Groups[]>{
    return this._http
      .get<Groups[]>(`${environment.baseUrl}${ApiPaths.GetAllGroups}`);
  }

  getUser(id: number): Observable<UserResponse> {
    return this._http.get<UserResponse>(`${environment.baseUrl}${ApiPaths.GetUpdateUser}${id}`).pipe(
      map(response => ({
        email: response.email,
        first_name: response.first_name,
        last_name: response.last_name,
        phone_number: response.phone_number,
        avatar: response.avatar,
        id_card: response.id_card,
        cars: response.cars,
        groups: response.groups
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
        cars: response.cars,
        groups: response.groups
      }))
    );
  }

  updateFullUser(id: number,changed: any): Observable<FullUserResponse>{
    return this._http.patch<FullUserResponse>(`${environment.baseUrl}${ApiPaths.GetUpdateUser}${id}/`,changed).pipe(
      map(response => ({
        email: response.email,
        first_name: response.first_name,
        last_name: response.last_name,
        phone_number: response.phone_number,
        avatar: response.avatar,
        id_card: response.id_card,
        cars: response.cars,
        groups: response.groups,
        id: response.id
      }))
    )
  }

  deleteUser(id: number): Observable<void> {
  return this._http.delete<void>(`${environment.baseUrl}${ApiPaths.DeleteUser}${id}`);
}

  isUserExpired(){
    const user = window.sessionStorage.getItem(TOKEN_KEY);
    if(this._jwtHelperService.isTokenExpired(user)){
      this.signOut();
      return true;
    }
    return false;
  }

  addUserCar(registration_plate: string){
    return this._http.post<any>(`${environment.baseUrl}${ApiPaths.CreateCar}`,{registration_plate}).pipe(
      map(response => ({
        email: response.drivers[0].email,
        first_name: response.drivers[0].first_name,
        last_name: response.drivers[0].last_name,
        phone_number: response.drivers[0].phone_number,
        avatar: response.drivers[0].avatar,
        id_card: response.drivers[0].id_card,
        cars: response.drivers[0].cars,
        groups: response.drivers[0].groups
      }))
    );
    }


}
