#!/usr/bin/env python3
"""
Simple RAP Cutter - Простая нарезка без FFmpeg
Работает только с WAV, сохраняет как WAV
"""

import os
from pathlib import Path
from pydub import AudioSegment
import sys

def create_rap_segments_wav(audio_file, output_dir):
    """
    Создает RAP сегменты в формате WAV (без FFmpeg)
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
        
        print(f"📊 Общая длительность: {total_duration_sec:.1f} секунд")
        print(f"📁 Сохраняем в: {output_dir}")
        print("🎵 Создаю сегменты для липсинка...")
        print("=" * 60)
        
        # Простые сегменты
        segments = [
            {"name": "intro", "start": 0, "duration": 15, "desc": "Начало - энергичный старт"},
            {"name": "verse1", "start": 15, "duration": 25, "desc": "Первый куплет"},
            {"name": "hook", "start": 40, "duration": 20, "desc": "Хук/припев"},
            {"name": "verse2", "start": 60, "duration": 30, "desc": "Основной куплет"},
            {"name": "finale", "start": max(0, total_duration_sec - 20), "duration": 20, "desc": "Финальная часть"},
        ]
        
        segment_count = 0
        
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
            
            # Сохраняем как WAV (без FFmpeg)
            filename = f"rap_{seg['name']}_{duration_sec:.0f}s.wav"
            segment_path = output_dir / filename
            
            print(f"💾 Сохраняю: {filename}")
            segment.export(str(segment_path), format="wav")
            
            segment_count += 1
            print(f"🎤 Сегмент {segment_count}: {filename}")
            print(f"   📝 {seg['desc']}")
            print(f"   ⏱️  {start_sec:.1f}с - {start_sec + duration_sec:.1f}с ({duration_sec:.1f}с)")
            print()
        
        print("=" * 60)
        print(f"🎉 ГОТОВО! Создано {segment_count} RAP-сегментов!")
        print(f"📁 Все файлы в: {output_dir}")
        print()
        print("💡 ИСПОЛЬЗОВАНИЕ:")
        print("   🎤 Выберите подходящий сегмент")
        print("   🎬 Загрузите в AI для липсинка")
        print("   🚀 Создавайте крутые видео!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("🎤 SIMPLE RAP CUTTER")
    print("Быстрая нарезка для липсинка")
    print("=" * 50)
    
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
    
    create_rap_segments_wav(source_file, output_dir)

if __name__ == "__main__":
    main() 