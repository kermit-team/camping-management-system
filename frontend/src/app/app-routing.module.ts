import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { ProfileComponent } from './profile/profile.component';
import { SuccessComponent } from './payment/success/success.component';
import { CancelComponent } from './payment/cancel/cancel.component';
import { UserGuard } from './guards/user-guard.guard';

const routes: Routes = [
  { path: 'profile', component: ProfileComponent, canActivate:[UserGuard]},
  { path: '', component: LandingPageComponent},
  { path: 'adminPanel', component: AdminPanelComponent},
  { path: 'payment/success', component: SuccessComponent},
  { path: 'payment/cancel', component: CancelComponent}


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
