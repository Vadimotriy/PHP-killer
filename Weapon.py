import pygame

from Constants import *
from Sprites import AnimatedSpite
from collections import deque

class Weapon(AnimatedSpite):
    def __init__(self, game):
        super().__init__(game, (1, 1), 'Data/Sprites/gun', 5, scale=3.0, time=90)
        self.images = deque([pygame.transform.scale(pygame.image.load(i).convert_alpha(), (153 * 3, 194 * 3))
                             for i in self.images])
        self.weapon_pos = (800 - (153 * 3) // 2, 900 - (194 * 3))
        self.damage = 40
        self.number = 1
        self.reloading = False

    def shoot(self):
        if self.reloading:
            self.game.player.shoot = False
            if self.state:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.number += 1
                if self.number == 6:
                    self.reloading = False
                    self.number = 1


    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_time()
        self.shoot()
