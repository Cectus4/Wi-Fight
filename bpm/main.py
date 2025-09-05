import librosa
import numpy as np

def advanced_beat_detection(audio_file):
    y, sr = librosa.load(audio_file)
    
    # Извлечение ударных характеристик
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
    
    # Определение темпа
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    
    # Более точное определение битов
    beat_frames = librosa.beat.beat_track(
        onset_envelope=onset_env,
        sr=sr,
        units='time',
        trim=False
    )[1]
    
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    return beat_times.tolist()

# Использование
beat_times = advanced_beat_detection("bpm/silentroom-protoflicker.mp3")
print(beat_times)
