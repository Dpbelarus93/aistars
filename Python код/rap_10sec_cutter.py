#!/usr/bin/env python3
"""
✂️ RAP 10SEC CUTTER ✂️
Нарезаем трек на 10-секундные фрагменты
Удаляем старые папки!

Разрабатывается с помощью AI!
"""

import wave
import numpy as np
from pathlib import Path
import shutil

def load_audio_simple(file_path):
    """
    Простая загрузка WAV файла
    """
    try:
        with wave.open(str(file_path), 'rb') as wav_file:
            frames = wav_file.readframes(-1)
            sample_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            
            # Конвертируем в numpy array
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Если стерео, берем среднее
            if channels == 2:
                audio_data = audio_data.reshape(-1, 2)
                audio_data = np.mean(audio_data, axis=1)
            
            # Нормализуем к [-1, 1]
            audio_data = audio_data.astype(np.float32) / 32768.0
            
            return audio_data, sample_rate
            
    except Exception as e:
        print(f"❌ Ошибка загрузки аудио: {e}")
        return None, None

def save_audio_segment(audio_data, sample_rate, start_time, end_time, output_file):
    """
    Сохраняет сегмент аудио
    """
    try:
        start_sample = int(start_time * sample_rate)
        end_sample = int(end_time * sample_rate)
        
        segment = audio_data[start_sample:end_sample]
        
        # Конвертируем обратно в int16
        segment_int16 = (segment * 32767).astype(np.int16)
        
        # Сохраняем как WAV
        with wave.open(str(output_file), 'wb') as wav_file:
            wav_file.setnchannels(1)  # Моно
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(segment_int16.tobytes())
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return False

def delete_old_folders():
    """
    Удаляет старые папки с сегментами
    """
    music_dir = Path.home() / "Desktop" / "эксперименты с музыкой"
    
    folders_to_delete = [
        "vocals_only",
        "professional_vocals", 
        "vocals_6sec_segments"
    ]
    
    print("🗑️  УДАЛЯЮ СТАРЫЕ ПАПКИ:")
    print("=" * 40)
    
    for folder_name in folders_to_delete:
        folder_path = music_dir / folder_name
        if folder_path.exists():
            try:
                shutil.rmtree(folder_path)
                print(f"✅ Удалена: {folder_name}")
            except Exception as e:
                print(f"❌ Ошибка удаления {folder_name}: {e}")
        else:
            print(f"⚠️  Не найдена: {folder_name}")
    
    print()

def create_10sec_segments():
    """
    Создает 10-секундные сегменты
    """
    
    # Находим оригинальный трек в правильной папке
    base_dir = Path.home() / "Desktop" / "хочу еще"
    rap_file = base_dir / "Аудио треки" / "Я в потоке, нет я в топе ,.wav"
    
    if not rap_file.exists():
        print("❌ Оригинальный RAP трек не найден!")
        print(f"   Ищу: {rap_file}")
        return False
    
    # Создаем папку для 10-секундных сегментов
    output_dir = base_dir / "rap_10sec_segments"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print("✂️ RAP 10SEC CUTTER")
    print("=" * 50)
    print(f"🎵 Трек: {rap_file.name}")
    print(f"📁 Выход: {output_dir.name}")
    print()
    
    # Загружаем аудио
    print("🔄 Загружаю аудио...")
    audio_data, sample_rate = load_audio_simple(rap_file)
    
    if audio_data is None:
        return False
    
    duration = len(audio_data) / sample_rate
    print(f"⏱️  Длительность: {duration:.1f} секунд")
    print()
    
    # Нарезаем на 10-секундные сегменты
    print("✂️  НАРЕЗАЮ 10-СЕКУНДНЫЕ СЕГМЕНТЫ:")
    print("=" * 60)
    
    segment_duration = 10.0  # 10 секунд
    current_time = 0
    segment_count = 0
    
    while current_time < duration - 1:  # Оставляем запас 1 секунда
        
        end_time = min(current_time + segment_duration, duration)
        actual_duration = end_time - current_time
        
        # Пропускаем слишком короткие сегменты
        if actual_duration < 5:
            break
            
        segment_count += 1
        
        # Создаем имя файла
        start_min = int(current_time // 60)
        start_sec = int(current_time % 60)
        end_min = int(end_time // 60)
        end_sec = int(end_time % 60)
        
        filename = f"rap_10sec_{segment_count:03d}_{start_min:02d}m{start_sec:02d}s-{end_min:02d}m{end_sec:02d}s.wav"
        output_file = output_dir / filename
        
        # Сохраняем сегмент
        if save_audio_segment(audio_data, sample_rate, current_time, end_time, output_file):
            
            size_kb = output_file.stat().st_size / 1024
            
            print(f"✅ {segment_count:2d}. {filename}")
            print(f"      ⏱️  {current_time:.1f}s - {end_time:.1f}s ({actual_duration:.1f}s)")
            print(f"      💾 {size_kb:.0f} KB")
            print()
        else:
            print(f"❌ Ошибка сохранения сегмента {segment_count}")
        
        # Переходим к следующему сегменту
        current_time += segment_duration
    
    print("=" * 60)
    print(f"🎉 НАРЕЗКА ЗАВЕРШЕНА!")
    print(f"✅ Создано: {segment_count} сегментов по 10 секунд")
    print(f"📁 Папка: {output_dir}")
    print()
    
    # Показываем статистику
    total_time = segment_count * 10
    print("📊 СТАТИСТИКА:")
    print(f"   🎤 Общее время сегментов: {total_time} сек ({total_time/60:.1f} мин)")
    print(f"   🎵 Длительность трека: {duration:.1f} сек ({duration/60:.1f} мин)")
    print(f"   📈 Покрытие: {(total_time/duration)*100:.1f}%")
    print()
    print("💡 ГОТОВЫ К ИСПОЛЬЗОВАНИЮ В ЛИПСИНКЕ!")
    
    return True

def copy_best_segments_to_desktop():
    """
    Копирует лучшие сегменты на рабочий стол
    """
    base_dir = Path.home() / "Desktop" / "хочу еще"
    segments_dir = base_dir / "rap_10sec_segments"
    desktop = Path.home() / "Desktop"
    
    if not segments_dir.exists():
        return
    
    # Берем первые 3 сегмента
    segment_files = sorted(list(segments_dir.glob("rap_10sec_*.wav")))[:3]
    
    if not segment_files:
        return
    
    print("📁 КОПИРУЮ ЛУЧШИЕ СЕГМЕНТЫ НА РАБОЧИЙ СТОЛ:")
    print("=" * 50)
    
    for i, segment_file in enumerate(segment_files, 1):
        
        simple_name = f"rap_10sec_{i:02d}.wav"
        target_file = desktop / simple_name
        
        # Удаляем старый файл если есть
        if target_file.exists():
            target_file.unlink()
        
        # Копируем
        shutil.copy2(segment_file, target_file)
        
        size_kb = target_file.stat().st_size / 1024
        
        print(f"✅ {i}. {simple_name}")
        print(f"      💾 {size_kb:.0f} KB")
        print(f"      ⏱️  10 секунд")
        print()

def main():
    print("✂️ RAP 10SEC CUTTER")
    print("Нарезаем на 10 секунд и убираем старое!")
    print("=" * 50)
    print()
    
    # Удаляем старые папки
    delete_old_folders()
    
    # Создаем новые 10-секундные сегменты
    if create_10sec_segments():
        print()
        copy_best_segments_to_desktop()
        
        print()
        print("🚀 ВСЁ ГОТОВО!")
        print("   📁 Новая папка: rap_10sec_segments")
        print("   🗑️  Старые папки удалены")
        print("   📋 Лучшие сегменты на рабочем столе")

if __name__ == "__main__":
    main() 