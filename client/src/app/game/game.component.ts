import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {ContentService} from '../content/content.service';

@Component({
    selector: 'app-game',
    templateUrl: './game.component.html',
    styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {
    currentQuestion;
    currentQuestionIndex;
    finished;
    constructor(
        private route: ActivatedRoute,
        private cartService: ContentService
      ) {
          this.currentQuestionIndex = 0;
          this.finished = false;
       }
    ngOnInit() {}

    nextQuestion() { this.currentQuestionIndex = this.cartService.switchQuestion(true); }
    prevQuestion() {this.currentQuestionIndex = this.cartService.switchQuestion(false); }

    reformatQuestion(question) {
        this.currentQuestion = {
            prompt: question.question,
            allAnswers: [],
            correctAnswer: question.correctAnswer,
            correctAnswerIndex: Math.floor(Math.random() * (question.wrongAnswers.length + 1)),
            selectionIndex: -1,
        };
        question.wrongAnswers.forEach(answer => {
            this.currentQuestion.allAnswers.append({
                text: answer,
                state: 'unselected'
            });
        });
        this.currentQuestion.allAnswers = question.wrongAnswers.splice(this.currentQuestion.correctAnswerIndex, 0, {
            text: this.currentQuestion.correctAnswer,
            state: 'unselected'
        });
    }
    selectAnswer(index) {
        this.currentQuestion.selectionIndex = index;
        if (this.currentQuestion.allAnswers[index].text !== this.currentQuestion.correctAnswer) {
            this.currentQuestion.allAnswers[index].state = 'incorrect';
        }
        this.currentQuestion.allAnswers[this.currentQuestion.correctAnswerIndex].state = 'correct';
    }

    saveSelection() {
        this.cartService.updateQuestionWithUserInput(this.currentQuestion, this.currentQuestionIndex);
    }
  }
