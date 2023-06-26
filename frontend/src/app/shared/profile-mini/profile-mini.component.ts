import { Component, OnInit, Input } from '@angular/core';
import { UserService } from '../user.service';
import { UserResponse } from '../user.models';
import { AuthService } from 'src/app/login/auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-profile-mini',
  templateUrl: './profile-mini.component.html',
  styleUrls: ['./profile-mini.component.scss']
})
export class ProfileMiniComponent implements OnInit {
  @Input() color: string = 'black'; 

  userData: UserResponse | null = null;
  showDropdown: boolean = false;
  isAdmin: boolean = false;

  constructor(private _userService: UserService,  private _authService: AuthService, private _router: Router) {}

  ngOnInit() {
    const userId: number | null = this._userService.getUserId();
    if (userId) {
      this._userService.getUser(userId).subscribe(
        (response: UserResponse) => {
          this.userData = response;
          console.log(this.isAdmin)
          this.isAdmin = response.groups.some(group => group.name === 'Administratorzy');

        },
        (error: any) => {
          console.error('Error while fetching user data:', error);
        }
      );
    }
  }
  logout() {
    this._authService.logout(); 
    if (window.location.href === 'http://localhost:4200/') {
      location.reload();
    }
  }
  toggleDropdown() {
    this.showDropdown = !this.showDropdown;
  }

}
