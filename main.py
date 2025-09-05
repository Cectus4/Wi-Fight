import pygame
import sys
import random
import math
from pygame import mixer

# Инициализация Pygame
pygame.init()
mixer.init()

# Размеры экрана
WIDTH, HEIGHT = 740, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кодовая Битва")

# Загрузка фоновых изображений для каждого уровня
backgrounds = []
try:
    # Фон для меню (оставляем цветной)
    # Фоны для уровней
    bg1 = pygame.image.load("images/backgrounds/background_1.png").convert()
    bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
    bg2 = pygame.image.load("images/backgrounds/background_2.png").convert()
    bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT))
    bg3 = pygame.image.load("images/backgrounds/background_3.png").convert()
    bg3 = pygame.transform.scale(bg3, (WIDTH, HEIGHT))
    backgrounds = [bg1, bg2, bg3]
except Exception as e:
    print(f"Не удалось загрузить фоны: {e}")
    backgrounds = []

# Загрузка изображения персонажа
character_img = None
try:
    character_img = pygame.image.load("images/character.png").convert_alpha()
    character_img = pygame.transform.scale(character_img, (200, 180))  # Уменьшили для нового разрешения
except Exception as e:
    print(f"Не удалось загрузить изображение персонажа: {e}")
    character_img = None

# Загрузка изображений врагов
enemy_images = []
try:
    for i in range(1, 4):  # enemy_1.png, enemy_2.png, enemy_3.png
        enemy_img = pygame.image.load(f"images/enemies/enemy_{i}.png").convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (140, 140))  # Уменьшили для нового разрешения
        enemy_images.append(enemy_img)
except Exception as e:
    print(f"Не удалось загрузить изображения врагов: {e}")
    enemy_images = []

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 255, 100)
RED = (255, 50, 50)
PURPLE = (180, 70, 255)
DARK_BLUE = (10, 20, 40)
LIGHT_BLUE = (100, 180, 255)
DARK_BG = (30, 30, 40, 200)  # Более нейтральный и прозрачный цвет для фона

# Шрифты
title_font = pygame.font.SysFont("Arial", 36, bold=True)  # Уменьшили шрифт
normal_font = pygame.font.SysFont("Arial", 18)  # Уменьшили шрифт
small_font = pygame.font.SysFont("Arial", 14)  # Уменьшили шрифт

# Состояния игры
MENU = 0
LEVEL_SELECTION = 1
GAMEPLAY = 2
RELAXATION = 3
VICTORY = 4
DEFEAT = 5

# Текущее состояние
game_state = MENU

# Уровни
levels = [
    {"name": "Новичок", "difficulty": 1, "boss_health": 100, "speed": 2},
    {"name": "Опытный", "difficulty": 2, "boss_health": 150, "speed": 3},
    {"name": "Эксперт", "difficulty": 3, "boss_health": 200, "speed": 4}
]
current_level = None

# Игровые переменные
boss_health = 0
score = 0
combo = 0
max_combo = 0
rhythm_timer = 0
rhythm_interval = 1000  # 1 секунда между битами
last_beat_time = 0
relaxation_start_time = 0
relaxation_duration = 15000  # 15 секунд релаксации
relaxation_phase_completed = False  # Флаг завершения фазы релаксации
miss_count = 0  # Счетчик промахов подряд

# Частицы
particles = []
binary_codes = []

# Функция для создания размытого фона
def create_blurred_background(background, blur_amount=40):  # Увеличили размытие
    scaled_bg = pygame.transform.scale(background, (WIDTH//blur_amount, HEIGHT//blur_amount))
    blurred_bg = pygame.transform.scale(scaled_bg, (WIDTH, HEIGHT))
    return blurred_bg

# Функция для создания виньетки
def create_vignette(width, height, intensity=70):
    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    for x in range(width):
        for y in range(height):
            # Вычисляем расстояние от центра
            dx = x - width/2
            dy = y - height/2
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Максимальное расстояние от центра до угла
            max_distance = math.sqrt((width/2)**2 + (height/2)**2)
            
            # Вычисляем прозрачность (чем дальше от центра, тем темнее)
            alpha = min(255, int(intensity * (distance / max_distance)))
            
            # Рисуем пиксель
            vignette.set_at((x, y), (0, 0, 0, alpha))
    
    return vignette

# Создаем виньетку
vignette = create_vignette(WIDTH, HEIGHT, 100)

# Класс для кнопок
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
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        text_surface = normal_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Создание кнопок
play_button = Button(WIDTH//2 - 80, 150, 160, 40, "Играть", GREEN, (0, 200, 80))
back_button = Button(30, HEIGHT - 50, 90, 30, "Назад", RED, (200, 40, 40))
level_buttons = [
    Button(WIDTH//2 - 80, 100 + i*70, 160, 50, f"Уровень {i+1}: {level['name']}", BLUE, LIGHT_BLUE) 
    for i, level in enumerate(levels)
]

# Функции рисования
def draw_menu():
    # Меню остается с цветным фоном
    screen.fill(DARK_BLUE)
    
    # Применяем виньетку
    screen.blit(vignette, (0, 0))
    
    # Заголовок
    title_text = title_font.render("КОДОВАЯ БИТВА", True, GREEN)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
    
    # Подзаголовок
    subtitle_text = normal_font.render("Сразитесь с багами ритмичным кодом!", True, WHITE)
    screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, 90))
    
    # Кнопки
    play_button.draw(screen)

def draw_level_selection():
    # Выбор уровня остается с цветным фоном
    screen.fill(DARK_BLUE)
    
    # Применяем виньетку
    screen.blit(vignette, (0, 0))
    
    title_text = title_font.render("Выбор уровня", True, WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))
    
    for button in level_buttons:
        button.draw(screen)
    
    back_button.draw(screen)

def draw_gameplay():
    # Используем фон соответствующего уровня
    if backgrounds and current_level:
        level_index = levels.index(current_level)
        if level_index < len(backgrounds):
            screen.blit(backgrounds[level_index], (0, 0))
        else:
            screen.fill(DARK_BLUE)
    else:
        screen.fill(DARK_BLUE)
    
    # Применяем виньетку
    screen.blit(vignette, (0, 0))
    
    # Рисуем закругленный темный фон под персонажем
    draw_rounded_rect(screen, 13, HEIGHT//2 - 65, 140, 190, 15, DARK_BG)
    
    # Рисуем закругленный темный фон под боссом
    draw_rounded_rect(screen, WIDTH - 150, HEIGHT//2 - 65, 140, 190, 15, DARK_BG)
    
    # Рисуем закругленный темный фон для статистики в центре сверху (увеличили высоту)
    draw_rounded_rect(screen, WIDTH//2 - 120, 10, 240, 100, 15, DARK_BG)
    
    # Рисуем босса
    draw_boss()
    
    # Рисуем игрока
    draw_player()
    
    # Рисуем бинарный код
    for code in binary_codes:
        code_text = small_font.render(code["text"], True, GREEN)
        screen.blit(code_text, (code["x"], code["y"]))
    
    # Рисуем частицы
    for particle in particles:
        pygame.draw.circle(screen, particle["color"], (particle["x"], particle["y"]), particle["size"])
    
    # Рисуем HUD
    draw_hud()
    
    # Рисуем индикатор ритма поверх всего
    draw_rhythm_indicator()

# Функция для рисования закругленного прямоугольника
def draw_rounded_rect(surface, x, y, width, height, radius, color):
    """Рисует прямоугольник с закругленными углами"""
    if color[3] > 0:  # Проверяем, есть ли альфа-канал
        rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    else:
        rect_surface = pygame.Surface((width, height))
        rect_surface.set_colorkey((0, 0, 0))
    
    # Рисуем основной прямоугольник
    pygame.draw.rect(rect_surface, color, (0, 0, width, height), border_radius=radius)
    surface.blit(rect_surface, (x, y))

def draw_boss():
    # Рисуем босса с использованием изображения
    if enemy_images and current_level:
        level_index = levels.index(current_level)
        if level_index < len(enemy_images):
            screen.blit(enemy_images[level_index], (WIDTH - 150, HEIGHT//2 - 35))
    
    # Полоска здоровья босса (исправлена для максимального здоровья)
    max_health = current_level["boss_health"]
    health_width = 150  # Уменьшили ширину для нового разрешения
    health_percentage = boss_health / max_health
    current_health_width = health_width * health_percentage
    
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 160, HEIGHT//2 - 90, health_width, 15), border_radius=3)
    pygame.draw.rect(screen, RED, (WIDTH - 158, HEIGHT//2 - 88, current_health_width - 4, 11), border_radius=2)
    
    health_text = small_font.render(f"БОСС: {boss_health}/{max_health}", True, WHITE)
    screen.blit(health_text, (WIDTH - 160, HEIGHT//2 - 105))

def draw_player():
    # Рисуем игрока (программиста) с использованием изображения
    if character_img:
        screen.blit(character_img, (-10, HEIGHT//2 - 40))

def draw_hud():
    # Очки и комбо (центрированные сверху)
    score_text = normal_font.render(f"Очки: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    
    combo_text = normal_font.render(f"Комбо: {combo}", True, GREEN if combo > 0 else WHITE)
    screen.blit(combo_text, (WIDTH//2 - combo_text.get_width()//2, 45))
    
    max_combo_text = small_font.render(f"Макс. комбо: {max_combo}", True, WHITE)
    screen.blit(max_combo_text, (WIDTH//2 - max_combo_text.get_width()//2, 70))
    
    # Промахи
    miss_text = small_font.render(f"Промахи: {miss_count}/3", True, RED if miss_count >= 2 else WHITE)
    screen.blit(miss_text, (WIDTH//2 - miss_text.get_width()//2, 95))

def draw_rhythm_indicator():
    # Индикатор ритма в центре экрана с пульсацией
    progress = rhythm_timer / rhythm_interval
    beat_size = 25 + 12 * math.sin(progress * math.pi * 2)  # Уменьшили размер для нового разрешения
    beat_color = GREEN if progress < 0.4 else RED
    
    # Затемнение фона только под индикатором ритма
    darken_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
    darken_surface.fill((0, 0, 0, 150))
    screen.blit(darken_surface, (WIDTH//2 - 60, HEIGHT//2 - 60))
    
    # Рисуем круг ритма в центре
    pygame.draw.circle(screen, beat_color, (WIDTH//2, HEIGHT//2), int(beat_size))
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), int(beat_size) + 4, 2)
    
    # Надпись о кликах перемещена ниже
    rhythm_text = normal_font.render("Нажми ПРОБЕЛ в ритм!", True, WHITE)
    screen.blit(rhythm_text, (WIDTH//2 - rhythm_text.get_width()//2, HEIGHT//2 + 40))

def draw_relaxation():
    # Для фазы релаксации используем затемненный и размытый фон уровня
    if backgrounds and current_level:
        level_index = levels.index(current_level)
        if level_index < len(backgrounds):
            # Создаем размытый фон с увеличенным размытием
            blurred_bg = create_blurred_background(backgrounds[level_index], 15)
            screen.blit(blurred_bg, (0, 0))
            
            # Добавляем затемнение на 80%
            darken_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darken_surface.fill((0, 0, 0, 100))  # 80% затемнение (255 * 0.8 = 204)
            screen.blit(darken_surface, (0, 0))
        else:
            screen.fill((10, 10, 30))
    else:
        screen.fill((10, 10, 30))
    
    # Применяем виньетку
    screen.blit(vignette, (0, 0))
    
    # Сообщение о релаксации
    relax_text = title_font.render("РАССЛАБЬТЕСЬ", True, LIGHT_BLUE)
    screen.blit(relax_text, (WIDTH//2 - relax_text.get_width()//2, HEIGHT//2 - 70))
    
    breathe_text = normal_font.render("Глубоко вдохните и выдохните", True, WHITE)
    screen.blit(breathe_text, (WIDTH//2 - breathe_text.get_width()//2, HEIGHT//2 - 30))
    
    # Исправленный таймер
    elapsed = pygame.time.get_ticks() - relaxation_start_time
    time_left = max(0, (relaxation_duration - elapsed) // 1000)
    timer_text = normal_font.render(f"Осталось: {time_left} сек", True, GREEN)
    screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, HEIGHT//2 + 10))
    
    # Анимация дыхания (только одна окружность)
    circle_size = 35 + 20 * math.sin(pygame.time.get_ticks() / 1000)
    pygame.draw.circle(screen, LIGHT_BLUE, (WIDTH//2, HEIGHT//2 + 60), circle_size, 4)

def draw_victory():
    # Для победы используем затемненный фон уровня с зеленым оттенком
    if backgrounds and current_level:
        level_index = levels.index(current_level)
        if level_index < len(backgrounds):
            # Создаем размытый фон с увеличенным размытием
            blurred_bg = create_blurred_background(backgrounds[level_index], 15)
            screen.blit(blurred_bg, (0, 0))
            
            # Добавляем зеленое затемнение для победы на 80%
            darken = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darken.fill((0, 100, 0, 204))  # 80% затемнение
            screen.blit(darken, (0, 0))
        else:
            screen.fill((10, 30, 10))
    else:
        screen.fill((10, 30, 10))
    
    # Применяем виньетку
    screen.blit(vignette, (0, 0))
    
    victory_text = title_font.render("ПОБЕДА!", True, GREEN)
    screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, HEIGHT//2 - 40))
    
    score_text = normal_font.render(f"Ваш счёт: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    
    combo_text = normal_font.render(f"Максимальное комбо: {max_combo}", True, WHITE)
    screen.blit(combo_text, (WIDTH//2 - combo_text.get_width()//2, HEIGHT//2 + 30))
    
    continue_text = normal_font.render("Нажмите ПРОБЕЛ для продолжения", True, LIGHT_BLUE)
    screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT - 40))

def draw_defeat():
    # Для поражения используем затемненный фон уровня с красным оттенком
    if backgrounds and current_level:
        level_index = levels.index(current_level)
        if level_index < len(backgrounds):
            # Создаем размытый фон с увеличенным размытием
            blurred_bg = create_blurred_background(backgrounds[level_index], 15)
            screen.blit(blurred_bg, (0, 0))
            
            # Добавляем красное затемнение для поражения на 80%
            darken = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darken.fill((100, 0, 0, 204))  # 80% затемнение
            screen.blit(darken, (0, 0))
        else:
            screen.fill((30, 10, 10))
    else:
        screen.fill((30, 10, 10))
    
    # Применяем виньетку
    screen.blit(vignette, (0, 0))
    
    defeat_text = title_font.render("ПОРАЖЕНИЕ", True, RED)
    screen.blit(defeat_text, (WIDTH//2 - defeat_text.get_width()//2, HEIGHT//2 - 70))
    
    philosophical_texts = [
        "Каждая ошибка - это шаг к мастерству.",
        "Код подобен жизни: полон неожиданных багов.",
        "Даже лучшие программисты когда-то начинали с 'Hello World'.",
        "Неудача - это возможность начать заново, но уже мудрее."
    ]
    
    text = random.choice(philosophical_texts)
    message_text = normal_font.render(text, True, WHITE)
    screen.blit(message_text, (WIDTH//2 - message_text.get_width()//2, HEIGHT//2 - 30))
    
    score_text = normal_font.render(f"Ваш счёт: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 10))
    
    continue_text = normal_font.render("Нажмите ПРОБЕЛ для продолжения", True, LIGHT_BLUE)
    screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT - 40))

# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if game_state == MENU:
            play_button.check_hover(mouse_pos)
            
            if play_button.is_clicked(mouse_pos, event):
                game_state = LEVEL_SELECTION
                
        elif game_state == LEVEL_SELECTION:
            for i, button in enumerate(level_buttons):
                button.check_hover(mouse_pos)
                if button.is_clicked(mouse_pos, event):
                    current_level = levels[i]
                    boss_health = current_level["boss_health"]
                    score = 0
                    combo = 0
                    max_combo = 0
                    miss_count = 0
                    rhythm_interval = 1000 // current_level["difficulty"]
                    game_state = GAMEPLAY
                    last_beat_time = current_time
                    relaxation_phase_completed = False  # Сброс флага релаксации
            
            back_button.check_hover(mouse_pos)
            if back_button.is_clicked(mouse_pos, event):
                game_state = MENU
                
        elif game_state == GAMEPLAY:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Более щадящая проверка попадания в ритм (увеличено окно)
                    progress = rhythm_timer / rhythm_interval
                    if progress < 0.4:  # 40% от интервала для нажатия
                        # Создаём выстрел двоичным кодом
                        binary_text = "".join(random.choice(["0", "1"]) for _ in range(8))
                        binary_codes.append({
                            "text": binary_text,
                            "x": 140,  # Обновили позицию для нового разрешения
                            "y": HEIGHT//2 - 10,
                            "speed": current_level["speed"] * 5
                        })
                        
                        # Уменьшаем здоровье босса
                        damage = 5 + combo // 2
                        boss_health = max(0, boss_health - damage)
                        
                        # Добавляем очки
                        score += 10 * (combo + 1)
                        combo += 1
                        max_combo = max(max_combo, combo)
                        
                        # Сбрасываем счетчик промахов
                        miss_count = 0
                        
                        # Создаём частицы для визуального эффекта
                        for _ in range(10):
                            particles.append({
                                "x": 140,
                                "y": HEIGHT//2 - 10,
                                "dx": random.uniform(2, 5),
                                "dy": random.uniform(-2, 2),
                                "color": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                                "size": random.randint(2, 5),
                                "life": 30
                            })
                    else:
                        # Сброс комбо при промахе
                        combo = 0
                        miss_count += 1
                        
                        # Активация фазы релаксации при 3+ промахах подряд
                        if miss_count >= 3 and not relaxation_phase_completed:
                            game_state = RELAXATION
                            relaxation_start_time = current_time
                        
        elif game_state in [VICTORY, DEFEAT]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = LEVEL_SELECTION
    
    # Обновление игровой логики
    if game_state == GAMEPLAY:
        # Обновление ритма
        rhythm_timer = (current_time - last_beat_time)
        if rhythm_timer >= rhythm_interval:
            rhythm_timer = 0
            last_beat_time = current_time
        
        # Переход к фазе релаксации при половине здоровья босса
        if (boss_health <= current_level["boss_health"] // 2 and 
            not relaxation_phase_completed and 
            relaxation_start_time == 0):
            game_state = RELAXATION
            relaxation_start_time = current_time
            
        # Проверка победы
        if boss_health <= 0:
            game_state = VICTORY
            
        # Обновление двоичных кодов
        for code in binary_codes[:]:
            code["x"] += code["speed"]
            if code["x"] > WIDTH:
                binary_codes.remove(code)
                
        # Обновление частиц
        for particle in particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["life"] -= 1
            
            if particle["life"] <= 0:
                particles.remove(particle)
                
    elif game_state == RELAXATION:
        # Проверка окончания фазы релаксации
        elapsed = current_time - relaxation_start_time
        if elapsed >= relaxation_duration:
            game_state = GAMEPLAY
            # Увеличиваем сложность для второй фазы
            rhythm_interval = max(300, rhythm_interval - 200)
            last_beat_time = current_time
            relaxation_start_time = 0
            relaxation_phase_completed = True  # Помечаем, что фаза релаксации завершена
            miss_count = 0  # Сбрасываем счетчик промахов
    
    # Отрисовка
    if game_state == MENU:
        draw_menu()
    elif game_state == LEVEL_SELECTION:
        draw_level_selection()
    elif game_state == GAMEPLAY:
        draw_gameplay()
    elif game_state == RELAXATION:
        draw_relaxation()
    elif game_state == VICTORY:
        draw_victory()
    elif game_state == DEFEAT:
        draw_defeat()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()