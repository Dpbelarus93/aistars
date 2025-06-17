#!/usr/bin/env python3
"""
⚡ QUICK VIDEO FIX ⚡
Быстрое решение проблемы загрузки видео
Просто копируем и переименовываем!
"""

from pathlib import Path
import shutil
import random

def find_smallest_videos():
    """
    Находит самые маленькие видео файлы
    """
    video_dir = Path.home() / "Desktop" / "хочу еще" / "готовые видео"
    
    if not video_dir.exists():
        print("❌ Папка с видео не найдена!")
        return []
    
    # Получаем все MP4 файлы с размерами
    video_files = []
    for video_file in video_dir.glob("*.mp4"):
        size_mb = video_file.stat().st_size / (1024 * 1024)
        video_files.append((video_file, size_mb))
    
    # Сортируем по размеру (от меньшего к большему)
    video_files.sort(key=lambda x: x[1])
    
    return video_files

def copy_compatible_videos():
    """
    Копирует видео с совместимыми именами на рабочий стол
    """
    
    video_files = find_smallest_videos()
    
    if not video_files:
        print("❌ Видео файлы не найдены!")
        return
    
    # Берем 5 самых маленьких файлов
    selected_files = video_files[:5]
    
    print(f"🎬 ВЫБРАНО {len(selected_files)} САМЫХ МАЛЕНЬКИХ ВИДЕО:")
    print("=" * 60)
    
    desktop = Path.home() / "Desktop"
    
    for i, (video_file, size_mb) in enumerate(selected_files, 1):
        
        # Создаем простое имя без специальных символов
        simple_name = f"video_{i:02d}.mp4"
        target_file = desktop / simple_name
        
        # Если файл уже есть, удаляем старый
        if target_file.exists():
            target_file.unlink()
        
        # Копируем файл
        shutil.copy2(video_file, target_file)
        
        print(f"📹 {i}. {simple_name}")
        print(f"   📊 Размер: {size_mb:.1f} MB")
        print(f"   ✅ Скопировано на рабочий стол")
        print()
    
    print("=" * 60)
    print("🎉 ГОТОВО! ВСЕ ФАЙЛЫ НА РАБОЧЕМ СТОЛЕ!")
    print()
    print("💡 ПОПРОБУЙ ТЕПЕРЬ ЗАГРУЗИТЬ:")
    print("   📹 video_01.mp4 (самый маленький)")
    print("   📹 video_02.mp4")
    print("   📹 video_03.mp4")
    print("   📹 video_04.mp4")
    print("   📹 video_05.mp4")
    print()
    
    # Показываем размеры для справки
    print("📊 РАЗМЕРЫ ФАЙЛОВ:")
    for i, (_, size_mb) in enumerate(selected_files, 1):
        print(f"   video_{i:02d}.mp4: {size_mb:.1f} MB")
    
    # Проверяем есть ли файлы больше 200MB
    large_files = [f for f in video_files if f[1] > 200]
    if large_files:
        print()
        print(f"⚠️  НАЙДЕНО {len(large_files)} ФАЙЛОВ БОЛЬШЕ 200MB")
        print("   (Они могут не загружаться)")

def show_audio_files():
    """
    Показывает доступные аудио файлы
    """
    print()
    print("🎤 ДОСТУПНЫЕ АУДИО ФАЙЛЫ:")
    print("=" * 40)
    
    audio_dir = Path.home() / "Desktop" / "эксперименты с музыкой" / "professional_vocals"
    
    if not audio_dir.exists():
        print("❌ Папка с аудио не найдена!")
        return
    
    audio_files = list(audio_dir.glob("vocals_*.mp3"))
    
    if not audio_files:
        print("❌ Аудио файлы не найдены!")
        return
    
    # Берем первые 3 файла
    selected_audio = audio_files[:3]
    
    desktop = Path.home() / "Desktop"
    
    for i, audio_file in enumerate(selected_audio, 1):
        
        simple_name = f"audio_{i:02d}.mp3"
        target_file = desktop / simple_name
        
        if target_file.exists():
            target_file.unlink()
        
        shutil.copy2(audio_file, target_file)
        
        size_kb = audio_file.stat().st_size / 1024
        
        print(f"🎵 {i}. {simple_name}")
        print(f"   📊 Размер: {size_kb:.0f} KB")
        print(f"   ✅ Скопировано на рабочий стол")
        print()

def main():
    print("⚡ QUICK VIDEO FIX")
    print("Быстрое решение проблемы загрузки!")
    print("=" * 40)
    print()
    
    print("🔧 ЧТО ДЕЛАЕМ:")
    print("   1. Находим самые маленькие видео")
    print("   2. Даем им простые имена")
    print("   3. Копируем на рабочий стол")
    print("   4. Готово к загрузке!")
    print()
    
    copy_compatible_videos()
    show_audio_files()
    
    print()
    print("🚀 ИНСТРУКЦИЯ:")
    print("   1. 📹 Попробуй загрузить video_01.mp4")
    print("   2. 🎤 Загрузи audio_01.mp3")
    print("   3. 🎬 Создай липсинк!")
    print()
    print("💡 ЕСЛИ НЕ РАБОТАЕТ - ПОПРОБУЙ СЛЕДУЮЩИЙ ФАЙЛ!")

if __name__ == "__main__":
    main() 