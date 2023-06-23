import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SearchComponent } from './components/search/search.component';
import { ReservationSummaryComponent } from './components/reservation-summary/reservation-summary.component';
import { UserReservationsComponent } from './components/user-reservations/user-reservations.component';


const routes: Routes = [
{ path: 'searchresults', component: SearchComponent},
{ path: 'reservationsummary', component: ReservationSummaryComponent},
{ path: 'reservations', component: UserReservationsComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ReservationRoutingModule { }
