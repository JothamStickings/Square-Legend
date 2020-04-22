import math


class Bullet:
    def __init__(self, vector, x, y, speed=4, damage=1):
        self.vector = vector
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage

    def move(self):
        vector = self.vector
        distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        multiplier = self.speed / distance
        self.x += vector[0] * multiplier
        self.y += vector[1] * multiplier

    def delete(self, bullet_list):
        try:
            bullet_list.remove(self)
            return bullet_list
        except ValueError:
            return bullet_list
        finally:
            del self


class Grenade:
    def __init__(self, vector, px, py, life=100):
        self.vector = vector
        self.x = px
        self.y = py
        self.life = life
        self.speed = 4
        self.damage = 4

    def move(self):
        vector = self.vector
        distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        multiplier = self.speed / distance
        self.speed *= 0.94
        self.life -= 1
        self.x += vector[0] * multiplier
        self.y += vector[1] * multiplier
        return self.life

    def get_life(self):
        return self.life

    def delete(self, grenade_list):
        try:
            grenade_list.remove(self)
            return grenade_list
        except ValueError:
            return grenade_list
        finally:
            del self