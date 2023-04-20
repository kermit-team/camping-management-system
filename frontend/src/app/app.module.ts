import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './login/register/register.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { SearchFormComponent } from './landing-page/search-form/search-form.component';
import { NavbarComponent } from './landing-page/navbar/navbar.component';
import { InstagramPostsComponent } from './landing-page/instagram-posts/instagram-posts.component';
import { UserLoginStateComponent } from './landing-page/navbar/user-login-state/user-login-state.component';
import { CarouselComponent } from './landing-page/carousel/carousel.component';
import { ContactFormComponent } from './landing-page/contact-form/contact-form.component';
import { FooterComponent } from './landing-page/footer/footer.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    LandingPageComponent,
    SearchFormComponent,
    NavbarComponent,
    InstagramPostsComponent,
    UserLoginStateComponent,
    CarouselComponent,
    ContactFormComponent,
    FooterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
