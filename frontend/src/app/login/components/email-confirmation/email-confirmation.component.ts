import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthHttpService } from '../../auth-http.service';

@Component({
  selector: 'app-email-confirmation',
  templateUrl: './email-confirmation.component.html',
  styleUrls: ['./email-confirmation.component.scss']
})
export class EmailConfirmationComponent implements OnInit{
  id: string = "";
  token: string = "";
  message: string = "";
  isInvalid: boolean = true;

  constructor(private _route: ActivatedRoute, private _authHttpService: AuthHttpService) { }

  ngOnInit(): void {
    this.id = this._route.snapshot.params['id'];
    this.token = this._route.snapshot.params['token'];

    this._authHttpService.emailConfirmation(this.id,this.token).subscribe(
      resp => {
        this.message = "Twoja rejestracja przebiegła pomyślnie";
        this.isInvalid = false;
      },
      err => {
        this.message = err.error.message;
      }
    )
  }
}
