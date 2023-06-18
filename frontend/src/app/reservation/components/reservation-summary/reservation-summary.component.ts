import { Component } from '@angular/core';
import { Route, Router } from '@angular/router';
import { UserResponse } from 'src/app/shared/user.models';
import { UserService } from 'src/app/shared/user.service';

@Component({
  selector: 'app-reservation-summary',
  templateUrl: './reservation-summary.component.html',
  styleUrls: ['./reservation-summary.component.scss']
})
export class ReservationSummaryComponent {
  summary: any;
  user: UserResponse;
  isUserValid: boolean = false;
  selectedCar: number | null = null;

  constructor(private _router: Router, private _userService: UserService){
    this.user = {
      email: '',
      first_name: '',
      last_name: '',
      phone_number: 0,
      avatar: '',
      id_card: '',
      cars: [],
      groups: []
    }
    const state = this._router.getCurrentNavigation()?.extras.state;
    if (state) {
      this.summary = state['formData'];
      console.log(this.summary)
    } else {
      this._router.navigate(['/']);
    }
    const id: number | null = this._userService.getUserId();
    if(id){
      this._userService.getUser(id).subscribe(
        res => {
          this.user = res;
          if(this.user.id_card && this.user.phone_number){
            this.isUserValid = true
          }
          else {
            this.isUserValid = false;
          }
        },
        err => {
          console.log(err);
          
        }
      )
    }
    else {
      console.log("brak usera")
    }  
   
    
  }

  setSelectedCar(id: number){
    if(this.user.cars){
       this.selectedCar = id;
    }
  }

  createReservation(){
    let toLocaleEnd = this.summary.date_to.toLocaleDateString('en-US', { timeZone: 'Europe/Warsaw', dateStyle: 'short' }).split('/');
    let formattedEnd = "20" + toLocaleEnd[2] + "-" + toLocaleEnd[0].toString().padStart(2, '0') + "-" + toLocaleEnd[1].toString().padStart(2, '0');
    let toLocaleStart = this.summary.date_from.toLocaleDateString('en-US', { timeZone: 'Europe/Warsaw', dateStyle: 'short' }).split('/');
    let formattedStart = "20" + toLocaleStart[2] + "-" + toLocaleStart[0].toString().padStart(2, '0') + "-" + toLocaleStart[1].toString().padStart(2, '0');

  }
}
