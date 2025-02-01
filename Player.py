import pygame
import math

from Constants import *


class Player:  # класс игрока
    def __init__(self, game):  # инициализация
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = 0

    def move(self):  # передвижение
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)

        move_x, move_y = 0, 0
        speed_x = cos * self.game.delta * PLAYER_SPEED
        speed_y = sin * self.game.delta * PLAYER_SPEED

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            move_x += speed_x
            move_y += speed_y
        if keys[pygame.K_a]:
            move_x += speed_y
            move_y -= speed_x
        if keys[pygame.K_s]:
            move_x -= speed_x
            move_y -= speed_y
        if keys[pygame.K_d]:
            move_x -= speed_y
            move_y += speed_x

        self.check_wall(move_x, move_y)
        self.angle %= 2 * math.pi

    def draw(self):  # тестовая отрисовка
        end = (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + HEIGHT * math.sin(self.angle))
        pygame.draw.line(self.game.screen, '#FF9900', (self.x * 100, self.y * 100), end, 2)
        pygame.draw.circle(self.game.screen, '#00FF00', (self.x * 100, self.y * 100), 10)

    def update(self):  # обновление данных
        self.move()
        self.draw()
        self.mouse()

    def check_wall(self, move_x, move_y):  # проверка стены
        def check(x, y):
            return True if (int(y), int(x)) not in self.game.map.walls else False

        scale = PLAYER_SIZE / self.game.delta
        if check(int(self.x + move_x * scale), self.y):
            self.x += move_x
        if check(self.x, int(self.y + move_y * scale)):
            self.y += move_y

    def mouse(self):
        x, y = pygame.mouse.get_pos()
        if x < BORDER_LEFT or x > BORDER_RIGHT or y < BORDER_LEFT or y > BORDER_DOWN:
            pygame.mouse.set_pos(800, 450)
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-MAX_REL, min(MAX_REL, self.rel))
        self.angle += self.rel * SENSIVITY * self.game.delta

    def pos(self):  # координата точная
        return self.x, self.y

    def floor_pos(self):  # координата клетки
        return int(self.x), int(self.y)
