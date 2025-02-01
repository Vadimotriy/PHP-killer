import pygame
import sys
#import pandas

from Constants import *
from Rendering import *
from Map import Map
from Player import Player
from Texturing import *


def load_image(name, colorkey=None):  # функция по загрузке изображений
    image = pygame.image.load(name)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def terminate():  # функция по выходу из игры
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):  # класс кнопок
    def __init__(self, spite_group, y):
        super().__init__(spite_group)
        image = pygame.Surface((400, 70))
        image.fill('#AAAAAA')
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 600, y

    def update(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


class Game:  # сама игра
    def __init__(self):  # инициализация
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PHP killer')
        self.clock = pygame.time.Clock()
        self.level = 1
        self.delta = 1

    def start_screen(self):  # стартовое окно
        background = load_image('Data/Sprites/background_start_screen.png')
        self.screen.blit(background, (0, 0))

        self.font = pygame.font.Font(None, 50)
        text = [self.font.render('Играть', True, '#FFFFFF'),
                self.font.render('Таблица лидеров', True, '#FFFFFF')]

        button_play = pygame.sprite.Group()  # кнопка играть
        play_button = Button(button_play, 200 - 20)
        button_play.draw(self.screen)
        self.screen.blit(text[0], (WIDTH // 2 - text[0].get_width() // 2, 200))

        button_table = pygame.sprite.Group()  # кнопка таблицы лидеров
        table_button = Button(button_table, 300 - 20)
        button_table.draw(self.screen)
        self.screen.blit(text[1], (WIDTH // 2 - text[1].get_width() // 2, 300))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.update(event.pos):  # переход к игре
                        return True
                    elif table_button.update(event.pos):  # переход к таблице лидеров
                        self.table()

                        self.screen.blit(background, (0, 0))
                        button_play.draw(self.screen)
                        self.screen.blit(text[0], (WIDTH // 2 - text[0].get_width() // 2, 200))
                        button_table.draw(self.screen)
                        self.screen.blit(text[1], (WIDTH // 2 - text[1].get_width() // 2, 300))

            pygame.display.flip()
            self.clock.tick(FPS)

    '''def table(self):  # таблица лидеров
        background = load_image('Data/Sprites/background_start_screen.png')
        self.screen.blit(background, (0, 0))

        csv = pandas.read_csv('Data/table_leaders.csv', sep=',')
        csv = csv.sort_values(by=['points'], ascending=False)

        names = list(csv['name'].head(4))
        names = list(map(lambda x: self.font.render(x, True, '#FFFFFF'), names))
        points = list(csv['points'].head(4))
        points = list(map(lambda x: self.font.render(str(x), True, '#FFFFFF'), points))
        info = [(self.font.render('Имя', True, '#FFFFFF'),
                 self.font.render('Очки', True, '#FFFFFF'))]
        x, y = 200, 100
        for i, j in info + list(zip(names, points)):  # вывод результатов
            self.screen.blit(i, (x, y))
            self.screen.blit(j, (x + 650, y))
            y += 150

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:  # возврат к стартовому окну
                    return True

            pygame.display.flip()
            self.clock.tick(FPS)'''

    def new_game(self):  # запуск новой игры
        self.map = Map(self, f'Data/Maps/level_{self.level}.txt')
        self.player = Player(self)
        pygame.mouse.set_visible(False)
        self.texturing = Texturing(self)
        self.raytracing = Raytracing(self)
        self.run()

    def run(self):  # запуск
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        terminate()

            self.player.update()
            self.raytracing.ray_cast()
            self.raytracing.get_objects_to_render()

            self.texturing.draw()

            pygame.display.flip()
            self.delta = self.clock.tick(FPS)