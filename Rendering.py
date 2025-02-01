import pygame
import math

from Constants import *


class Raytracing:  # класс отрисовки лучей
    def __init__(self, game):  # инициализация
        self.game = game

    def ray_cast(self):  # отрисовка лучей
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
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            depth = min(depth_vert, depth_hort)
            self.draw_wals(depth, ray, ray_angle)
            ray_angle += DELTA_ANGLE

    def draw_wals(self, depth, ray, ray_angle):  # отрисовка стен
        depth *= math.cos(self.game.player.angle - ray_angle)
        color = [255 / (1 + depth ** 5 * 0.00002) for _ in range(3)]

        projection_screen = SCREEN_DIST / (depth + 0.0001)
        rect = (ray * SCALE, (HEIGHT // 2) - projection_screen // 2, SCALE, projection_screen)

        pygame.draw.rect(self.game.screen, color, rect)
