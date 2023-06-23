import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/shared/user.service';
import { UserResponse, Groups, FullUserResponse, FullUserRequest } from 'src/app/shared/user.models';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss']
})
export class AdminPanelComponent implements OnInit {
  
  selectedUser: FullUserResponse | null = null;
  users: FullUserResponse[] = [];
  groups: Groups[] | null = null;
  isModalVisible = false;
  // editedUser: FullUserResponse = {
  //   email: '',
  //   first_name: '',
  //   last_name: '',
  //   phone_number: 0,
  //   avatar: '',
  //   id_card: '',
  //   cars: [],
  //   groups: [],
  //   id: 0
  // };

  userForm: FormGroup;

  constructor(
    private userService: UserService,
    private formBuilder: FormBuilder
  ) {
    this.userForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone_number: ['', Validators.required],
      groups: ['', Validators.required]
    });
  }

  ngOnInit() {
    this.getUsers();
    this.getGroups();
  }

  getUsers() {
    this.userService.getAllUsers().subscribe(
      (response) => {
        this.users = response;
        console.log(this.users)
      },
      (error) => {
        console.error('Błąd podczas pobierania użytkowników', error);
      }
    );
  }

  getGroups() {
    this.userService.getAllGroups().subscribe(
      (response) => {
        this.groups = response;
      },
      (error) =>{
        console.error('Błąd podczas pobierania grup', error);
      }
    )
  }

  // getGroupName(groups: Groups): string {
  //   if (groups && groups.length > 0) {
  //     return groups[0].name;
  //   }
  //   return '';
  // }

  deleteUser(user: FullUserResponse): void {
    this.userService.deleteUser(user.id).subscribe(
      () => {
        console.log(`Usunięto użytkownika: ${user.first_name} ${user.last_name}`);
        // Usuń użytkownika z tabelki
        const index = this.users.indexOf(user);
        if (index !== -1) {
          this.users.splice(index, 1);
        }
      },
      (error) => {
        console.error('Błąd podczas usuwania użytkownika', error);
      }
    );
  }
  
  openModal(user: FullUserResponse) {
    this.isModalVisible = true;
    this.selectedUser = { ...user };
    //this.editedUser = { ...user };
    this.userForm.patchValue({
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      phone_number: user.phone_number,
      groups: user.groups ? user.groups[0].name : null
    });
  }
  
  closeModal() {
    this.isModalVisible = false;
    this.userForm.reset();
  }
  
  updateUser(id: number) {
    if (this.userForm.valid) {
      const editedData:FullUserResponse = this.userForm.value;
      console.log(typeof(parseInt(this.userForm.value.groups)))
      const updatedUser = {
        first_name: this.userForm.value.first_name,
        last_name: this.userForm.value.last_name,
        email: this.userForm.value.email,
        phone_number: this.userForm.value.phone_number,
        groups: parseInt(this.userForm.value.groups)
      }
      // const updatedUser: FullUserRequest = {
      //   first_name: this.userForm.value.first_name,
      //   last_name: this.userForm.value.last_name,
      //   email: this.userForm.value.email,
      //   phone_number: this.userForm.value.phone_number,
      //   avatar: '',
      //   id_card: '',
      //   cars: [],
      //   groups: this.userForm.value.groups ? this.userForm.value.groups[0].name : null
      // };
      
      // Wywołaj funkcję updateFullUser() z serwisu UserService
      this.userService.updateFullUser(id, updatedUser).subscribe(
        (response) => {
          console.log('Dane użytkownika zaktualizowane', response);
          // Zaktualizuj dane wyświetlane w tabeli
          // const index = this.users.findIndex((user) => user.id === id);
          // if (index !== -1) {
          //   this.users[index] = { ...updatedUser };
          // }
          this.closeModal();
        },
        (error) => {
          console.error('Błąd podczas aktualizacji danych użytkownika', error);
        }
      );
    } else {
      console.error('Formularz jest nieprawidłowy');
    }
  }
  
  
}
