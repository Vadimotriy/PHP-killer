import pygame


def load_level(name):
    with open(name) as file:
        map_level = map(lambda x: list(map(int, list(x))), file.read().split('\n'))
    return list(map_level)

class Map:
    def __init__(self, game, name):
        self.game = game
        self.map = load_level(name)
        self.walls = self.get_map()

    def get_map(self):
        walls = []
        for row in range(9):
            for column in range(16):
                if self.map[row][column]:
                    walls.append((row, column))
        return walls

    def draw(self):
        for row, column in self.walls:
            pygame.draw.rect(self.game.screen, '#FFFFFF', (column * 100, row * 100, 100, 100), 2)