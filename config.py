import pygame

STAGES = {
    "MENU": 0,
    "LEVEL_SELECTION": 1,
    "GAMEPLAY": 2,
    "RELAXATION": 3,
    "VICTORY": 4,
    "DEFEAT": 5
}

WIDTH = 1280
HEIGHT = 720

LEVELS = [
    {
        "name": "Джуниор", 
        "difficulty": 1, 
        "boss_health": 100, 
        "speed": 2
    },
    {
        "name": "Миддл", 
        "difficulty": 2, 
        "boss_health": 150, 
        "speed": 3
    },
    {
        "name": 
        "Сеньор", 
        "difficulty": 3, 
        "boss_health": 200, 
        "speed": 4
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
    "DARK_RED": (200, 35, 51)
}