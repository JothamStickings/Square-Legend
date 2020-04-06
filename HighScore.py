# -------------------------------------------------------------------------------
# Name:       Highscore
# Purpose:
#
# Author:      JothamStickings
#
# Created:     05/12/2018
# Copyright:   (c) ph2stickings 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import sqlite3
from graphics import *


class TableAlreadyExistsError(Exception):
    pass


class HighScoreTable:

    def __init__(self, filename=":memory:"):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()

    def create_table(self):
        try:
            self.c.execute("""
                  CREATE TABLE tblHighScores
                 (name STRING,
                  score INT)""")

            self.conn.commit()
        except sqlite3.OperationalError:
            raise TableAlreadyExistsError

    def enter_score(self, name, score):
        self.c.execute("INSERT INTO tblHighScores VALUES (:n, :s)", {'n': name, 's': score})
        self.conn.commit()

    def display_table(self):
        scores = GraphWin("High Scores", 400, 500)
        scores.setBackground("black")
        self.c.execute("SELECT name, score FROM tblHighScores ORDER BY score DESC")
        scorelist = self.c.fetchall()

        if not scorelist:
            txt = Text(Point(200, 200), "No Scores Available")
            txt.setFill("white")
            txt.draw(scores)
        elif len(scorelist) < 11:
            for row in range(1, 3):
                for column in range(1, 11):
                    rect = Rectangle(Point(row * 100, column * 40), Point(row * 100 + 100, column * 40 + 40))
                    rect.setFill("black")
                    rect.setOutline("white")
                    rect.draw(scores)

            for p in range(1, len(scorelist) + 1):
                nam = Text(Point(150, p * 40 + 20), scorelist[p - 1][0])
                scr = Text(Point(250, p * 40 + 20), scorelist[p - 1][1])
                nam.setFill("white")
                scr.setFill("white")
                nam.draw(scores)
                scr.draw(scores)

        else:
            for row in range(1, 3):
                for column in range(1, 11):
                    rect = Rectangle(Point(row * 100, column * 40), Point(row * 100 + 100, column * 40 + 40))
                    rect.setFill("black")
                    rect.setOutline("white")
                    rect.draw(scores)

            for p in range(1, 11):
                nam = Text(Point(150, p * 40 + 20), scorelist[p - 1][0])
                scr = Text(Point(250, p * 40 + 20), scorelist[p - 1][1])
                nam.setFill("white")
                scr.setFill("white")
                nam.draw(scores)
                scr.draw(scores)

        try:
            scores.getMouse()
            scores.close()
        except GraphicsError:
            pass


def main():
    tab = HighScoreTable(":memory:")
    tab.create_table()
    tab.display_table()
    for i in range(10):
        tab.enter_score("death", i * 10)
    tab.enter_score("Me", 78)
    tab.display_table()
    pass


if __name__ == '__main__':
    main()
