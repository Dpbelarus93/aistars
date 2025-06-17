#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎤 RAP LIP SYNC MIXER
🎬 Создаем 20 липсинк видео: 10 треков × 2 фото = 20 результатов
🎵 Микс лучших кусочков рэпа с лучшими фотками
"""

import os
import random
import shutil
from pathlib import Path
from typing import List
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - 🎤 [%(levelname)s] - %(message)s'
)

class RapLipSyncMixer:
    """🎵 Микс-мастер для рэп липсинка"""
    
    def __init__(self):
        self.logger = logging.getLogger("RapLipSyncMixer")
        
        # Базовые пути
        self.base_dir = Path("хочу еще")
        
        # Рабочие директории
        self.workspace = self.base_dir / "LIP_SYNC_WORKSPACE"
        self.input_photos = self.workspace / "input_photos"
        self.input_audio = self.workspace / "input_audio"
        self.output_videos = self.workspace / "output_videos"
        
        # Создание директорий
        for dir_path in [self.input_photos, self.input_audio, self.output_videos]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Источники материалов
        self.photo_sources = [
            Path("Фотографии"),
            Path("upscaled_images")
        ]
        
        self.audio_sources = [
            Path(".."),  # Корень проекта - там rap_10sec_*.wav
            Path("../эксперименты с музыкой")
        ]
        
        self.logger.info("🎤 Rap Lip Sync Mixer инициализирован")
    
    def find_best_photos(self, count: int = 10) -> List[Path]:
        """📸 Находим лучшие фото для липсинка"""
        
        self.logger.info(f"📸 Ищем {count} лучших фото...")
        
        all_photos = []
        
        # Собираем все фото
        for source in self.photo_sources:
            if source.exists():
                # JPG из папки Фотографии
                if source.name == "Фотографии":
                    photos = list(source.glob("*.jpg"))
                    # Отбираем лучшие по размеру (больше = лучше качество)
                    photos.sort(key=lambda p: p.stat().st_size, reverse=True)
                    all_photos.extend(photos[:15])  # Топ 15 JPG
                
                # PNG из upscaled_images
                elif source.name == "upscaled_images":
                    photos = list(source.glob("*.png"))
                    # Берем каждое 10-е изображение для разнообразия
                    selected_photos = photos[::10]
                    all_photos.extend(selected_photos[:15])  # Топ 15 PNG
        
        # Перемешиваем и берем нужное количество
        random.shuffle(all_photos)
        selected = all_photos[:count]
        
        self.logger.info(f"📸 Отобрано {len(selected)} фото")
        for i, photo in enumerate(selected, 1):
            self.logger.info(f"  {i}. {photo.name} ({photo.stat().st_size // 1024}KB)")
        
        return selected
    
    def find_best_audio(self, count: int = 10) -> List[Path]:
        """🎵 Находим лучшие аудио треки"""
        
        self.logger.info(f"🎵 Ищем {count} лучших треков...")
        
        all_audio = []
        
        # Собираем все аудио
        for source in self.audio_sources:
            if source.exists():
                # Основные 10-секундные треки
                if source == Path(".."):
                    tracks = list(source.glob("rap_10sec_*.wav"))
                    all_audio.extend(tracks)
                
                # 5-секундные сегменты из экспериментов
                elif source.name == "эксперименты с музыкой":
                    tracks = list(source.glob("rap_5sec_*.wav"))
                    # Берем каждый 3-й для разнообразия
                    selected_tracks = tracks[::3]
                    all_audio.extend(selected_tracks[:7])  # Топ 7 сегментов
        
        # Перемешиваем и берем нужное количество
        random.shuffle(all_audio)
        selected = all_audio[:count]
        
        self.logger.info(f"🎵 Отобрано {len(selected)} треков")
        for i, track in enumerate(selected, 1):
            self.logger.info(f"  {i}. {track.name} ({track.stat().st_size // 1024}KB)")
        
        return selected
    
    def setup_workspace(self):
        """🛠️ Настройка рабочего пространства"""
        
        self.logger.info("🛠️ Настраиваю рабочее пространство...")
        
        # Очищаем старые файлы
        for file in self.input_photos.glob("*"):
            file.unlink()
        for file in self.input_audio.glob("*"):
            file.unlink()
        
        # Находим материалы
        best_photos = self.find_best_photos(10)
        best_audio = self.find_best_audio(10)
        
        # Копируем фото
        copied_photos = 0
        for i, photo in enumerate(best_photos, 1):
            try:
                dest = self.input_photos / f"photo_{i:02d}_{photo.stem}.{photo.suffix[1:]}"
                shutil.copy2(photo, dest)
                copied_photos += 1
            except Exception as e:
                self.logger.error(f"Ошибка копирования фото {photo.name}: {e}")
        
        # Копируем аудио
        copied_audio = 0
        for i, audio in enumerate(best_audio, 1):
            try:
                dest = self.input_audio / f"track_{i:02d}_{audio.stem}.wav"
                shutil.copy2(audio, dest)
                copied_audio += 1
            except Exception as e:
                self.logger.error(f"Ошибка копирования аудио {audio.name}: {e}")
        
        self.logger.info(f"✅ Готово: {copied_photos} фото, {copied_audio} треков")
        
        return {"photos": copied_photos, "audio": copied_audio}
    
    def generate_lip_sync_plan(self):
        """📋 Генерация плана липсинк миксов"""
        
        photos = sorted(list(self.input_photos.glob("*")))
        audios = sorted(list(self.input_audio.glob("*")))
        
        plan = []
        
        # Каждый трек с 2 разными фото
        for i, audio in enumerate(audios, 1):
            # Выбираем 2 случайных фото для этого трека
            selected_photos = random.sample(photos, min(2, len(photos)))
            
            for j, photo in enumerate(selected_photos, 1):
                mix_name = f"mix_{i:02d}_{j:01d}_{audio.stem}_{photo.stem}"
                
                plan.append({
                    "name": mix_name,
                    "audio": audio,
                    "photo": photo,
                    "output": self.output_videos / f"{mix_name}.mp4"
                })
        
        self.logger.info(f"📋 План создан: {len(plan)} липсинк миксов")
        
        return plan
    
    def create_mix_summary(self, plan):
        """📊 Создание сводки миксов"""
        
        summary = f"""
🎤 RAP LIP SYNC MIXER - ПЛАН СОЗДАНИЯ
{'='*60}

📊 СТАТИСТИКА:
  • Всего миксов: {len(plan)}
  • Уникальных треков: {len(set(mix['audio'].name for mix in plan))}
  • Уникальных фото: {len(set(mix['photo'].name for mix in plan))}

🎵 ТРЕКИ В РАБОТЕ:"""
        
        unique_tracks = list(set(mix['audio'].name for mix in plan))
        for i, track in enumerate(unique_tracks, 1):
            summary += f"\n  {i:2d}. {track}"
        
        summary += f"""

📸 ФОТО В РАБОТЕ:"""
        
        unique_photos = list(set(mix['photo'].name for mix in plan))
        for i, photo in enumerate(unique_photos, 1):
            summary += f"\n  {i:2d}. {photo}"
        
        summary += f"""

🎬 ДЕТАЛЬНЫЙ ПЛАН:"""
        
        for i, mix in enumerate(plan, 1):
            summary += f"""
  {i:2d}. {mix['name']}
      🎵 {mix['audio'].name}
      📸 {mix['photo'].name}
      📹 → {mix['output'].name}"""
        
        return summary

def main():
    """🚀 Главная функция"""
    
    print("🎤" * 60)
    print("🎵 RAP LIP SYNC MIXER")
    print("🎬 10 треков × 2 фото = 20 крутых видео!")
    print("🎤" * 60)
    print()
    
    # Инициализация
    mixer = RapLipSyncMixer()
    
    # Настройка workspace
    print("🛠️ Настройка рабочего пространства...")
    setup_result = mixer.setup_workspace()
    print(f"✅ Материалы подготовлены: {setup_result['photos']} фото, {setup_result['audio']} треков")
    print()
    
    # Генерация плана
    print("📋 Создание плана миксов...")
    plan = mixer.generate_lip_sync_plan()
    
    # Сводка
    summary = mixer.create_mix_summary(plan)
    print(summary)
    print()
    
    # Сохранение плана
    plan_file = Path("хочу еще/rap_mix_plan.txt")
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"📄 План сохранен: {plan_file}")
    print()
    
    print("🎬 ГОТОВО К ЗАПУСКУ ЛИПСИНКА!")
    print("Следующий шаг: запустить professional_lip_sync_automation.py")
    print("🎤" * 60)

if __name__ == "__main__":
    main() 