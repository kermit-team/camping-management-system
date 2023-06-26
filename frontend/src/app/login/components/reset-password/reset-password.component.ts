import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthHttpService } from '../../auth-http.service';
import { AbstractControl, FormBuilder, FormControl, FormGroup, ValidatorFn, Validators } from '@angular/forms';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent implements OnInit{
  form: FormGroup = new FormGroup({
    password: new FormControl(''),
    confirmPassword: new FormControl('')
  });

  id: string = "";
  token: string = "";
  message: string = "";
  isSuccessful: boolean = false;
  areErrors: boolean = false;
  isSubmitted: boolean = false;
  isLinkInvalid: boolean = true;

  constructor(private _route: ActivatedRoute, private _authHttpService: AuthHttpService, private _formBuilder: FormBuilder) { }
  ngOnInit(): void {
    this.id = this._route.snapshot.params['id'];
    this.token = this._route.snapshot.params['token'];
    this.form = this._formBuilder.group(
      {
        password: ['',
        [
          Validators.required,
          Validators.minLength(8),
          Validators.pattern(/^(?=.*[A-Z])(?=.*[\W_]).+$/),
        ]
      ],
      confirmPassword: ['', Validators.required]
      },{validator: this.match('password','confirmPassword')}
    );
    this._authHttpService.confirmResetPassword(this.id, this.token,"").subscribe(
      resp => {
      },
      err => {
        if(err.error.password){
          this.message = "";
        }
        else {
          this.areErrors = true;
          this.message = err.error.message
        }
      }
    )
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
    this.id = this._route.snapshot.params['id'];
    this.token = this._route.snapshot.params['token'];

    if (this.form.invalid) {
      return;
    }

    this._authHttpService.confirmResetPassword(this.id, this.token, this.form.value.password).subscribe(
      resp => {
        this.isSuccessful = true;
        this.message = "Hasło zostało zmienione";
      },
      err => {
        this.areErrors = true;
        this.message = err.error;
      }
    )
  }
}
