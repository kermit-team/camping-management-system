import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';


@Component({
  selector: 'app-search-form',
  templateUrl: './search-form.component.html',
  styleUrls: ['./search-form.component.scss']
})
export class SearchFormComponent {
  range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null),
  });
  // tomorrow: string;
  // firstDate: string='';
  // secondDate: string='';
  // minSecondDate: string='';
  // maxFirstDate:string='';
  // constructor(){
  //   const now = new Date();
  //   this.firstDate = now.toISOString().substring(0, 10);
  //   now.setDate(now.getDate() + 1);
  //   this.tomorrow = now.toISOString().substring(0, 10);
    
  // }
  // updateSecondDate() {
  //   this.minSecondDate = this.firstDate;
  // }
}

