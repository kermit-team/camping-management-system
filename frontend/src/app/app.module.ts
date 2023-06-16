import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { LandingPageComponent } from './landing-page/landing-page.component';
import { SearchFormComponent } from './landing-page/search-form/search-form.component';
import { NavbarComponent } from './landing-page/navbar/navbar.component';
import { InstagramPostsComponent } from './landing-page/instagram-posts/instagram-posts.component';
import { UserLoginStateComponent } from './landing-page/navbar/user-login-state/user-login-state.component';
import { CarouselComponent } from './landing-page/carousel/carousel.component';
import { ContactFormComponent } from './landing-page/contact-form/contact-form.component';
import { FooterComponent } from './landing-page/footer/footer.component';
import { AuthModule } from './login/auth.module';
import { ProfileComponent } from './profile/profile.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import {MatNativeDateModule} from '@angular/material/core';
import { SearchComponent } from './reservation/components/search/search.component';
import { MAT_DATE_LOCALE } from '@angular/material/core'
import { ReservationModule } from './reservation/reservation.module';
import { SharedModule } from './shared/shared.module';
import { CarComponent } from './profile/car/car.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';


@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    SearchFormComponent,
    NavbarComponent,
    InstagramPostsComponent,
    UserLoginStateComponent,
    CarouselComponent,
    ContactFormComponent,
    FooterComponent,
    ProfileComponent,
    CarComponent,
    AdminPanelComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AuthModule,
    ReservationModule,
    ReactiveFormsModule,
    FormsModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    MatNativeDateModule,
    SharedModule
  ],
  providers: [{provide: MAT_DATE_LOCALE, useValue: 'pl'}],
  bootstrap: [AppComponent],
  exports: []
})
export class AppModule { }
