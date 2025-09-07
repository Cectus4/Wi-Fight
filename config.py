STAGES = {
    "MENU": 0,
    "LEVEL_SELECTION": 1,
    "GAMEPLAY": 2,
    "VICTORY": 3,
    "DEFEAT": 4
}

WIDTH = 1280
HEIGHT = 720

LEVELS = [
    {
        "NAME": "Джуниор", 
        "DIFFICULTY": 1, 
        "HEALTH": 100, 
        "SPEED": 60
    },
    {
        "NAME": "Миддл", 
        "DIFFICULTY": 2, 
        "HEALTH": 150, 
        "SPEED": 90
    },
    {
        "NAME": "Сеньор", 
        "DIFFICULTY": 3, 
        "HEALTH": 200, 
        "SPEED": 120
    }
]

COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "LIGHT_SKY": (135, 206, 235),
    "MEDIUM_SKY": (0, 191, 255),
    "DARK_SKY": (25, 25, 112),
    "GRASS": (0, 102, 51),
    "CHILL_RED": (220, 53, 69),
    "DARK_RED": (200, 35, 51),
    "GREEN": (0, 255, 100),
    "RED": (255, 50, 50),
    "SHADOW_COLOR": (0, 0, 0, 100)
}

PARALLAX_STRENGTH = 0.05

SMOOTH_FACTOR = 0.1

PATHS = {
    "BGS": "img/bg/",
    "ENEMIES": "img/enemy/",
    "MUSIC": "music/",
    "IMG": "img/"
}

TIMING = 0.2

DAMAGE = 10

GAME_NAME = "Wi-Fight"

LABELS = {
    "QUIT": "Выход",
    "PLAY": "Играть",
    "BACK": "Вернуться"
}