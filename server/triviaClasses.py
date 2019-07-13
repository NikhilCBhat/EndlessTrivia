'''
Ideal functions for Website
'''
import re
import wikipedia
import random

class QuestionObject(object):
    def __init__(self, numIncorrect=5):
        self.correctAnswer = wikipedia.random(1)
        self.allAnswers = wikipedia.random(numIncorrect)
        self.allAnswers.append(self.correctAnswer)
        random.shuffle(self.allAnswers)
        self.question = None
        while self.question is None:
            try:
                self.question = wikipedia.summary(self.correctAnswer, sentences=1)
            except wikipedia.exceptions.DisambiguationError:
                pass

        self.question = self.replaceWithBlanks(self.correctAnswer, self.question)

    def replaceWithBlanks(self, toReplace, sentence):
        for x in toReplace.split():
            pattern = re.compile(r'[\W_]+')
            x = pattern.sub('', x)
            reg = re.compile(r"\b%s\b" % x, re.IGNORECASE)
            sentence = reg.sub("_____", sentence)
        return sentence.replace("_ _", "_")

    def printQuestion(self):
        print(self.question)
        for i,v in enumerate(self.allAnswers):
            print(str(i+1)+".",v)

class Player(object):
    def __init__(self, name="", score=0):
        self.name = name
        self.score = score
    def __repr__(self):
        return "%s: %d"%(self.name, self.score)

class Leaderboard(object):
    def __init__(self, players=[]):
        self.players = players
    
    def addNewPlayer(self, player):
        self.players.append(player)
        self.players.sort(key=lambda x: x.score, reverse=True)
    
    def getTopPlayers(self, count):
        return self.players[0:count]