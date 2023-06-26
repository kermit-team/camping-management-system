import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.scss']
})
export class CarComponent implements OnInit,OnChanges{

  @Input() carId: number = 0;
  //Mode for displaying (0) and deleting (1)
  @Input() mode: number = 0;
  @Output() carDeleted: EventEmitter<number> = new EventEmitter<number>()
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

  deleteCar(){
    this._htpp.delete<any>(`http://localhost:8000/api/cars/${this.carId}/`).subscribe(
      res => {
        this.carDeleted.emit(this.carId);
      },
      err => {
        console.log(err);
      }
    )
  }
}
