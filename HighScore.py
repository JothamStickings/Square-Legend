#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ph2stickings
#
# Created:     05/12/2018
# Copyright:   (c) ph2stickings 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sqlite3
from graphics import *

class HighScoreTable():

    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()

    def CreateTable(self):

        self.c.execute("""
                  CREATE TABLE tblHighScores
                 (name STRING,
                  score INT)""")

        self.conn.commit()

    def EnterScore(self, name, score):
        self.c.execute("INSERT INTO tblHighScores VALUES (:n, :s)", {'n': name, 's': score})
        self.conn.commit()

    def DisplayTable(self):
        scores = GraphWin("High Scores", 400, 500)
        scores.setBackground("black")
        self.c.execute("SELECT name, score FROM tblHighScores ORDER BY score DESC")
        scorelist = self.c.fetchall()


        if scorelist == []:
            txt = Text(Point(200, 200), "No Scores Available")
            txt.setFill("white")
            txt.draw(scores)
        elif len(scorelist) < 11:
            for row in range(1,3):
                for column in range(1, 11):
                    rect = Rectangle(Point(row*100, column*40), Point(row*100+100, column*40+40))
                    rect.setFill("black")
                    rect.setOutline("white")
                    rect.draw(scores)

            for p in range(1, len(scorelist)+1):
                nam = Text(Point(150, p*40+20), scorelist[p-1][0])
                scr = Text(Point(250, p*40+20), scorelist[p-1][1])
                nam.setFill("white")
                scr.setFill("white")
                nam.draw(scores)
                scr.draw(scores)

        else:
            for row in range(1,3):
                for column in range(1, 11):
                    rect = Rectangle(Point(row*100, column*40), Point(row*100+100, column*40+40))
                    rect.setFill("black")
                    rect.setOutline("white")
                    rect.draw(scores)

            for p in range(1, 11):
                nam = Text(Point(150, p*40+20), scorelist[p-1][0])
                scr = Text(Point(250, p*40+20), scorelist[p-1][1])
                nam.setFill("white")
                scr.setFill("white")
                nam.draw(scores)
                scr.draw(scores)

        try:
            scores.getMouse()
            scores.close()
        except:
            pass


def main():
    tab = HighScoreTable(":memory:")
    tab.CreateTable()
    tab.DisplayTable()
    for i in range(10):
        tab.EnterScore("death", i*10)
    tab.EnterScore("Me", 78)
    tab.DisplayTable()
    pass

if __name__ == '__main__':
    main()
