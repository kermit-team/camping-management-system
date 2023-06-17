//FIXME: Error handling
import { Component, OnInit } from '@angular/core';
import { UserService } from '../shared/user.service';
import { UserResponse } from '../shared/user.models';
import { Groups } from '../shared/user.models';
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
  groups: Groups[] = [];
  photoUrl:string = "localhost:8000";
  mode: number = 0;
  defaultPhotoUrl: string =
    '../../assets/3687823_adventure_automotive_car_transport_transportation_icon.svg';
  isEditingName: boolean = false;
  isEditingLastName: boolean = false;
  isEditingEmail: boolean = false;
  isEditingPhone: boolean = false;
  isEditingId: boolean = false;
  isEditingPassword: boolean = false;


  user: UserResponse = {
    email: '',
    first_name: '',
    last_name: '',
    phone_number: 0,
    avatar: '',
    id_card: '',
    cars: [],
    groups: []
  };
  editedUser: UserResponse = this.user;

  userNameForm: FormGroup= new FormGroup({
    first_name: new FormControl('')
  });
  userLastNameForm: FormGroup = new FormGroup({
    last_name: new FormControl('')
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
  carAddForm: FormGroup= new FormGroup({
    registration_plate: new FormControl('')
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
          this.userNameForm = this._formBuilder.group({
            first_name: [res.first_name, Validators.required]
          });
          this.userLastNameForm = this._formBuilder.group({
            last_name: [res.last_name, Validators.required],
          });
          this.userPhoneForm = this._formBuilder.group({
            phone_number: [res.phone_number, Validators.required],
          });
          if(this.user.avatar != "")
            this.photoUrl += this.user.avatar;
        },
        (err) => {
          console.log(err);
        }
      );
    }
    this.userIdForm = this._formBuilder.group({
      id_card: ['', Validators.required],
    });
    
    
  }
  toggleEditingLastName() {
    this.isEditingLastName = !this.isEditingLastName;
    if (this.isEditingLastName) {
      this.editedUser = { ...this.user };

    } else {

      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
        cars: [],
        groups: []
      };
    }
  }
  toggleEditingName() {
    this.isEditingName = !this.isEditingName;
    if (this.isEditingName) {
      this.editedUser = { ...this.user };

    } else {

      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
        cars: [],
        groups: []
      };
    }
  }

  toggleEditingPhone() {
    this.isEditingPhone = !this.isEditingPhone;
    if (this.isEditingPhone) {
      this.editedUser = { ...this.user };
 
    } else {

      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
        cars: [],
        groups: []
      };
    }
  }
  toggleEditingId() {
    this.isEditingId = !this.isEditingId;
    if (this.isEditingId) {
      this.editedUser = { ...this.user };

    } else {

      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
        cars: [],
        groups: []
      };
    }
  }
  toggleEditingPassword() {
    this.isEditingPassword = !this.isEditingPassword;
    if (this.isEditingPassword) {
      this.editedUser = { ...this.user };

    } else {

      this.editedUser = {
        email: '',
        first_name: '',
        last_name: '',
        phone_number: 0,
        avatar: '',
        id_card: '',
        cars: [],
        groups: []
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

            },
            (err) => {
              console.log(err);
            }
          );
      }
    }
    if (formType == 'lastname') {
      if (this.userLastNameForm.valid) {
        const last_name = this.userLastNameForm.get('last_name')?.value;

        this._userService
          .updateUser(this.id!, { last_name })
          .subscribe(
            (res) => {
              this.user = res;
              this.isEditingLastName = false;

            },
            (err) => {
              console.log(err);
            }
          );
      }
    }

    if (formType == 'phone') {
      if (this.userPhoneForm.valid) {
        const phone_number = this.userPhoneForm.get('phone_number')?.value;
        this._userService.updateUser(this.id!, { phone_number }).subscribe(
          (res) => {
            this.user = res;
            this.isEditingPhone = false;

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

          },
          (err) => {
            console.log(err);
          }
        );

        this.isEditingId = false;
      }
    }
  }
  addCarMode(){
    this.mode = this.mode == 0 || this.mode == 1 ? 2 : 0; 
  }
  deleteCarMode(){
    this.mode = this.mode == 0 || this.mode == 2 ? 1 : 0;
  }
  addCar(){
    const plate = this.carAddForm.get('registration_plate')?.value;
    this._userService.addUserCar(plate).subscribe(
      res => {
        this.user = res;
        this.mode = 0;
      },
      err => {
        console.log(err);
      }
    )
  }
  onCarDeleted(deletedCarId: number){
    this.user.cars = this.user.cars.filter(car => car !== deletedCarId)
  }
}
