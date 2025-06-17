#!/usr/bin/env python3
"""
Full RAP 5-Second Cutter - Весь трек по 5 секунд
Режет весь трек на кусочки по 5 секунд для выбора лучших частей
"""

import os
from pathlib import Path
from pydub import AudioSegment
import sys

def cut_full_track_5sec(audio_file, output_dir):
    """
    Режет весь трек на сегменты по 5 секунд
    """
    
    audio_path = Path(audio_file)
    
    if not audio_path.exists():
        print(f"❌ Файл не найден: {audio_file}")
        return False
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎤 Загружаю RAP трек: {audio_path.name}")
    
    try:
        # Загружаем WAV файл
        print("📡 Загружаю WAV файл...")
        audio = AudioSegment.from_wav(str(audio_path))
        total_duration_sec = len(audio) / 1000
        
        # 5 секунд = 5000 миллисекунд
        segment_length_sec = 5
        segment_length_ms = 5000
        
        # Считаем количество сегментов
        total_segments = int(len(audio) / segment_length_ms)
        if len(audio) % segment_length_ms > 0:
            total_segments += 1
        
        print(f"📊 Общая длительность: {total_duration_sec:.1f} секунд")
        print(f"📦 Будет создано: {total_segments} сегментов по {segment_length_sec} секунд")
        print(f"📁 Сохраняем в: {output_dir}")
        print("🔪 Режем весь трек на кусочки...")
        print("=" * 60)
        
        # Режем на части по 5 секунд
        for i in range(total_segments):
            start_ms = i * segment_length_ms
            end_ms = min((i + 1) * segment_length_ms, len(audio))
            
            # Извлекаем сегмент
            segment = audio[start_ms:end_ms]
            
            # Время начала и конца в секундах
            start_sec = start_ms / 1000
            end_sec = end_ms / 1000
            actual_duration = (end_ms - start_ms) / 1000
            
            # Формируем имя файла с временными метками
            filename = f"rap_5sec_{i+1:03d}_{start_sec:.0f}s-{end_sec:.0f}s.wav"
            segment_path = output_dir / filename
            
            # Сохраняем как WAV
            segment.export(str(segment_path), format="wav")
            
            # Показываем прогресс каждые 10 сегментов
            if (i + 1) % 10 == 0 or i + 1 == total_segments:
                print(f"✅ Обработано {i+1}/{total_segments} сегментов ({((i+1)/total_segments)*100:.1f}%)")
        
        print("=" * 60)
        print(f"🎉 ГОТОВО! Создано {total_segments} сегментов по 5 секунд!")
        print(f"📁 Все файлы сохранены в: {output_dir}")
        print()
        print("🎯 ЧТО ПОЛУЧИЛОСЬ:")
        print(f"   📦 {total_segments} файлов по ~5 секунд каждый")
        print("   🎤 Полный охват всего трека")
        print("   ⚡ Быстрый выбор лучших моментов")
        print()
        print("💡 КАК ИСПОЛЬЗОВАТЬ:")
        print("   1. Прослушайте все сегменты")
        print("   2. Выберите самые крутые для рэпа")
        print("   3. Используйте для липсинка!")
        print()
        print("🔥 ФАЙЛЫ НАЗВАНЫ ПО СХЕМЕ:")
        print("   rap_5sec_001_0s-5s.wav (1-й сегмент: 0-5 секунд)")
        print("   rap_5sec_002_5s-10s.wav (2-й сегмент: 5-10 секунд)")
        print("   и так далее...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🔪 FULL RAP 5-SECOND CUTTER")
    print("Весь трек по 5 секунд для идеального выбора")
    print("=" * 60)
    
    # Файл для обработки
    source_file = Path("../Аудио треки/Я в потоке, нет я в топе ,.wav")
    
    if not source_file.exists():
        print(f"❌ Файл не найден: {source_file}")
        return
    
    # Папка на рабочем столе
    desktop_path = Path.home() / "Desktop"
    output_dir = desktop_path / "эксперименты с музыкой"
    
    print(f"🎯 Файл: {source_file.name}")
    print(f"📂 Папка: {output_dir}")
    print()
    
    cut_full_track_5sec(source_file, output_dir)

if __name__ == "__main__":
    main() 