#!/usr/bin/env python3
"""
Audio Splitter - Автоматическая резка аудио треков
Поддерживает MP3, WAV, M4A, FLAC и другие форматы
"""

import os
from pathlib import Path
from pydub import AudioSegment
import sys

def split_audio(audio_file, segment_length_seconds=30, output_dir=None):
    """
    Режет аудио файл на равные части
    
    Args:
        audio_file: путь к аудио файлу
        segment_length_seconds: длительность каждого сегмента в секундах
        output_dir: папка для сохранения (по умолчанию рядом с исходным файлом)
    """
    
    audio_path = Path(audio_file)
    
    if not audio_path.exists():
        print(f"❌ Файл не найден: {audio_file}")
        return False
    
    # Определяем папку для сохранения
    if output_dir is None:
        output_dir = audio_path.parent / f"{audio_path.stem}_split"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    print(f"🎵 Загружаю аудио файл: {audio_path.name}")
    
    try:
        # Загружаем аудио (pydub автоматически определит формат)
        audio = AudioSegment.from_file(str(audio_path))
        
        # Конвертируем длительность в миллисекунды
        segment_length_ms = segment_length_seconds * 1000
        
        # Общая информация
        total_duration_sec = len(audio) / 1000
        total_segments = int(len(audio) / segment_length_ms) + (1 if len(audio) % segment_length_ms > 0 else 0)
        
        print(f"📊 Общая длительность: {total_duration_sec:.1f} секунд")
        print(f"📦 Будет создано: {total_segments} сегментов по {segment_length_seconds} сек")
        print(f"📁 Сохраняем в: {output_dir}")
        print("=" * 50)
        
        # Режем на части
        for i in range(total_segments):
            start_ms = i * segment_length_ms
            end_ms = min((i + 1) * segment_length_ms, len(audio))
            
            # Извлекаем сегмент
            segment = audio[start_ms:end_ms]
            
            # Формируем имя файла
            segment_filename = f"{audio_path.stem}_part_{i+1:03d}.mp3"
            segment_path = output_dir / segment_filename
            
            # Сохраняем сегмент
            segment.export(str(segment_path), format="mp3")
            
            # Статистика
            segment_duration = (end_ms - start_ms) / 1000
            start_time = start_ms / 1000
            end_time = end_ms / 1000
            
            print(f"✅ Часть {i+1}/{total_segments}: {segment_filename}")
            print(f"   ⏱️  {start_time:.1f}с - {end_time:.1f}с ({segment_duration:.1f}с)")
        
        print("=" * 50)
        print(f"🎉 ГОТОВО! Создано {total_segments} частей в папке: {output_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке файла: {e}")
        return False

def split_by_timestamps(audio_file, timestamps, output_dir=None):
    """
    Режет аудио по заданным временным меткам
    
    Args:
        audio_file: путь к аудио файлу
        timestamps: список временных меток в секундах [(start1, end1), (start2, end2), ...]
        output_dir: папка для сохранения
    """
    
    audio_path = Path(audio_file)
    
    if not audio_path.exists():
        print(f"❌ Файл не найден: {audio_file}")
        return False
    
    if output_dir is None:
        output_dir = audio_path.parent / f"{audio_path.stem}_custom_split"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    print(f"🎵 Загружаю аудио файл: {audio_path.name}")
    
    try:
        audio = AudioSegment.from_file(str(audio_path))
        total_duration_sec = len(audio) / 1000
        
        print(f"📊 Общая длительность: {total_duration_sec:.1f} секунд")
        print(f"📦 Будет создано: {len(timestamps)} сегментов")
        print(f"📁 Сохраняем в: {output_dir}")
        print("=" * 50)
        
        for i, (start_sec, end_sec) in enumerate(timestamps):
            start_ms = int(start_sec * 1000)
            end_ms = int(end_sec * 1000)
            
            # Проверяем границы
            if end_ms > len(audio):
                end_ms = len(audio)
            
            # Извлекаем сегмент
            segment = audio[start_ms:end_ms]
            
            # Формируем имя файла
            segment_filename = f"{audio_path.stem}_segment_{i+1:03d}_{start_sec:.0f}s-{end_sec:.0f}s.mp3"
            segment_path = output_dir / segment_filename
            
            # Сохраняем сегмент
            segment.export(str(segment_path), format="mp3")
            
            segment_duration = (end_ms - start_ms) / 1000
            print(f"✅ Сегмент {i+1}: {segment_filename}")
            print(f"   ⏱️  {start_sec:.1f}с - {end_sec:.1f}с ({segment_duration:.1f}с)")
        
        print("=" * 50)
        print(f"🎉 ГОТОВО! Создано {len(timestamps)} сегментов в папке: {output_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке файла: {e}")
        return False

def find_audio_files(directory="."):
    """Находит все аудио файлы в папке"""
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(Path(directory).glob(f"*{ext}"))
        audio_files.extend(Path(directory).glob(f"*{ext.upper()}"))
    
    return audio_files

def main():
    print("🎵 AUDIO SPLITTER - Автоматическая резка аудио")
    print("=" * 50)
    
    # Ищем аудио файлы
    audio_files = find_audio_files("../Аудио треки")
    
    if not audio_files:
        # Ищем в текущей папке
        audio_files = find_audio_files(".")
    
    if not audio_files:
        print("❌ Аудио файлы не найдены!")
        print("Поддерживаемые форматы: MP3, WAV, M4A, FLAC, AAC, OGG")
        return
    
    print(f"🎯 Найдено {len(audio_files)} аудио файлов:")
    for i, file in enumerate(audio_files, 1):
        print(f"  {i}. {file.name}")
    
    print("\n📋 РЕЖИМЫ РАБОТЫ:")
    print("1. Равные части (например, по 30 секунд)")
    print("2. По временным меткам (ручной выбор)")
    print("3. Обработать все файлы по 30 секунд")
    
    try:
        mode = input("\nВыберите режим (1-3): ").strip()
        
        if mode == "1":
            # Выбираем файл
            file_num = int(input(f"Выберите файл (1-{len(audio_files)}): ")) - 1
            selected_file = audio_files[file_num]
            
            # Выбираем длительность
            duration = int(input("Длительность каждой части в секундах (по умолчанию 30): ") or "30")
            
            split_audio(selected_file, duration)
            
        elif mode == "2":
            # Выбираем файл
            file_num = int(input(f"Выберите файл (1-{len(audio_files)}): ")) - 1
            selected_file = audio_files[file_num]
            
            print("Введите временные метки в формате: начало-конец (в секундах)")
            print("Например: 0-30, 30-60, 60-90")
            timestamps_input = input("Временные метки: ")
            
            timestamps = []
            for pair in timestamps_input.split(","):
                start, end = map(float, pair.strip().split("-"))
                timestamps.append((start, end))
            
            split_by_timestamps(selected_file, timestamps)
            
        elif mode == "3":
            # Обрабатываем все файлы
            for audio_file in audio_files:
                print(f"\n🎵 Обрабатываю: {audio_file.name}")
                split_audio(audio_file, 30)
        
        else:
            print("❌ Неверный выбор!")
    
    except (ValueError, IndexError) as e:
        print(f"❌ Ошибка ввода: {e}")
    except KeyboardInterrupt:
        print("\n👋 Прервано пользователем")

if __name__ == "__main__":
    main() 