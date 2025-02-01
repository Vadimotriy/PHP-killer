import pygame


from Constants import *


class Texturing:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.walltextures()

    def texture_change(self, path):
        return pygame.transform.scale((pygame.image.load(path).convert_alpha()), (256, 256))

    def walltextures(self):
        return {
            1: self.texture_change('Data/Sprites/wall_1.png'),
            2: self.texture_change('Data/Sprites/wall_2.jpg'),
            3: self.texture_change('Data/Sprites/wall_3.jpg')}
