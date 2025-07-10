#!/usr/bin/env python3
import os
import shutil
from PIL import Image
import hashlib
from pathlib import Path
import time

def get_file_hash(filepath):
    """Получить MD5 хеш файла"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def get_image_quality_score(filepath):
    """Определить качество изображения по разрешению"""
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            pixels = width * height
            
            # 4K: 3840x2160 = 8,294,400 pixels
            # Full HD: 1920x1080 = 2,073,600 pixels
            
            if pixels >= 8000000:  # 4K+
                return (4, pixels, width, height)
            elif pixels >= 2000000:  # Full HD+
                return (3, pixels, width, height)
            elif pixels >= 1000000:  # HD+
                return (2, pixels, width, height)
            else:
                return (1, pixels, width, height)
    except Exception as e:
        print(f"Ошибка обработки {filepath}: {e}")
        return (0, 0, 0, 0)

def main():
    print("🔍 Поиск нейрофото за последний месяц...")
    
    # Найти все изображения за последний месяц
    month_ago = time.time() - (30 * 24 * 60 * 60)
    
    image_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filepath = os.path.join(root, file)
                try:
                    if os.path.getmtime(filepath) > month_ago:
                        image_files.append(filepath)
                except:
                    continue
    
    print(f'📸 Найдено {len(image_files)} изображений за последний месяц')
    
    # Группировка по хешам для удаления дубликатов
    print("🔄 Анализ дубликатов и качества...")
    hash_groups = {}
    
    for i, filepath in enumerate(image_files):
        if i % 100 == 0:
            print(f"   Обработано: {i}/{len(image_files)}")
        
        try:
            file_hash = get_file_hash(filepath)
            quality_score, pixels, width, height = get_image_quality_score(filepath)
            
            if file_hash not in hash_groups:
                hash_groups[file_hash] = []
            
            hash_groups[file_hash].append({
                'path': filepath,
                'quality': quality_score,
                'pixels': pixels,
                'width': width,
                'height': height,
                'size': os.path.getsize(filepath)
            })
        except Exception as e:
            print(f"Ошибка обработки {filepath}: {e}")
            continue
    
    print(f'✨ Найдено {len(hash_groups)} уникальных изображений')
    
    # Выбор лучшего из каждой группы
    print("🎯 Отбор лучших версий...")
    best_images = []
    
    for file_hash, group in hash_groups.items():
        # Сортировка: сначала по качеству, потом по размеру файла
        best = max(group, key=lambda x: (x['quality'], x['pixels'], x['size']))
        if best['quality'] >= 2:  # Только HD и выше
            best_images.append(best)
    
    print(f'🏆 Отобрано {len(best_images)} лучших изображений')
    
    # Создание папки и копирование
    print("📁 Создание папки 'нейрофото' и копирование...")
    os.makedirs('нейрофото', exist_ok=True)
    
    copied = 0
    quality_stats = {4: 0, 3: 0, 2: 0}
    
    for img in sorted(best_images, key=lambda x: x['quality'], reverse=True):
        try:
            filename = os.path.basename(img['path'])
            dest_path = os.path.join('нейрофото', filename)
            
            # Если файл с таким именем уже есть, добавляем номер
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(dest_path):
                dest_path = os.path.join('нейрофото', f'{base_name}_{counter}{ext}')
                counter += 1
            
            shutil.copy2(img['path'], dest_path)
            copied += 1
            quality_stats[img['quality']] += 1
            
            quality_names = {4: '4K+', 3: 'Full HD', 2: 'HD'}
            quality_name = quality_names.get(img['quality'], 'Unknown')
            
            if copied <= 10:  # Показываем первые 10
                print(f'   ✅ {filename} ({quality_name}: {img["width"]}x{img["height"]})')
            elif copied == 11:
                print(f'   ... и еще {len(best_images) - 10} файлов')
            
        except Exception as e:
            print(f'❌ Ошибка копирования {img["path"]}: {e}')
    
    print(f'\n🎉 ГОТОВО! Скопировано {copied} изображений в папку "нейрофото"')
    print(f'📊 Статистика качества:')
    print(f'   4K+: {quality_stats[4]} изображений')
    print(f'   Full HD: {quality_stats[3]} изображений') 
    print(f'   HD: {quality_stats[2]} изображений')

if __name__ == "__main__":
    main() 