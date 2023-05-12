import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginResponse } from './auth.models';
import { environment, ApiPaths } from 'src/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthHttpService {
  constructor(private _http: HttpClient) {}

  login(email: string, password: string): Observable<LoginResponse> {
    return this._http.post<LoginResponse>(
      `${environment.baseUrl}${ApiPaths.Auth}`,
      { email, password }
    );
  }
  register(
    email: string,
    password: string,
    first_name: string,
    last_name: string
  ): Observable<any> {
    return this._http.post(`${environment.baseUrl}${ApiPaths.Register}`, {
      email,
      password,
      first_name,
      last_name,
    });
  }
  emailConfirmation(id: string, token: string): Observable<any>{
    return this._http.get(`${environment.baseUrl}${ApiPaths.EmailConfirmation}${id}/${token}`);
  }
  resetPassword(email: string): Observable<any>{
    return this._http.post(`${environment.baseUrl}${ApiPaths.ResetPassword}`,{email}) 
  }
  confirmResetPassword(id: string, token: string, password: string): Observable<any>{
    return this._http.post(`${environment.baseUrl}${ApiPaths.ConfirmResetPassword}${id}/${token}`,{password})
  }
}
