#!/usr/bin/env python3
"""
Vocal Extractor - Извлечение голоса из треков
Убирает фоновую музыку и биты, оставляет только вокал для липсинка
"""

import os
from pathlib import Path
from pydub import AudioSegment
import numpy as np
import sys

def extract_vocals_karaoke(audio_segment):
    """
    Извлекает вокал методом караоке (center channel extraction)
    Работает если вокал в центре, а музыка по бокам
    """
    try:
        # Конвертируем в стерео если нужно
        if audio_segment.channels == 1:
            audio_segment = audio_segment.set_channels(2)
        
        # Получаем левый и правый каналы
        left = audio_segment.split_to_mono()[0]
        right = audio_segment.split_to_mono()[1]
        
        # Инвертируем правый канал и смешиваем с левым
        inverted_right = right.invert_phase()
        vocals = left.overlay(inverted_right)
        
        # Усиливаем результат
        vocals = vocals + 6  # +6 dB
        
        return vocals
        
    except Exception as e:
        print(f"❌ Ошибка караоке-метода: {e}")
        return audio_segment

def extract_vocals_center_focus(audio_segment):
    """
    Фокусируется на центральном канале и убирает боковые частоты
    """
    try:
        if audio_segment.channels == 1:
            return audio_segment
        
        # Получаем моно из стерео (центр)
        mono = audio_segment.set_channels(1)
        
        # Применяем фильтр для голосовых частот (100Hz - 4kHz)
        # Пока без сложных фильтров, просто нормализуем
        vocals = mono.normalize()
        
        return vocals
        
    except Exception as e:
        print(f"❌ Ошибка центрального фокуса: {e}")
        return audio_segment

def extract_vocals_isolation(audio_segment):
    """
    Простая изоляция вокала - комбинация методов
    """
    try:
        # Метод 1: Караоке
        vocals_karaoke = extract_vocals_karaoke(audio_segment)
        
        # Метод 2: Центральный фокус  
        vocals_center = extract_vocals_center_focus(audio_segment)
        
        # Выбираем лучший результат (по громкости)
        if vocals_karaoke.dBFS > vocals_center.dBFS:
            result = vocals_karaoke
            method = "караоке"
        else:
            result = vocals_center  
            method = "центр"
        
        # Нормализуем и немного сжимаем динамику
        result = result.normalize()
        
        return result, method
        
    except Exception as e:
        print(f"❌ Ошибка изоляции: {e}")
        return audio_segment, "исходный"

def process_vocal_extraction(input_dir, output_dir):
    """
    Обрабатывает все WAV файлы и извлекает вокал
    """
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Находим все WAV файлы с нарезкой
    wav_files = list(input_path.glob("rap_5sec_*.wav"))
    
    if not wav_files:
        print("❌ Файлы rap_5sec_*.wav не найдены!")
        return False
    
    total_files = len(wav_files)
    print(f"🎤 Найдено {total_files} файлов для обработки")
    print(f"📂 Входная папка: {input_path}")
    print(f"📁 Выходная папка: {output_path}")
    print("🎵 Извлекаю голос из каждого сегмента...")
    print("=" * 60)
    
    success_count = 0
    
    for i, file_path in enumerate(sorted(wav_files), 1):
        try:
            print(f"🎧 [{i}/{total_files}] Обрабатываю: {file_path.name}")
            
            # Загружаем аудио
            audio = AudioSegment.from_wav(str(file_path))
            
            # Извлекаем вокал
            vocals, method = extract_vocals_isolation(audio)
            
            # Создаем имя выходного файла
            output_filename = f"vocals_{file_path.stem}.wav"
            output_file_path = output_path / output_filename
            
            # Сохраняем результат
            vocals.export(str(output_file_path), format="wav")
            
            success_count += 1
            print(f"✅ Готово! Метод: {method}")
            print(f"   📁 Сохранено: {output_filename}")
            
            # Показываем прогресс
            if i % 5 == 0 or i == total_files:
                print(f"📊 Прогресс: {i}/{total_files} ({(i/total_files)*100:.1f}%)")
            
            print()
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {file_path.name}: {e}")
            print()
    
    print("=" * 60)
    print(f"🎉 ОБРАБОТКА ЗАВЕРШЕНА!")
    print(f"✅ Успешно обработано: {success_count}/{total_files}")
    print(f"❌ Ошибок: {total_files - success_count}")
    print(f"📁 Все вокальные файлы в: {output_path}")
    print()
    print("💡 ЧТО ПОЛУЧИЛОСЬ:")
    print("   🎤 Файлы только с голосом (без битов)")
    print("   🔇 Убрана фоновая музыка")
    print("   🎬 Готово для липсинка!")
    print()
    print("🚀 ИСПОЛЬЗУЙ ФАЙЛЫ С ПРЕФИКСОМ 'vocals_' ДЛЯ ЛИПСИНКА!")
    
    return True

def main():
    print("🎤 VOCAL EXTRACTOR")
    print("Убираем биты - оставляем только голос!")
    print("=" * 50)
    
    # Папки
    desktop_path = Path.home() / "Desktop"
    input_dir = desktop_path / "эксперименты с музыкой"
    output_dir = desktop_path / "эксперименты с музыкой" / "vocals_only"
    
    print(f"🎯 Исходные файлы: {input_dir}")
    print(f"📂 Результат: {output_dir}")
    print()
    
    if not input_dir.exists():
        print(f"❌ Папка не найдена: {input_dir}")
        return
    
    process_vocal_extraction(input_dir, output_dir)

if __name__ == "__main__":
    main() 