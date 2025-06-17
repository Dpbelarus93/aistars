#!/usr/bin/env python3
"""
🔧 SIMPLE VIDEO FIXER 🔧
Простое исправление видео без ffmpeg
Делаем файлы браузер-совместимыми!
"""

import subprocess
import sys
from pathlib import Path
import shutil

def install_moviepy():
    """
    Устанавливаем moviepy для обработки видео
    """
    print("🎬 УСТАНОВКА MOVIEPY...")
    print("=" * 40)
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "moviepy"], check=True)
        print("✅ MoviePy установлен!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        return False

def fix_video_compatibility(input_file, output_file):
    """
    Исправляет совместимость видео файла
    """
    try:
        from moviepy.editor import VideoFileClip
        
        print(f"🔧 Исправляю: {input_file.name}")
        
        # Загружаем видео
        clip = VideoFileClip(str(input_file))
        
        # Сохраняем с совместимыми параметрами
        clip.write_videofile(
            str(output_file),
            codec='libx264',           # H.264 кодек
            audio_codec='aac',         # AAC аудио
            fps=24,                   # Стандартный FPS
            preset='medium',          # Баланс качества/скорости
            ffmpeg_params=[
                '-pix_fmt', 'yuv420p',     # Совместимый формат пикселей
                '-movflags', '+faststart'   # Быстрый старт для веба
            ]
        )
        
        clip.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def create_browser_compatible_videos():
    """
    Создает браузер-совместимые версии видео
    """
    
    source_dir = Path.home() / "Desktop" / "хочу еще" / "готовые видео"
    output_dir = Path.home() / "Desktop" / "browser_videos"
    
    output_dir.mkdir(exist_ok=True)
    
    # Находим первые 3 видео для тестирования
    video_files = list(source_dir.glob("*.mp4"))[:3]
    
    if not video_files:
        print("❌ Видео файлы не найдены!")
        return False
    
    print(f"🎬 ИСПРАВЛЯЮ {len(video_files)} ВИДЕО:")
    print("=" * 50)
    
    success_count = 0
    
    for i, video_file in enumerate(video_files, 1):
        
        # Простое имя для браузера
        new_name = f"browser_video_{i}.mp4"
        output_file = output_dir / new_name
        
        print(f"📹 [{i}/{len(video_files)}] {video_file.name}")
        print(f"   ➡️  {new_name}")
        
        if fix_video_compatibility(video_file, output_file):
            success_count += 1
            
            # Размеры файлов
            original_size = video_file.stat().st_size / (1024 * 1024)
            new_size = output_file.stat().st_size / (1024 * 1024)
            
            print(f"✅ ГОТОВО! {original_size:.1f}MB → {new_size:.1f}MB")
            
            # Копируем на рабочий стол
            desktop_file = Path.home() / "Desktop" / f"UPLOAD_READY_{new_name}"
            shutil.copy2(output_file, desktop_file)
            print(f"📁 Скопировано: {desktop_file.name}")
            
        else:
            print(f"❌ ОШИБКА")
        
        print()
    
    print("=" * 50)
    print(f"🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
    print(f"✅ Успешно: {success_count}/{len(video_files)}")
    print()
    print("🌐 ИСПРАВЛЕНИЯ:")
    print("   📹 Кодек: H.264 (100% совместимость)")
    print("   🎵 Аудио: AAC")
    print("   ⚡ FastStart включен")
    print("   📱 Оптимизировано для браузеров")
    print()
    print("💡 ФАЙЛЫ НА РАБОЧЕМ СТОЛЕ ГОТОВЫ К ЗАГРУЗКЕ!")
    
    return True

def main():
    print("🔧 SIMPLE VIDEO FIXER")
    print("Делаем видео браузер-совместимыми!")
    print("=" * 40)
    print()
    
    # Проверяем moviepy
    try:
        import moviepy
        print("✅ MoviePy готов!")
    except ImportError:
        print("⚠️  MoviePy не найден")
        if not install_moviepy():
            return
        
        # Перезагружаем после установки
        try:
            import moviepy
            print("✅ MoviePy установлен и готов!")
        except ImportError:
            print("❌ Не удалось загрузить MoviePy")
            return
    
    print()
    create_browser_compatible_videos()

if __name__ == "__main__":
    main() 