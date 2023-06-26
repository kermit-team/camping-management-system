import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserReservationsItemComponent } from './user-reservations-item.component';

describe('UserReservationsItemComponent', () => {
  let component: UserReservationsItemComponent;
  let fixture: ComponentFixture<UserReservationsItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserReservationsItemComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserReservationsItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
