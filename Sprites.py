import pygame

from Constants import *
from collections import deque


class Sprite:
    def __init__(self, game, pos, path='Data/Sprites/NPC/php.png', scale=0.6, shift=0.45):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.imagewidth = self.image.get_width()
        self.image_ratio = self.imagewidth / self.image.get_height()
        self.cx, self.cy, self.theta, self.x_screen, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.scale = scale
        self.shift = shift

    def sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.scale
        pwidth, pheight = proj * self.image_ratio, proj

        image = pygame.transform.scale(self.image, (pwidth, pheight))

        shift = proj * self.shift
        pos = self.x_screen - pwidth // 2, (HEIGHT // 2) - (pheight // 2) + shift

        self.game.raytracing.object_to_rendering.append((self.norm_dist, image, pos))

    def sprite_get(self):
        cx = self.x - self.player.x
        cy = self.y - self.player.y
        self.cx, self.cy = cx, cy
        self.theta = math.atan2(cy, cx)

        delta = self.theta - self.player.angle
        if (cx > 0 and self.player.angle > math.pi) or (cx < 0 and cy < 0):
            delta += math.tau

        rays_delta = delta / DELTA_ANGLE
        self.x_screen = ((RAYS_NUM // 2) + rays_delta) * SCALE

        self.dist = math.hypot(cx, cy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.imagewidth // 2 < self.x_screen < (WIDTH + (self.imagewidth // 2)) and self.norm_dist > 0.5:
            self.sprite_projection()

    def update(self):  # обновление
        self.sprite_get()


class AnimatedSpite(Sprite):  # класс анимированных спрайтов (для оружия и врагов)
    def __init__(self, game, pos, path, max_num, scale=1.0, shift=0.0, time=120):  # инициализация
        super().__init__(game, pos, f'{path}/1.png', scale, shift)
        self.time = time
        self.time_prev = pygame.time.get_ticks()

        self.path = path
        self.max_num = max_num
        self.state = False

        self.get_images()

    def get_images(self):  # получаем все изображения для спрайта
        self.images = deque()
        for i in range(1, self.max_num + 1):
            self.images.append(f'{self.path}/{i}.png')

    def check_time(self):  # проверяем нужно ли поменять изображение для спрайта
        self.state = False
        now = pygame.time.get_ticks()
        if now - self.time_prev > self.time:
            self.time_prev = now
            self.state = True

    def animate(self):  # меняем изображение в спрайте
        if self.state:
            self.images.rotate(-1)
            self.image = pygame.image.load(self.images[0]).convert_alpha()

    def update(self):  # обновление
        super().update()
        self.check_time()
        self.animate()


class AllObjects:  # класс, в котором хранятся все объекты
    def __init__(self, game):  # инициализация
        self.game = game
        self.list = []

        for i in OBJECTS_COORDS[self.game.level]:
            self.list.append(Sprite(self.game, i))

    def update(self):  # обновление
        for i in self.list:
            i.update()
