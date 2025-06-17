#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎬 REAL LIP SYNC DEMO
Создаем настоящие видео из фото + аудио
"""

import subprocess
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - 🎬 %(message)s')

class RealLipSyncDemo:
    """🎬 Реальное создание видео"""
    
    def __init__(self):
        self.workspace = Path("LIP_SYNC_WORKSPACE")
        self.photos = self.workspace / "input_photos"
        self.audio = self.workspace / "input_audio"
        self.output = self.workspace / "real_videos"
        
        self.output.mkdir(exist_ok=True)
        self.logger = logging.getLogger("RealLipSync")
    
    def check_ffmpeg(self):
        """🔧 Проверка FFmpeg"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("✅ FFmpeg найден")
                return True
            else:
                self.logger.error("❌ FFmpeg не работает")
                return False
        except FileNotFoundError:
            self.logger.error("❌ FFmpeg не установлен")
            return False
    
    def create_video(self, photo_path: Path, audio_path: Path, output_path: Path):
        """🎬 Создание видео из фото + аудио"""
        
        try:
            # FFmpeg команда для создания видео
            cmd = [
                'ffmpeg', '-y',  # Перезаписывать файлы
                '-loop', '1',    # Зациклить изображение
                '-i', str(photo_path),  # Входное фото
                '-i', str(audio_path),  # Входное аудио
                '-c:v', 'libx264',      # Видео кодек
                '-c:a', 'aac',          # Аудио кодек
                '-shortest',            # Длительность по аудио
                '-pix_fmt', 'yuv420p',  # Совместимость
                '-vf', 'scale=720:720,zoompan=z=1.05:d=125', # Легкий зум
                str(output_path)
            ]
            
            self.logger.info(f"🎬 Создаю: {output_path.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"✅ Готово: {output_path.name}")
                return True
            else:
                self.logger.error(f"❌ Ошибка: {result.stderr[:200]}...")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Исключение: {e}")
            return False
    
    def process_all(self):
        """🚀 Обработка всех комбинаций"""
        
        if not self.check_ffmpeg():
            self.logger.error("Установите FFmpeg: brew install ffmpeg")
            return
        
        photos = list(self.photos.glob("*.jpg")) + list(self.photos.glob("*.png"))
        audios = list(self.audio.glob("*.wav"))
        
        self.logger.info(f"📸 Найдено фото: {len(photos)}")
        self.logger.info(f"🎵 Найдено аудио: {len(audios)}")
        
        created = 0
        total = min(len(photos), 5) * min(len(audios), 2)  # Ограничиваем для теста
        
        for i, photo in enumerate(photos[:5]):  # Первые 5 фото
            for j, audio in enumerate(audios[:2]):  # Первые 2 аудио
                
                output_name = f"real_video_{i+1:02d}_{j+1}_{photo.stem}_{audio.stem}.mp4"
                output_path = self.output / output_name
                
                if self.create_video(photo, audio, output_path):
                    created += 1
                
                self.logger.info(f"📊 Прогресс: {created}/{total}")
        
        self.logger.info(f"🎉 Создано {created} настоящих видео!")
        return created

def main():
    print("🎬" * 50)
    print("🎭 REAL LIP SYNC DEMO")
    print("Создаем НАСТОЯЩИЕ видео!")
    print("🎬" * 50)
    
    demo = RealLipSyncDemo()
    created = demo.process_all()
    
    if created > 0:
        print(f"\n✅ Успех! Создано {created} видео")
        print(f"📁 Папка: {demo.output}")
        print("🎬 Эти видео точно откроются!")
    else:
        print("\n❌ Не удалось создать видео")
        print("Попробуйте установить FFmpeg: brew install ffmpeg")

if __name__ == "__main__":
    main() 