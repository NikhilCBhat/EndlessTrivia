import {Injectable} from '@angular/core';

@Injectable({
    providedIn: 'root'
})

export class ContentService {
    MAX_QUESTIONS = 7;
    questions = [];
    currentIndex = 0;
    completed = false;

    switchQuestion(forward) {
        if (forward) {
            this.currentIndex++;
            return this.currentIndex;
        } else {
            this.currentIndex--;
            return this.currentIndex;
        }
    }
}
