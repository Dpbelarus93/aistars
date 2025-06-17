#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎬 CREATE LIP SYNC WORKSPACE
Создаем идеальную структуру для работы с липсинком
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🎬 %(message)s')

class LipSyncWorkspaceCreator:
    """🎬 Создатель рабочего пространства для липсинка"""
    
    def __init__(self):
        self.base_dir = Path(".")
        self.workspace_dir = self.base_dir / "LIP_SYNC_FINAL"
        self.logger = logging.getLogger("LipSyncWorkspace")
        
        # Три основные папки
        self.photos_dir = self.workspace_dir / "01_PHOTOS"
        self.audio_dir = self.workspace_dir / "02_AUDIO_TRACKS"  
        self.videos_dir = self.workspace_dir / "03_READY_VIDEOS"
        
        # Создаем структуру
        for dir_path in [self.photos_dir, self.audio_dir, self.videos_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def collect_all_photos(self):
        """📸 Собираем ВСЕ фотографии из всех источников"""
        self.logger.info("Собираю все фотографии...")
        
        photo_sources = [
            Path("Фотографии"),
            Path("upscaled_images"),
            Path("ORGANIZED_LIP_SYNC/PHOTOS"),
            Path("LIP_SYNC_WORKSPACE/input_photos")
        ]
        
        collected = 0
        for source in photo_sources:
            if source.exists():
                self.logger.info(f"Проверяю: {source}")
                
                # Ищем все форматы фото
                for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.bmp']:
                    for photo in source.glob(ext):
                        if photo.stat().st_size > 50000:  # Больше 50KB
                            # Создаем понятное имя
                            new_name = f"photo_{collected+1:03d}_{photo.stem}.{photo.suffix[1:]}"
                            dest = self.photos_dir / new_name
                            
                            # Копируем если еще нет
                            if not dest.exists():
                                shutil.copy2(photo, dest)
                                collected += 1
                                
                                if collected % 10 == 0:
                                    self.logger.info(f"Скопировано {collected} фото...")
        
        self.logger.info(f"✅ Собрано {collected} фотографий в {self.photos_dir}")
        return collected
    
    def collect_all_audio(self):
        """🎵 Собираем ВСЕ аудио треки"""
        self.logger.info("Собираю все аудио треки...")
        
        audio_sources = [
            Path("rap_10sec_segments"),
            Path("эксперименты с музыкой"),
            Path("ORGANIZED_LIP_SYNC/AUDIO_SEGMENTS"),
            Path("LIP_SYNC_WORKSPACE/input_audio")
        ]
        
        collected = 0
        for source in audio_sources:
            if source.exists():
                self.logger.info(f"Проверяю: {source}")
                
                # Ищем все форматы аудио
                for ext in ['*.wav', '*.mp3', '*.m4a', '*.aac']:
                    for audio in source.glob(ext):
                        if audio.stat().st_size > 30000:  # Больше 30KB
                            # Создаем понятное имя
                            new_name = f"track_{collected+1:03d}_{audio.stem}.{audio.suffix[1:]}"
                            dest = self.audio_dir / new_name
                            
                            # Копируем если еще нет
                            if not dest.exists():
                                shutil.copy2(audio, dest)
                                collected += 1
                                
                                if collected % 5 == 0:
                                    self.logger.info(f"Скопировано {collected} треков...")
        
        self.logger.info(f"✅ Собрано {collected} аудио треков в {self.audio_dir}")
        return collected
    
    def create_instructions(self, photos_count, audio_count):
        """📋 Создаем инструкции для работы"""
        
        # Инструкция в папке с фото
        photo_readme = self.photos_dir / "README.md"
        with open(photo_readme, 'w', encoding='utf-8') as f:
            f.write(f"""# 📸 ФОТОГРАФИИ ДЛЯ ЛИПСИНКА

## 📊 СТАТИСТИКА:
- **Всего фото:** {photos_count}
- **Готовы для HeyGen:** ✅
- **Форматы:** JPG, PNG, WEBP

## 💡 РЕКОМЕНДАЦИИ:
- Выбирайте фото с четким лицом
- Избегайте слишком темных/размытых
- Лучше работают нейтральные выражения лица

## 🎯 ДЛЯ HEYGEN:
1. Выберите 5-10 лучших фото
2. Загружайте по одному как аватар
3. Сохраняйте успешные настройки
""")
        
        # Инструкция в папке с аудио
        audio_readme = self.audio_dir / "README.md"
        with open(audio_readme, 'w', encoding='utf-8') as f:
            f.write(f"""# 🎵 АУДИО ТРЕКИ ДЛЯ ЛИПСИНКА

## 📊 СТАТИСТИКА:
- **Всего треков:** {audio_count}
- **Готовы для HeyGen:** ✅
- **Форматы:** WAV, MP3, M4A

## 💡 РЕКОМЕНДАЦИИ:
- Предпочитайте треки 5-20 секунд
- Четкая речь работает лучше музыки
- В HeyGen выбирайте тип "Speech"

## 🎯 ДЛЯ HEYGEN:
1. Начните с коротких треков (5-10 сек)
2. Загружайте как "Speech", не "Music"
3. Язык: English для рэпа
""")
        
        # Главная инструкция
        main_readme = self.workspace_dir / "START_HERE.md"
        with open(main_readme, 'w', encoding='utf-8') as f:
            f.write(f"""# 🎬 LIP SYNC WORKSPACE - НАЧНИТЕ ЗДЕСЬ!

## 📁 СТРУКТУРА ПРОЕКТА:

### 📸 **01_PHOTOS** ({photos_count} фото)
- Все ваши фотографии готовы для липсинка
- Выберите лучшие для создания аватаров
- Читайте README.md в папке для деталей

### 🎵 **02_AUDIO_TRACKS** ({audio_count} треков)
- Все аудио треки готовы для синхронизации
- Предпочитайте короткие сегменты (5-20 сек)
- Читайте README.md в папке для настроек

### 🎬 **03_READY_VIDEOS** (пока пусто)
- Сюда сохраняйте готовые видео из HeyGen
- Организуйте по папкам: test/, final/, best/

## 🚀 БЫСТРЫЙ СТАРТ:

### 1️⃣ **ТЕСТОВОЕ ВИДЕО (5 минут)**
1. Откройте **app.heygen.com**
2. Выберите 1 фото из папки 01_PHOTOS
3. Выберите 1 короткий трек из 02_AUDIO_TRACKS
4. Создайте аватар → Audio to Video
5. Настройки: HD, Speech, English
6. Сохраните результат в 03_READY_VIDEOS/test/

### 2️⃣ **МАССОВОЕ ПРОИЗВОДСТВО**
1. Создайте 5-10 аватаров из лучших фото
2. Выберите 10-20 лучших треков
3. Запустите пакетную генерацию
4. Планируйте: 10 фото × 20 треков = 200 видео!

## 💰 **ЭКОНОМИКА:**
- **Ваша подписка HeyGen:** ~$30/месяц
- **Потенциал:** 200+ видео за месяц
- **Стоимость за видео:** $0.15
- **Альтернатива:** $50+ за видео вручную
- **ЭКОНОМИЯ:** 99%! 🔥

## 🎯 **ЦЕЛЬ:**
Создать библиотеку из {photos_count//10} × {audio_count//5} = {(photos_count//10) * (audio_count//5)} уникальных липсинк видео!

---

## 📞 **ПОДДЕРЖКА:**
- Все материалы организованы и готовы
- Инструкции в каждой папке
- Начинайте с тестового видео!

**УДАЧИ В СОЗДАНИИ! 🎬✨**
""")
        
        self.logger.info("✅ Инструкции созданы")
    
    def create_workspace(self):
        """🎬 Создаем полное рабочее пространство"""
        
        self.logger.info("🎬 СОЗДАЮ РАБОЧЕЕ ПРОСТРАНСТВО ДЛЯ ЛИПСИНКА...")
        self.logger.info("=" * 60)
        
        # Собираем материалы
        photos = self.collect_all_photos()
        audio = self.collect_all_audio()
        
        # Создаем инструкции
        self.create_instructions(photos, audio)
        
        # Создаем подпапки в готовых видео
        (self.videos_dir / "test").mkdir(exist_ok=True)
        (self.videos_dir / "final").mkdir(exist_ok=True)
        (self.videos_dir / "best").mkdir(exist_ok=True)
        
        self.logger.info("=" * 60)
        self.logger.info("🎉 РАБОЧЕЕ ПРОСТРАНСТВО ГОТОВО!")
        self.logger.info(f"📸 Фотографий: {photos}")
        self.logger.info(f"🎵 Аудио треков: {audio}")
        self.logger.info(f"🎬 Потенциал видео: {photos * audio}")
        self.logger.info(f"📁 Папка: {self.workspace_dir}")
        self.logger.info("🚀 НАЧИНАЙТЕ СОЗДАВАТЬ ЛИПСИНК!")
        
        return self.workspace_dir

def main():
    creator = LipSyncWorkspaceCreator()
    workspace_path = creator.create_workspace()
    
    # Открываем папку
    import subprocess
    subprocess.run(["open", str(workspace_path)])
    
    print(f"\n🎯 РАБОЧЕЕ ПРОСТРАНСТВО ОТКРЫТО: {workspace_path}")
    print("📋 Читайте START_HERE.md для начала работы!")

if __name__ == "__main__":
    main() 