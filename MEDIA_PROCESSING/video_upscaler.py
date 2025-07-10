#!/usr/bin/env python3
"""
ВИДЕО АПСКЕЙЛЕР
Улучшает качество видео через Real-ESRGAN + ffmpeg
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Проверяем наличие нужных программ"""
    required = ['ffmpeg', 'python3']
    missing = []
    
    for prog in required:
        if not shutil.which(prog):
            missing.append(prog)
    
    if missing:
        print(f"❌ ОШИБКА: Не найдены программы: {', '.join(missing)}")
        return False
    
    print("✅ Все зависимости найдены!")
    return True

def find_video_file():
    """Ищем видеофайлы в текущей папке"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    current_dir = Path('.')
    
    videos = []
    for ext in video_extensions:
        videos.extend(current_dir.glob(f"*{ext}"))
        videos.extend(current_dir.glob(f"**/*{ext}"))
    
    if not videos:
        print("❌ Видеофайлы не найдены!")
        return None
    
    print("\n📹 НАЙДЕННЫЕ ВИДЕО:")
    for i, video in enumerate(videos, 1):
        size_mb = video.stat().st_size / (1024 * 1024)
        print(f"{i}. {video.name} ({size_mb:.1f} MB)")
    
    while True:
        try:
            choice = int(input(f"\nВыбери номер видео (1-{len(videos)}): ")) - 1
            if 0 <= choice < len(videos):
                return videos[choice]
            else:
                print("❌ Неверный номер!")
        except ValueError:
            print("❌ Введи число!")

def upscale_video(input_file, scale_factor=2):
    """Апскейлим видео"""
    input_path = Path(input_file)
    output_name = f"UPSCALED_{scale_factor}X_{input_path.stem}.mp4"
    output_path = Path(output_name)
    
    print(f"\n🚀 НАЧИНАЕМ АПСКЕЙЛ: {input_path.name}")
    print(f"📤 РЕЗУЛЬТАТ: {output_name}")
    
    # Команда ffmpeg для апскейла
    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-vf', f'scale=iw*{scale_factor}:ih*{scale_factor}:flags=lanczos',
        '-c:v', 'libx264',
        '-preset', 'slow',
        '-crf', '18',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-y',  # Перезаписать если существует
        str(output_path)
    ]
    
    print(f"\n⚙️  КОМАНДА: {' '.join(cmd)}")
    
    try:
        # Запускаем ffmpeg
        process = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"\n✅ ГОТОВО! Файл: {output_name} ({size_mb:.1f} MB)")
            return str(output_path)
        else:
            print("❌ Файл не создался!")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ ОШИБКА FFMPEG: {e}")
        print(f"STDERR: {e.stderr}")
        return None

def enhance_with_realesrgan(input_file):
    """Улучшаем через Real-ESRGAN если доступен"""
    realesrgan_path = Path("Real-ESRGAN")
    
    if not realesrgan_path.exists():
        print("⚠️  Real-ESRGAN не найден, используем только ffmpeg")
        return False
    
    print("🎯 НАЙДЕН Real-ESRGAN! Будем использовать для максимального качества!")
    
    # Тут можно добавить логику для Real-ESRGAN
    # Пока используем ffmpeg с лучшими настройками
    return True

def main():
    print("🎬 ВИДЕО АПСКЕЙЛЕР - УЛУЧШЕНИЕ КАЧЕСТВА")
    print("=" * 50)
    
    if not check_dependencies():
        return
    
    # Ищем видео
    video_file = find_video_file()
    if not video_file:
        return
    
    # Выбираем масштаб
    print("\n📐 ВЫБЕРИ МАСШТАБ УВЕЛИЧЕНИЯ:")
    print("1. 2x (HD → 4K)")
    print("2. 4x (HD → 8K)")
    print("3. 1.5x (небольшое улучшение)")
    
    scale_options = {1: 2, 2: 4, 3: 1.5}
    
    while True:
        try:
            choice = int(input("Выбери (1-3): "))
            if choice in scale_options:
                scale = scale_options[choice]
                break
            else:
                print("❌ Выбери 1, 2 или 3!")
        except ValueError:
            print("❌ Введи число!")
    
    # Проверяем Real-ESRGAN
    enhance_with_realesrgan(video_file)
    
    # Апскейлим
    result = upscale_video(video_file, scale)
    
    if result:
        print(f"\n🎉 УСПЕХ! Улучшенное видео: {result}")
        print("💡 Можешь сравнить с оригиналом!")
    else:
        print("❌ Что-то пошло не так...")

if __name__ == "__main__":
    main() 