import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReservationRoutingModule } from './reservation-routing.module';
import { PlotComponent } from './components/plot/plot.component';
import { SearchComponent } from './components/search/search.component';

import { SharedModule } from '../shared/shared.module';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ReservationSummaryComponent } from './components/reservation-summary/reservation-summary.component';
import { UserReservationsComponent } from './components/user-reservations/user-reservations.component';
import { UserReservationsItemComponent } from './components/user-reservations/user-reservations-item/user-reservations-item.component';



@NgModule({
  declarations: [
    PlotComponent,
    SearchComponent,
    ReservationSummaryComponent,
    UserReservationsComponent,
    UserReservationsItemComponent
  ],
  imports: [
    CommonModule,
    ReservationRoutingModule,
    SharedModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    MatNativeDateModule,
    FormsModule,
    ReactiveFormsModule,
  ]
})
export class ReservationModule { }
