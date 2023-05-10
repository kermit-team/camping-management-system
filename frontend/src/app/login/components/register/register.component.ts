import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth.service';
import { AuthHttpService } from '../../auth-http.service';
import { AbstractControl, FormBuilder, FormControl, FormGroup, ValidatorFn, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit{
  form: FormGroup = new FormGroup({
    name: new FormControl(''),
    surname: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
    confirmPassword: new FormControl(''),
  });

  isSubmitted = false
  isSuccessful = false;
  isSignUpFailed = false;
  message = '';
  passwordErrors = [];

  constructor(private _authService: AuthService, private _formBuilder: FormBuilder){};

  ngOnInit(): void {
    this.form = this._formBuilder.group(
      {
        name: ['', Validators.required],
        surname: ['', Validators.required],
        email: ['', [Validators.required, Validators.email]],
        password: [
          '',
          [
            Validators.required,
            Validators.minLength(8),
            Validators.pattern(/^(?=.*[A-Z])(?=.*[\W_]).+$/),
          ]
        ],
        confirmPassword: ['', Validators.required]
      },{ validator: this.match('password','confirmPassword') }
    );
  }
  match(controlName: string, checkControlName: string): ValidatorFn {
    return (controls: AbstractControl) => {
      const control = controls.get(controlName);
      const checkControl = controls.get(checkControlName);

      if (checkControl?.errors && !checkControl.errors['matching']) {
        return null;
      }

      if (control?.value !== checkControl?.value) {
        controls.get(checkControlName)?.setErrors({ matching: true });
        return { matching: true };
      } else {
        return null;
      }
    }
  }

  get f(): { [key: string]: AbstractControl } {
    return this.form.controls;
  }




  onSubmit(): void {
    this.isSubmitted = true;

    if (this.form.invalid) {
      return;
    }
    this._authService.register(this.form.value.email,this.form.value.password,this.form.value.name,this.form.value.surname).subscribe(
      (res)=> {
        this.message = 'Rejestracja pomyślna. Potwierdź teraz maila i <a [routerLink]="[\'/login\']" style="color:#ae9560">Zaloguj się</a>';
        
      },
      (err) => {
        this.message = err.error.details;
      }
    )
    // this._authService.register(first_name,last_name,email,password).subscribe(
    //   data => {
    //     console.log(data);
    //     this.isSuccessful = true;
    //     this.isSignUpFailed = false;
    //   },
    //   err => {
    //     this.errorMessage = err.error.message;
    //     this.isSignUpFailed = true;
    //   }
    // );
  }
}
