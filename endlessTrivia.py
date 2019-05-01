import wikipedia
import string
from random import shuffle
import re

## -- Variables -- ##
alphabet = dict(enumerate(string.ascii_lowercase, 1))
rerun = True
reselect = True
score = 0
question = ""
difficulty2Options = {'easy': 3, 'medium': 4, 'hard': 5}

## -- Main -- ##
if __name__ == '__main__':

    ## Keep playing the game
    while rerun:

        ## Select your level
        while reselect:
            game_level = input("Choose the difficulty (Easy/Medium/Hard):  ")

            if game_level.lower() in difficulty2Options.keys():
                alternate_options = difficulty2Options[game_level.lower()]
                reselect = False
            else:
              print("Difficulty not supported! Try again!")  

        ## Get a wikipedia topic
        topic = wikipedia.random(1)
        alternates = wikipedia.random(alternate_options)

        ## Get the question
        try:
            question = wikipedia.summary(topic, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            print("Sorry, try again!")

        for x in topic.split():
            question = question.replace(x, "____")
        question = question.replace("_ _", "_")

        ## Get the answers
        choices = []
        choices.extend(alternates)
        choices.append(topic)
        shuffle(choices)
        prefixes = []
        for x in range(len(choices)):
            prefixes.append(alphabet[x+1])
        answers = dict(zip(prefixes, choices))

        ## Display the question & answers
        print(question)
        for key in answers:
            print("%s) %s" % (key, answers[key]))

        ## Get the user's selection
        selection = input("Choose your answer:  ")

        ## Respond to the user
        if selection in answers.keys():
            if answers[selection] == topic:
                print("Correct!")
                score += 1
            else:
                print("Incorrect :( ")
                print("the correct answer was %s" % topic)
        else:
            print("Invalid choice!")
            print("the correct answer was %s" % topic)

        ## Evaluate whether to keep playing
        rerun = input("Your score is %s, would you like to keep playing? (yes/no) " % str(score))
        rerun = rerun.lower() == "yes"
