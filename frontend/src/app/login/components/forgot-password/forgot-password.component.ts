import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthHttpService } from '../../auth-http.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent {
  form: FormGroup = new FormGroup({
    email: new FormControl('', Validators.required)
  });
  isSubmitted = false;
  message = '';
  isResetCorrect: boolean = false

  constructor(private _authHttpService: AuthHttpService){}

  get f(): { [key: string]: AbstractControl } {
    return this.form.controls;
  }

  onSubmit(): void {
    this.isSubmitted = true;
    if(this.form.invalid)
    return;
    this._authHttpService.resetPassword(this.form.value.email).subscribe(
      res => {
        this.isResetCorrect = true;
      },
      err => {
        if(err.error.message){
          this.message = err.error.message;
        }
        else {
          this.message = err.error.detail;
        }
      }
    )
  }
}
