import { Component, OnInit } from '@angular/core';
import { ReservationService } from '../../reservation.service';
import { UserService } from 'src/app/shared/user.service';
import { ReservationResponse } from '../../reservation.models';

@Component({
  selector: 'app-user-reservations',
  templateUrl: './user-reservations.component.html',
  styleUrls: ['./user-reservations.component.scss']
})
export class UserReservationsComponent implements OnInit{

  reservations: ReservationResponse[] = [];
  constructor(private _reservationService: ReservationService, private _userService: UserService) {
  }

  ngOnInit(): void {
    const id = this._userService.getUserId();
    if(id){
      this._reservationService.getUserReservations(id).subscribe(
        res => {
          this.reservations = res;
          console.log(this.reservations)
        },
        err => {
          console.error(err);
        }
      )
    }
    
  }
}
