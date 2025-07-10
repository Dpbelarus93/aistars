#!/usr/bin/env python3
"""
АПСКЕЙЛ ФИНАЛЬНОГО КЛИПА
Улучшает качество клипа "Хочу еще финал !.mov"
"""

import os
import subprocess
import shutil
from pathlib import Path

def main():
    print("🎬 АПСКЕЙЛ ФИНАЛЬНОГО КЛИПА")
    print("=" * 40)
    
    # Путь к твоему клипу
    input_file = Path("~/Desktop/Хочу еще !/Хочу еще финал !.mov").expanduser()
    
    if not input_file.exists():
        print(f"❌ ФАЙЛ НЕ НАЙДЕН: {input_file}")
        return
    
    # Проверяем ffmpeg
    if not shutil.which('ffmpeg'):
        print("❌ FFMPEG не найден! Установи его сначала")
        return
    
    # Информация о файле
    size_mb = input_file.stat().st_size / (1024 * 1024)
    print(f"📹 НАЙДЕН КЛИП: {input_file.name}")
    print(f"📊 РАЗМЕР: {size_mb:.1f} MB")
    
    # Выбираем качество
    print("\n📐 ВЫБЕРИ КАЧЕСТВО АПСКЕЙЛА:")
    print("1. 2x (HD → 4K) - рекомендуется")
    print("2. 4x (HD → 8K) - максимум")
    print("3. 1.5x (небольшое улучшение)")
    
    scale_options = {1: 2, 2: 4, 3: 1.5}
    
    while True:
        try:
            choice = int(input("Выбери (1-3): "))
            if choice in scale_options:
                scale = scale_options[choice]
                break
            else:
                print("❌ Выбери 1, 2 или 3!")
        except ValueError:
            print("❌ Введи число!")
    
    # Создаем выходной файл
    output_file = Path(f"UPSCALED_{scale}X_хочу_еще_финал.mp4")
    
    print(f"\n🚀 НАЧИНАЕМ АПСКЕЙЛ {scale}x")
    print(f"📤 РЕЗУЛЬТАТ: {output_file.name}")
    
    # Команда ffmpeg с максимальным качеством
    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-vf', f'scale=iw*{scale}:ih*{scale}:flags=lanczos',
        '-c:v', 'libx264',
        '-preset', 'slower',  # Максимальное качество
        '-crf', '16',         # Очень высокое качество
        '-c:a', 'aac',
        '-b:a', '256k',       # Высокое качество звука
        '-movflags', '+faststart',  # Для быстрого воспроизведения
        '-y',
        str(output_file)
    ]
    
    print(f"\n⚙️  КОМАНДА FFMPEG:")
    print(' '.join(cmd))
    
    try:
        print("\n⏳ ОБРАБОТКА... (может занять несколько минут)")
        
        # Запускаем с прогрессом
        process = subprocess.run(cmd, check=True)
        
        if output_file.exists():
            new_size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"\n✅ ГОТОВО!")
            print(f"📁 ФАЙЛ: {output_file.name}")
            print(f"📊 РАЗМЕР: {new_size_mb:.1f} MB")
            print(f"📈 УВЕЛИЧЕНИЕ: {new_size_mb/size_mb:.1f}x")
            print(f"🎯 КАЧЕСТВО: {scale}x улучшение")
            
        else:
            print("❌ Файл не создался!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ ОШИБКА: {e}")
        
    except KeyboardInterrupt:
        print("\n⚠️  ПРЕРВАНО ПОЛЬЗОВАТЕЛЕМ")

if __name__ == "__main__":
    main() 