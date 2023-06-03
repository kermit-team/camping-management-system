import { Component, OnInit, Input } from '@angular/core';
import { UserService } from '../user.service';
import { UserResponse } from '../user.models';


@Component({
  selector: 'app-profile-mini',
  templateUrl: './profile-mini.component.html',
  styleUrls: ['./profile-mini.component.scss']
})
export class ProfileMiniComponent implements OnInit {
  @Input() color: string = 'black'; 

  userData: UserResponse | null = null;

  constructor(private _userService: UserService) {}

  ngOnInit() {
    const userId: number | null = this._userService.getUserId();
    if (userId) {
      this._userService.getUser(userId).subscribe(
        (response: UserResponse) => {
          this.userData = response;
        },
        (error: any) => {
          console.error('Error while fetching user data:', error);
        }
      );
    }
  }
}
