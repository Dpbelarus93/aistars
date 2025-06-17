#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎯 ORGANIZE LIP SYNC MATERIALS
Приводим в порядок ВСЕ материалы для липсинка
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🎯 %(message)s')

class LipSyncOrganizer:
    """🎯 Организатор материалов для липсинка"""
    
    def __init__(self):
        self.base_dir = Path(".")
        self.organized_dir = self.base_dir / "ORGANIZED_LIP_SYNC"
        self.logger = logging.getLogger("LipSyncOrganizer")
        
        # Создаем организованную структуру
        self.photos_dir = self.organized_dir / "PHOTOS"
        self.audio_full_dir = self.organized_dir / "AUDIO_FULL_TRACKS"
        self.audio_segments_dir = self.organized_dir / "AUDIO_SEGMENTS"
        self.audio_vocals_dir = self.organized_dir / "AUDIO_VOCALS_ONLY"
        self.for_heygen_dir = self.organized_dir / "FOR_HEYGEN"
        
        # Создаем все папки
        for dir_path in [self.photos_dir, self.audio_full_dir, 
                        self.audio_segments_dir, self.audio_vocals_dir, self.for_heygen_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def collect_photos(self):
        """📸 Собираем все лучшие фото"""
        self.logger.info("Собираю фотографии...")
        
        photo_sources = [
            "Фотографии",
            "upscaled_images", 
            "LIP_SYNC_WORKSPACE/input_photos"
        ]
        
        collected = 0
        for source in photo_sources:
            source_path = Path(source)
            if source_path.exists():
                # Ищем фото файлы
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
                    for photo in source_path.glob(ext):
                        if photo.stat().st_size > 100000:  # Больше 100KB
                            new_name = f"photo_{collected+1:03d}_{photo.name}"
                            dest = self.photos_dir / new_name
                            shutil.copy2(photo, dest)
                            collected += 1
                            
                            if collected >= 20:  # Лимит 20 лучших фото
                                break
                    if collected >= 20:
                        break
        
        self.logger.info(f"✅ Собрано {collected} фотографий")
        return collected
    
    def collect_audio_segments(self):
        """🎵 Собираем все аудио сегменты"""
        self.logger.info("Собираю аудио сегменты...")
        
        audio_sources = [
            "rap_10sec_segments",
            "эксперименты с музыкой", 
            "LIP_SYNC_WORKSPACE/input_audio"
        ]
        
        collected = 0
        for source in audio_sources:
            source_path = Path(source)
            if source_path.exists():
                # Ищем аудио файлы
                for ext in ['*.wav', '*.mp3', '*.m4a']:
                    for audio in source_path.glob(ext):
                        if audio.stat().st_size > 50000:  # Больше 50KB
                            new_name = f"segment_{collected+1:03d}_{audio.name}"
                            dest = self.audio_segments_dir / new_name
                            shutil.copy2(audio, dest)
                            collected += 1
        
        self.logger.info(f"✅ Собрано {collected} аудио сегментов")
        return collected
    
    def create_heygen_kit(self):
        """🎭 Создаем идеальный набор для HeyGen"""
        self.logger.info("Создаю набор для HeyGen...")
        
        # Отбираем 10 лучших фото
        photos = sorted(self.photos_dir.glob("*.png"))[:10]
        
        # Отбираем 10 лучших аудио (предпочитаем 10-секундные)
        audio_10sec = sorted(self.audio_segments_dir.glob("*rap_10sec*"))[:5]
        audio_5sec = sorted(self.audio_segments_dir.glob("*rap_5sec*"))[:5]
        
        selected_audio = audio_10sec + audio_5sec
        
        # Копируем в HeyGen папку
        for i, photo in enumerate(photos, 1):
            dest = self.for_heygen_dir / f"heygen_photo_{i:02d}.png"
            shutil.copy2(photo, dest)
        
        for i, audio in enumerate(selected_audio, 1):
            dest = self.for_heygen_dir / f"heygen_audio_{i:02d}.wav"
            shutil.copy2(audio, dest)
        
        # Создаем инструкцию
        instruction = self.for_heygen_dir / "HEYGEN_READY.md"
        with open(instruction, 'w', encoding='utf-8') as f:
            f.write(f"""# 🎭 ГОТОВО ДЛЯ HEYGEN!

## 📸 ФОТОГРАФИИ ({len(photos)} шт.)
""")
            for i, photo in enumerate(photos, 1):
                f.write(f"- heygen_photo_{i:02d}.png\n")
                
            f.write(f"""
## 🎵 АУДИО ТРЕКИ ({len(selected_audio)} шт.)
""")
            for i, audio in enumerate(selected_audio, 1):
                f.write(f"- heygen_audio_{i:02d}.wav\n")
                
            f.write("""
## 🚀 ПЛАН СОЗДАНИЯ:
1. Создать 10 аватаров из фото
2. Для каждого аватара - 1 видео с каждым аудио
3. Итого: 10 × 10 = 100 видео!

## 💡 РЕКОМЕНДАЦИИ HEYGEN:
- Качество: HD (1080p)
- Фон: Solid color
- Sync accuracy: Maximum
- Стиль: Natural movement
""")
        
        self.logger.info(f"✅ Создан набор для HeyGen: {len(photos)} фото + {len(selected_audio)} аудио")
        return len(photos), len(selected_audio)
    
    def create_report(self):
        """📊 Создаем отчет о собранных материалах"""
        
        # Подсчитываем файлы
        photos_count = len(list(self.photos_dir.glob("*")))
        segments_count = len(list(self.audio_segments_dir.glob("*")))
        heygen_photos = len(list(self.for_heygen_dir.glob("heygen_photo_*")))
        heygen_audio = len(list(self.for_heygen_dir.glob("heygen_audio_*")))
        
        report = self.organized_dir / "MATERIALS_REPORT.md"
        with open(report, 'w', encoding='utf-8') as f:
            f.write(f"""# 📊 ОТЧЕТ О МАТЕРИАЛАХ ДЛЯ ЛИПСИНКА

## 🎯 СТАТИСТИКА:
- 📸 **Фотографий собрано:** {photos_count}
- 🎵 **Аудио сегментов:** {segments_count}
- 🎭 **Готово для HeyGen:** {heygen_photos} фото + {heygen_audio} аудио

## 📁 СТРУКТУРА:
```
ORGANIZED_LIP_SYNC/
├── PHOTOS/                    # Все фото
├── AUDIO_SEGMENTS/            # Все аудио сегменты  
├── FOR_HEYGEN/               # 🎯 ГОТОВО ДЛЯ HEYGEN!
│   ├── heygen_photo_01.png
│   ├── heygen_audio_01.wav
│   └── HEYGEN_READY.md
└── MATERIALS_REPORT.md       # Этот файл
```

## 🚀 СЛЕДУЮЩИЕ ШАГИ:
1. Откройте папку FOR_HEYGEN/
2. Используйте файлы heygen_photo_* и heygen_audio_*
3. Создавайте липсинк видео в HeyGen
4. Планируйте {heygen_photos} × {heygen_audio} = {heygen_photos * heygen_audio} видео!

## 💡 РЕКОМЕНДАЦИИ:
- Начните с 1-2 тестовых видео
- Используйте настройки из HEYGEN_READY.md
- Сохраняйте успешные шаблоны в HeyGen
""")
        
        self.logger.info(f"✅ Отчет создан: {report}")
        
    def organize_all(self):
        """🎯 Организуем ВСЕ материалы"""
        
        self.logger.info("🎯 НАЧИНАЮ ПОЛНУЮ ОРГАНИЗАЦИЮ МАТЕРИАЛОВ...")
        self.logger.info("=" * 50)
        
        # Собираем все
        photos = self.collect_photos()
        segments = self.collect_audio_segments()
        
        # Создаем набор для HeyGen
        heygen_photos, heygen_audio = self.create_heygen_kit()
        
        # Создаем отчет
        self.create_report()
        
        self.logger.info("=" * 50)
        self.logger.info("🎉 ОРГАНИЗАЦИЯ ЗАВЕРШЕНА!")
        self.logger.info(f"📸 Фото: {photos}")
        self.logger.info(f"🎵 Аудио: {segments}")  
        self.logger.info(f"🎭 Для HeyGen: {heygen_photos} × {heygen_audio} = {heygen_photos * heygen_audio} видео")
        self.logger.info(f"📁 Папка: {self.organized_dir}")
        self.logger.info("🚀 ГОТОВО ДЛЯ ЛИПСИНКА!")

def main():
    organizer = LipSyncOrganizer()
    organizer.organize_all()

if __name__ == "__main__":
    main() 