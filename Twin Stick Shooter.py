# Twin Stick Shooter

import pygame
from random import *
import math
from HighScore import *

highscores = HighScoreTable("SquareLegendHighscores.db")
try:
    highscores.create_table()
except TableAlreadyExistsError:
    pass


def display_instructions():
    instructions = GraphWin("Menu", 400, 500)
    instructions.setBackground("white")
    txt1 = Text(Point(200, 50), "Movement: WASD or Arrow Keys")
    txt1.setFill("black")
    txt1.setSize(12)
    txt1.draw(instructions)

    txt2 = Text(Point(200, 100), "Shoot: Hold Left Mouse Button")
    txt2.setFill("black")
    txt2.draw(instructions)

    txt3 = Text(Point(200, 150), "Jump: Middle Mouse Button or Space")
    txt3.setFill("black")
    txt3.draw(instructions)

    txt4 = Text(Point(200, 200), "Grenade: Right Mouse Button")
    txt4.setFill("black")
    txt4.draw(instructions)

    txt5 = Text(Point(200, 450), "Music: https://www.bensound.com")
    txt5.setFill("black")
    txt5.draw(instructions)

    txt6 = Text(Point(200, 475), "Sound: SwissArcadeGameEntertainment")
    txt6.setFill("black")
    txt6.draw(instructions)

    try:
        instructions.getMouse()
    except GraphicsError:
        pass
    instructions.close()


def get_name(score):
    box = GraphWin("Name", 200, 100)
    box.setBackground("black")
    name_box = Entry(Point(100, 50), 15)
    txt = Text(Point(40, 10), "Type Name:")
    txt.setFill("white")
    enter = Text(Point(150, 80), "Enter")
    enter.setFill("green")
    enter.draw(box)
    score_txt = "Final Score:" + str(score)
    final_score = Text(Point(50, 80), score_txt)
    final_score.setFill("white")
    final_score.draw(box)
    name_box.draw(box)
    txt.draw(box)
    try:
        box.getMouse()
    except GraphicsError:
        pass
    name = name_box.getText()
    box.close()
    return name


# initialise pygame
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


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


class Enemy:
    def __init__(self, type=None, x=500, y=50):
        self.x = x
        self.y = y
        self.type = type
        if not self.type:
            self.hp = 3
            self.speed = 1.5
        elif self.type == "shooter" or self.type == "sniper" or self.type == "friend" or self.type == "superSniper":
            self.hp = 2
            self.speed = 0.5
        elif self.type == "breeder" or self.type == "breeder2":
            self.hp = 15
            self.speed = 0.4
        elif self.type == "warper":
            self.speed = 1
            self.hp = 2
        elif self.type == "warrior":
            self.speed = 2.2
            self.hp = 5

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


class Item:
    def __init__(self, x, y, t):
        self.type = t
        self.x = x
        self.y = y

    def delete(self, l):
        try:
            l.remove(self)
            return l
        except ValueError:
            return l
        finally:
            del self


def touching(bullet, thing, width, height):
    if thing.y + height >= bullet.y >= thing.y - height:
        if thing.x + width >= bullet.x >= thing.x - width:
            return True
    return False


def check_on_screen(bullet, bullet_list):
    if bullet.y < 0 or bullet.x < 0 or bullet.y > 600 or bullet.x > 1000:
        return bullet.delete(bullet_list)
    return bullet_list


def teleport_player(tel, player, screen, change_x, change_y, charges):
    tel.play()
    pygame.draw.rect(screen, red, (int(player.x - 6), int(player.y - 6), 12, 12))
    player.x += change_x*50
    player.y += change_y*50
    if player.y > SCREEN_HEIGHT-5:
        player.y = SCREEN_HEIGHT-5
    if player.y < 5:
        player.y = 5
    if player.x > SCREEN_WIDTH-5:
        player.x = SCREEN_WIDTH-5
    if player.x < 5:
        player.x = 5
    pygame.draw.rect(screen, red, (int(player.x - 7), int(player.y - 7), 14, 14))
    return charges-1


def play_game():
    # useful definitions
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]

    # Screen setting up
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    pygame.display.set_caption("Game")

    clock = pygame.time.Clock()

    pygame.mixer.init()

    # sounds
    shot = pygame.mixer.Sound("sounds/Effects/Bass Drum/Wav/Bass Drum__001.wav")
    shot.set_volume(0.5)
    exp = pygame.mixer.Sound("sounds/Effects/Explosion2/Wav/Explosion2__008.wav")
    pickup = pygame.mixer.Sound("sounds/Effects/Pickup/Wav/Pickup__003.wav")
    pickup.set_volume(2)
    tel = pygame.mixer.Sound("sounds/Effects/Pew/Wav/Pew__008.wav")
    tel.set_volume(0.5)
    tel_enemy = pygame.mixer.Sound("sounds/Effects/Pew/Wav/Pew__008.wav")
    tel_enemy.set_volume(0.3)
    power = pygame.mixer.Sound("sounds/Effects/Powerup/Wav/Powerup__008.wav")
    power.set_volume(0.5)

    # Sets up the game loop that runs a frame of the game until done is True
    done = False
    player = Player()
    bullet_list = []
    enemy_bullet_list = []
    item_list = []
    enemy_list = []
    grenade_list = []
    enemy = Enemy()
    enemy_list.append(enemy)
    score = 0
    speed = 4
    damage = 1
    count = 0
    default_reload_speed = 1.5
    reload = default_reload_speed
    change_x = 0
    change_y = 0
    max_charges = 1
    charges = max_charges
    grenade_reload = 5

    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    pygame.mixer.music.load('sounds/Music/music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    while not done:
        screen.fill(white)
        mouse = pygame.mouse.get_pressed()

        played_shot = False

        if mouse[0]:
            if reload == 10:
                shot.play()
                played_shot = True
            if reload <= 0:
                if not played_shot:
                    shot.play()
                reload = default_reload_speed
                pos = pygame.mouse.get_pos()
                vx = pos[0] - player.x
                vy = pos[1] - player.y
                bullet = Bullet((vx, vy), int(player.x), int(player.y), speed, damage)
                bullet_list.append(bullet)

        change_x = 0
        change_y = 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 5:
            change_x = -1.25
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < SCREEN_WIDTH-5:
            change_x = 1.25
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y > 5:
            change_y = -1.25
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y < SCREEN_HEIGHT-5:
            change_y = 1.25
        if not (keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_s] or keys[pygame.K_w]):
            change_y = 0
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_a]):
            change_x = 0
        if change_x != 0 and change_y != 0:
            change_x *= 0.71
            change_y *= 0.71
        player.x += change_x
        player.y += change_y
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RCTRL or event.key == pygame.K_SPACE or event.key == pygame.K_SLASH) and charges > 0:
                    charges = teleport_player(tel, player, screen, change_x, change_y, charges)
            if pygame.mouse.get_pressed()[1] and event.type == pygame.MOUSEBUTTONDOWN and charges > 0:
                charges = teleport_player(tel, player, screen, change_x, change_y, charges)
            if pygame.mouse.get_pressed()[2] and event.type == pygame.MOUSEBUTTONDOWN and grenade_reload <= 0:
                grenade_reload = 5
                pos = pygame.mouse.get_pos()
                vx = pos[0] - player.x
                vy = pos[1] - player.y
                new_grenade = Grenade((vx, vy), int(player.x), player.y)
                grenade_list.append(new_grenade)

        if randint(0, 5000) <= 20 + score / 100 and len(enemy_list) <= 5 + score / 10:
            enemy = Enemy(None, SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 5000) <= 10 + score / 100 and len(enemy_list) <= 5 + score / 10:
            enemy = Enemy("shooter", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 5000) <= 5 + score / 100 and len(enemy_list) <= 5 + score / 10 and score >= 5:
            enemy = Enemy("sniper", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 5100) <= 1 + score / 200 and len(enemy_list) <= 5 + score / 10 and score >= 25:
            enemy = Enemy("breeder", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 5050) <= 4 + score / 200 and len(enemy_list) <= 5 + score / 10 and score >= 50:
            enemy = Enemy("warper", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 5050) <= 4 + score / 400 and len(enemy_list) <= 5 + score / 10 and score >= 100:
            enemy = Enemy("warrior", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 6000) <= 3 + score / 250 and len(enemy_list) <= 5 + score / 10 and score >= 125:
            enemy = Enemy("superSniper", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)
        elif randint(0, 5500) <= 1 + score / 400 and len(enemy_list) <= 5 + score / 10 and score >= 150:
            enemy = Enemy("breeder2", SCREEN_WIDTH//2+randint(-40, 40), randint(25, 75))
            enemy_list.append(enemy)

        pygame.draw.rect(screen, black, (int(player.x - 5), int(player.y - 5), 10, 10))

        for i in range(player.hp):
            pygame.draw.rect(screen, black, (0, i * 10, 10, 5))

        for i in range(speed - 4):
            pygame.draw.rect(screen, black, (15, i * 15, 2, 10))
            pygame.draw.rect(screen, black, (14, i * 15 + 1, 4, 1))

        for i in range(int((damage - 1) * 2)):
            pygame.draw.rect(screen, black, (25, i * 12, 9, 9))
            pygame.draw.rect(screen, white, (27, i * 12 + 1, 5, 7))
            pygame.draw.rect(screen, white, (26, i * 12 + 2, 7, 5))
            pygame.draw.rect(screen, black, (29, i * 12 + 1, 1, 7))
            pygame.draw.rect(screen, black, (26, i * 12 + 4, 7, 1))

        for i in range(1, charges+1):
            pygame.draw.rect(screen, black, (SCREEN_WIDTH-18, i * 10, 14, 2))
            pygame.draw.rect(screen, black, (SCREEN_WIDTH-8, i * 10 - 2, 2, 6))

        for item in item_list:
            if item.type == 0:
                pygame.draw.rect(screen, green, (int(item.x - 3), int(item.y - 1), 6, 2))
                pygame.draw.rect(screen, green, (int(item.x - 1), int(item.y - 3), 2, 6))
            elif item.type == 1:
                pygame.draw.rect(screen, red, (int(item.x - 3), int(item.y - 1), 6, 2))
                pygame.draw.rect(screen, red, (int(item.x - 1), int(item.y - 3), 2, 6))
            elif item.type == 2:
                pygame.draw.rect(screen, blue, (int(item.x - 3), int(item.y - 1), 6, 2))
                pygame.draw.rect(screen, blue, (int(item.x - 1), int(item.y - 3), 2, 6))
            if touching(player, item, 7, 7):
                if item.type == 0:
                    pickup.play()
                    player.hp += 1
                elif item.type == 1:
                    power.play()
                    item_choice = randint(0, 2)
                    if item_choice == 0 and speed <= 10:
                        speed += 1
                        default_reload_speed *= 0.93
                    elif item_choice == 0 and speed > 10:
                        item_choice = randint(1, 2)
                    if item_choice == 1:
                        damage += 0.5
                    if item_choice == 2:
                        f = Enemy("friend", int(player.x + 2), player.y + 4)
                        enemy_list.append(f)
                elif item.type == 2:
                    power.play()
                    max_charges += 1
                    charges = max_charges
                item_list = item.delete(item_list)

        for enemy in enemy_list:
            if not enemy.type:
                pygame.draw.rect(screen, black, (int(enemy.x - 5), int(enemy.y - 5), 10, 10))
                enemy.move(player, count)
                if touching(enemy, player, 5, 5):
                    done = player.hit(screen)
                    dead, enemy_list = enemy.hit(enemy_list, 1)
            elif enemy.type == "shooter":
                pygame.draw.rect(screen, black, (int(enemy.x - 3), int(enemy.y - 3), 6, 6))
                enemy.move(player)
                if randint(0, 120) <= 2:
                    vx = player.x - enemy.x
                    vy = player.y - enemy.y
                    bullet = Bullet((vx, vy), int(enemy.x), enemy.y)
                    enemy_bullet_list.append(bullet)
            elif enemy.type == "sniper":
                pygame.draw.rect(screen, black, (int(enemy.x - 3), int(enemy.y - 3), 6, 6))
                pygame.draw.rect(screen, black, (int(enemy.x - 5), int(enemy.y - 1), 10, 2))
                pygame.draw.rect(screen, black, (int(enemy.x - 1), int(enemy.y - 5), 2, 10))
                enemy.move(player)
                if randint(0, 500) <= 1:
                    vx = player.x - enemy.x
                    vy = player.y - enemy.y
                    bullet = Bullet((vx, vy), int(enemy.x), int(enemy.y), 8, 2)
                    enemy_bullet_list.append(bullet)
            elif enemy.type == "warper":
                enemy.move(player)
                pygame.draw.rect(screen, black, (int(enemy.x - 5), int(enemy.y - 5), 10, 10))
                pygame.draw.rect(screen, white, (int(enemy.x - 3), int(enemy.y - 3), 6, 6))
                dy = player.y - enemy.y
                dx = player.x - enemy.x
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if randint(0, 375) <= 1 and distance > 25:
                    tel_enemy.play()
                    pygame.draw.rect(screen, red, (int(enemy.x - 5), int(enemy.y - 5), 10, 10))
                    enemy.x += dx * 1.4
                    enemy.y += dy * 1.4
                    pygame.draw.rect(screen, red, (int(enemy.x - 5), int(enemy.y - 5), 10, 10))
                if touching(enemy, player, 5, 5):
                    done = player.hit(screen)
                    dead, enemy_list = enemy.hit(enemy_list, 1)
            elif enemy.type == "warrior":
                enemy.move(player, count)
                pygame.draw.rect(screen, black, (int(enemy.x - 4), int(enemy.y - 4), 9, 9))
                pygame.draw.rect(screen, white, (int(enemy.x - 2), int(enemy.y - 3), 5, 7))
                pygame.draw.rect(screen, white, (int(enemy.x - 3), int(enemy.y - 2), 7, 5))
                pygame.draw.rect(screen, black, (int(enemy.x), int(enemy.y - 3), 1, 7))
                pygame.draw.rect(screen, black, (int(enemy.x - 3), int(enemy.y), 7, 1))
                if randint(0, 240) <= 2:
                    vx = player.x - enemy.x
                    vy = player.y - enemy.y
                    bullet = Bullet((vx, vy), int(enemy.x), enemy.y)
                    enemy_bullet_list.append(bullet)
                if touching(enemy, player, 7, 7):
                    done = player.hit(screen)
                    dead, enemy_list = enemy.hit(enemy_list, 1)
            elif enemy.type == "friend":
                enemy.move(player)
                pygame.draw.rect(screen, black, (int(enemy.x - 5), int(enemy.y - 2), 10, 4))
                pygame.draw.rect(screen, black, (int(enemy.x - 2), int(enemy.y - 5), 4, 10))
                for e in enemy_list:
                    if e.type != "friend":
                        if randint(0, 500) <= 1:
                            vx = e.x - enemy.x
                            vy = e.y - enemy.y
                            bullet = Bullet((vx, vy), int(enemy.x), enemy.y)
                            bullet_list.append(bullet)
            elif enemy.type == "breeder":
                pygame.draw.rect(screen, black, (int(enemy.x - 15), int(enemy.y - 15), 30, 30))
                pygame.draw.rect(screen, black, (int(enemy.x - 20), int(enemy.y - 5), 40, 10))
                pygame.draw.rect(screen, black, (int(enemy.x - 5), int(enemy.y - 20), 10, 40))
                enemy.move(player)
                if randint(0, 500) <= 3 and len(enemy_list) <= 5 + score / 10:
                    temp = Enemy(None, int(enemy.x), enemy.y)
                    enemy_list.append(temp)
            elif enemy.type == "breeder2":
                pygame.draw.rect(screen, black, (int(enemy.x - 15), int(enemy.y - 15), 30, 30))
                pygame.draw.rect(screen, black, (int(enemy.x - 20), int(enemy.y - 5), 40, 10))
                pygame.draw.rect(screen, black, (int(enemy.x - 5), int(enemy.y - 20), 10, 40))
                pygame.draw.rect(screen, white, (int(enemy.x - 3), int(enemy.y - 10), 6, 20))
                pygame.draw.rect(screen, white, (int(enemy.x - 10), int(enemy.y - 3), 20, 5))
                enemy.move(player)
                if randint(0, 500) <= 3 and len(enemy_list) <= 5 + score / 10:
                    if randint(0, 1) == 0:
                        temp = Enemy("shooter", int(enemy.x), enemy.y)
                        enemy_list.append(temp)
                    else:
                        temp = Enemy("sniper", int(enemy.x), enemy.y)
                        enemy_list.append(temp)
                if randint(0, 200) <= 3:
                    b = Bullet((1, 0), int(enemy.x), enemy.y)
                    enemy_bullet_list.append(b)
                    b = Bullet((0, 1), int(enemy.x), enemy.y)
                    enemy_bullet_list.append(b)
                    b = Bullet((-1, 0), int(enemy.x), enemy.y)
                    enemy_bullet_list.append(b)
                    b = Bullet((0, -1), int(enemy.x), enemy.y)
                    enemy_bullet_list.append(b)
            elif enemy.type == "superSniper":
                pygame.draw.rect(screen, black, (int(enemy.x - 3), int(enemy.y - 3), 6, 6))
                pygame.draw.rect(screen, black, (int(enemy.x - 7), int(enemy.y - 1), 14, 2))
                pygame.draw.rect(screen, black, (int(enemy.x - 1), int(enemy.y - 7), 2, 14))
                pygame.draw.rect(screen, white, (int(enemy.x - 2), int(enemy.y - 1), 4, 2))
                pygame.draw.rect(screen, white, (int(enemy.x - 1), int(enemy.y - 2), 2, 4))
                enemy.move(player)
                if randint(0, 500) <= 1:
                    vx = player.x - enemy.x
                    vy = player.y - enemy.y
                    distance = math.sqrt(vx ** 2 + vy ** 2)
                    vx += change_x * (distance / 8)
                    vy += change_y * (distance / 8)
                    bullet = Bullet((vx, vy), int(enemy.x), int(enemy.y), 8, 2)
                    enemy_bullet_list.append(bullet)

        for bullet in bullet_list:
            pygame.draw.rect(screen, black, (int(bullet.x - 1), int(bullet.y - 1), 2, 2))
            bullet.move()
            for enemy in enemy_list:
                if enemy.type == "breeder" or enemy.type == "breeder2":
                    size = 15
                else:
                    size = 5
                if touching(bullet, enemy, size, size) and enemy.type != "friend":
                    bullet_list = bullet.delete(bullet_list)
                    dead, enemy_list = enemy.hit(enemy_list, bullet.damage)
                    if dead:
                        score += 1
                        if randint(0, 15) == 9:
                            item = Item(int(enemy.x), int(enemy.y), 0)
                            item_list.append(item)
                        if randint(1, 15) == 1 and enemy.type == "sniper":
                            item = Item(int(enemy.x), int(enemy.y), 1)
                            item_list.append(item)
                        if randint(1, 5) == 2 and enemy.type == "warper":
                            item = Item(int(enemy.x), int(enemy.y), 2)
                            item_list.append(item)
                        elif randint(1, 3) == 2 and (enemy.type == "breeder"
                                                     or enemy.type == "breeder2"
                                                     or enemy.type == "superSniper"):
                            item = Item(int(enemy.x), int(enemy.y), 1)
                            item_list.append(item)
                        elif randint(1, 5) == 3 and (enemy.type == "warrior"):
                            item = Item(int(enemy.x), int(enemy.y), 1)
                            item_list.append(item)
                        charges = max_charges
            bullet_list = check_on_screen(bullet, bullet_list)

        for bullet in enemy_bullet_list:
            pygame.draw.rect(screen, black, (int(bullet.x - 1), int(bullet.y - 1), 2, 2))
            bullet.move()
            if touching(bullet, player, 5, 5):
                enemy_bullet_list = bullet.delete(enemy_bullet_list)
                done = player.hit(screen, bullet.damage)
            enemy_bullet_list = check_on_screen(bullet, enemy_bullet_list)

        for grenade in grenade_list:
            pygame.draw.rect(screen, black, (int(grenade.x - 2), int(grenade.y - 2), 4, 4))
            if grenade.get_life() < 90 and 520 % grenade.get_life() == 0:
                pygame.draw.rect(screen, white, (int(grenade.x - 2), int(grenade.y - 2), 4, 4))
            life = grenade.move()
            grenade_list = check_on_screen(grenade, grenade_list)
            if life == 10:
                exp.play()
            if life <= 3:
                pygame.draw.rect(screen, black, (int(grenade.x - 15), int(grenade.y - 15), 30, 30))
            if life == 0:
                pygame.draw.rect(screen, black, (int(grenade.x - 25), int(grenade.y - 25), 50, 50))
                for enemy in enemy_list:
                    if touching(enemy, grenade, 20, 20):
                        enemy.hit(enemy_list, grenade.damage)
                    if touching(enemy, grenade, 30, 30):
                        enemy.hit(enemy_list, grenade.damage-1)
                if touching(player, grenade, 20, 20):
                    done = player.hit(screen, grenade.damage)
                if touching(player, grenade, 30, 30):
                    done = player.hit(screen, grenade.damage-2)
                grenade.delete(grenade_list)

        clock.tick(60)
        count += 1
        reload -= 0.1
        grenade_reload -= 0.1

        pygame.display.flip()

        # quits pygame
    pygame.quit()

    name = get_name(score)
    if name != "":
        highscores.enter_score(name, score)


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
            play_game()
        elif 340 <= y <= 360 and 183 <= x <= 218:
            break
        elif 390 <= y <= 410 and 160 <= x <= 240:
            highscores.display_table()
        elif 440 <= y <= 460 and 165 <= x <= 235:
            display_instructions()

    menu.close()
