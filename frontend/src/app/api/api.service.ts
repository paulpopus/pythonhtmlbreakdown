import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from './../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private httpClient: HttpClient) { }

  public getSample(){
    return this.httpClient.get(`${environment.apiUrl}/sample`);
  }

  public processHTML(HTML: string) {
    return this.httpClient.get(`${environment.apiUrl}/process?html=${encodeURI(HTML)}`);
  }

  public processURL(URL: string) {
    return this.httpClient.get(`${environment.apiUrl}/process?url=${encodeURI(URL)}`);
  }

  public getWarnings(){
    return this.httpClient.get(`${environment.apiUrl}/warnings`);
  }
}
