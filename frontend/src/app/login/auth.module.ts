import { ModuleWithProviders, NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { ForgotPasswordComponent } from "./components/forgot-password/forgot-password.component";
import { LoginComponent } from "./components/login/login.component";
import { RegisterComponent } from "./components/register/register.component";
import { AuthRoutingModule } from "./auth-routing.module";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { HTTP_INTERCEPTORS, HttpClientModule } from "@angular/common/http";
import { JwtModule } from "@auth0/angular-jwt";
import { AuthService } from "./auth.service";
import { AuthInterceptor, authInterceptorProviders } from "./auth.interceptor";

@NgModule({
    declarations: [
      
      LoginComponent,
      RegisterComponent,
      ForgotPasswordComponent
    ],
    imports: [
      BrowserModule,
      AuthRoutingModule,
      FormsModule,
      ReactiveFormsModule,
      HttpClientModule,
      JwtModule.forRoot({
        config: {
            tokenGetter: null!!
        }
    }),
    ],
    providers: [authInterceptorProviders]
  })
  export class AuthModule {
    public static forRoot(): ModuleWithProviders<AuthModule> {
        return {
            ngModule: AuthModule,
            providers: [AuthService]
        };
    }
}