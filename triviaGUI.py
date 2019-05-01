import tkinter
from tkinter import *
import wikipedia
from functools import partial
from string import ascii_lowercase
from random import shuffle

## -- Wiki Variables -- ##
topic = ""
alternate_options = 3
alphabet = dict(enumerate(ascii_lowercase, 1))
difficulty2Options = {'easy': 3, 'medium': 4, 'hard': 5}
score = 0
currentAnswers = {}
currentQuestion = ""

## -- Functions -- ##

## Convenience function to get the geometry string
def getGeometry(w, h):
    return str(w) + 'x' + str(h)

## Runs when an answer choice is made
def answered(a):
    global currentQuestion
    currentQuestion = newQuestion()
    global currentAnswers
    if currentAnswers[a] == topic:
        global score
        score += 1
    currentAnswers = newAnswers()

## Generates the next question
def newQuestion():
    topic = wikipedia.random(1)

    question = None
    while question is None:
        try:
            question = wikipedia.summary(topic, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            print(e)

    for x in topic.split():
        question = question.replace(x, "____")

    return question.replace("_ _", "_")

## Generates the next answer
def newAnswers():
    global topic
    global alternate_options
    alternates = wikipedia.random(alternate_options)
    choices = []
    choices.extend(alternates)
    choices.append(topic)
    shuffle(choices)
    prefixes = [i for i in range(len(choices))]
    answers = dict(zip(prefixes, choices))
    return answers

## -- Frame Variables --##
WELCOME_HEIGHT = 600
WELCOME_WIDTH = 800
GAME_HEIGHT = 800
GAME_WIDTH = 1200
WELCOME_GEOMETRY = getGeometry(WELCOME_WIDTH, WELCOME_HEIGHT)
GAME_GEOMETRY = getGeometry(GAME_WIDTH, GAME_HEIGHT)
BACKGROUND_COLOR = 'deep sky blue'

## -- Initial Frame -- ##
welcomeWindow = Tk()
welcomeWindow.title("endlessTrivia")
welcomeWindow.geometry(WELCOME_GEOMETRY)
welcomeWindow.configure(background=BACKGROUND_COLOR)
titleLabel = Label(welcomeWindow, text="~ Title ~", anchor="center", font=("Helvetica", 62), bg=BACKGROUND_COLOR)
titleLabel.place(x=WELCOME_WIDTH/2, y=WELCOME_HEIGHT*0.3, anchor="center")

## -- Run the Game -- ##
def startGame(difficulty):

    ## Update the number of options
    global alternate_options
    alternate_options = difficulty2Options[difficulty]

    ## Setup the Game Window
    gameWindow = Toplevel(welcomeWindow)
    gameWindow.geometry(GAME_GEOMETRY)
    gameWindow.configure(background=BACKGROUND_COLOR)
    questionLabel = Label(gameWindow, text=currentQuestion, anchor="center", font=("Helvetica", 20), bg=BACKGROUND_COLOR)
    questionLabel.place(x=GAME_WIDTH/2, y=GAME_HEIGHT*0.1, anchor="center")
    scoreLabel = Label(gameWindow, text=score, anchor="center", font=("Helvetica", 20), bg=BACKGROUND_COLOR)
    scoreLabel.place(x=GAME_WIDTH*0.9, y=GAME_HEIGHT*0.9, anchor="center")
    buttons = dict.fromkeys([i for i in range(alternate_options)])
    
    ## Update the text on the screen, on-click
    def updateText():
        questionLabel.configure(text=currentQuestion)
        scoreLabel.configure(text=score)
        for key in buttons.keys():
            if buttons[key] is not None:
                buttons[key].configure(text=currentAnswers[key])
        gameWindow.after(1, updateText)
    updateText()
    
    ## Place the buttons
    for key in buttons.keys():
        buttons[key] = Button(gameWindow, text=currentAnswers[key], command=partial(answered, key), bg='powder blue', font=("Helvetica", 20))
        buttons[key].place(x = GAME_WIDTH/2, y = GAME_HEIGHT*(0.3+key/10), anchor='center')

## -- Start the Opening Window -- ##
if __name__ == "__main__":
    currentQuestion = newQuestion()
    currentAnswers = newAnswers()

    i = 1
    for key in difficulty2Options.keys():
        button = Button(welcomeWindow, text=key, command=partial(startGame, key), bg='powder blue', font=("Helvetica", 30))
        button.place(x=WELCOME_WIDTH/(len(difficulty2Options) + 1)*i , y=WELCOME_HEIGHT*0.67, anchor="center")
        i += 1

    welcomeWindow.mainloop()

