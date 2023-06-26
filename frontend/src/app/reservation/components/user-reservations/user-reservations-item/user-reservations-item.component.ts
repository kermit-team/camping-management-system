import { Component, Input, OnInit, SimpleChanges } from '@angular/core';
import {
  Car,
  Payment,
  PlotResponse,
  ReservationResponse,
} from 'src/app/reservation/reservation.models';
import { ReservationService } from 'src/app/reservation/reservation.service';
import { UserResponse } from 'src/app/shared/user.models';

@Component({
  selector: 'app-user-reservations-item',
  templateUrl: './user-reservations-item.component.html',
  styleUrls: ['./user-reservations-item.component.scss'],
})
export class UserReservationsItemComponent implements OnInit {
  constructor(private _reservationService: ReservationService) {}

  @Input() reservation: ReservationResponse = {
    id: 0,
    user: {} as UserResponse,
    car: {} as Car,
    camping_plot: {} as PlotResponse,
    payment: {} as Payment,
    date_from: '',
    date_to: '',
    number_of_adults: 0,
    number_of_children: 0,
    number_of_babies: 0,
  };
  canCancel: boolean = false;
  message: string = '';

  ngOnInit(): void {
    const targetDate = new Date(this.reservation.date_from);
    const currentDate = new Date();
    const minDate = new Date(targetDate.getTime());
    minDate.setDate(targetDate.getDate() - 7);

    if (currentDate.getTime() <= minDate.getTime()) {
      this.canCancel = true;
    } else {
      this.canCancel = false;
    }
  }

  cancelReservation() {
    this._reservationService.deleteReservation(this.reservation.id).subscribe(
      (res) => {
        this.message = 'Pomyślnie usunięto';
        window.location.reload();
      },
      (err) => {
        this.message = 'Błąd';
      }
    );
  }
}
