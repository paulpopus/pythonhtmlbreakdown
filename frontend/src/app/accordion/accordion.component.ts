import { Component, OnInit, Input, OnChanges, SimpleChanges, SimpleChange } from '@angular/core';

@Component({
  selector: 'app-accordion',
  templateUrl: './accordion.component.html',
  styleUrls: ['./accordion.component.scss']
})
export class AccordionComponent implements OnInit {

  constructor() { }

  @Input() firstCodeBlock: string;

  @Input() secondCodeBlock: string;

  isOpen: boolean = false;

  ngOnInit(): void {
  }

  toggleAccordion() {
    this.isOpen = !this.isOpen;
  }

}
