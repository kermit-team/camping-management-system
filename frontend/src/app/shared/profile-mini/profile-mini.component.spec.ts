import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileMiniComponent } from './profile-mini.component';

describe('ProfileMiniComponent', () => {
  let component: ProfileMiniComponent;
  let fixture: ComponentFixture<ProfileMiniComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileMiniComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProfileMiniComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
