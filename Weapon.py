import pygame

from Sprites import AnimatedSpite
from collections import deque


class Weapon(AnimatedSpite):  # класс оружия (анимированный спрайт)
    def __init__(self, game):  # инициализация
        super().__init__(game, (1, 1), 'Data/Sprites/gun', 5, scale=3.0, time=90)
        self.images = deque([pygame.transform.scale(pygame.image.load(i).convert_alpha(), (153 * 3, 194 * 3))
                             for i in self.images])
        self.weapon_pos = (800 - (153 * 3) // 2, 900 - (194 * 3))
        self.number = 1
        self.reloading = False

    def shoot(self):  # стрельба
        if self.reloading:  # сделать новый выстрел можно только когда револьвер в "спокойном состоянии"
            self.game.player.shoot = False
            if self.state:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.number += 1
                if self.number == 6:
                    self.reloading = False
                    self.number = 1

    def draw(self):  # отрисовка оружия
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):  # обновление
        self.check_time()
        self.shoot()
