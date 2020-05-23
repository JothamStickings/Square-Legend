from Enemy import Enemy
from random import randint


class Spawn:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type_list = [None, None, None, None, None, None, None, None, "shooter", "shooter", "shooter", "shooter",
                          "shooter", "sniper", "sniper", "sniper", "warper", "warper", "warrior",
                          None, None, None, None, None, None, None, None, "shooter", "shooter", "shooter", "shooter",
                          "shooter", "sniper", "sniper", "sniper", "warper", "warper", "warrior",
                          "superSniper"]

    def get_enemy(self):
        enemy_type = self.type_list[randint(0, len(self.type_list)-1)]
        return Enemy(enemy_type, self.x, self.y)

    def __del__(self, spawn_list=None):
        if spawn_list is None:
            spawn_list = [self]
        try:
            spawn_list.remove(self)
        finally:
            del self
