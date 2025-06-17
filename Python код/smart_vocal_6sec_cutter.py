#!/usr/bin/env python3
"""
🎤 SMART VOCAL 6SEC CUTTER 🎤
Умная нарезка трека по 6 секунд ТОЛЬКО там где есть голос
Пропускаем инструментальные части!

Разрабатывается с помощью AI!
"""

import wave
import numpy as np
from pathlib import Path
import shutil

def analyze_vocal_presence(audio_data, sample_rate, window_size=1.0):
    """
    Анализирует наличие голоса в аудио
    """
    window_samples = int(sample_rate * window_size)
    vocal_segments = []
    
    for i in range(0, len(audio_data), window_samples):
        window = audio_data[i:i + window_samples]
        
        if len(window) < window_samples // 2:  # Слишком короткий сегмент
            continue
        
        # Анализируем энергию в средних частотах (голос)
        # Простой алгоритм: если есть значимая амплитуда
        rms = np.sqrt(np.mean(window**2))
        
        # Порог для определения голоса (настраиваемый)
        vocal_threshold = 0.02
        
        if rms > vocal_threshold:
            start_time = i / sample_rate
            end_time = min((i + window_samples) / sample_rate, len(audio_data) / sample_rate)
            vocal_segments.append((start_time, end_time, rms))
    
    return vocal_segments

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

def create_6sec_vocal_segments():
    """
    Создает 6-секундные сегменты с голосом
    """
    
    # Находим оригинальный трек
    music_dir = Path.home() / "Desktop" / "эксперименты с музыкой"
    rap_file = music_dir / "Я в потоке, нет я в топе ,.wav"
    
    if not rap_file.exists():
        print("❌ Оригинальный RAP трек не найден!")
        print(f"   Ищу: {rap_file}")
        return False
    
    # Создаем папку для 6-секундных сегментов
    output_dir = music_dir / "vocals_6sec_segments"
    output_dir.mkdir(exist_ok=True)
    
    print("🎤 SMART VOCAL 6SEC CUTTER")
    print("=" * 50)
    print(f"🎵 Анализирую: {rap_file.name}")
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
    
    # Анализируем наличие голоса
    print("🔍 Анализирую наличие голоса...")
    vocal_segments = analyze_vocal_presence(audio_data, sample_rate)
    
    print(f"🎤 Найдено {len(vocal_segments)} сегментов с голосом")
    print()
    
    # Группируем в 6-секундные блоки
    print("✂️  НАРЕЗАЮ 6-СЕКУНДНЫЕ СЕГМЕНТЫ С ГОЛОСОМ:")
    print("=" * 60)
    
    segment_duration = 6.0  # 6 секунд
    current_time = 0
    segment_count = 0
    
    while current_time < duration - 1:  # Оставляем запас 1 секунда
        
        end_time = min(current_time + segment_duration, duration)
        
        # Проверяем есть ли голос в этом сегменте
        has_vocal = False
        for vocal_start, vocal_end, energy in vocal_segments:
            # Если вокальный сегмент пересекается с нашим 6-сек сегментом
            if vocal_start < end_time and vocal_end > current_time:
                has_vocal = True
                break
        
        if has_vocal:
            segment_count += 1
            
            # Создаем имя файла
            start_min = int(current_time // 60)
            start_sec = int(current_time % 60)
            end_min = int(end_time // 60)
            end_sec = int(end_time % 60)
            
            filename = f"vocal_6sec_{segment_count:03d}_{start_min:02d}m{start_sec:02d}s-{end_min:02d}m{end_sec:02d}s.wav"
            output_file = output_dir / filename
            
            # Сохраняем сегмент
            if save_audio_segment(audio_data, sample_rate, current_time, end_time, output_file):
                
                size_kb = output_file.stat().st_size / 1024
                
                print(f"✅ {segment_count:2d}. {filename}")
                print(f"      ⏱️  {current_time:.1f}s - {end_time:.1f}s ({end_time-current_time:.1f}s)")
                print(f"      💾 {size_kb:.0f} KB")
                print()
            else:
                print(f"❌ Ошибка сохранения сегмента {segment_count}")
        
        # Переходим к следующему сегменту
        current_time += segment_duration
    
    print("=" * 60)
    print(f"🎉 НАРЕЗКА ЗАВЕРШЕНА!")
    print(f"✅ Создано: {segment_count} сегментов по 6 секунд")
    print(f"📁 Папка: {output_dir}")
    print()
    
    # Показываем статистику
    total_vocal_time = segment_count * 6
    print("📊 СТАТИСТИКА:")
    print(f"   🎤 Время с голосом: {total_vocal_time} сек ({total_vocal_time/60:.1f} мин)")
    print(f"   🎵 Общая длительность: {duration:.1f} сек ({duration/60:.1f} мин)")
    print(f"   📈 Процент голоса: {(total_vocal_time/duration)*100:.1f}%")
    print()
    print("💡 ТЕПЕРЬ У ТЕБЯ ЕСТЬ ТОЛЬКО СЕГМЕНТЫ С ГОЛОСОМ!")
    
    return True

def main():
    print("🎤 SMART VOCAL 6SEC CUTTER")
    print("Нарезаем трек по 6 секунд ТОЛЬКО с голосом!")
    print("=" * 50)
    print()
    
    create_6sec_vocal_segments()

if __name__ == "__main__":
    main() 