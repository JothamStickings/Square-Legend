from game import *
from HighScore import *

highscores = HighScoreTable("SquareLegendHighscores.db")
try:
    highscores.create_table()
except TableAlreadyExistsError:
    pass

if __name__ == "__main__":
    menu = GraphWin("Menu", 400, 500)
    menu.setBackground("white")
    title = Text(Point(200, 100), "Square\nLegend")
    title.setFill("black")
    title.setSize(30)
    title.draw(menu)
    play = Text(Point(200, 300), "Play")
    play.setFill("black")
    play.draw(menu)
    close = Text(Point(200, 350), "Close")
    close.setFill("black")
    close.draw(menu)
    hs = Text(Point(200, 400), "High Scores")
    hs.setFill("black")
    inst = Text(Point(200, 450), "Controls")
    inst.setFill("black")
    inst.draw(menu)
    hs.draw(menu)

    while True:
        try:
            click = menu.getMouse()
        except GraphicsError:
            menu.close()
            break
        y = click.getY()
        x = click.getX()

        if 290 <= y <= 310 and 183 <= x <= 218:
            play_game(highscores)
        elif 340 <= y <= 360 and 183 <= x <= 218:
            break
        elif 390 <= y <= 410 and 160 <= x <= 240:
            highscores.display_table()
        elif 440 <= y <= 460 and 165 <= x <= 235:
            display_instructions()

    menu.close()
