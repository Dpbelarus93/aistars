#!/usr/bin/env python3
"""
Быстрое сжатие обложки YouTube под 2MB
"""

from PIL import Image
import os
import sys

def compress_thumbnail(input_path, output_path=None, max_size_mb=2):
    """Сжимает изображение под нужный размер"""
    
    if not output_path:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_compressed{ext}"
    
    # Открываем изображение
    img = Image.open(input_path)
    
    # Конвертируем в RGB если нужно
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Целевой размер в байтах
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # Начинаем с качества 95
    quality = 95
    
    while quality > 10:
        # Сохраняем во временный файл
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Проверяем размер
        file_size = os.path.getsize(output_path)
        
        if file_size <= max_size_bytes:
            print(f"✅ Сжато до {file_size / 1024 / 1024:.2f} MB (качество {quality})")
            return output_path
        
        quality -= 5
    
    print("⚠️ Не удалось сжать до нужного размера")
    return output_path

def main():
    # Ищем последний скачанный файл изображения
    downloads_path = os.path.expanduser("~/Downloads")
    
    # Ищем файлы изображений
    image_files = []
    for file in os.listdir(downloads_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            full_path = os.path.join(downloads_path, file)
            image_files.append((full_path, os.path.getmtime(full_path)))
    
    if not image_files:
        print("❌ Не найдено изображений в папке Загрузки")
        return
    
    # Сортируем по времени изменения (последний сверху)
    image_files.sort(key=lambda x: x[1], reverse=True)
    latest_image = image_files[0][0]
    
    print(f"📁 Найдено: {os.path.basename(latest_image)}")
    
    # Проверяем размер
    file_size = os.path.getsize(latest_image)
    size_mb = file_size / 1024 / 1024
    
    print(f"📊 Текущий размер: {size_mb:.2f} MB")
    
    if size_mb <= 2:
        print("✅ Файл уже меньше 2MB!")
        return
    
    # Сжимаем
    output_path = compress_thumbnail(latest_image)
    print(f"💾 Сохранено: {os.path.basename(output_path)}")

if __name__ == "__main__":
    main() 