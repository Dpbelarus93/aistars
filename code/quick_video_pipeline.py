#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Video Pipeline
Быстрый пайплайн для обработки изображений и создания видео

Шаги:
1. Проверка обработанных изображений  
2. Настройка DaVinci Resolve API
3. Автоматический импорт в DaVinci
4. Создание timeline
5. Опциональный экспорт через OpenCV
"""

import os
import sys
import subprocess
from pathlib import Path

# Добавляем папку с кодом в PATH
sys.path.insert(0, str(Path(__file__).parent / "Python код"))

def check_upscaled_images():
    """Проверяет наличие обработанных изображений"""
    print("📸 Проверка обработанных изображений...")
    
    upscaled_dir = Path("upscaled_images")
    if not upscaled_dir.exists():
        print("❌ Папка upscaled_images не найдена!")
        return False
    
    png_files = list(upscaled_dir.glob("upscaled__*.png"))
    if not png_files:
        print("❌ Обработанные PNG файлы не найдены!")
        return False
    
    print(f"✅ Найдено {len(png_files)} обработанных изображений")
    return True

def setup_davinci():
    """Настройка окружения DaVinci Resolve"""
    print("🔧 Настройка DaVinci Resolve API...")
    
    try:
        from setup_davinci_env import setup_davinci_environment
        return setup_davinci_environment()
    except ImportError:
        print("❌ Модуль setup_davinci_env не найден!")
        return False

def launch_davinci_import():
    """Запуск импорта в DaVinci Resolve"""
    print("🎬 Запуск импорта в DaVinci Resolve...")
    
    try:
        from davinci_auto_import import DaVinciAutoImporter
        
        importer = DaVinciAutoImporter()
        
        # Импортируем изображения
        success = importer.import_image_sequence(
            image_folder="upscaled_images",
            timeline_name="AI_Generated_Scene",
            fps=24
        )
        
        if success:
            print("✅ Timeline создан в DaVinci Resolve!")
            
            # Спрашиваем про автоэкспорт
            export_choice = input("\n🤔 Экспортировать видео автоматически? (y/n): ")
            if export_choice.lower() in ['y', 'yes', 'да']:
                output_dir = Path("final_video")
                output_dir.mkdir(exist_ok=True)
                output_file = output_dir / "ai_generated_video.mp4"
                
                return importer.export_timeline(output_file)
            
            return True
        else:
            print("❌ Не удалось создать timeline")
            return False
            
    except ImportError as e:
        print(f"❌ Не удалось импортировать модуль DaVinci: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при работе с DaVinci: {e}")
        return False

def run_opencv_processing():
    """Создание видео через OpenCV"""
    print("🎥 Создание видео через OpenCV...")
    
    try:
        from create_video_opencv import create_video_from_images
        
        # Определяем пути
        input_dir = Path("upscaled_images")
        output_dir = Path("final_video")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "ai_video_opencv.mp4"
        
        # Создаем видео
        success = create_video_from_images(
            input_dir=input_dir,
            output_path=output_file,
            fps=24,
            codec='mp4v'
        )
        
        if success:
            print(f"✅ Видео создано: {output_file}")
            return True
        else:
            print("❌ Не удалось создать видео через OpenCV")
            return False
            
    except ImportError as e:
        print(f"❌ OpenCV не доступен: {e}")
        print("💡 Установите: pip install opencv-python")
        return False
    except Exception as e:
        print(f"❌ Ошибка при создании видео: {e}")
        return False

def run_ffmpeg_processing():
    """Альтернативный путь через FFmpeg если доступен"""
    print("🎥 Запуск обработки через FFmpeg...")
    
    try:
        # Используем FFmpeg для создания видео из изображений
        upscaled_dir = Path("upscaled_images")
        output_dir = Path("final_video")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "ai_video_ffmpeg.mp4"
        
        # FFmpeg команда для создания видео
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", "24",
            "-i", str(upscaled_dir / "upscaled__%05d_.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            str(output_file)
        ]
        
        print(f"🔄 Запуск FFmpeg...")
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Видео создано: {output_file}")
            return True
        else:
            print(f"❌ Ошибка FFmpeg: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ FFmpeg не установлен!")
        return False
    except Exception as e:
        print(f"❌ Ошибка при создании видео: {e}")
        return False

def main():
    """Основная функция"""
    print("🚀 Quick Video Pipeline")
    print("=" * 50)
    
    # Шаг 1: Проверка изображений
    if not check_upscaled_images():
        print("\n❌ Сначала обработайте изображения!")
        print("💡 Запустите один из upscaler скриптов")
        return False
    
    # Шаг 2: Попытка подключения к DaVinci
    print("\n" + "=" * 50)
    davinci_available = setup_davinci()
    
    if davinci_available:
        print("\n🎬 DaVinci Resolve доступен!")
        
        davinci_success = False
        try:
            davinci_success = launch_davinci_import()
            if davinci_success:
                print("\n✅ Пайплайн завершен успешно!")
                print("🎬 Видео готово в DaVinci Resolve!")
                return True
        except Exception as e:
            print(f"❌ Ошибка в DaVinci пайплайне: {e}")
        
        # Если DaVinci не сработал, переходим к альтернативам
        if not davinci_success:
            davinci_available = False
    
    # Альтернативные методы создания видео
    if not davinci_available:
        print("\n⚠️  DaVinci Resolve недоступен")
        print("🎥 Переключаемся на альтернативные методы...")
        
        # Сначала пробуем OpenCV
        print("\n📄 Попытка 1: OpenCV")
        if run_opencv_processing():
            print("\n✅ Видео создано через OpenCV!")
            return True
        
        # Потом FFmpeg если есть
        print("\n📄 Попытка 2: FFmpeg")
        ffmpeg_choice = input("Попробовать FFmpeg? (y/n): ")
        if ffmpeg_choice.lower() in ['y', 'yes', 'да']:
            if run_ffmpeg_processing():
                print("\n✅ Видео создано через FFmpeg!")
                return True
        
        print("\n💡 Рекомендации:")
        print("1. Установите и запустите DaVinci Resolve")
        print("2. Или установите OpenCV: pip install opencv-python")
        print("3. Или установите FFmpeg")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 ГОТОВО! Ваше видео готово!")
    else:
        print("\n❌ Пайплайн не завершился")
        sys.exit(1) 