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

clock = pygame.time.Clock()

character = pygame.image.load(PATHS.get("IMG")+'character.png')

junior_enemy = pygame.image.load(PATHS.get("ENEMIES")+'junior_enemy.png')
middle_enemy = pygame.image.load(PATHS.get("ENEMIES")+'middle_enemy.png')
senior_enemy = pygame.image.load(PATHS.get("ENEMIES")+'senior_enemy.png')

title_screen_background_image = pygame.transform.scale(pygame.image.load(PATHS.get("BGS")+'title_screen_background.png').convert(), (1400, 800))
level_selection_background_image = pygame.transform.scale(pygame.image.load(PATHS.get("BGS")+'level_selection_background.png').convert(), (1400, 800))
junior_gameplay_background_image = pygame.transform.scale(pygame.image.load(PATHS.get("BGS")+'junior_gameplay_background.png').convert(), (1400, 800))
middle_gameplay_background_image = pygame.transform.scale(pygame.image.load(PATHS.get("BGS")+'middle_gameplay_background.png').convert(), (1400, 800))
senior_gameplay_background_image = pygame.transform.scale(pygame.image.load(PATHS.get("BGS")+'senior_gameplay_background.png').convert(), (1400, 800))

current_offset_x, current_offset_y = 0, 0
target_offset_x, target_offset_y = 0, 0
last_beat_time = 0

player_health = None
enemy_health = None

combo = 0
stamina = 3

binary_codes = []

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
        if (event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)):
            return True
        return False

title_screen_quit_button = Button(705, HEIGHT//2 + 100, 300, 100, "Выйти", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
title_screen_play_button = Button(275, HEIGHT//2 + 100, 300, 100, "Играть", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

level_selection_screen_easy_button = Button(300, HEIGHT//2 + 100, 200, 100, LEVELS[0].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
level_selection_screen_medium_button = Button(540, HEIGHT//2 + 100, 200, 100, LEVELS[1].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
level_selection_screen_hard_button = Button(780, HEIGHT//2 + 100, 200, 100, LEVELS[2].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

gameplay_back_button = Button(20, 20, 90, 60, "Back", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))

# бит таймер)

def draw_beat_timer():

    shadow_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, COLORS.get("SHADOW_COLOR"), (WIDTH/2-75, HEIGHT/2-75, 150, 150), border_radius=15)
    screen.blit(shadow_surface, (0, 0))

    sin = math.sin(((current_time-last_beat_time)/(60/LEVELS[current_level].get("SPEED")*1000)) * math.pi)
    beat_size = 49 - 24 * sin
    beat_color = COLORS.get("GREEN") if sin<0.2 else COLORS.get("RED")

    pygame.draw.circle(screen, beat_color, (WIDTH//2, HEIGHT//2), int(beat_size))
    pygame.draw.circle(screen, COLORS.get("WHITE"), (WIDTH//2, HEIGHT//2), int(beat_size) + 4, 2)

# тайтл скрин

def draw_title_screen():

    screen.blit(title_screen_background_image, (-60 + bg_offset_x, -40 + bg_offset_y))

    title_text = title_font.render("Wi-Fight", True, COLORS.get("WHITE"))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT/6))
    
    title_screen_quit_button.draw(screen)
    title_screen_play_button.draw(screen)

# выбор уровня

def draw_level_selection():

    screen.blit(level_selection_background_image, (-60 + bg_offset_x, -40 + bg_offset_y))

    title_text = title_font.render("Выбери уровень:", True, COLORS.get("WHITE"))
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT/6))

    level_selection_screen_easy_button.draw(screen)
    level_selection_screen_medium_button.draw(screen)
    level_selection_screen_hard_button.draw(screen)

# геймплей

def draw_gameplay():

    if(current_level==0):
        screen.blit(junior_gameplay_background_image, (-60 + bg_offset_x, -40 + bg_offset_y))
        screen.blit(junior_enemy, (WIDTH/8*7-250, HEIGHT/6*2.75))
    if(current_level==1):
        screen.blit(middle_gameplay_background_image, (-60 + bg_offset_x, -40 + bg_offset_y))
        screen.blit(middle_enemy, (WIDTH/8*7-250, HEIGHT/6*2.75))
    if(current_level==2):
        screen.blit(senior_gameplay_background_image, (-60 + bg_offset_x, -40 + bg_offset_y))
        screen.blit(senior_enemy, (WIDTH/8*7-250, HEIGHT/6*2.75))

    shadow_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surface, COLORS.get("SHADOW_COLOR"), (WIDTH/8, HEIGHT/6*5.35, 200, 60))
    pygame.draw.ellipse(shadow_surface, COLORS.get("SHADOW_COLOR"), (WIDTH/8*7-200, HEIGHT/6*5.35, 200, 60))
    screen.blit(shadow_surface, (0, 0))

    shadow_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, COLORS.get("SHADOW_COLOR"), (WIDTH/2-100, -25, 200, 225), border_radius=15)
    screen.blit(shadow_surface, (0, 0))

    screen.blit(character, (WIDTH/8-65, HEIGHT/6*2.75))

    text = normal_font.render("YOUR HEALTH: "+str(player_health), True, COLORS.get("WHITE"))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT/30))
    gameplay_back_button.draw(screen)

    i = 2
    for key in LEVELS[current_level].keys():
        if(key=="HEALTH"):
            text = normal_font.render(str(key)+": "+str(enemy_health)+"/"+str(LEVELS[current_level].get(key)), True, COLORS.get("WHITE"))
        else:
            text = normal_font.render(str(key)+": "+str(LEVELS[current_level].get(key)), True, COLORS.get("WHITE"))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT/30*i))
        i+=1
    
    text = normal_font.render("STAMINA: "+str(stamina), True, COLORS.get("WHITE"))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT/30*7))

    draw_beat_timer()


# процессы игровые

while(running):

    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    target_offset_x = (mouse_pos[0] - 640) / 640
    target_offset_y = (mouse_pos[1] - 360) / 360

    current_offset_x += (target_offset_x - current_offset_x) * SMOOTH_FACTOR
    current_offset_y += (target_offset_y - current_offset_y) * SMOOTH_FACTOR

    bg_offset_x = int(current_offset_x * PARALLAX_STRENGTH * 200)
    bg_offset_y = int(current_offset_y * PARALLAX_STRENGTH * 200)

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
                pygame.mixer.music.load(PATHS.get("MUSIC")+"junior_music.mp3")
                pygame.mixer.music.play()
                game_stage = STAGES.get("GAMEPLAY")
                player_health = 100
                enemy_health = LEVELS[0].get("HEALTH")
                current_level = 0

            if(level_selection_screen_medium_button.is_clicked(mouse_pos, event)):
                pygame.mixer.music.load(PATHS.get("MUSIC")+"middle_music.mp3")
                pygame.mixer.music.play()
                game_stage = STAGES.get("GAMEPLAY")
                player_health = 100
                enemy_health = LEVELS[1].get("HEALTH")
                current_level = 1

            if(level_selection_screen_hard_button.is_clicked(mouse_pos, event)):
                pygame.mixer.music.load(PATHS.get("MUSIC")+"senior_music.mp3")
                pygame.mixer.music.play()
                game_stage = STAGES.get("GAMEPLAY")
                player_health = 100
                enemy_health = LEVELS[2].get("HEALTH")
                current_level = 2

        elif(game_stage == STAGES.get("GAMEPLAY")):

            gameplay_back_button.check_hover(mouse_pos)

            if(gameplay_back_button.is_clicked(mouse_pos, event)):
                player_health = None
                enemy_health = None
                current_level = None
                game_stage = STAGES.get("MENU")
                stamina=3
                pygame.mixer.music.stop()

            if(event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if(math.sin(((current_time-last_beat_time)/(60/LEVELS[current_level].get("SPEED")*1000)) * math.pi)<0.2):
                    enemy_health-=DAMAGE
                    combo+=1
                    stamina=3
                    if(enemy_health==0):
                        player_health = None
                        enemy_health = None
                        current_level = None
                        game_stage = STAGES.get("MENU")
                        stamina=3
                        pygame.mixer.music.stop()
                        combo=0
                else:
                    combo=0
                    player_health-=DAMAGE
                    stamina-=1
                    if(stamina==0):
                        player_health = None
                        enemy_health = None
                        current_level = None
                        game_stage = STAGES.get("MENU")
                        stamina=3
                        pygame.mixer.music.stop()

                    elif(player_health==0):
                        player_health = None
                        enemy_health = None
                        current_level = None
                        game_stage = STAGES.get("MENU")
                        stamina=3
                        pygame.mixer.music.stop()

    if(game_stage == STAGES.get("GAMEPLAY")):
        if(current_time-last_beat_time>(60/LEVELS[current_level].get("SPEED")*1000)):
            last_beat_time = current_time

    if(game_stage == STAGES.get("MENU")):
        draw_title_screen()
    if(game_stage == STAGES.get("LEVEL_SELECTION")):
        draw_level_selection()
    if(game_stage == STAGES.get("GAMEPLAY")):
        draw_gameplay()
    
    pygame.display.flip()
    clock.tick(60)



pygame.quit()
sys.exit()