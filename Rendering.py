import pygame
import math

from Constants import *


class Raytracing:  # класс отрисовки лучей
    def __init__(self, game):  # инициализация
        self.game = game
        self.raycasting_result = []
        self.object_to_texturing = []
        self.textures = self.game.texturing.wall_textures

    def get_objects_to_render(self):  # получаем объекты для рендера
        self.object_to_rendering = []
        for ray, data in enumerate(self.raycasting_result):
            depth, projection_screen, texture, offset = data

            wall = self.textures[texture].subsurface(offset * (256 - SCALE), 0, SCALE, 256)
            wall = pygame.transform.scale(wall, (SCALE, projection_screen))
            wall_pos = (ray * SCALE, 450 - projection_screen // 2)
            '''else:
                texture_height = 256 * HEIGHT / projection_screen
                wall = self.textures[texture].subsurface(offset * (256 - SCALE), 128 - texture_height // 2,
                                                         SCALE, texture_height)
                wall = pygame.transform.scale(wall, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)'''

            self.object_to_rendering.append((depth, wall, wall_pos))


    def ray_cast(self):  # отрисовка лучей, получаем точки для рендера
        self.raycasting_result.clear()
        texture_vert, texture_hort = 1, 1
        x, y = self.game.player.pos()
        x_map, y_map = self.game.player.floor_pos()
        ray_angle = self.game.player.angle - (PLAYER_FOV / 2) + 0.0001

        for ray in range(RAYS_NUM):
            sin = math.sin(ray_angle)
            cos = math.cos(ray_angle)

            # по горизонтали
            y_hort, dy = (y_map + 1, 1) if sin > 0 else (y_map - 1e-6, -1)
            depth_hort = (y_hort - y) / sin
            x_hort = x + depth_hort * cos

            delta_depth = dy / sin
            dx = delta_depth * cos

            for i in range(MAX_DEPTH):
                coords = int(y_hort), int(x_hort)
                if coords in self.game.map.walls:
                    texture_hort = self.game.map.map[coords[0]][coords[1]]
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
                if coords in self.game.map.walls:
                    texture_vert = self.game.map.map[coords[0]][coords[1]]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hort:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hort, texture_hort
                x_hort %= 1
                offset = (1 - x_hort) if sin > 0 else x_hort

            depth *= math.cos(self.game.player.angle - ray_angle)

            projection_screen = SCREEN_DIST / (depth + 0.0001)
            self.raycasting_result.append((depth, projection_screen, texture, offset))

            ray_angle += DELTA_ANGLE
