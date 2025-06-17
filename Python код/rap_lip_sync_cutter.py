#!/usr/bin/env python3
"""
RAP Lip-Sync Cutter - Нарезка рап-треков для липсинка
Создает оптимальные сегменты для зачитки и анимации губ
"""

import os
from pathlib import Path
from pydub import AudioSegment
import sys

def create_rap_segments(audio_file, output_dir):
    """
    Создает специальные сегменты для RAP и липсинка
    """
    
    audio_path = Path(audio_file)
    
    if not audio_path.exists():
        print(f"❌ Файл не найден: {audio_file}")
        return False
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎤 Загружаю RAP трек: {audio_path.name}")
    
    try:
        # Загружаем WAV файл напрямую
        print("📡 Загружаю WAV файл...")
        audio = AudioSegment.from_wav(str(audio_path))
        total_duration_sec = len(audio) / 1000
        
        print(f"📊 Общая длительность: {total_duration_sec:.1f} секунд")
        print(f"📁 Сохраняем в: {output_dir}")
        print("🎵 Создаю оптимальные сегменты для липсинка...")
        print("=" * 60)
        
        # Определяем сегменты для рапа
        segments = [
            # Короткие сегменты для быстрой зачитки
            {"name": "intro_hook", "start": 0, "duration": 15, "desc": "Вступление - короткий хук"},
            {"name": "verse_1", "start": 15, "duration": 20, "desc": "Первый куплет"},
            {"name": "energy_peak", "start": 35, "duration": 25, "desc": "Энергичная часть"},
            {"name": "chorus_section", "start": 60, "duration": 18, "desc": "Припев/хук"},
            {"name": "finale_power", "start": max(0, total_duration_sec - 22), "duration": 22, "desc": "Мощный финал"},
        ]
        
        # Дополнительные варианты длительности
        duration_variants = [
            {"suffix": "short", "duration": 10, "desc": "Короткий сегмент"},
            {"suffix": "medium", "duration": 30, "desc": "Средний сегмент"}, 
            {"suffix": "long", "duration": 45, "desc": "Длинный сегмент"},
        ]
        
        segment_count = 0
        
        # Создаем основные сегменты
        for seg in segments:
            start_sec = seg["start"]
            duration_sec = seg["duration"]
            
            # Проверяем границы
            if start_sec >= total_duration_sec:
                continue
                
            if start_sec + duration_sec > total_duration_sec:
                duration_sec = total_duration_sec - start_sec
            
            start_ms = int(start_sec * 1000)
            end_ms = int((start_sec + duration_sec) * 1000)
            
            # Извлекаем сегмент
            segment = audio[start_ms:end_ms]
            
            # Сохраняем в MP3 формате
            filename = f"rap_{seg['name']}_{duration_sec:.0f}s.mp3"
            segment_path = output_dir / filename
            
            print(f"💾 Сохраняю: {filename}")
            segment.export(str(segment_path), format="mp3", bitrate="192k")
            
            segment_count += 1
            print(f"🎤 Сегмент {segment_count}: {filename}")
            print(f"   📝 {seg['desc']}")
            print(f"   ⏱️  {start_sec:.1f}с - {start_sec + duration_sec:.1f}с ({duration_sec:.1f}с)")
            print()
        
        # Создаем дополнительные варианты от начала
        print("🔥 Создаю дополнительные варианты для экспериментов:")
        print("-" * 60)
        
        for variant in duration_variants:
            duration_sec = variant["duration"]
            
            if duration_sec > total_duration_sec:
                duration_sec = total_duration_sec
            
            start_ms = 0
            end_ms = int(duration_sec * 1000)
            
            segment = audio[start_ms:end_ms]
            
            filename = f"rap_experiment_{variant['suffix']}_{duration_sec:.0f}s.mp3"
            segment_path = output_dir / filename
            
            print(f"💾 Сохраняю: {filename}")
            segment.export(str(segment_path), format="mp3", bitrate="192k")
            
            segment_count += 1
            print(f"🎯 Эксперимент {segment_count - 5}: {filename}")
            print(f"   📝 {variant['desc']} для липсинка")
            print(f"   ⏱️  0.0с - {duration_sec:.1f}с ({duration_sec:.1f}с)")
            print()
        
        print("=" * 60)
        print(f"🎉 ГОТОВО! Создано {segment_count} RAP-сегментов для липсинка!")
        print(f"📁 Все файлы сохранены в: {output_dir}")
        print()
        print("💡 РЕКОМЕНДАЦИИ ДЛЯ ЛИПСИНКА:")
        print("   🎤 Короткие сегменты (10-15с) - для быстрой зачитки")
        print("   🎵 Средние сегменты (20-30с) - для полноценного куплета")
        print("   🔥 Длинные сегменты (40-45с) - для развернутого перформанса")
        print()
        print("🚀 СЛЕДУЮЩИЕ ШАГИ:")
        print("   1. Выберите лучший сегмент для вашего стиля")
        print("   2. Загрузите в AI для липсинка")
        print("   3. Синхронизируйте с видео")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке файла: {e}")
        print("💡 Попробуйте конвертировать WAV в MP3 сначала")
        return False

def main():
    print("🎤 RAP LIP-SYNC CUTTER")
    print("Специальная нарезка для зачитки и анимации губ")
    print("=" * 60)
    
    # Ищем конкретный файл
    source_file = Path("../Аудио треки/Я в потоке, нет я в топе ,.wav")
    
    if not source_file.exists():
        print(f"❌ Файл не найден: {source_file}")
        print("Проверьте путь к файлу...")
        return
    
    # Создаем папку на рабочем столе
    desktop_path = Path.home() / "Desktop"
    output_dir = desktop_path / "эксперименты с музыкой"
    
    print(f"🎯 Обрабатываю: {source_file.name}")
    print(f"📂 Создаю папку: {output_dir}")
    
    # Создаем сегменты
    create_rap_segments(source_file, output_dir)

if __name__ == "__main__":
    main() 