import pygame

from Constants import *


class Sprite:
    def __init__(self, game, path='Data/Sprites/NPC/php.png', pos=(10.5, 3.5)):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.imagewidth = self.image.get_width()
        self.image_ratio = self.imagewidth / self.image.get_height()
        self.cx, self.cy, self.theta, self.x_screen, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1



    def sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist
        pwidth, pheight = proj * self.image_ratio, proj

        image = pygame.transform.scale(self.image, (pwidth, pheight))

        pos = self.x_screen - pwidth // 2, (HEIGHT // 2) - (pheight // 2)

        self.game.raytracing.object_to_rendering.append((self.norm_dist, image, pos))


    def sprite_get(self):
        cx = self.x - self.player.x
        cy = self.y - self.player.y
        self.cx, self.cy = cx, cy
        self.theta = math.atan2(cx, cy)

        delta = self.theta - self.player.angle
        if (cx > 0 and self.player.angle > math.pi) or (cx < 0 and cy < 0):
            delta += math.tau

        rays_delta = delta / DELTA_ANGLE
        self.x_screen = ((RAYS_NUM // 2) + rays_delta) * SCALE

        self.dist = math.hypot (cx, cy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.imagewidth // 2 < self.x_screen < (WIDTH + (self.imagewidth // 2)) and self.norm_dist > 0.5:
            self.sprite_projection()



    def update(self):
        self.sprite_get()


#  кароч
#  путь до php слоника (его размер 256x256)
#  'Data/Sprites/NPC/php.png'
