import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../auth.service';
import { Router } from '@angular/router';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  form: FormGroup = new FormGroup({
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
  });
  isSubmitted = false;
  isLoggedIn = false;
  isLoginFailed = false;
  message = '';

  constructor(
    private _authService: AuthService,
    private _router: Router
  ) {}
  ngOnInit(): void {
    if (this._authService.getToken()) {
      this.isLoggedIn = true;
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
    this._authService
      .login(this.form.value.username, this.form.value.password)
      .subscribe(
        (res) => {
          this.message = 'Logowanie pomyślne';
          this._router.navigate(['/']);
        },
        (err) => {
          this.message = err.error.detail;
        }
      );
  }
}
