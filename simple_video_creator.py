#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎬 SIMPLE VIDEO CREATOR
Создаем видео без FFmpeg - альтернативное решение
"""

import shutil
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🎬 %(message)s')

class SimpleVideoCreator:
    """🎬 Простое создание видео"""
    
    def __init__(self):
        self.workspace = Path("LIP_SYNC_WORKSPACE")
        self.photos = self.workspace / "input_photos"
        self.audio = self.workspace / "input_audio"
        self.output = self.workspace / "simple_videos"
        
        self.output.mkdir(exist_ok=True)
        self.logger = logging.getLogger("SimpleVideo")
    
    def check_system_tools(self):
        """🔧 Проверка системных инструментов"""
        
        # Проверяем системный ffmpeg (может быть предустановлен)
        try:
            result = subprocess.run(['which', 'ffmpeg'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("✅ Системный FFmpeg найден")
                return "ffmpeg"
        except:
            pass
        
        # Проверяем QuickTime Player (macOS)
        try:
            result = subprocess.run(['which', 'osascript'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("✅ AppleScript доступен")
                return "applescript"
        except:
            pass
        
        self.logger.warning("⚠️ Видео инструменты не найдены")
        return None
    
    def create_simple_slideshow(self, photo_path: Path, audio_path: Path, output_path: Path):
        """🎬 Создание простого слайд-шоу"""
        
        try:
            # Копируем фото в выходную папку
            photo_copy = output_path.parent / f"{output_path.stem}_photo.jpg"
            shutil.copy2(photo_path, photo_copy)
            
            # Копируем аудио в выходную папку  
            audio_copy = output_path.parent / f"{output_path.stem}_audio.wav"
            shutil.copy2(audio_path, audio_copy)
            
            # Создаем инструкцию
            instruction = output_path.parent / f"{output_path.stem}_instruction.txt"
            with open(instruction, 'w', encoding='utf-8') as f:
                f.write(f"""
🎬 ИНСТРУКЦИЯ ДЛЯ СОЗДАНИЯ ВИДЕО

📸 Фото: {photo_copy.name}
🎵 Аудио: {audio_copy.name}
📹 Результат: {output_path.name}

🛠️ СПОСОБЫ СОЗДАНИЯ:

1️⃣ АВТОМАТИЧЕСКИ (если есть FFmpeg):
   ffmpeg -loop 1 -i "{photo_copy.name}" -i "{audio_copy.name}" -c:v libx264 -c:a aac -shortest -pix_fmt yuv420p "{output_path.name}"

2️⃣ ВРУЧНУЮ:
   • Откройте фото в любом видео редакторе
   • Добавьте аудио дорожку
   • Экспортируйте как MP4

3️⃣ ОНЛАЙН:
   • Загрузите на Canva/CapCut/InShot
   • Создайте видео из фото + аудио
   
🎯 РЕЗУЛЬТАТ: Видео длительностью {self.get_audio_duration(audio_path)} секунд
""")
            
            self.logger.info(f"📋 Создана инструкция: {instruction.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Ошибка: {e}")
            return False
    
    def get_audio_duration(self, audio_path: Path) -> str:
        """⏱️ Примерная длительность аудио"""
        try:
            size_mb = audio_path.stat().st_size / (1024 * 1024)
            # Примерно 1MB = 10 секунд для WAV
            duration = int(size_mb * 10)
            return f"~{duration}"
        except:
            return "неизвестно"
    
    def process_all(self):
        """🚀 Обработка всех комбинаций"""
        
        tool = self.check_system_tools()
        
        photos = list(self.photos.glob("*.jpg")) + list(self.photos.glob("*.png"))
        audios = list(self.audio.glob("*.wav"))
        
        self.logger.info(f"📸 Найдено фото: {len(photos)}")
        self.logger.info(f"🎵 Найдено аудио: {len(audios)}")
        
        created = 0
        total = min(len(photos), 3) * min(len(audios), 2)  # Ограничиваем для демо
        
        for i, photo in enumerate(photos[:3]):  # Первые 3 фото
            for j, audio in enumerate(audios[:2]):  # Первые 2 аудио
                
                output_name = f"video_{i+1:02d}_{j+1}_{photo.stem}_{audio.stem}.mp4"
                output_path = self.output / output_name
                
                if self.create_simple_slideshow(photo, audio, output_path):
                    created += 1
                
                self.logger.info(f"📊 Прогресс: {created}/{total}")
        
        self.logger.info(f"🎉 Подготовлено {created} комплектов для видео!")
        return created

def main():
    print("🎬" * 50)
    print("🎭 SIMPLE VIDEO CREATOR")
    print("Готовим материалы для видео!")
    print("🎬" * 50)
    
    creator = SimpleVideoCreator()
    created = creator.process_all()
    
    if created > 0:
        print(f"\n✅ Готово! Подготовлено {created} комплектов")
        print(f"📁 Папка: {creator.output}")
        print("📋 В каждом комплекте: фото + аудио + инструкция")
        print("\n🛠️ СЛЕДУЮЩИЕ ШАГИ:")
        print("1. Установите FFmpeg: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. Или используйте онлайн инструменты (Canva, CapCut)")
        print("3. Или любой видео редактор (iMovie, DaVinci Resolve)")
    else:
        print("\n❌ Не удалось подготовить материалы")

if __name__ == "__main__":
    main() 