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

# Глобальные переменные
game_stage = STAGES.get("MENU")
current_level = None
normal_font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 120, bold=True)
running = True
clock = pygame.time.Clock()
current_offset_x, current_offset_y = 0, 0
target_offset_x, target_offset_y = 0, 0
last_beat_time = 0
player_health = None
enemy_health = None
combo = 0
stamina = 3
binary_codes = []

# Загрузка ресурсов
def load_images():
    images = {
        "character": pygame.image.load(PATHS.get("IMG") + 'character.png'),
        "junior_enemy": pygame.image.load(PATHS.get("ENEMIES") + 'junior_enemy.png'),
        "middle_enemy": pygame.image.load(PATHS.get("ENEMIES") + 'middle_enemy.png'),
        "senior_enemy": pygame.image.load(PATHS.get("ENEMIES") + 'senior_enemy.png'),
        "victory_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'victory_background.png').convert(), (1400, 800)),
        "defeat_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'defeat_background.png').convert(), (1400, 800)),
        "title_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'title_screen_background.png').convert(), (1400, 800)),
        "level_select_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'level_selection_background.png').convert(), (1400, 800)),
        "junior_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'junior_gameplay_background.png').convert(), (1400, 800)),
        "middle_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'middle_gameplay_background.png').convert(), (1400, 800)),
        "senior_bg": pygame.transform.scale(pygame.image.load(PATHS.get("BGS") + 'senior_gameplay_background.png').convert(), (1400, 800))
    }
    return images

images = load_images()

# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
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
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pos)

# Создание кнопок
def create_buttons():
    buttons = {
        "title_quit": Button(705, HEIGHT//2 + 100, 300, 100, "Выйти", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
        "title_play": Button(275, HEIGHT//2 + 100, 300, 100, "Играть", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
        "level_easy": Button(300, HEIGHT//2 + 100, 200, 100, LEVELS[0].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
        "level_medium": Button(540, HEIGHT//2 + 100, 200, 100, LEVELS[1].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
        "level_hard": Button(780, HEIGHT//2 + 100, 200, 100, LEVELS[2].get("NAME"), COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
        "game_back": Button(20, 20, 90, 60, "Back", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED")),
        "end_back": Button(WIDTH/2-150, HEIGHT/3*2, 300, 100, "Back", COLORS.get("CHILL_RED"), COLORS.get("DARK_RED"))
    }
    return buttons

buttons = create_buttons()

# Утилиты
def create_binary_code():
    binary_text = "".join(random.choice(["0", "1"]) for _ in range(8))
    binary_codes.append({
        "text": binary_text,
        "x": WIDTH/4,
        "y": HEIGHT/2,
        "speed": 10
    })

def draw_shadow(surface, shape, dimensions, color=COLORS.get("SHADOW_COLOR")):
    shadow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    if shape == "rect":
        pygame.draw.rect(shadow_surface, color, dimensions, border_radius=15)
    elif shape == "ellipse":
        pygame.draw.ellipse(shadow_surface, color, dimensions)
    surface.blit(shadow_surface, (0, 0))

def draw_health_bar(surface, x, y, width, height, current, max_value, border_color=COLORS.get("BLACK"), fill_color=COLORS.get("RED")):
    pygame.draw.rect(surface, border_color, (x, y, width, height), border_radius=5)
    fill_width = (width - 20) * (current / max_value)
    pygame.draw.rect(surface, fill_color, (x + 10, y + 10, fill_width, height - 20), border_radius=5)

def draw_title(surface, text, y_offset=HEIGHT/6):
    title_text = title_font.render(text, True, COLORS.get("WHITE"))
    surface.blit(title_text, (WIDTH//2 - title_text.get_width()//2, y_offset))

# Отрисовка экранов
def draw_beat_timer(surface):
    draw_shadow(surface, "rect", (WIDTH/2-75, HEIGHT/2-75, 150, 150))
    
    sin = math.sin(((pygame.time.get_ticks()-last_beat_time)/(60/LEVELS[current_level].get("SPEED")*1000)) * math.pi)
    beat_size = 49 - 24 * sin
    beat_color = COLORS.get("GREEN") if sin < 0.2 else COLORS.get("RED")

    pygame.draw.circle(surface, beat_color, (WIDTH//2, HEIGHT//2), int(beat_size))
    pygame.draw.circle(surface, COLORS.get("WHITE"), (WIDTH//2, HEIGHT//2), int(beat_size) + 4, 2)

def draw_screen_with_background(surface, background_key, title_text=None, buttons_to_draw=None):
    surface.blit(images[background_key], (-60 + bg_offset_x, -40 + bg_offset_y))
    
    if title_text:
        draw_title(surface, title_text)
    
    if buttons_to_draw:
        for button_key in buttons_to_draw:
            buttons[button_key].draw(surface)

def draw_gameplay(surface):
    level_keys = ["junior", "middle", "senior"]
    current_key = level_keys[current_level]
    
    draw_screen_with_background(surface, f"{current_key}_bg")
    surface.blit(images[f"{current_key}_enemy"], (WIDTH/8*7-250, HEIGHT/6*2.75))
    
    # Health bars
    draw_health_bar(surface, WIDTH/8*7-200, HEIGHT/6*2, 200, 40, enemy_health, LEVELS[current_level].get("HEALTH"))
    draw_health_bar(surface, WIDTH/8*2-150, HEIGHT/6*2, 200, 40, player_health, 100)
    
    # Shadows
    draw_shadow(surface, "ellipse", (WIDTH/8, HEIGHT/6*5.35, 200, 60))
    draw_shadow(surface, "ellipse", (WIDTH/8*7-200, HEIGHT/6*5.35, 200, 60))
    draw_shadow(surface, "rect", (WIDTH/2-100, -25, 200, 225))
    
    # Character and UI
    surface.blit(images["character"], (WIDTH/8-65, HEIGHT/6*2.75))
    buttons["game_back"].draw(surface)
    
    # Text info
    info_texts = [
        f"YOUR HEALTH: {player_health}",
        f"HEALTH: {enemy_health}/{LEVELS[current_level].get('HEALTH')}",
        f"SPEED: {LEVELS[current_level].get('SPEED')}",
        f"NAME: {LEVELS[current_level].get('NAME')}",
        f"COMBO: {combo}",
        f"STAMINA: {stamina}"
    ]
    
    for i, text in enumerate(info_texts):
        text_surface = normal_font.render(text, True, COLORS.get("WHITE"))
        surface.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT/30 * (i+1)))
    
    # Binary codes
    for code in binary_codes[:]:
        code["x"] += code["speed"] 
        if code["x"] > WIDTH: 
            binary_codes.remove(code)
        else:
            code_text = normal_font.render(code["text"], True, COLORS.get("GREEN"))
            surface.blit(code_text, (code["x"], code["y"]))
    
    draw_beat_timer(surface)

# Основной игровой цикл
while running:
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    # Параллакс эффект
    target_offset_x = (mouse_pos[0] - 640) / 640
    target_offset_y = (mouse_pos[1] - 360) / 360
    current_offset_x += (target_offset_x - current_offset_x) * SMOOTH_FACTOR
    current_offset_y += (target_offset_y - current_offset_y) * SMOOTH_FACTOR
    bg_offset_x = int(current_offset_x * PARALLAX_STRENGTH * 200)
    bg_offset_y = int(current_offset_y * PARALLAX_STRENGTH * 200)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif game_stage == STAGES.get("MENU"):
            for btn in ["title_play", "title_quit"]:
                buttons[btn].check_hover(mouse_pos)
                if buttons[btn].is_clicked(mouse_pos, event):
                    if btn == "title_play":
                        game_stage = STAGES.get("LEVEL_SELECTION")
                    else:
                        running = False
        
        elif game_stage == STAGES.get("LEVEL_SELECTION"):
            for i, level_key in enumerate(["level_easy", "level_medium", "level_hard"]):
                buttons[level_key].check_hover(mouse_pos)
                if buttons[level_key].is_clicked(mouse_pos, event):
                    level_music = ["junior_music", "middle_music", "senior_music"][i]
                    pygame.mixer.music.load(PATHS.get("MUSIC") + f"{level_music}.mp3")
                    pygame.mixer.music.play()
                    game_stage = STAGES.get("GAMEPLAY")
                    player_health = 100
                    enemy_health = LEVELS[i].get("HEALTH")
                    current_level = i
        
        elif game_stage == STAGES.get("GAMEPLAY"):
            buttons["game_back"].check_hover(mouse_pos)
            if buttons["game_back"].is_clicked(mouse_pos, event):
                player_health = enemy_health = current_level = None
                game_stage = STAGES.get("MENU")
                stamina = 3
                pygame.mixer.music.stop()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sin_val = math.sin(((current_time-last_beat_time)/(60/LEVELS[current_level].get("SPEED")*1000)) * math.pi)
                
                if sin_val < 0.2:  # Успешное попадание в ритм
                    create_binary_code() 
                    enemy_health -= DAMAGE
                    combo += 1
                    stamina = 3
                    
                    if enemy_health <= 0:
                        player_health = enemy_health = current_level = None
                        game_stage = STAGES.get("VICTORY")
                        stamina = combo = 0
                        pygame.mixer.music.stop()
                else:  # Промах
                    combo = 0
                    player_health -= DAMAGE
                    stamina -= 1
                    
                    if stamina <= 0 or player_health <= 0:
                        player_health = enemy_health = current_level = None
                        game_stage = STAGES.get("DEFEAT")
                        stamina = 3
                        pygame.mixer.music.stop()
        
        elif game_stage in [STAGES.get("DEFEAT"), STAGES.get("VICTORY")]:
            buttons["end_back"].check_hover(mouse_pos)
            if buttons["end_back"].is_clicked(mouse_pos, event):
                game_stage = STAGES.get("MENU")
    
    # Обновление битов
    if game_stage == STAGES.get("GAMEPLAY") and current_time - last_beat_time > (60/LEVELS[current_level].get("SPEED")*1000):
        last_beat_time = current_time
    
    # Отрисовка экранов
    if game_stage == STAGES.get("DEFEAT"):
        draw_screen_with_background(screen, "defeat_bg", "Поражение((", ["end_back"])
    elif game_stage == STAGES.get("VICTORY"):
        draw_screen_with_background(screen, "victory_bg", "Победа!!", ["end_back"])
    elif game_stage == STAGES.get("MENU"):
        draw_screen_with_background(screen, "title_bg", "Wi-Fight", ["title_play", "title_quit"])
    elif game_stage == STAGES.get("LEVEL_SELECTION"):
        draw_screen_with_background(screen, "level_select_bg", "Выбери уровень:", ["level_easy", "level_medium", "level_hard"])
    elif game_stage == STAGES.get("GAMEPLAY"):
        draw_gameplay(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()