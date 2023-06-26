import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { RouterModule } from '@angular/router';
import { ProfileMiniComponent } from './profile-mini/profile-mini.component';
import { CarComponent } from './car/car.component';



@NgModule({
  declarations: [HeaderComponent,ProfileMiniComponent, CarComponent],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [HeaderComponent,ProfileMiniComponent, CarComponent]
})
export class SharedModule { }
