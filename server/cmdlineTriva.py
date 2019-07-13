from triviaClasses import QuestionObject, Player

difficulty2Options = {'Easy': 3, 'Medium': 4, 'Hard': 5}

if __name__ == '__main__':

    player = Player()
    
    ## Select the level
    while True:
        gameLevel = input("Choose the difficulty (Easy/Medium/Hard):  ")
        if gameLevel in difficulty2Options:
            numOptions = difficulty2Options[gameLevel]
            break
        else:
            print("Invalid input - try again!")

    ## Keep playing the game
    while True:
       
        question = QuestionObject(numOptions)
        question.printQuestion()
        selection = int(input("Choose your answer:  "))

        if question.allAnswers[selection-1] == question.correctAnswer:
            print("Correct!")
            player.score += 1
        else:
            print("Incorrect")

        rerun = input("Do you want to keep playing? (yes/no)")
        if rerun == "no":
            break

    print("Thanks for playing! You scored: %s points"%player.score)