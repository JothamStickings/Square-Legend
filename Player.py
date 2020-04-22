import pygame


class Player:
    def __init__(self):
        self.x = 250
        self.y = 250
        self.hp = 5

    def hit(self, screen, damage=1):
        self.hp -= damage
        pygame.draw.rect(screen, (255, 255, 255), (int(self.y - 5), int(self.x - 5), 10, 10))
        if self.hp <= 0:
            return True
        return False