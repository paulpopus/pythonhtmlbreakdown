import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api/api.service';

@Component({
  selector: 'app-apidoc',
  templateUrl: './apidoc.component.html',
  styleUrls: ['./apidoc.component.scss']
})
export class ApidocComponent implements OnInit {

  constructor(private apiService: ApiService) { }

  sampleHTMLExampleBlock1: string = 'GET /sample';
  sampleHTMLExampleBlock2: string = null;

  processHTMLExampleBlock1: string = 'GET /process?html=%3Cdiv%20style=%22background:%20black;%22%20class=%22box%22%3EMy%20content%21%3C/div%3E';
  processHTMLExampleBlock2: string = null;

  processURLExampleBlock1: string = 'GET /process?url=http://example.com/';
  processURLExampleBlock2: string = null;

  warningsExampleBlock1: string = 'GET /warnings';
  warningsExampleBlock2: string = null;


  ngOnInit(): void {
    this.apiService.getSample().subscribe((data)=>{
      this.sampleHTMLExampleBlock2 = JSON.stringify(data, null, 2);
    });

    this.apiService.processHTML('<div style="background: black;" class="box">My content!</div>').subscribe((data)=>{
      this.processHTMLExampleBlock2 = JSON.stringify(data, null, 2);
    });

    this.apiService.processURL('http://example.com/').subscribe((data)=>{
      this.processURLExampleBlock2 = JSON.stringify(data, null, 2);
    });

    this.apiService.getWarnings().subscribe((data)=>{
      this.warningsExampleBlock2 = JSON.stringify(data, null, 2);
    });
  }

}
