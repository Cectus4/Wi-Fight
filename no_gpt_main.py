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
        if (event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)): #TODO
            return True
        return False

def calc_pos(n, w, ind):
    f = WIDTH-ind*2-w*n
    arr = [ind]
    for i in range(n-1):
        arr.append(arr[-1]+w+f//(n-1))
    return arr

#print(calc_pos(2, 300, 275))
#print(calc_pos(3, 200, 300))
print(calc_pos(2, 300, 50))

title_screen_quit_button = Button(275, HEIGHT//2 + 100, 300, 100, "Выйти", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
title_screen_play_button = Button(705, HEIGHT//2 + 100, 300, 100, "Играть", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

level_selection_screen_easy_button = Button(300, HEIGHT//2 + 100, 200, 100, LEVELS[0].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
level_selection_screen_medium_button = Button(540, HEIGHT//2 + 100, 200, 100, LEVELS[1].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
level_selection_screen_hard_button = Button(780, HEIGHT//2 + 100, 200, 100, LEVELS[2].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

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

    level_selection_screen_easy_button.draw(screen)
    level_selection_screen_medium_button.draw(screen)
    level_selection_screen_hard_button.draw(screen)

# геймплей

def draw_gameplay():
    
    screen.fill(COLORS.get("GRASS"))
    pygame.draw.rect(screen, COLORS.get("DARK_SKY"), [0, 0, WIDTH, HEIGHT/3.5])
    pygame.draw.rect(screen, COLORS.get("MEDIUM_SKY"), [0, HEIGHT/3.5, WIDTH, HEIGHT/6])
    pygame.draw.rect(screen, COLORS.get("LIGHT_SKY"), [0, HEIGHT/3.5+HEIGHT/6, WIDTH, HEIGHT/9])
    pygame.draw.rect(screen, COLORS.get("BLACK"), [50, HEIGHT/3, 300, HEIGHT/5*2.5])
    pygame.draw.rect(screen, COLORS.get("BLACK"), [930, HEIGHT/3, 300, HEIGHT/5*2.5])
    pygame.draw.ellipse(screen, COLORS.get("WHITE"), [930, HEIGHT/3, 300, HEIGHT/5*2.5])
    pygame.draw.ellipse(screen, COLORS.get("WHITE"), [50, HEIGHT/3, 300, HEIGHT/5*2.5])

    i = 1
    for key in LEVELS[current_level].keys():
        text = normal_font.render(str(key)+": "+str(LEVELS[current_level].get(key)), True, COLORS.get("WHITE"))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT/18*i))
        i+=1

# процессы игровые

while(running):

    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():

        if(event.type == pygame.QUIT):
            running = False
            
        elif(game_stage == STAGES.get("MENU")):
            title_screen_play_button.check_hover(mouse_pos)
            title_screen_quit_button.check_hover(mouse_pos)
            
            if(title_screen_play_button.is_clicked(mouse_pos, event)):
                game_stage = STAGES.get("LEVEL_SELECTION")
            
            elif(title_screen_quit_button.is_clicked(mouse_pos, event)):
                running = False

        elif(game_stage == STAGES.get("LEVEL_SELECTION")):
            level_selection_screen_easy_button.check_hover(mouse_pos)
            level_selection_screen_medium_button.check_hover(mouse_pos)
            level_selection_screen_hard_button.check_hover(mouse_pos)

            if(level_selection_screen_easy_button.is_clicked(mouse_pos, event)):
                game_stage = STAGES.get("GAMEPLAY")
                current_level = 0

            if(level_selection_screen_medium_button.is_clicked(mouse_pos, event)):
                game_stage = STAGES.get("GAMEPLAY")
                current_level = 1

            if(level_selection_screen_hard_button.is_clicked(mouse_pos, event)):
                game_stage = STAGES.get("GAMEPLAY")
                current_level = 2

        elif(game_stage == STAGES.get("GAMEPLAY")):
            pass

    if(game_stage == STAGES.get("MENU")):
        draw_title_screen()
    if(game_stage == STAGES.get("LEVEL_SELECTION")):
        draw_level_selection()
    if(game_stage == STAGES.get("GAMEPLAY")):
        draw_gameplay()

    pygame.display.flip()



pygame.quit()
sys.exit()