#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Mass 8K Upscaler для нейрофото 🚀
Специальный скрипт для апскейла фото за последние 2 дня до 8K с супер детализацией
"""

import os
import sys
import subprocess
from pathlib import Path
import datetime
from typing import List

# Добавляем путь к нашим модулям
sys.path.append("Python код")
from comfy_upscaler_fixed import ComfyUpscalerFixed

class NeuroPhotoUpscaler:
    def __init__(self):
        self.server_url = "http://localhost:8188"
        self.upscaler = ComfyUpscalerFixed(self.server_url)
        self.input_dir = "нейрофото"
        self.output_dir = "нейрофото_8K_ULTRA"
        
    def get_recent_photos(self, days: int = 2) -> List[Path]:
        """Получает фото за последние N дней"""
        recent_photos = []
        
        # Ищем фото за 26-27 июня 2025
        patterns = [
            "2025-06-26*.jpg",
            "2025-06-27*.jpg"
        ]
        
        for pattern in patterns:
            photos = list(Path(self.input_dir).glob(pattern))
            recent_photos.extend(photos)
        
        print(f"📸 Найдено фото за последние {days} дня: {len(recent_photos)}")
        return recent_photos
    
    def get_8k_upscale_workflow(self, image_filename: str) -> dict:
        """
        Создает workflow для 8K апскейла с супер детализацией
        """
        return {
            "1": {
                "inputs": {
                    "image": image_filename
                },
                "class_type": "LoadImage"
            },
            # Первый апскейл x2
            "2": {
                "inputs": {
                    "upscale_method": "lanczos",
                    "scale_by": 2.0,
                    "image": ["1", 0]
                },
                "class_type": "ImageScaleBy"
            },
            # Второй апскейл x2 для достижения 8K
            "3": {
                "inputs": {
                    "upscale_method": "lanczos", 
                    "scale_by": 2.0,
                    "image": ["2", 0]
                },
                "class_type": "ImageScaleBy"
            },
            # Повышение резкости
            "4": {
                "inputs": {
                    "sharpen_radius": 1.0,
                    "sigma": 1.0,
                    "alpha": 1.5,
                    "image": ["3", 0]
                },
                "class_type": "ImageSharpen"
            },
            # Сохранение результата
            "5": {
                "inputs": {
                    "filename_prefix": "8K_ULTRA_",
                    "images": ["4", 0]
                },
                "class_type": "SaveImage"
            }
        }
    
    def check_comfyui_connection(self) -> bool:
        """Проверяет подключение к ComfyUI"""
        try:
            import requests
            response = requests.get(f"{self.server_url}/system_stats", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка подключения к ComfyUI: {e}")
            return False
    
    def upscale_to_8k(self, image_path: Path) -> bool:
        """Апскейлит одно изображение до 8K"""
        print(f"🚀 8K апскейл: {image_path.name}")
        
        # Загружаем изображение
        upload_result = self.upscaler.upload_image(str(image_path))
        if not upload_result:
            return False
        
        uploaded_filename = upload_result["name"]
        print(f"📤 Загружено: {uploaded_filename}")
        
        # Создаем 8K workflow
        workflow = self.get_8k_upscale_workflow(uploaded_filename)
        
        # Добавляем в очередь
        prompt_id = self.upscaler.queue_workflow(workflow)
        if not prompt_id:
            return False
        
        print(f"📋 Задача в очереди: {prompt_id}")
        
        # Ждем завершения (увеличиваем таймаут для 8K)
        if not self.upscaler.wait_for_completion(prompt_id, timeout=600):
            return False
        
        # Получаем и скачиваем результаты
        output_files = self.upscaler.get_output_images(prompt_id)
        
        if not output_files:
            print(f"❌ Нет результатов для {image_path.name}")
            return False
        
        # Скачиваем все результаты
        success = True
        for filename in output_files:
            if not self.upscaler.download_image(filename, self.output_dir):
                success = False
        
        if success:
            print(f"✅ 8K готов: {image_path.name}")
        
        return success
    
    def run_mass_upscale(self):
        """Запускает массовый 8K апскейл"""
        print("🚀 MASS 8K UPSCALER ДЛЯ НЕЙРОФОТО 🚀")
        print("=" * 60)
        
        # Проверяем ComfyUI
        if not self.check_comfyui_connection():
            print("❌ ComfyUI недоступен! Запустите ComfyUI сервер.")
            print("💡 Команда: cd ComfyUI && python main.py")
            return
        
        print("✅ ComfyUI подключен")
        
        # Создаем выходную папку
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 Выходная папка: {self.output_dir}")
        
        # Получаем список фото
        recent_photos = self.get_recent_photos()
        
        if not recent_photos:
            print("❌ Фото за последние 2 дня не найдены")
            return
        
        print(f"🎯 Начинаем 8K апскейл {len(recent_photos)} фотографий...")
        print("=" * 60)
        
        # Обрабатываем каждое фото
        successful = 0
        failed = 0
        
        for i, photo_path in enumerate(recent_photos, 1):
            print(f"\n[{i}/{len(recent_photos)}] ", end="")
            
            try:
                if self.upscale_to_8k(photo_path):
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Критическая ошибка: {e}")
                failed += 1
        
        # Финальная статистика
        print("\n" + "=" * 60)
        print(f"🎉 РЕЗУЛЬТАТЫ МАССОВОГО 8K АПСКЕЙЛА:")
        print(f"✅ Успешно обработано: {successful}")
        print(f"❌ Ошибок: {failed}")
        print(f"📊 Всего фотографий: {len(recent_photos)}")
        print(f"📁 Результаты сохранены в: {self.output_dir}")
        print("=" * 60)


def main():
    """Основная функция"""
    upscaler = NeuroPhotoUpscaler()
    upscaler.run_mass_upscale()


if __name__ == "__main__":
    main() 