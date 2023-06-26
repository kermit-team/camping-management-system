import { Component } from '@angular/core';
import { Route, Router } from '@angular/router';
import { UserResponse } from 'src/app/shared/user.models';
import { UserService } from 'src/app/shared/user.service';
import { ReservationService } from '../../reservation.service';

@Component({
  selector: 'app-reservation-summary',
  templateUrl: './reservation-summary.component.html',
  styleUrls: ['./reservation-summary.component.scss'],
})
export class ReservationSummaryComponent {
  summary: any;
  user: UserResponse;
  isUserValid: boolean = false;
  selectedCar: number | null = null;

  constructor(
    private _router: Router,
    private _userService: UserService,
    private _reservationService: ReservationService
  ) {
    this.user = {
      email: '',
      first_name: '',
      last_name: '',
      phone_number: 0,
      avatar: '',
      id_card: '',
      cars: [],
      groups: [],
    };
    const state = this._router.getCurrentNavigation()?.extras.state;
    if (state) {
      this.summary = state['formData'];
    } else {
      this._router.navigate(['/']);
    }
    const id: number | null = this._userService.getUserId();
    if (id) {
      this._userService.getUser(id).subscribe(
        (res) => {
          this.user = res;
          if (this.user.id_card && this.user.phone_number) {
            this.isUserValid = true;
          } else {
            this.isUserValid = false;
          }
        },
        (err) => {
          console.log(err);
        }
      );
    } else {
      console.log('brak usera');
    }
  }

  setSelectedCar(id: number) {
    if (this.user.cars) {
      this.selectedCar = id;
    }
  }

  createReservation() {
    if (this.isUserValid && this.selectedCar) {
      const parts = this.summary.date_from.split('.');
      const dateFrom = `${parts[2]}-${parts[1]}-${parts[0]}`;
      const parts2 = this.summary.date_to.split('.');
      const dateTo = `${parts2[2]}-${parts2[1]}-${parts2[0]}`;
      const formData = {
        date_from: dateFrom,
        date_to: dateTo,
        number_of_adults: this.summary.number_of_adults,
        number_of_children: this.summary.number_of_children,
        number_of_babies: this.summary.number_of_babies,
        car: this.selectedCar,
        camping_plot: this.summary.camping_plot.id,
      };
      this._reservationService.createReservation(formData).subscribe(
        res => {
            window.location.href = res.checkout_url
        },
        err => {
          console.error(err);
        }
      )
    }
  }
}
