import { Component } from '@angular/core';
import { UserService } from 'src/app/shared/user.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  color: string = 'white';
  constructor(public _userService : UserService){}
  id: number | null = this._userService.getUserId()
}
