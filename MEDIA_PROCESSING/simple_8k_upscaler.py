#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Simple 8K Upscaler для нейрофото 🚀
Простой скрипт для апскейла без ComfyUI - использует PIL и OpenCV
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from typing import List

class Simple8KUpscaler:
    def __init__(self):
        self.input_dir = "нейрофото"
        self.output_dir = "нейрофото_8K_SIMPLE"
        
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
    
    def enhance_image_quality(self, image: Image.Image) -> Image.Image:
        """Улучшает качество изображения"""
        # Увеличиваем резкость
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        # Увеличиваем контрастность
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Увеличиваем насыщенность
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        
        # Применяем фильтр повышения резкости
        image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        return image
    
    def upscale_to_8k_pil(self, image_path: Path) -> bool:
        """Апскейлит изображение до 8K используя PIL"""
        try:
            print(f"🚀 PIL 8K апскейл: {image_path.name}")
            
            # Открываем изображение
            with Image.open(image_path) as img:
                # Конвертируем в RGB если нужно
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                original_size = img.size
                print(f"📏 Исходный размер: {original_size[0]}x{original_size[1]}")
                
                # Вычисляем новый размер для 8K (7680x4320)
                target_width = 7680
                target_height = int((target_width * original_size[1]) / original_size[0])
                
                # Если высота больше 4320, ограничиваем по высоте
                if target_height > 4320:
                    target_height = 4320
                    target_width = int((target_height * original_size[0]) / original_size[1])
                
                new_size = (target_width, target_height)
                print(f"🎯 Целевой размер: {new_size[0]}x{new_size[1]}")
                
                # Апскейлим с высоким качеством
                upscaled = img.resize(new_size, Image.LANCZOS)
                
                # Улучшаем качество
                enhanced = self.enhance_image_quality(upscaled)
                
                # Сохраняем результат
                output_filename = f"8K_SIMPLE_{image_path.stem}.jpg"
                output_path = Path(self.output_dir) / output_filename
                
                enhanced.save(
                    output_path, 
                    'JPEG', 
                    quality=95, 
                    optimize=True,
                    progressive=True
                )
                
                print(f"✅ Сохранено: {output_filename}")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка при обработке {image_path.name}: {e}")
            return False
    
    def upscale_to_8k_opencv(self, image_path: Path) -> bool:
        """Апскейлит изображение до 8K используя OpenCV (альтернативный метод)"""
        try:
            print(f"🚀 OpenCV 8K апскейл: {image_path.name}")
            
            # Читаем изображение
            img = cv2.imread(str(image_path))
            if img is None:
                print(f"❌ Не удалось прочитать {image_path.name}")
                return False
            
            original_height, original_width = img.shape[:2]
            print(f"📏 Исходный размер: {original_width}x{original_height}")
            
            # Вычисляем новый размер для 8K
            target_width = 7680
            target_height = int((target_width * original_height) / original_width)
            
            if target_height > 4320:
                target_height = 4320
                target_width = int((target_height * original_width) / original_height)
            
            print(f"🎯 Целевой размер: {target_width}x{target_height}")
            
            # Апскейлим с интерполяцией INTER_CUBIC
            upscaled = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
            
            # Применяем фильтр резкости
            kernel = np.array([[-1,-1,-1],
                              [-1, 9,-1],
                              [-1,-1,-1]])
            sharpened = cv2.filter2D(upscaled, -1, kernel)
            
            # Смешиваем оригинал и резкий
            enhanced = cv2.addWeighted(upscaled, 0.7, sharpened, 0.3, 0)
            
            # Сохраняем результат
            output_filename = f"8K_OPENCV_{image_path.stem}.jpg"
            output_path = Path(self.output_dir) / output_filename
            
            # Сохраняем с высоким качеством
            cv2.imwrite(str(output_path), enhanced, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            print(f"✅ Сохранено: {output_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при обработке {image_path.name}: {e}")
            return False
    
    def run_mass_upscale(self):
        """Запускает массовый 8K апскейл"""
        print("🚀 SIMPLE MASS 8K UPSCALER ДЛЯ НЕЙРОФОТО 🚀")
        print("=" * 60)
        
        # Создаем выходную папку
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 Выходная папка: {self.output_dir}")
        
        # Получаем список фото
        recent_photos = self.get_recent_photos()
        
        if not recent_photos:
            print("❌ Фото за последние 2 дня не найдены")
            return
        
        print(f"🎯 Начинаем 8K апскейл {len(recent_photos)} фотографий...")
        print("📋 Используем PIL + OpenCV для максимального качества")
        print("=" * 60)
        
        # Обрабатываем каждое фото
        successful_pil = 0
        successful_opencv = 0
        failed = 0
        
        for i, photo_path in enumerate(recent_photos, 1):
            print(f"\n[{i}/{len(recent_photos)}] ", end="")
            
            try:
                # Пробуем оба метода для лучшего результата
                pil_success = self.upscale_to_8k_pil(photo_path)
                opencv_success = self.upscale_to_8k_opencv(photo_path)
                
                if pil_success:
                    successful_pil += 1
                if opencv_success:
                    successful_opencv += 1
                if not pil_success and not opencv_success:
                    failed += 1
                    
            except Exception as e:
                print(f"❌ Критическая ошибка: {e}")
                failed += 1
        
        # Финальная статистика
        print("\n" + "=" * 60)
        print(f"🎉 РЕЗУЛЬТАТЫ МАССОВОГО 8K АПСКЕЙЛА:")
        print(f"✅ PIL успешно: {successful_pil}")
        print(f"✅ OpenCV успешно: {successful_opencv}")
        print(f"❌ Ошибок: {failed}")
        print(f"📊 Всего фотографий: {len(recent_photos)}")
        print(f"📁 Результаты сохранены в: {self.output_dir}")
        print("=" * 60)


def main():
    """Основная функция"""
    try:
        upscaler = Simple8KUpscaler()
        upscaler.run_mass_upscale()
    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main() 