import pygame
import os
import sys

# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Мультимедийный плеер")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (100, 200, 100)
RED = (200, 100, 100)
BLUE = (100, 100, 200)

# Список песен (замените на ваши файлы)
songs = [
    "music/middle_music.mp3",
    "music/senior_music.mp3", 
]

current_song_index = 0
music_playing = False

# Загрузка первой песни
def load_current_song():
    try:
        if os.path.exists(songs[current_song_index]):
            pygame.mixer.music.load(songs[current_song_index])
            return True
        else:
            print(f"Файл {songs[current_song_index]} не найден!")
            return False
    except:
        print("Ошибка загрузки музыки")
        return False

# Загружаем первую песню
if songs and load_current_song():
    print(f"Загружена: {songs[current_song_index]}")
else:
    print("Нет доступных песен!")

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка нажатий клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                if not music_playing and songs:
                    pygame.mixer.music.play()
                    music_playing = True
            
            elif event.key == pygame.K_s:  # Stop
                if music_playing:
                    pygame.mixer.music.stop()
                    music_playing = False
            
            elif event.key == pygame.K_SPACE:  # Pause/Resume
                if music_playing:
                    pygame.mixer.music.pause()
                    music_playing = False
                else:
                    pygame.mixer.music.unpause()
                    music_playing = True
            
            elif event.key == pygame.K_RIGHT:  # Следующая песня
                if songs:
                    pygame.mixer.music.stop()
                    current_song_index = (current_song_index + 1) % len(songs)
                    if load_current_song() and music_playing:
                        pygame.mixer.music.play()
            
            elif event.key == pygame.K_LEFT:  # Предыдущая песня
                if songs:
                    pygame.mixer.music.stop()
                    current_song_index = (current_song_index - 1) % len(songs)
                    if load_current_song() and music_playing:
                        pygame.mixer.music.play()
    
    # Отрисовка
    screen.fill(WHITE)
    
    # Отображение текущей песни
    font = pygame.font.Font(None, 36)
    if songs:
        song_name = os.path.basename(songs[current_song_index])
        text = font.render(f"Now: {song_name}", True, BLACK)
        screen.blit(text, (20, 20))
    
    # Статус
    status = "Playing" if music_playing else "Stopped"
    status_text = font.render(f"Status: {status}", True, BLACK)
    screen.blit(status_text, (20, 60))
    
    # Инструкция
    instructions = [
        "P - Play music",
        "S - Stop music", 
        "Space - Pause/Resume",
        "→ - Next song",
        "← - Previous song"
    ]
    
    for i, instruction in enumerate(instructions):
        text = pygame.font.Font(None, 24).render(instruction, True, BLACK)
        screen.blit(text, (20, 120 + i * 30))
    
    # Прогресс песни (если играет)
    if music_playing and pygame.mixer.music.get_busy():
        try:
            pos = pygame.mixer.music.get_pos() / 1000  # в секундах
            progress_text = font.render(f"Time: {pos:.1f}s", True, BLACK)
            screen.blit(progress_text, (20, 280))
        except:
            pass
    
    pygame.display.flip()

pygame.quit()
sys.exit()