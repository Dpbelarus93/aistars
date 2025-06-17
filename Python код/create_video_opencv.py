#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Video with OpenCV
Создание видео из последовательности изображений с помощью OpenCV
"""

import cv2
import os
import glob
from pathlib import Path
import numpy as np

def create_video_from_images(input_dir, output_path, fps=24, codec='mp4v'):
    """
    Создает видео из последовательности изображений
    
    Args:
        input_dir (str): Путь к папке с изображениями
        output_path (str): Путь для сохранения видео
        fps (int): Частота кадров
        codec (str): Кодек видео
    """
    
    print(f"🎬 Создание видео из изображений...")
    print(f"📁 Входная папка: {input_dir}")
    print(f"🎥 Выходной файл: {output_path}")
    print(f"⚡ FPS: {fps}")
    
    # Поиск изображений
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"❌ Папка не найдена: {input_dir}")
        return False
    
    # Находим все PNG файлы с паттерном upscaled__*
    image_files = sorted(list(input_path.glob("upscaled__*.png")))
    
    if not image_files:
        print(f"❌ Изображения не найдены в: {input_dir}")
        return False
    
    print(f"📸 Найдено {len(image_files)} изображений")
    
    # Читаем первое изображение для определения размера
    first_image = cv2.imread(str(image_files[0]))
    if first_image is None:
        print(f"❌ Не удалось прочитать первое изображение: {image_files[0]}")
        return False
    
    height, width, layers = first_image.shape
    print(f"📐 Размер кадра: {width}x{height}")
    
    # Создаем выходную папку
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Настройка кодека
    if codec == 'mp4v':
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_file = output_path.with_suffix('.mp4')
    elif codec == 'XVID':
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_file = output_path.with_suffix('.avi')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_file = output_path.with_suffix('.mp4')
    
    # Создаем VideoWriter
    video_writer = cv2.VideoWriter(
        str(output_file), 
        fourcc, 
        fps, 
        (width, height)
    )
    
    if not video_writer.isOpened():
        print("❌ Не удалось создать VideoWriter")
        return False
    
    print("🔄 Обработка кадров...")
    
    # Добавляем кадры в видео
    for i, image_file in enumerate(image_files):
        # Читаем изображение
        frame = cv2.imread(str(image_file))
        
        if frame is None:
            print(f"⚠️  Не удалось прочитать: {image_file}")
            continue
        
        # Убеждаемся что размер соответствует
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))
        
        # Добавляем кадр в видео
        video_writer.write(frame)
        
        # Показываем прогресс
        if (i + 1) % 10 == 0:
            print(f"📈 Обработано {i + 1}/{len(image_files)} кадров")
    
    # Освобождаем ресурсы
    video_writer.release()
    cv2.destroyAllWindows()
    
    if output_file.exists():
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        duration = len(image_files) / fps
        print(f"✅ Видео создано успешно!")
        print(f"📁 Файл: {output_file}")
        print(f"📊 Размер: {file_size:.1f} MB")
        print(f"⏱️  Длительность: {duration:.1f} секунд")
        print(f"🎬 Всего кадров: {len(image_files)}")
        return True
    else:
        print("❌ Видео не было создано")
        return False

def main():
    """Основная функция"""
    print("🎥 OpenCV Video Creator")
    print("=" * 50)
    
    # Определяем пути
    current_dir = Path(__file__).parent.parent
    input_dir = current_dir / "upscaled_images"
    output_dir = current_dir / "final_video"
    output_file = output_dir / "ai_video_opencv.mp4"
    
    # Создаем видео
    success = create_video_from_images(
        input_dir=input_dir,
        output_path=output_file,
        fps=24,
        codec='mp4v'
    )
    
    if success:
        print("\n🎉 Готово! Видео успешно создано!")
    else:
        print("\n❌ Не удалось создать видео")
        return False

if __name__ == "__main__":
    main() 