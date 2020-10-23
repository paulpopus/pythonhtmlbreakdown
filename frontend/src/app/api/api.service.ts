import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private httpClient: HttpClient) { }

  public getSample(){
    return this.httpClient.get(`http://localhost:64232/sample`);
  }

  public processHTML(HTML: string) {
    return this.httpClient.get(`http://localhost:64232/process?html=${encodeURI(HTML)}`);
  }

  public processURL(URL: string) {
    return this.httpClient.get(`http://localhost:64232/process?url=${encodeURI(URL)}`);
  }

  public getWarnings(){
    return this.httpClient.get(`http://localhost:64232/warnings`);
  }
}
