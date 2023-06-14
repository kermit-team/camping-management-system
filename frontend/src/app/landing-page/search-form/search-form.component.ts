import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { NavigationExtras, Router } from '@angular/router';
export const MY_FORMATS = {
  parse: {
    dateInput: 'LL',
  },
  display: {
    dateInput: 'LL',
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  },
};

@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss']
})
export class SearchFormComponent {
  minDate: Date;
  tomorrow: Date;
  now = new Date();
  search = new FormGroup({
    start: new FormControl<Date>(new Date()),
    end: new FormControl<Date>(new Date(this.now.getFullYear(), this.now.getMonth(), this.now.getDate() + 1)),
    adults: new FormControl(1),
    children: new FormControl(0),
  });
  constructor(private _router: Router){
    const now = new Date();
    this.minDate = now;
    this.tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1)
  }
  onSubmit(){

    const queryParams = { formData: JSON.stringify(this.search.value) };
    this._router.navigate(['/searchresults'], { state: { formData: this.search.value } });


    // const { start, end, adults, children } = this.search.value;
    // console.log(this.search.value)
    //const startWithoutTime = new Date(start).setHours(0, 0, 0, 0);
    // const endWithoutTime = new Date(end).setHours(0, 0, 0, 0);

    // const queryParams = {
    //   start: startWithoutTime,
    //   end: endWithoutTime,
    //   adults,
    //   children,
    // };

    // const navigationExtras: NavigationExtras = {
    //   queryParams,
    // };

    // Navigate to the next component with the query parameters in the URL
    //this._router.navigate(['/searchresults'], navigationExtras);
  }
}

