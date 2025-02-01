import pygame
import math

from Constants import *


class Raytracing:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
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

            pygame.draw.line(self.game.screen, 'yellow', (100 * x, 100 * y),
                             (100 * x + 100 * depth * cos, 100 * y + 100 * depth * sin), 2)

            ray_angle += DELTA_ANGLE
