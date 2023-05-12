import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { AuthHttpService } from './auth-http.service';
import { LoginResponse } from './auth.models';
import { Observable, tap } from 'rxjs';

const TOKEN_KEY = 'access';
const REFRESH_KEY = 'refresh';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private _jwtHelperService: JwtHelperService,
    private _authHttpService: AuthHttpService
  ) {}

  login(email: string, password: string): Observable<LoginResponse> {
    return this._authHttpService.login(email, password).pipe(
      tap(
        response => {
          this.saveToken(response);
        }
      )
    )
  }

  register(email:string, password: string, first_name:string, last_name:string){
    return this._authHttpService.register(email,password,first_name,last_name);
  }


  signOut(): void {
    window.sessionStorage.clear();
  }
  public saveToken(token: LoginResponse): void {
    window.sessionStorage.setItem(TOKEN_KEY, token.access);
    window.sessionStorage.setItem(REFRESH_KEY, token.refresh);
  }


  
  public getToken(): string | null {
    return window.sessionStorage.getItem(TOKEN_KEY);
  }
 
  public getUser(): any {
    const user = window.sessionStorage.getItem(TOKEN_KEY);
    if (user) {
      console.log(this._jwtHelperService.decodeToken(user));
      return this._jwtHelperService.decodeToken(user);
    }

    return {};
  }
}
