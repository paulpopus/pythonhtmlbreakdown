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

  showDeclarations: boolean = true;
  showComments: boolean = true;
  showElements: boolean = true;

  constructor(private apiService: ApiService) { }

  getSampleData() {
    this.apiService.getSample().subscribe((data: ApiResult)=>{
      this.elements = data.elements;
      this.statistics = data.statistics;
    });
  }

  ngOnInit() {
    console.log('initiated')
    console.log("Warning is:" + this.warningsOnly)
  }

  getBreakdown(HTML: string) {
    this.apiService.processHTML(HTML).subscribe((data: ApiResult)=>{
      this.elements = data.elements;
      this.statistics = data.statistics;
    });
    console.log(this.elements)
  }

  toggleWarningsOnly() {
    this.warningsOnly = !this.warningsOnly
    console.log("Warning is:" + this.warningsOnly)
  }

  toggleTagInList(tag: string) {
    if (this.warningsOnly) {
      this.warningsOnly = false;
    } else {
      if (this.hiddenTags.includes(tag)) {
        let index = this.hiddenTags.indexOf(tag);
        this.hiddenTags.splice(index, 1);
      } else {
        this.hiddenTags.push(tag)
      }
    }

    this.hiddenTags = this.hiddenTags.concat()
  }


  isTagHidden(tag: string) {
    return !this.hiddenTags.includes(tag)
  }
}
