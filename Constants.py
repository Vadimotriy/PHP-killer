import math

# базовые константы
WIDTH = 1600
HEIGHT = 900

FPS = 60

# настройки игрока
PLAYER_POS = (1.5, 5)
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE = 60

# настройка видимости игрока
PLAYER_FOV = math.pi / 3
RAYS_NUM = WIDTH // 2
DELTA_ANGLE = PLAYER_FOV / RAYS_NUM
MAX_DEPTH = 20

SCREEN_DIST = (WIDTH // 2) / math.tan(PLAYER_FOV / 2)
SCALE = 2

# настройки мыши
SENSIVITY = 0.0001
BORDER_LEFT = 400
BORDER_RIGHT = 1100
BORDER_DOWN = 500
MAX_REL = 40

# словарь с координатами PHP слоников
OBJECTS_COORDS = {
    1: ((6.5, 3.5), (1.5, 7.5), (13.5, 1.5), (8.3, 4.5), (11.5, 7.5)),
    2: (),
    3: ()
}