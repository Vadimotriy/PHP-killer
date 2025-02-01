import pygame

from Constants import *


class Texturing:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.walltextures()

    def draw(self):
        self.object_render()

    def object_render(self):
        object_list = self.game.raytracing.object_to_rendering
        for depth, image, pos in object_list:
            self.screen.blit(image, pos)

    def texture_change(self, path):  # преобразование текстур
        return pygame.transform.scale((pygame.image.load(path).convert_alpha()), (256, 256))

    def walltextures(self):  # перенос текстур
        return {
            1: self.texture_change('Data/Sprites/wall_1.png'),
            2: self.texture_change('Data/Sprites/wall_2.jpg'),
            3: self.texture_change('Data/Sprites/wall_3.jpg')}
