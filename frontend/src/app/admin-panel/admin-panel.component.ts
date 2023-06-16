import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/shared/user.service';
import { UserResponse } from 'src/app/shared/user.models';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss']
})
export class AdminPanelComponent implements OnInit  { 
  selectedUserId: number | null = null;
  selectedUser: UserResponse | null = null;
  users: UserResponse[] = [];

  constructor(private userService: UserService) { }

  ngOnInit() {
    // Pobierz użytkowników z bazy danych
    this.getUsers();
  }

  getUsers() {
    this.userService.getAllUsers().subscribe(
      (response) => {
        this.users = response;
      },
      (error) => {
        console.error('Błąd podczas pobierania użytkowników', error);
      }
    );
  }

  getUserById(id: number) {
    if (id) {
      this.userService.getUser(id).subscribe(
        (response) => {
          this.selectedUser = response;
        },
        (error) => {
          console.error('Błąd podczas pobierania danych użytkownika', error);
        }
      );
    } else {
      this.selectedUser = null;
    }
  }

  updateUser() {
    if (this.selectedUserId !== null && this.selectedUser !== null) {
      const changedData = {
        email: this.selectedUser.email,
        first_name: this.selectedUser.first_name,
        last_name: this.selectedUser.last_name,
        phone_number: this.selectedUser.phone_number,
        avatar: this.selectedUser.avatar,
        id_card: this.selectedUser.id_card
      };

      this.userService.updateUser(this.selectedUserId, changedData).subscribe(
        (response) => {
          console.log('Dane użytkownika zaktualizowane', response);
          // Możesz wykonać dodatkowe akcje po zaktualizowaniu danych użytkownika
        },
        (error) => {
          console.error('Błąd podczas aktualizacji danych użytkownika', error);
        }
      );
    } else {
      console.error('Błąd: Brak wybranego użytkownika lub ID');
    }
  }
}
