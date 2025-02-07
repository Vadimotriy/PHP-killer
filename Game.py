import sys
import pandas
import time
import pygame.mixer

from Rendering import *
from Map import Map
from Player import Player
from Texturing import *
from Sprites import AllObjects
from Weapon import Weapon


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
    def __init__(self, spite_group, y):  # инициализация
        super().__init__(spite_group)
        image = pygame.Surface((400, 70))
        image.fill('#AAAAAA')
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 600, y

    def update(self, pos):  # обновление
        if self.rect.collidepoint(pos):  # использование collide
            return True
        return False


class Sound:  # класс звуков
    def __init__(self, game):  # инициализация микшера
        self.game = game
        pygame.mixer.init()
        self.sounds()

    def sounds(self):  # коллекция звуков
        self.gun = pygame.mixer.Sound('Data/Sprites/gun/audio.mp3')
        self.kill = pygame.mixer.Sound('Data/Sprites/NPC/audio.mp3')
        self.win = pygame.mixer.Sound('Data/win.mp3')


class Game:  # сама игра
    def __init__(self):  # инициализация
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('PHP killer')
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.csv = pandas.read_csv('Data/table_leaders.csv', sep=',')  # csv таблица с таблицей лидеров

        self.level = 0
        self.delta = 1

    def start_screen(self):  # стартовое окно
        background = load_image('Data/Sprites/background_start_screen.png')
        self.screen.blit(background, (0, 0))

        font = pygame.font.Font('Data/font/minecraft-ten-font-cyrillic.ttf', 25)
        text = [font.render('Играть', True, '#FFFFFF'),
                font.render('Таблица лидеров', True, '#FFFFFF')]

        button_play = pygame.sprite.Group()  # кнопка играть
        play_button = Button(button_play, 200 - 20)
        button_play.draw(self.screen)
        self.screen.blit(text[0], (WIDTH // 2 - text[0].get_width() // 2, 200))

        button_table = pygame.sprite.Group()  # кнопка таблицы лидеров
        table_button = Button(button_table, 300 - 20)
        button_table.draw(self.screen)
        self.screen.blit(text[1], (WIDTH // 2 - text[1].get_width() // 2, 300))

        while True:  # цикл
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # цикл
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.update(event.pos):  # переход к игре
                        self.start_time = time.time()  # засекаем время
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

    def table(self):  # таблица лидеров
        background = load_image('Data/Sprites/background_start_screen.png')
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font('Data/font/minecraft-ten-font-cyrillic.ttf', 30)

        self.csv = self.csv.sort_values(by=['points'], ascending=True)  # сортируем csv

        names = list(self.csv['name'].head(4))
        names = list(map(lambda x: font.render(x, True, '#FFFFFF'), names))
        points = list(self.csv['points'].head(4))
        points = list(map(lambda x: font.render(str(x), True, '#FFFFFF'), points))
        info = [(font.render('Имя', True, '#FFFFFF'),
                 font.render('Время, сек', True, '#FFFFFF'))]
        x, y = 200, 100
        for i, j in info + list(zip(names, points)):  # вывод результатов
            self.screen.blit(i, (x, y))
            self.screen.blit(j, (x + 650, y))
            y += 150

        while True:  # цикл
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # выход
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:  # возврат к стартовому окну при любом клике
                    return True

            pygame.display.flip()
            self.clock.tick(FPS)

    def new_game(self):  # запуск нового уровня
        self.level += 1
        pygame.mouse.set_visible(False)

        self.map = Map(self, f'Data/Maps/level_{self.level}.txt')  # создание всех объектов
        self.player = Player(self)
        self.texturing = Texturing(self)
        self.raytracing = Raytracing(self)
        self.all_objects = AllObjects(self)
        self.all_objects.new_level()
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.num_php = NUMBER_OF_PHPS[self.level]

        self.run()

    def run(self):  # цикл основной игры
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:  # если нажат Esc, то закрытие
                    if event.key == 27:
                        terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:  # при клике левой кнопке мыши стрельба
                    if event.button == 1:
                        self.player.shooting()

            self.player.update()  # обновление всех классов
            self.raytracing.update()
            self.all_objects.update()
            self.weapon.update()

            self.texturing.draw()  # отрисовка карты и оружия
            self.weapon.draw()

            if self.num_php == 0:  # выход из цикла если все слоники убиты
                break

            pygame.display.flip()
            self.delta = self.clock.tick(FPS)

        if self.level != 3:  # переход к новому уровню
            self.show_text('Уровень пройден!', 100)
            self.new_game()
        else:  # завершение игры, запись в таблицу лидеров
            self.show_text('Победа!', 200)
            self.sound.win.play()
            end_time = time.time()
            name = self.nameget()
            self.csv.loc[-1] = [name, round(end_time - self.start_time)]
            self.csv.index += 1
            self.csv.to_csv('Data/table_leaders.csv', index=False)

    def show_text(self, text, size):  # вывод текста ('Победа!' или 'Уровень пройден!')
        def draw(text, size):
            self.screen.fill((0, 0, 0))
            font = pygame.font.Font('Data/font/minecraft-ten-font-cyrillic.ttf', size)
            text = font.render(text, True, (255, 0, 0))
            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = HEIGHT // 2 - text.get_height() // 2
            self.screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            time.sleep(3)

        draw(text, size)

    def nameget(self):  # получаем от игрока имя
        background = load_image('Data/Sprites/background_start_screen.png')
        self.screen.blit(background, (0, 0))

        font = pygame.font.Font('Data/font/minecraft-ten-font-cyrillic.ttf', 50)
        text = ''
        cz = font.render('введите имя', True, '#FFFFFF')
        while True:  # цикл ввода имени
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # завершение
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == 8 and text:  # Backspace
                        text = text[:-1]  # тест
                    elif event.key == 13 and text:  # Enter
                        return text
                    else:
                        if event.key in FG.keys():  # цифры, буквы на английском, пробел и _
                            text += str(FG[event.key])

            self.screen.blit(background, (0, 0))
            self.screen.blit(cz, (WIDTH // 2 - cz.get_width() // 2, 100))

            text_render = font.render(text, True, '#FFFFFF')
            self.screen.blit(text_render, (100, HEIGHT // 2 - text_render.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(FPS)
