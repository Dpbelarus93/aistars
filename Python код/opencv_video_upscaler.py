#!/usr/bin/env python3
"""
Simple Video 4K Upscaler using OpenCV
Простой апскейл видео до 4K через OpenCV
"""

import cv2
import os
from pathlib import Path
import sys

def upscale_video_to_4k(input_path, output_path):
    """Апскейлит видео до 4K разрешения"""
    print(f"🎬 Апскейл видео до 4K: {input_path}")
    
    # Открываем входное видео
    cap = cv2.VideoCapture(str(input_path))
    
    # Получаем параметры
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"📊 Исходное разрешение: {orig_width}x{orig_height}")
    print(f"📊 FPS: {fps}")
    print(f"📊 Кадров: {frame_count}")
    
    # 4K разрешение
    target_width = 3840
    target_height = 2160
    
    print(f"🎯 Целевое разрешение: {target_width}x{target_height}")
    
    # Создаём выходной файл
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (target_width, target_height))
    
    frame_num = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Апскейлим кадр до 4K
        upscaled_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
        
        # Записываем кадр
        out.write(upscaled_frame)
        
        frame_num += 1
        
        # Показываем прогресс
        if frame_num % 10 == 0:
            progress = (frame_num / frame_count) * 100
            print(f"📈 Обработано {frame_num}/{frame_count} кадров ({progress:.1f}%)")
    
    # Освобождаем ресурсы
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"✅ Готово! 4K видео сохранено: {output_path}")
    
    # Проверяем размер файла
    if Path(output_path).exists():
        file_size = Path(output_path).stat().st_size / (1024 * 1024)  # MB
        print(f"📁 Размер файла: {file_size:.1f} MB")

def main():
    if len(sys.argv) < 3:
        print("Использование: python opencv_video_upscaler.py input.mp4 output.mp4")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2]
    
    # Создаём выходную папку
    Path(output_video).parent.mkdir(exist_ok=True)
    
    upscale_video_to_4k(input_video, output_video)

if __name__ == "__main__":
    main() 