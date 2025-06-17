#!/usr/bin/env python3
"""
Mass Video 4K Upscaler - Массовый апскейл всех видео до 4K
Обрабатывает все видео из папки "Видео для клипа" (218 штук)
НЕ заходит в подпапку "Новая папка с объектами"
"""

import cv2
import os
from pathlib import Path
import sys
import time
from datetime import datetime

def upscale_video_to_4k(input_path, output_path):
    """Апскейлит одно видео до 4K разрешения"""
    try:
        print(f"🎬 Обрабатываю: {input_path.name}")
        
        # Открываем входное видео
        cap = cv2.VideoCapture(str(input_path))
        
        if not cap.isOpened():
            print(f"❌ Не удалось открыть: {input_path}")
            return False
        
        # Получаем параметры
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 4K разрешение
        target_width = 3840
        target_height = 2160
        
        # Создаём выходной файл
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (target_width, target_height))
        
        if not out.isOpened():
            print(f"❌ Не удалось создать выходной файл: {output_path}")
            cap.release()
            return False
        
        frame_num = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Апскейлим кадр до 4K
            upscaled_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
            
            # Записываем кадр
            out.write(upscaled_frame)
            frame_num += 1
        
        # Освобождаем ресурсы
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
        # Статистика
        elapsed_time = time.time() - start_time
        file_size = output_path.stat().st_size / (1024 * 1024)  # MB
        
        print(f"✅ Готово! {orig_width}x{orig_height} → 4K, {frame_num} кадров, {elapsed_time:.1f}с, {file_size:.1f}MB")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке {input_path}: {e}")
        return False

def process_all_videos():
    """Обрабатывает все видео"""
    
    # Исходная папка (только файлы верхнего уровня!)
    input_dir = Path("../Видео для клипа")
    
    # Выходная папка
    output_dir = Path("../готовые видео")
    output_dir.mkdir(exist_ok=True)
    
    # Находим все видео файлы ТОЛЬКО в основной папке (не в подпапках!)
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    video_files = []
    
    for file in input_dir.iterdir():
        # Пропускаем папки (включая "Новая папка с объектами")
        if file.is_dir():
            continue
        
        # Берём только видео файлы
        if file.suffix.lower() in video_extensions:
            video_files.append(file)
    
    total_videos = len(video_files)
    print(f"🎯 Найдено {total_videos} видео файлов для обработки")
    print(f"📁 Исходная папка: {input_dir}")
    print(f"📁 Выходная папка: {output_dir}")
    print(f"⚠️  НЕ обрабатываем подпапку 'Новая папка с объектами'")
    
    if total_videos == 0:
        print("❌ Видео файлы не найдены!")
        return
    
    # Обрабатываем каждое видео
    success_count = 0
    failed_count = 0
    start_time = time.time()
    
    for i, video_file in enumerate(video_files, 1):
        print(f"\n📈 ПРОГРЕСС: {i}/{total_videos} ({(i/total_videos)*100:.1f}%)")
        
        # Создаём имя выходного файла
        output_filename = f"4K_{video_file.stem}.mp4"
        output_path = output_dir / output_filename
        
        # Пропускаем если уже обработано
        if output_path.exists():
            print(f"⏭️  Уже обработано: {video_file.name}")
            success_count += 1
            continue
        
        # Обрабатываем видео
        if upscale_video_to_4k(video_file, output_path):
            success_count += 1
        else:
            failed_count += 1
        
        # Показываем общий прогресс
        elapsed = time.time() - start_time
        avg_time_per_video = elapsed / i
        estimated_remaining = (total_videos - i) * avg_time_per_video
        
        print(f"⏱️  Прошло: {elapsed/60:.1f}мин, Осталось: ~{estimated_remaining/60:.1f}мин")
    
    # Финальная статистика
    total_time = time.time() - start_time
    print(f"\n🎉 ЗАДАЧА ЗАВЕРШЕНА!")
    print(f"✅ Успешно обработано: {success_count}/{total_videos}")
    print(f"❌ Ошибок: {failed_count}")
    print(f"⏱️  Общее время: {total_time/60:.1f} минут")
    print(f"📁 Результаты сохранены в: {output_dir}")

if __name__ == "__main__":
    print("🚀 МАССОВЫЙ АПСКЕЙЛ 218 ВИДЕО ДО 4K")
    print("=" * 50)
    print(f"🕐 Начало обработки: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    process_all_videos()
    
    print("=" * 50)
    print(f"🕐 Завершение: {datetime.now().strftime('%H:%M:%S')}")
    print("🎬 ВСЕ 218 ВИДЕО ГОТОВЫ ДЛЯ ДАЛЬНЕЙШЕЙ ОБРАБОТКИ!") 