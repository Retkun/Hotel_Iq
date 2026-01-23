import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ColtDashboardComponent } from './colt-dashboard.component';

describe('ColtDashboardComponent', () => {
  let component: ColtDashboardComponent;
  let fixture: ComponentFixture<ColtDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ColtDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ColtDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
