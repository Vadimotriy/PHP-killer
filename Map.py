import pygame


def load_level(name):  # загрузка уровня из txt файла
    with open(name) as file:
        map_level = map(lambda x: list(map(int, list(x))), file.read().split('\n'))
    return list(map_level)


class Map:  # класс карты
    def __init__(self, game, name):  # инициализация
        self.game = game
        self.map = load_level(name)
        self.walls = self.get_map()

    def get_map(self):  # поиск стен
        walls = []
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if self.map[row][column]:
                    walls.append((row, column))
        return walls

    def draw(self):  # тестовая отрисовка
        for row, column in self.walls:
            pygame.draw.rect(self.game.screen, '#FFFFFF', (column * 50, row * 50, 50, 50), 2)
