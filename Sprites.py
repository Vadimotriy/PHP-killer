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

        self.alive = True

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

    def check_live(self):  # проверка жив ли слоник
        if self.game.player.shoot and self.check_walls():
            if 800 - 128 < self.x_screen < 800 + 128:
                self.game.player.shoot = False
                self.alive = False
                self.game.sound.kill.play()

    def check_walls(self):  # проверка, находится ли игрок в прямой видимости от слоника
        if self.game.player.floor_pos() == (int(self.x), int(self.y)):
            return True

        x, y = self.game.player.pos()
        x_map, y_map = self.game.player.floor_pos()
        wall_dist_vert, wall_dist_hort = 0, 0
        player_dist_vert, player_dist_hort = 0, 0

        sin = math.sin(self.theta)
        cos = math.cos(self.theta)

        # по горизонтали
        y_hort, dy = (y_map + 1, 1) if sin > 0 else (y_map - 1e-6, -1)
        depth_hort = (y_hort - y) / sin
        x_hort = x + depth_hort * cos

        delta_depth = dy / sin
        dx = delta_depth * cos

        for i in range(MAX_DEPTH):
            coords = int(y_hort), int(x_hort)
            if coords == (int(self.y), int(self.x)):
                player_dist_hort = depth_hort
                break
            if coords in self.game.map.walls:
                wall_dist_hort = depth_hort
                break
            x_hort += dx
            y_hort += dy
            depth_hort += delta_depth

        # по вертикале
        x_vert, dx = (x_map + 1, 1) if cos > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - x) / cos
        y_vert = y + depth_vert * sin

        delta_depth = dx / cos
        dy = delta_depth * sin

        for i in range(MAX_DEPTH):
            coords = int(y_vert), int(x_vert)
            if coords == (int(self.y), int(self.x)):
                player_dist_hort = depth_vert
                break
            if coords in self.game.map.walls:
                wall_dist_vert = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_vert, player_dist_hort)
        wall_dist = max(wall_dist_vert, wall_dist_hort)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def update(self):  # обновление
        if self.alive:
            self.check_live()
            self.sprite_get()

    def draw(self):  # тестовая отрисовка видимости
        pygame.draw.circle(self.game.screen, '#FF0000', (100 * self.x, 100 * self.y), 15)
        if self.check_walls():
            start_pos, end_pos = (100 * self.game.player.x, 100 * self.game.player.y), (100 * self.x, 100 * self.y)
            pygame.draw.line(self.game.screen, '#FFBB00', start_pos, end_pos)


class AnimatedSpite(Sprite):  # класс анимированных спрайтов (для оружия)
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

    def update(self):  # обновление
        for i in self.list:
            i.update()

    def new_level(self):  # загрузка объектов нового уровня
        self.list.clear()

        for i in OBJECTS_COORDS[self.game.level]:  # выставляем всех слоников на карту
            self.list.append(Sprite(self.game, i))
