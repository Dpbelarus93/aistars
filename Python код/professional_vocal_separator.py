#!/usr/bin/env python3
"""
🎤 PROFESSIONAL VOCAL SEPARATOR 🎤
Топовое решение для разделения голоса от битов
Использует лучшие AI модели: Demucs v4 HTDemucs

Разрабатывается с помощью AI для максимального качества!
"""

import os
import subprocess
import sys
from pathlib import Path
import time

def install_requirements():
    """
    Устанавливаем необходимые зависимости
    """
    print("🔧 УСТАНОВКА ПРОФЕССИОНАЛЬНЫХ ИНСТРУМЕНТОВ...")
    print("=" * 60)
    
    # Обновляем pip
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    
    # Устанавливаем Demucs v4 (самая лучшая модель)
    print("🚀 Устанавливаю Demucs v4 HTDemucs (SOTA модель)...")
    subprocess.run([sys.executable, "-m", "pip", "install", "demucs"], check=True)
    
    # Устанавливаем ffmpeg-python для аудио
    print("🎵 Устанавливаю аудио инструменты...")
    subprocess.run([sys.executable, "-m", "pip", "install", "ffmpeg-python"], check=True)
    
    print("✅ ВСЕ ИНСТРУМЕНТЫ УСТАНОВЛЕНЫ!")
    print()

def separate_vocals_professional(input_dir, output_dir):
    """
    Профессиональное разделение голоса от битов
    Использует state-of-the-art модель HTDemucs
    """
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Находим все WAV файлы
    wav_files = list(input_path.glob("rap_5sec_*.wav"))
    
    if not wav_files:
        print("❌ Файлы rap_5sec_*.wav не найдены!")
        return False
    
    total_files = len(wav_files)
    print(f"🎤 ПРОФЕССИОНАЛЬНАЯ ОБРАБОТКА: {total_files} файлов")
    print(f"🤖 Модель: HTDemucs v4 (State-of-the-Art)")
    print(f"📂 Входная папка: {input_path}")
    print(f"📁 Выходная папка: {output_path}")
    print("🔥 НАЧИНАЮ МАГИЮ ИИ...")
    print("=" * 60)
    
    success_count = 0
    
    for i, file_path in enumerate(sorted(wav_files), 1):
        try:
            print(f"🎧 [{i}/{total_files}] Обрабатываю: {file_path.name}")
            
            # Используем Demucs v4 HTDemucs для разделения
            # htdemucs_ft - это fine-tuned версия (лучшее качество)
            cmd = [
                "python", "-m", "demucs.separate",
                "--name", "htdemucs_ft",  # Лучшая модель
                "--two-stems=vocals",     # Только голос + инструментал
                "--out", str(output_path),
                "--mp3",                  # Сохраняем как MP3 для оптимизации
                "--mp3-bitrate", "320",   # Максимальное качество MP3
                str(file_path)
            ]
            
            # Запускаем Demucs
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Ищем созданные файлы
                stem_dir = output_path / "htdemucs_ft" / file_path.stem
                vocals_file = stem_dir / "vocals.mp3"
                instrumental_file = stem_dir / "no_vocals.mp3"
                
                if vocals_file.exists():
                    # Переименовываем в удобный формат
                    new_vocals_name = f"vocals_{file_path.stem}.mp3"
                    new_vocals_path = output_path / new_vocals_name
                    
                    # Перемещаем файл
                    vocals_file.rename(new_vocals_path)
                    
                    success_count += 1
                    print(f"✅ УСПЕХ! Чистый голос извлечен")
                    print(f"   📁 Сохранено: {new_vocals_name}")
                    
                    # Удаляем временную папку
                    import shutil
                    shutil.rmtree(stem_dir, ignore_errors=True)
                else:
                    print(f"❌ Файл не создан: {vocals_file}")
            else:
                print(f"❌ Ошибка Demucs: {result.stderr}")
            
            # Показываем прогресс
            if i % 5 == 0 or i == total_files:
                print(f"📊 Прогресс: {i}/{total_files} ({(i/total_files)*100:.1f}%)")
            
            print()
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {file_path.name}: {e}")
            print()
    
    print("=" * 60)
    print(f"🎉 ПРОФЕССИОНАЛЬНАЯ ОБРАБОТКА ЗАВЕРШЕНА!")
    print(f"✅ Успешно обработано: {success_count}/{total_files}")
    print(f"❌ Ошибок: {total_files - success_count}")
    print(f"📁 Все вокальные файлы в: {output_path}")
    print()
    print("🔥 ЧТО ПОЛУЧИЛОСЬ:")
    print("   🎤 КРИСТАЛЬНО ЧИСТЫЙ ГОЛОС без битов")
    print("   🤖 Обработано AI моделью HTDemucs v4")
    print("   🎯 Качество: ПРОФЕССИОНАЛЬНОЕ")
    print("   🎬 Готово для ЛИПСИНКА!")
    print()
    print("🚀 ИСПОЛЬЗУЙ ФАЙЛЫ С ПРЕФИКСОМ 'vocals_' ДЛЯ ЛИПСИНКА!")
    
    return True

def main():
    print("🎤 PROFESSIONAL VOCAL SEPARATOR")
    print("Топовое AI решение для разделения голоса!")
    print("Модель: HTDemucs v4 (State-of-the-Art)")
    print("=" * 50)
    
    # Проверяем установку Demucs
    try:
        result = subprocess.run(["python", "-m", "demucs.separate", "--help"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  Demucs не установлен. Устанавливаю...")
            install_requirements()
    except FileNotFoundError:
        print("⚠️  Demucs не найден. Устанавливаю...")
        install_requirements()
    
    # Папки
    desktop_path = Path.home() / "Desktop"
    input_dir = desktop_path / "эксперименты с музыкой"
    output_dir = desktop_path / "эксперименты с музыкой" / "professional_vocals"
    
    print(f"🎯 Исходные файлы: {input_dir}")
    print(f"📂 Результат: {output_dir}")
    print()
    
    if not input_dir.exists():
        print(f"❌ Папка не найдена: {input_dir}")
        return
    
    separate_vocals_professional(input_dir, output_dir)

if __name__ == "__main__":
    main() 