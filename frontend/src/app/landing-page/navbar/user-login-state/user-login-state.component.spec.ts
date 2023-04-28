import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserLoginStateComponent } from './user-login-state.component';

describe('UserLoginStateComponent', () => {
  let component: UserLoginStateComponent;
  let fixture: ComponentFixture<UserLoginStateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserLoginStateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserLoginStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
