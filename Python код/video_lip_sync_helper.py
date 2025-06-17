#!/usr/bin/env python3
"""
🎬 VIDEO LIP SYNC HELPER 🎬
Помощник для подготовки видео к липсинку
Выбираем видео и аудио, готовим к загрузке!
"""

import os
import shutil
from pathlib import Path
import random

def show_available_videos():
    """
    Показывает доступные 4K видео
    """
    video_dir = Path.home() / "Desktop" / "хочу еще" / "готовые видео"
    
    if not video_dir.exists():
        print("❌ Папка с видео не найдена!")
        return []
    
    # Ищем MP4 файлы
    video_files = list(video_dir.glob("*.mp4"))
    
    if not video_files:
        print("❌ MP4 файлы не найдены!")
        return []
    
    print(f"🎬 НАЙДЕНО {len(video_files)} ВИДЕО:")
    print("=" * 50)
    
    for i, video in enumerate(sorted(video_files)[:10], 1):  # Показываем первые 10
        size_mb = video.stat().st_size / (1024 * 1024)
        print(f"{i:2d}. {video.name} ({size_mb:.1f} MB)")
    
    if len(video_files) > 10:
        print(f"    ... и еще {len(video_files) - 10} видео")
    
    return sorted(video_files)

def show_available_audio():
    """
    Показывает доступные аудио файлы для липсинка
    """
    audio_dir = Path.home() / "Desktop" / "эксперименты с музыкой" / "professional_vocals"
    
    if not audio_dir.exists():
        print("❌ Папка с голосом не найдена!")
        return []
    
    # Ищем MP3 файлы с голосом
    audio_files = list(audio_dir.glob("vocals_*.mp3"))
    
    if not audio_files:
        print("❌ Аудио файлы не найдены!")
        return []
    
    print(f"🎤 НАЙДЕНО {len(audio_files)} АУДИО:")
    print("=" * 50)
    
    for i, audio in enumerate(sorted(audio_files)[:10], 1):  # Показываем первые 10
        size_kb = audio.stat().st_size / 1024
        print(f"{i:2d}. {audio.name} ({size_kb:.0f} KB)")
    
    if len(audio_files) > 10:
        print(f"    ... и еще {len(audio_files) - 10} аудио")
    
    return sorted(audio_files)

def copy_to_desktop(file_path):
    """
    Копирует файл на рабочий стол для удобной загрузки
    """
    desktop = Path.home() / "Desktop"
    target = desktop / file_path.name
    
    # Если файл уже есть, добавляем суффикс
    counter = 1
    while target.exists():
        stem = file_path.stem
        suffix = file_path.suffix
        target = desktop / f"{stem}_{counter}{suffix}"
        counter += 1
    
    shutil.copy2(file_path, target)
    return target

def main():
    print("🎬 VIDEO LIP SYNC HELPER")
    print("Готовим видео и аудио для липсинка!")
    print("=" * 50)
    print()
    
    # Показываем видео
    print("📹 ДОСТУПНЫЕ ВИДЕО:")
    videos = show_available_videos()
    print()
    
    # Показываем аудио  
    print("🎤 ДОСТУПНЫЕ АУДИО:")
    audios = show_available_audio()
    print()
    
    if not videos or not audios:
        print("❌ Не хватает файлов для создания липсинка!")
        return
    
    # Выбираем случайные файлы для демо
    selected_video = random.choice(videos)
    selected_audio = random.choice(audios)
    
    print("🎯 РЕКОМЕНДУЕМАЯ КОМБИНАЦИЯ:")
    print("=" * 50)
    print(f"📹 Видео: {selected_video.name}")
    print(f"🎤 Аудио: {selected_audio.name}")
    print()
    
    # Копируем на рабочий стол
    print("📁 КОПИРУЮ НА РАБОЧИЙ СТОЛ...")
    
    video_copy = copy_to_desktop(selected_video)
    audio_copy = copy_to_desktop(selected_audio)
    
    print(f"✅ Видео скопировано: {video_copy.name}")
    print(f"✅ Аудио скопировано: {audio_copy.name}")
    print()
    
    print("🚀 ИНСТРУКЦИЯ ДЛЯ ЛИПСИНКА:")
    print("=" * 50)
    print("1. 📹 Загрузи видео в AI платформу")
    print("2. 🎤 Загрузи аудио файл")
    print("3. 🎬 Запусти создание липсинка")
    print("4. ⏰ Жди результат!")
    print()
    print("💡 ФАЙЛЫ НА РАБОЧЕМ СТОЛЕ ГОТОВЫ К ЗАГРУЗКЕ!")
    
    # Показываем размеры файлов
    video_size = video_copy.stat().st_size / (1024 * 1024)
    audio_size = audio_copy.stat().st_size / 1024
    
    print()
    print("📊 ИНФОРМАЦИЯ О ФАЙЛАХ:")
    print(f"📹 Видео: {video_size:.1f} MB (4K качество)")
    print(f"🎤 Аудио: {audio_size:.0f} KB (чистый голос)")
    print(f"⏱️  Длительность: ~5 секунд")

if __name__ == "__main__":
    main() 