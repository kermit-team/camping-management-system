import {
  Component,
  EventEmitter,
  Input,
  Output,
  SimpleChanges,
} from '@angular/core';
import { PlotResponse } from '../../reservation.models';
import { UserService } from 'src/app/shared/user.service';
import { UserResponse } from 'src/app/shared/user.models';
import { Router } from '@angular/router';

@Component({
  selector: 'app-plot',
  templateUrl: './plot.component.html',
  styleUrls: ['./plot.component.scss'],
})
export class PlotComponent {
  startDate: string = '';
  endDate: string = '';
  numberOfDays: number = 0;
  price: number = 0;
  isSumOfPeopleRight: boolean = true;
  carOrIdError: boolean = true;
  multipleCars: boolean = false;

  constructor(private _userService: UserService, private _router: Router) {}

  @Output() dataEvent = new EventEmitter<string>();

  @Input() plot: PlotResponse = {
    id: 0,
    position: 0,
    camping_section: {
      id: 0,
      name: '',
      price_per_adult: '',
      price_per_child: '',
      plot_price: '',
    },
  };
  @Input() info: any = {};

  ngOnChanges(changes: SimpleChanges): void {
    if (this.info && this.info.start) {
      this.startDate = `${this.info.start
        .getDate()
        .toString()
        .padStart(2, '0')}.${(this.info.start.getMonth() + 1)
        .toString()
        .padStart(2, '0')}.${this.info.start.getFullYear()}`;
      this.endDate = `${this.info.end.getDate().toString().padStart(2, '0')}.${(
        this.info.end.getMonth() + 1
      )
        .toString()
        .padStart(2, '0')}.${this.info.end.getFullYear()}`;
      this.numberOfDays = Math.ceil(
        Math.abs(this.info.end.getTime() - this.info.start.getTime()) /
          (1000 * 3600 * 24)
      );

      // this.price =
      //   parseFloat(this.plot.camping_section.plot_price) +
      //   this.info.adults *
      //     parseFloat(this.plot.camping_section.price_per_adult) *
      //     this.numberOfDays +
      //   this.info.children *
      //     parseFloat(this.plot.camping_section.price_per_child) *
      //     this.numberOfDays;

      this.price =
        parseFloat(this.plot.camping_section.plot_price) * this.numberOfDays +
        this.info.adults *
          parseFloat(this.plot.camping_section.price_per_adult) +
        this.info.children *
          parseFloat(this.plot.camping_section.price_per_child);

      this.isSumOfPeopleRight =
        parseInt(this.info.children) + parseInt(this.info.adults) > 10
          ? false
          : true;
    }
  }

  createReservation() {
    let userId: number | null = this._userService.getUserId();
    let isExpired: boolean = this._userService.isUserExpired();
    if (!isExpired && userId) {
      this._router.navigate(['/reservationsummary'], {
        state: {
          formData: {
            number_of_adults: this.info.adults,
            number_of_children: this.info.children,
            number_of_babies: this.info.babies,
            date_from: this.startDate,
            date_to: this.endDate,
            user: userId,
            camping_plot: this.plot,
            number_of_days: this.numberOfDays,
            price: this.price,
          },
        },
      });
    } else {
      this._router.navigate(['/login']);
    }
  }
}
