import { Component, Input, SimpleChanges } from '@angular/core';
import { PlotResponse } from '../../reservation.models';

@Component({
  selector: 'app-plot',
  templateUrl: './plot.component.html',
  styleUrls: ['./plot.component.scss']
})
export class PlotComponent {
  startDate: string ='';
  endDate: string ='';
  numberOfDays: number = 0;
  price: number = 0;
  @Input() plot: PlotResponse = {
    id: 0,
    position: 0,
    camping_section: {id:0,name:"",price_per_adult:"",price_per_child:'',plot_price:''}
  };
  @Input() info: any = {};

  ngOnChanges(changes: SimpleChanges): void {
    if (this.info && this.info.start) {
      this.startDate = `${this.info.start.getDate().toString().padStart(2, '0')}.${(this.info.start.getMonth()+1).toString().padStart(2, '0')}.${this.info.start.getFullYear()}`;
      this.endDate = `${this.info.end.getDate().toString().padStart(2, '0')}.${(this.info.end.getMonth()+1).toString().padStart(2, '0')}.${this.info.end.getFullYear()}`;
      this.numberOfDays = Math.ceil(Math.abs(this.info.end.getTime() - this.info.start.getTime()) / (1000 * 3600 * 24));
      this.price = parseFloat(this.plot.camping_section.plot_price) + this.info.adults*parseFloat(this.plot.camping_section.price_per_adult)*this.numberOfDays + this.info.children*parseFloat(this.plot.camping_section.price_per_child)*this.numberOfDays;
    }
  }

}
