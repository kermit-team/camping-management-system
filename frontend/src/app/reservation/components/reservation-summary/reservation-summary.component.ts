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
      cars: []
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
          
        },
        err => {
          console.log(err);
          
        }
      )
    }
    else {
      console.log("brak usera")
    }  
    if(this.user.id_card || this.user.phone_number || this.user.cars){
      this.isUserValid = true
    }
    else {
      this.isUserValid = false;
    }
    
  }

  setSelectedCar(id: number){
    if(this.user.cars){
       this.selectedCar = id;
    }
  }

  createReservation(){
    
  }
}
