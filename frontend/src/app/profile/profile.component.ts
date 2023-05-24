import { Component, OnInit } from '@angular/core';
import { UserService } from '../shared/user.service';
import { UserResponse } from '../shared/user.models';
import { Router } from '@angular/router';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent implements OnInit {
  id: number | null = null;
  defaultPhotoUrl: string =
    '../../assets/3687823_adventure_automotive_car_transport_transportation_icon.svg';
  isEditingName: boolean = false;
  isEditingEmail: boolean = false;
  isEditingPhone: boolean = false;
  isEditingId: boolean = false;
  isEditingPassword: boolean = false;
  editOrCancelName: string = 'Edytuj';
  editOrCancelEmail: string = 'Edytuj';
  editOrCancelPhone: string = 'Edytuj';
  editOrCancelId: string = 'Edytuj';
  editOrCancelPassword: string = 'Edytuj';

  user: UserResponse = {
    email: '',
    first_name: '',
    last_name: '',
    phone_number: 0,
    avatar: '',
    id_card: '',
  };
  editedUser: UserResponse = this.user;

  userNameForm: FormGroup = new FormGroup({
    first_name: new FormControl(''),
    last_name: new FormControl(''),
  });
  userEmailForm: FormGroup = new FormGroup({
    email: new FormControl(''),
  });
  userPhoneForm: FormGroup = new FormGroup({
    phone_number: new FormControl(''),
  });
  userIdForm: FormGroup = new FormGroup({
    id_card: new FormControl(''),
  });
  userPasswordForm: FormGroup = new FormGroup({
    password: new FormControl(''),
  });

  constructor(
    private _userService: UserService,
    private _router: Router,
    private _formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.id = this._userService.getUserId();

    if (this.id == null) {
      this._userService.signOut();
      this._router.navigate(['/login']);
    } else {
      this._userService.getUser(this.id).subscribe(
        (res) => {
          this.user = res;
        },
        (err) => {
          console.log(err);
        }
      );
    }
    this.userNameForm = this._formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
    });
    this.userEmailForm = this._formBuilder.group({
      email: ['', Validators.required],
    });
    this.userPhoneForm = this._formBuilder.group({
      phone_number: ['', Validators.required],
    });
    this.userIdForm = this._formBuilder.group({
      id_card: ['', Validators.required],
    });
    this.userPasswordForm = this._formBuilder.group({
      password: ['', Validators.required],
    });
  }

  toggleEditingName() {
    this.isEditingName = !this.isEditingName;
    if (this.isEditingName) {
      this.editedUser = { ...this.user };
      this.editOrCancelName = 'Anuluj';
    } else {
      this.editOrCancelName = 'Edytuj';
      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
      };
    }
  }
  toggleEditingEmail() {
    this.isEditingEmail = !this.isEditingEmail;
    if (this.isEditingEmail) {
      this.editedUser = { ...this.user };
      this.editOrCancelEmail = 'Anuluj';
    } else {
      this.editOrCancelEmail = 'Edytuj';
      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
      };
    }
  }
  toggleEditingPhone() {
    this.isEditingPhone = !this.isEditingPhone;
    if (this.isEditingPhone) {
      this.editedUser = { ...this.user };
      this.editOrCancelPhone = 'Anuluj';
    } else {
      this.editOrCancelPhone = 'Edytuj';
      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
      };
    }
  }
  toggleEditingId() {
    this.isEditingId = !this.isEditingId;
    if (this.isEditingId) {
      this.editedUser = { ...this.user };
      this.editOrCancelId = 'Anuluj';
    } else {
      this.editOrCancelId = 'Edytuj';
      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
      };
    }
  }
  toggleEditingPassword() {
    this.isEditingPassword = !this.isEditingPassword;
    if (this.isEditingPassword) {
      this.editedUser = { ...this.user };
      this.editOrCancelPassword = 'Anuluj';
    } else {
      this.editOrCancelPassword = 'Edytuj';
      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
      };
    }
  }

  submitForm(formType: string) {
    if (formType == 'name') {
      if (this.userNameForm.valid) {
        const first_name = this.userNameForm.get('first_name')?.value;
        const last_name = this.userNameForm.get('last_name')?.value;

        this._userService
          .updateUser(this.id!, { first_name, last_name })
          .subscribe(
            (res) => {
              this.user = res;
              this.isEditingName = false;
              this.editOrCancelName = 'Edytuj';
            },
            (err) => {
              console.log(err);
            }
          );
      }
    }
    if (formType == 'email') {
      if (this.userEmailForm.valid) {
        this.editedUser.email = this.userEmailForm.get('email')?.value;
        this.isEditingEmail = false;
      }
    }
    if (formType == 'phone') {
      if (this.userPhoneForm.valid) {
        const phone_number = this.userPhoneForm.get('phone_number')?.value;
        this._userService.updateUser(this.id!, { phone_number }).subscribe(
          (res) => {
            this.user = res;
            this.isEditingPhone = false;
            this.editOrCancelPhone = 'Edytuj';
          },
          (err) => {
            console.log(err);
          }
        );
        this.isEditingPhone = false;
      }
    }
    if (formType == 'id') {
      if (this.userIdForm.valid) {
        const id_card = this.userIdForm.get('id_card')?.value;
        this._userService.updateUser(this.id!, { id_card }).subscribe(
          (res) => {
            this.user = res;
            this.isEditingId = false;
            this.editOrCancelId = 'Edytuj';
          },
          (err) => {
            console.log(err);
          }
        );

        this.isEditingId = false;
      }
    }
    // else if(formType == "password"){
    //   this.editedUser.password = this.userNameForm.get('password')?.value;
    // }
  }
}
