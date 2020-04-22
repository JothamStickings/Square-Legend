import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


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

    def move(self, player, count=0):
        if self.type == "friend":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            if distance <= 50 and 0 < self.y < 600 and 1000 > self.x > 0:
                self.x -= dx * m
                self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
        if self.type is None or self.type == "warper":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            self.x += dx * m
            self.y += dy * m
        elif self.type == "warrior":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            self.x += dx * m * (2 / 3)
            self.y += dy * m * (2 / 3)
            if count % 120 <= 60:
                self.x -= dy * m / 3
                self.y += dx * m / 3
            else:
                self.x += dy * m / 2
                self.y -= dx * m / 2
        elif self.type == "shooter":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            if distance <= 200:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
        elif self.type == "sniper":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            if distance <= 400:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
        elif self.type == "breeder":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            if distance <= 100 and 5 < self.y < SCREEN_HEIGHT-5 and SCREEN_WIDTH-5 > self.x > 5:
                self.x -= dx * m
                self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
        elif self.type == "breeder2":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            if distance <= 250:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
        elif self.type == "superSniper":
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            m = self.speed / distance
            if distance <= 450:
                if SCREEN_WIDTH-5 > self.x > 5:
                    self.x -= dx * m
                if 5 < self.y < SCREEN_HEIGHT-5:
                    self.y -= dy * m
            else:
                self.x += dx * m
                self.y += dy * m
