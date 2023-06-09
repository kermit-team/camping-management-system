import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ReservationService } from '../../reservation.service';
import { PlotResponse } from '../../reservation.models';
import { FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit{
  formData: any;
  allPlots: PlotResponse[]= [];
  minDate: Date;
  search: FormGroup;

  constructor(
    private _router: Router,
    private _reservationService: ReservationService
  ) {
    const state = this._router.getCurrentNavigation()?.extras.state;
    if (state && state['formData']) {
      this.formData = state['formData'];
    } else {
      this._router.navigate(['/']);
    }
    
    this.minDate = new Date();
    this.search = new FormGroup({
      start: new FormControl<Date>(this.formData.start),
      end: new FormControl<Date>(this.formData.end),
      adults: new FormControl(1),
      children: new FormControl(0),
    });
  }

  ngOnInit(): void {
    this._reservationService.getAllAvailablePlots().subscribe(
      res => {
        this.allPlots = res;
        console.log(this.allPlots)
      },
      err => {
        console.log(err);
      }
    )
  }
  onSubmit(){
    this.formData = this.search.value;
  }
}
