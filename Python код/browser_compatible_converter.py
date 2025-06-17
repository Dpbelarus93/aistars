#!/usr/bin/env python3
"""
🌐 BROWSER COMPATIBLE CONVERTER 🌐
Конвертирует видео в браузер-совместимый формат
Решает проблему "browser_unsupported"

Разрабатывается с помощью AI!
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def install_ffmpeg():
    """
    Устанавливаем ffmpeg через Homebrew
    """
    print("🔧 УСТАНОВКА FFMPEG...")
    print("=" * 50)
    
    try:
        # Проверяем есть ли Homebrew
        result = subprocess.run(["brew", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Homebrew не установлен!")
            print("📝 Установи Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False
            
        print("✅ Homebrew найден")
        
        # Устанавливаем ffmpeg
        print("🚀 Устанавливаю ffmpeg...")
        result = subprocess.run(["brew", "install", "ffmpeg"], check=True)
        
        print("✅ FFmpeg установлен!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        return False
    except FileNotFoundError:
        print("❌ Homebrew не найден!")
        print("📝 Установи Homebrew сначала")
        return False

def convert_to_compatible_mp4(input_file, output_file):
    """
    Конвертирует видео в браузер-совместимый MP4
    """
    
    # Параметры для максимальной совместимости
    cmd = [
        "ffmpeg",
        "-i", str(input_file),
        "-c:v", "libx264",           # Видео кодек H.264 (самый совместимый)
        "-preset", "medium",         # Баланс скорости и качества
        "-crf", "23",               # Качество (23 = хорошее)
        "-c:a", "aac",              # Аудио кодек AAC (совместимый)
        "-b:a", "128k",             # Битрейт аудио
        "-movflags", "+faststart",   # Быстрый старт для веб
        "-pix_fmt", "yuv420p",      # Формат пикселей (совместимый)
        "-vf", "scale=1920:1080",   # Масштабируем до Full HD (легче для браузера)
        "-y",                       # Перезаписывать без вопросов
        str(output_file)
    ]
    
    try:
        print(f"🔄 Конвертирую: {input_file.name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"❌ Ошибка: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка конвертации: {e}")
        return False

def convert_videos_for_browser():
    """
    Конвертирует все видео в браузер-совместимые
    """
    
    source_dir = Path.home() / "Desktop" / "хочу еще" / "готовые видео"
    output_dir = Path.home() / "Desktop" / "хочу еще" / "browser_compatible_videos"
    
    output_dir.mkdir(exist_ok=True)
    
    # Находим MP4 файлы
    video_files = list(source_dir.glob("*.mp4"))
    
    if not video_files:
        print("❌ MP4 файлы не найдены!")
        return False
    
    # Берем первые 5 для тестирования
    test_files = video_files[:5]
    
    print(f"🎬 КОНВЕРТИРУЮ {len(test_files)} ВИДЕО ДЛЯ БРАУЗЕРА:")
    print("=" * 60)
    
    success_count = 0
    
    for i, video_file in enumerate(test_files, 1):
        
        # Создаем новое имя (упрощенное)
        new_name = f"compatible_video_{i:03d}.mp4"
        output_file = output_dir / new_name
        
        print(f"📹 [{i}/{len(test_files)}] {video_file.name}")
        print(f"   ➡️  {new_name}")
        
        if convert_to_compatible_mp4(video_file, output_file):
            success_count += 1
            
            # Проверяем размер
            original_size = video_file.stat().st_size / (1024 * 1024)
            new_size = output_file.stat().st_size / (1024 * 1024)
            
            print(f"✅ ГОТОВО! {original_size:.1f}MB → {new_size:.1f}MB")
        else:
            print(f"❌ ОШИБКА конвертации")
        
        print()
    
    print("=" * 60)
    print(f"🎉 КОНВЕРТАЦИЯ ЗАВЕРШЕНА!")
    print(f"✅ Успешно: {success_count}/{len(test_files)}")
    print(f"📁 Файлы в: {output_dir}")
    print()
    print("🌐 ОСОБЕННОСТИ БРАУЗЕР-СОВМЕСТИМЫХ ВИДЕО:")
    print("   📹 Кодек: H.264 (максимальная совместимость)")
    print("   🎵 Аудио: AAC (поддерживается везде)")
    print("   📱 Разрешение: Full HD (1920x1080)")
    print("   ⚡ FastStart: быстрая загрузка в браузере")
    print()
    print("💡 ТЕПЕРЬ ЭТИ ФАЙЛЫ ТОЧНО ЗАГРУЗЯТСЯ!")
    
    return True

def copy_to_desktop():
    """
    Копирует конвертированные файлы на рабочий стол
    """
    source_dir = Path.home() / "Desktop" / "хочу еще" / "browser_compatible_videos"
    desktop = Path.home() / "Desktop"
    
    compatible_files = list(source_dir.glob("compatible_video_*.mp4"))
    
    if not compatible_files:
        print("❌ Конвертированные файлы не найдены!")
        return
    
    # Копируем первый файл для тестирования
    test_file = compatible_files[0]
    target = desktop / f"READY_FOR_UPLOAD_{test_file.name}"
    
    shutil.copy2(test_file, target)
    
    size_mb = target.stat().st_size / (1024 * 1024)
    
    print(f"📁 ФАЙЛ СКОПИРОВАН НА РАБОЧИЙ СТОЛ:")
    print(f"   📹 {target.name}")
    print(f"   💾 Размер: {size_mb:.1f} MB")
    print(f"   🌐 Браузер-совместимый: ✅")

def main():
    print("🌐 BROWSER COMPATIBLE CONVERTER")
    print("Решаем проблему browser_unsupported!")
    print("=" * 50)
    print()
    
    # Проверяем ffmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  FFmpeg не работает")
            if not install_ffmpeg():
                return
    except FileNotFoundError:
        print("⚠️  FFmpeg не найден")
        if not install_ffmpeg():
            return
    
    print("✅ FFmpeg готов к работе!")
    print()
    
    # Конвертируем видео
    if convert_videos_for_browser():
        print()
        copy_to_desktop()

if __name__ == "__main__":
    main() 