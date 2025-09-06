# Импорты

import pygame
import sys
import random
import math
from pygame import mixer
from config import *

# Инициализация

pygame.init()
mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wi-Fight")

game_stage = STAGES.get("MENU")

current_level = None

normal_font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 120, bold=True)

running = True

# Создание кнопок

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=8)
        
        text_surface = normal_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and (self.width+self.x>pos[0]>self.width)): #TODO
            return True
        return False


title_screen_quit_button = Button(WIDTH//2 + 50, HEIGHT//2 + 100, 300, 100, "Выйти", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
title_screen_play_button = Button(WIDTH//2 - 350, HEIGHT//2 + 100, 300, 100, "Играть", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

level_selection_screen_easy_button = Button(WIDTH//2 + 50, HEIGHT//2 + 100, 300, 100, LEVELS[0].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
level_selection_screen_medium_button = Button(WIDTH//2 + 50, HEIGHT//2 + 100, 300, 100, LEVELS[1].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
level_selection_screen_hard_button = Button(WIDTH//2 + 50, HEIGHT//2 + 100, 300, 100, LEVELS[2].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

# тайтл скрин

def draw_title_screen():

    screen.fill(COLORS.get("GRASS"))
    pygame.draw.rect(screen, COLORS.get("DARK_SKY"), [0, 0, WIDTH, HEIGHT/3.5])
    pygame.draw.rect(screen, COLORS.get("MEDIUM_SKY"), [0, HEIGHT/3.5, WIDTH, HEIGHT/6])
    pygame.draw.rect(screen, COLORS.get("LIGHT_SKY"), [0, HEIGHT/3.5+HEIGHT/6, WIDTH, HEIGHT/9])

    title_text = title_font.render("Wi-Fight", True, COLORS.get("WHITE"))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT/6))
    
    title_screen_quit_button.draw(screen)
    title_screen_play_button.draw(screen)

# выбор уровня

def draw_level_selection():

    screen.fill(COLORS.get("BLACK"))

    title_text = title_font.render("Выбери уровень:", True, COLORS.get("WHITE"))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT/6))

    for button in level_selection_buttons:
        button.draw(screen)

# процессы игровые

while running:

    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
        if game_stage == STAGES.get("MENU"):
            play_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)
            
            if(play_button.is_clicked(mouse_pos, event)):
                game_stage = STAGES.get("LEVEL_SELECTION")
            
            elif(quit_button.is_clicked(mouse_pos, event)):
                running = False

        if game_stage == STAGES.get("LEVEL_SELECTION"):
            pass

        

    if(game_stage == STAGES.get("MENU")):
        draw_title_screen()
    if(game_stage == STAGES.get("LEVEL_SELECTION")):
        draw_level_selection()

    pygame.display.flip()



pygame.quit()
sys.exit()