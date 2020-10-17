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
    let string = HTML.replace(/\s/g, "")
    return this.httpClient.get(`http://localhost:64232/process?html=${encodeURI(HTML)}`);
  }
}
