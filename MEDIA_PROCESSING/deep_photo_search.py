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

def get_image_info(filepath):
    """Получить полную информацию об изображении"""
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            pixels = width * height
            format_type = img.format
            mode = img.mode
            
            # Определение качества
            if pixels >= 8000000:  # 4K+
                quality = (4, "4K+")
            elif pixels >= 2000000:  # Full HD+
                quality = (3, "Full HD")
            elif pixels >= 1000000:  # HD+
                quality = (2, "HD")
            else:
                quality = (1, "Low")
            
            return {
                'width': width,
                'height': height,
                'pixels': pixels,
                'format': format_type,
                'mode': mode,
                'quality_score': quality[0],
                'quality_name': quality[1]
            }
    except Exception as e:
        return None

def is_likely_ai_generated(filepath, filename):
    """Определить, похоже ли изображение на AI-генерированное"""
    ai_indicators = [
        'upscaled', '4k', 'generated', 'ai', 'flux', 'midjourney', 'dalle',
        'stable', 'diffusion', 'neural', 'gan', 'synthetic', 'rendered',
        'комфи', 'нейро', 'ии', 'generated', 'output'
    ]
    
    filepath_lower = filepath.lower()
    filename_lower = filename.lower()
    
    # Проверка по пути и имени файла
    for indicator in ai_indicators:
        if indicator in filepath_lower or indicator in filename_lower:
            return True
    
    # Проверка по размеру (AI часто генерирует стандартные размеры)
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            # Стандартные AI размеры
            ai_sizes = [
                (1024, 1024), (512, 512), (768, 768), (1536, 1536),
                (1920, 1080), (1080, 1920), (2048, 2048), (1344, 768),
                (768, 1344), (1152, 896), (896, 1152), (2688, 1536),
                (1536, 2688), (5376, 3072), (3072, 5376)
            ]
            if (width, height) in ai_sizes or (height, width) in ai_sizes:
                return True
    except:
        pass
    
    return False

def main():
    print("🔍 ТОТАЛЬНЫЙ ПОИСК ВСЕХ ИЗОБРАЖЕНИЙ...")
    print("📂 Сканирую ВСЕ папки и подпапки...")
    
    # Найти ВСЕ изображения без ограничений по времени
    all_image_files = []
    ai_image_files = []
    
    # Расширения изображений
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif'}
    
    # Приоритетные папки для поиска
    priority_folders = [
        './upscaled_images',
        './video/4k_upscaled', 
        './lipsync/4k_upscaled',
        './хочу еще/lipsync/4k_upscaled',
        './готовые видео',
        './Видео для клипа',
        './photos',
        './Фотографии',
        './misc',
        './ALL_TRACK_PHOTOS',
        './LIP_SYNC_FINAL'
    ]
    
    print("🎯 Проверяю приоритетные папки...")
    for folder in priority_folders:
        if os.path.exists(folder):
            print(f"   📁 Сканирую: {folder}")
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in image_extensions):
                        filepath = os.path.join(root, file)
                        all_image_files.append(filepath)
                        
                        if is_likely_ai_generated(filepath, file):
                            ai_image_files.append(filepath)
    
    print("🌍 Сканирую остальные папки...")
    for root, dirs, files in os.walk('.'):
        # Пропускаем уже проверенные папки
        skip_folder = False
        for priority in priority_folders:
            if root.startswith(priority.lstrip('./')):
                skip_folder = True
                break
        
        if skip_folder:
            continue
            
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                filepath = os.path.join(root, file)
                all_image_files.append(filepath)
                
                if is_likely_ai_generated(filepath, file):
                    ai_image_files.append(filepath)
    
    print(f'📸 Найдено ВСЕГО изображений: {len(all_image_files)}')
    print(f'🤖 Из них AI-генерированных: {len(ai_image_files)}')
    
    # Анализ дубликатов среди AI изображений
    print("🔄 Анализ AI изображений и удаление дубликатов...")
    
    hash_groups = {}
    processed = 0
    
    for filepath in ai_image_files:
        processed += 1
        if processed % 50 == 0:
            print(f"   Обработано: {processed}/{len(ai_image_files)}")
        
        try:
            file_hash = get_file_hash(filepath)
            img_info = get_image_info(filepath)
            
            if img_info is None:
                continue
                
            if file_hash not in hash_groups:
                hash_groups[file_hash] = []
            
            hash_groups[file_hash].append({
                'path': filepath,
                'filename': os.path.basename(filepath),
                'size': os.path.getsize(filepath),
                'mtime': os.path.getmtime(filepath),
                **img_info
            })
        except Exception as e:
            print(f"Ошибка обработки {filepath}: {e}")
            continue
    
    print(f'✨ Найдено {len(hash_groups)} уникальных AI изображений')
    
    # Выбор лучшего из каждой группы
    print("🏆 Отбор лучших версий...")
    best_images = []
    
    for file_hash, group in hash_groups.items():
        # Сортировка: качество -> размер -> время модификации
        best = max(group, key=lambda x: (x['quality_score'], x['pixels'], x['size'], x['mtime']))
        if best['quality_score'] >= 2:  # HD и выше
            best_images.append(best)
    
    # Сортировка по качеству и времени
    best_images.sort(key=lambda x: (x['quality_score'], x['mtime']), reverse=True)
    
    print(f'🎯 Отобрано {len(best_images)} лучших AI изображений')
    
    # Очистка и пересоздание папки
    if os.path.exists('нейрофото'):
        shutil.rmtree('нейрофото')
    os.makedirs('нейрофото', exist_ok=True)
    
    # Копирование с детальной статистикой
    print("📁 Копирование в папку 'нейрофото'...")
    
    copied = 0
    quality_stats = {4: 0, 3: 0, 2: 0}
    
    for img in best_images:
        try:
            filename = img['filename']
            dest_path = os.path.join('нейрофото', filename)
            
            # Если файл с таким именем уже есть, добавляем номер
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(dest_path):
                dest_path = os.path.join('нейрофото', f'{base_name}_{counter}{ext}')
                counter += 1
            
            shutil.copy2(img['path'], dest_path)
            copied += 1
            quality_stats[img['quality_score']] += 1
            
            # Показываем первые 15 файлов
            if copied <= 15:
                mtime_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(img['mtime']))
                print(f'   ✅ {filename}')
                print(f'      {img["quality_name"]}: {img["width"]}x{img["height"]} | {mtime_str}')
            elif copied == 16:
                print(f'   ... и еще {len(best_images) - 15} файлов')
            
        except Exception as e:
            print(f'❌ Ошибка копирования {img["path"]}: {e}')
    
    print(f'\n🎉 ГОТОВО! Скопировано {copied} уникальных AI изображений')
    print(f'📊 Статистика качества:')
    print(f'   🏆 4K+: {quality_stats[4]} изображений')
    print(f'   🥇 Full HD: {quality_stats[3]} изображений') 
    print(f'   🥈 HD: {quality_stats[2]} изображений')
    
    # Поиск изображений в розовом пиджаке
    print(f'\n🔍 ПОИСК ИЗОБРАЖЕНИЙ В РОЗОВОМ ПИДЖАКЕ...')
    pink_keywords = ['pink', 'rose', 'розов', 'пиджак', 'jacket', 'suit', 'блейзер']
    
    found_pink = []
    for img in best_images:
        filename_lower = img['filename'].lower()
        path_lower = img['path'].lower()
        
        for keyword in pink_keywords:
            if keyword in filename_lower or keyword in path_lower:
                found_pink.append(img)
                break
    
    if found_pink:
        print(f'🌸 Найдено {len(found_pink)} изображений с розовым пиджаком:')
        for img in found_pink[:5]:  # Показываем первые 5
            print(f'   💗 {img["filename"]} ({img["quality_name"]}: {img["width"]}x{img["height"]})')
    else:
        print('🤔 Изображения в розовом пиджаке не найдены по ключевым словам')
        print('   Проверьте папку нейрофото вручную - они могут быть там!')

if __name__ == "__main__":
    main() 