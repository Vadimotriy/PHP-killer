import pygame

from Constants import *


class Texturing:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.walltextures()
        self.sky = self.texture_change('Data/Sprites/sky.jpg', (WIDTH, (HEIGHT // 2)))
        self.sky_offset = 0

    def draw(self):
        self.background_draw()
        self.object_render()

    def background_draw(self): #отрисовка заднего фона
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky, (-self.sky_offset, 0))
        self.screen.blit(self.sky, (-self.sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, (30, 30, 30), (0, (HEIGHT // 2), WIDTH, HEIGHT)) #пол

    def object_render(self):
        object_list = self.game.raytracing.object_to_rendering
        for depth, image, pos in object_list:
            self.screen.blit(image, pos)

    def texture_change(self, path, res=(256, 256)):  # преобразование текстур
        return pygame.transform.scale((pygame.image.load(path).convert_alpha()), res)

    def walltextures(self):  # перенос текстур
        return {
            1: self.texture_change('Data/Sprites/wall_1.png'),
            2: self.texture_change('Data/Sprites/wall_2.jpg'),
            3: self.texture_change('Data/Sprites/wall_3.jpg')}
