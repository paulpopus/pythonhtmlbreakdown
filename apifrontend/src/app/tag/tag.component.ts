import { Component, OnInit, Input, OnChanges, SimpleChanges, SimpleChange } from '@angular/core';

@Component({
  selector: 'app-tag',
  templateUrl: './tag.component.html',
  styleUrls: ['./tag.component.scss']
})



export class TagComponent implements OnInit, OnChanges {

  constructor() { }

  @Input() element: any;

  @Input() hiddenTags: Array<string>;

  open: boolean = true;

  isHidden: boolean = false;

  ngOnInit(): void {
    this.element.depth > 1 ? this.open = false : this.open = true
  }

  getMarginLeft() {
    let margin = 0;

    if (this.element.depth > 0 && this.element.depth < 6) {
      margin = this.element.depth * 20;
    } else if (this.element.depth > 5) {
      margin = 20 * 5;
    }

    return margin
  }

  ngOnChanges(changes: SimpleChanges) {
    if (this.hiddenTags.includes(this.element.type)) {
      this.isHidden = true
    } else {
      this.isHidden = false
    }
  }

  toggleCloseOpenTag() {
    this.open = !this.open
  }
}
