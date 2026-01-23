import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebhelpDashboardComponent } from './webhelp-dashboard.component';

describe('WebhelpDashboardComponent', () => {
  let component: WebhelpDashboardComponent;
  let fixture: ComponentFixture<WebhelpDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WebhelpDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WebhelpDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
