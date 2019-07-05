import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {ContentService} from '../content/content.service';

@Component({
    selector: 'app-game',
    templateUrl: './game.component.html',
    styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {
    currentIndex;
    finished;
    constructor(
        private route: ActivatedRoute,
        private cartService: ContentService
      ) {
          this.currentIndex = 0;
          this.finished = false;
       }
    ngOnInit() {}

    nextQuestion() { this.currentIndex = this.cartService.switchQuestion(true); }
    prevQuestion() {this.currentIndex = this.cartService.switchQuestion(false); }
  }
