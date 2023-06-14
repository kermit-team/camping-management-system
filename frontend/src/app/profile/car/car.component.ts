import { HttpClient } from '@angular/common/http';
import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.scss']
})
export class CarComponent implements OnInit,OnChanges{

  @Input() carId: number = 0;
  registration: string = '';
  constructor(private _htpp: HttpClient){}

  ngOnInit(): void {
    this._htpp.get<any>(`http://localhost:8000/api/cars/${this.carId}`).subscribe(
      res => {
        this.registration = res.registration_plate;
      }
    )
  }

  ngOnChanges(changes: SimpleChanges): void {
    
  }
}
