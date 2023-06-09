import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { RouterModule } from '@angular/router';
import { ProfileMiniComponent } from './profile-mini/profile-mini.component';



@NgModule({
  declarations: [HeaderComponent,ProfileMiniComponent],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [HeaderComponent,ProfileMiniComponent]
})
export class SharedModule { }
