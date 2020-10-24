import { Component, OnInit} from '@angular/core';
import { ApiService } from '../api/api.service';

interface ApiResult {
  statistics: Array<any>;
  elements: Array<any>;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {
  elements: Object;
  statistics: Object;

  hiddenTags: Array<string> = [];

  warningsOnly: boolean = false;

  showComments: boolean = true;
  showElements: boolean = true;

  constructor(private apiService: ApiService) { }

  getSampleData() {
    this.apiService.getSample().subscribe((data: ApiResult)=>{
      this.elements = data.elements;
      this.statistics = data.statistics;
    });
  }

  isValidUrl(url: string) {
    try {
      new URL(url);
    } catch (error) {
      return false;
    }

    return true;
  }

  getDataByHTML(HTML: string) {
    this.apiService.processHTML(HTML).subscribe((data: ApiResult)=>{
      this.elements = data.elements;
      this.statistics = data.statistics;
    });
  }

  getDataByURL(URL: string) {
    this.apiService.processURL(URL).subscribe((data: ApiResult)=>{
      this.elements = data.elements;
      this.statistics = data.statistics;
    });
  }

  ngOnInit() {

  }

  getBreakdown(value: string) {
    if (this.isValidUrl(value)) {
      this.getDataByURL(value);
    } else {
      this.getDataByHTML(value);
    }
  }

  toggleWarningsOnly() {
    this.warningsOnly = !this.warningsOnly
  }

  toggleTagInList(tag: string) {
    if (this.warningsOnly) {
      this.warningsOnly = false;
    } else {
      if (this.hiddenTags.includes(tag)) {
        let index = this.hiddenTags.indexOf(tag);
        this.hiddenTags.splice(index, 1);
      } else {
        this.hiddenTags.push(tag);
      }
    }

    this.hiddenTags = this.hiddenTags.concat();
  }


  isTagHidden(tag: string) {
    return !this.hiddenTags.includes(tag);
  }
}
