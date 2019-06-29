import re
from tkinter import Tk, Button, Label, Scale, Toplevel
import wikipedia
from functools import partial
from random import shuffle

## -- Wiki Variables -- ##

# Constants
ALTERNATE_OPTIONS = 7
NUM_PLAYERS = 10

# Variables
correctAnswer = ""
difficulty2Options = {'easy': 3, 'medium': 4, 'hard': 5}
scores = []
currentTeam = 0
currentAnswers = {}
currentQuestion = ""

## -- Frame Variables --##

## Size & Color
WELCOME_HEIGHT = 600
WELCOME_WIDTH = 800
GAME_HEIGHT = 800
GAME_WIDTH = 1200
def getGeometry(w, h):
    return str(w) + 'x' + str(h)
WELCOME_GEOMETRY = getGeometry(WELCOME_WIDTH, WELCOME_HEIGHT)
GAME_GEOMETRY = getGeometry(GAME_WIDTH, GAME_HEIGHT)
BACKGROUND_COLOR = 'deep sky blue'

## Window & Label
welcomeWindow = Tk()
welcomeWindow.title("endlessTrivia")
welcomeWindow.geometry(WELCOME_GEOMETRY)
welcomeWindow.configure(background=BACKGROUND_COLOR)
titleLabel = Label(welcomeWindow, text="~ Endless Trivia ~", anchor="center", font=("Helvetica", 62), bg=BACKGROUND_COLOR)
titleLabel.place(x=WELCOME_WIDTH/2, y=WELCOME_HEIGHT*0.2, anchor="center")
playersLabel = Label(welcomeWindow, text="Number of Players:", anchor="center", font=("Helvetica", 25), bg=BACKGROUND_COLOR)
playersLabel.place(x=WELCOME_WIDTH*0.2, y=WELCOME_HEIGHT*0.7, anchor="center")
playersSlider = Scale(welcomeWindow, from_=1, to=20, orient='horizontal', length=WELCOME_WIDTH*0.5, font=("Helvetica", 20), bg=BACKGROUND_COLOR)
playersSlider.place(x=WELCOME_WIDTH*0.65, y=WELCOME_HEIGHT*0.7, anchor="center")

## -- Functions -- ##

## Runs when an answer choice is made
def answered(a):
    global currentAnswers
    global currentTeam
    if currentAnswers[a] == correctAnswer:
        global scores
        scores[currentTeam] += 1
    global currentQuestion
    currentQuestion = newQuestion()
    currentAnswers = newAnswers()
    currentTeam += 1
    currentTeam  = currentTeam%NUM_PLAYERS

## Generates the next question
def newQuestion():
    global correctAnswer
    correctAnswer = wikipedia.random(1)

    question = None
    while question is None:
        try:
            question = wikipedia.summary(correctAnswer, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            print(e)

    for x in correctAnswer.split():
        pattern = re.compile('[\W_]+')
        x = pattern.sub('', x)
        reg = re.compile(r"\b%s\b" % x, re.IGNORECASE)
        question = reg.sub("_____", question)

    return question.replace("_ _", "_")

## Generates the next answers
def newAnswers():
    alternates = wikipedia.random(ALTERNATE_OPTIONS)
    choices = []
    choices.extend(alternates)
    choices.append(correctAnswer)
    shuffle(choices)
    prefixes = [i for i in range(len(choices))]
    answers = dict(zip(prefixes, choices))
    return answers

## -- Run the Game -- ##
def startGame(difficulty):
    global NUM_PLAYERS
    NUM_PLAYERS = playersSlider.get()
    global scores
    scores = [0] * NUM_PLAYERS
    
    ## Update the number of options
    global ALTERNATE_OPTIONS
    ALTERNATE_OPTIONS = difficulty2Options[difficulty]
    print(difficulty, ALTERNATE_OPTIONS)

    ## Setup the Game Window
    gameWindow = Toplevel(welcomeWindow)
    gameWindow.geometry(GAME_GEOMETRY)
    gameWindow.configure(background=BACKGROUND_COLOR)
    questionLabel = Label(gameWindow, text=currentQuestion, anchor="center", font=("Helvetica", 20), wraplength=GAME_WIDTH*0.8, justify="center", bg=BACKGROUND_COLOR)
    questionLabel.place(x=GAME_WIDTH/2, y=GAME_HEIGHT*0.1, anchor="center")
    scoresLabel = Label(gameWindow, text=scores[currentTeam], anchor="center", font=("Helvetica", 20), bg=BACKGROUND_COLOR)
    scoresLabel.place(x=GAME_WIDTH*0.9, y=GAME_HEIGHT*0.9, anchor="center")
    answerButtons = dict.fromkeys([i for i in range(ALTERNATE_OPTIONS)])

    ## Update the text on the screen, on-click
    def updateText():
        questionLabel.configure(text=currentQuestion)
        scoresLabel.configure(text="Team %d scores: %d"%(currentTeam+1, scores[currentTeam]))
        for key in answerButtons:
            if answerButtons[key] is not None:
                answerButtons[key].configure(text=currentAnswers[key])
        gameWindow.after(1, updateText)
    
    updateText()
    print(answerButtons)
    print(currentAnswers)
    print(currentQuestion)

    ## Place the answerButtons
    for key in answerButtons:
        answerButtons[key] = Button(gameWindow, text=currentAnswers[key], command=partial(answered, key), bg='powder blue', font=("Helvetica", 20))
        answerButtons[key].place(x = GAME_WIDTH/2, y = GAME_HEIGHT*(0.3+key/10), anchor='center')

## -- Start the Opening Window -- ##
if __name__ == "__main__":
    currentQuestion = newQuestion()
    currentAnswers = newAnswers()

    for index, key in enumerate(difficulty2Options):
        button = Button(welcomeWindow, text=key, command=partial(startGame, key), bg='powder blue', font=("Helvetica", 30))
        button.place(x=WELCOME_WIDTH/(len(difficulty2Options) + 1)*(index+1) , y=WELCOME_HEIGHT*0.5, anchor="center")

    welcomeWindow.mainloop()

