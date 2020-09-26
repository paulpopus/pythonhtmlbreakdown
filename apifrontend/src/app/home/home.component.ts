import { Component} from '@angular/core';
import { ApiService } from '../api/api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent {
  elements: Object;

  hiddenTags: Array<string> = [];

  showDeclarations: boolean = true;
  showComments: boolean = true;
  showElements: boolean = true;

  constructor(private apiService: ApiService) { }

  getSampleData() {
    this.apiService.getSample().subscribe((data)=>{
      this.elements = data;
    });
  }

  getBreakdown(HTML: string) {
    this.apiService.processHTML(HTML).subscribe((data)=>{
      this.elements = data;
    });
  }

  toggleTagInList(tag: string) {
    if (this.hiddenTags.includes(tag)) {
      let index = this.hiddenTags.indexOf(tag);
      this.hiddenTags.splice(index, 1);
    } else {
      this.hiddenTags.push(tag)
    }
    this.hiddenTags = this.hiddenTags.concat()
  }


  isTagHidden(tag: string) {
    return !this.hiddenTags.includes(tag)
  }
}
