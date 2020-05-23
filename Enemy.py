import math

from constants import SCREEN_HEIGHT
from constants import SCREEN_WIDTH


class Enemy:
    def __init__(self, caste=None, x=500, y=50):
        self.x = x
        self.y = y
        self.type = caste
        if not self.type:
            self.hp = 3
            self.speed = 1.5
        elif self.type == "shooter" or self.type == "sniper" or self.type == "superSniper":
            self.hp = 2
            self.speed = 0.5
        elif self.type == "breeder":
            self.hp = 15
            self.speed = 0.4
        elif self.type == "warper":
            self.speed = 1
            self.hp = 2
        elif self.type == "warrior":
            self.speed = 2.2
            self.hp = 5
        elif self.type == "breeder2" or self.type == "friend":
            self.hp = 25
            self.speed = 0.5

    def hit(self, enemy_list, damage):
        self.hp -= damage
        if self.hp <= 0:
            try:
                enemy_list.remove(self)
            finally:
                del self
                return True, enemy_list
        return False, enemy_list

    def get_vector(self, p):
        dx = p.x - self.x
        dy = p.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        m = self.speed / distance
        return dx, dy, distance, m

    def move(self, player, count=0):
        dx, dy, distance, m = self.get_vector(player)

        if self.type == "friend":
            if distance <= 50 and 0 < self.y < 600 and 1000 > self.x > 0:
                self.x -= dx * m
                self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m

        elif self.type is None or self.type == "warper":
            self.x += dx * m
            self.y += dy * m

        elif self.type == "warrior":
            self.x += dx * m * (2 / 3)
            self.y += dy * m * (2 / 3)
            if count % 120 <= 60:
                self.x -= dy * m / 3
                self.y += dx * m / 3
            else:
                self.x += dy * m / 2
                self.y -= dx * m / 2

        elif self.type == "shooter":
            if distance <= 200:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m

        elif self.type == "sniper":
            if distance <= 400:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m

        elif self.type == "breeder":
            if distance <= 100 and 5 < self.y < SCREEN_HEIGHT-5 and SCREEN_WIDTH-5 > self.x > 5:
                self.x -= dx * m
                self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m

        elif self.type == "breeder2":
            if distance <= 250:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m

        elif self.type == "superSniper":
            if distance <= 450:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
