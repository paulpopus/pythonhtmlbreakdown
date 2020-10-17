import { Component, OnInit } from '@angular/core';
import { ApiService } from './api/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'apifrontend';
  apiConnection: boolean = false;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    if (this.apiService.getSample()) {
      this.apiConnection = true;
    }
  }
}
