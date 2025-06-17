#!/usr/bin/env python3
"""
🎯 Upscale одного изображения
"""

from comfy_upscaler_fixed import ComfyUpscalerFixed
import sys
import os

def upscale_single_image(image_path: str):
    """Обрабатывает одно изображение"""
    
    if not os.path.exists(image_path):
        print(f"❌ Файл не найден: {image_path}")
        return
    
    print(f"🎯 Обрабатываем только: {image_path}")
    
    # Создаем upscaler
    upscaler = ComfyUpscalerFixed("http://localhost:8188")
    
    # Проверяем подключение
    import requests
    try:
        response = requests.get("http://localhost:8188/system_stats", timeout=5)
        if response.status_code != 200:
            print("❌ ComfyUI недоступен")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    print("✅ ComfyUI доступен")
    
    # Обрабатываем файл
    output_dir = "upscaled_images"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        success = upscaler.upscale_image(image_path, output_dir, use_model=False)
        if success:
            print("🎉 Готово! Результат сохранен в папке upscaled_images")
        else:
            print("❌ Ошибка при обработке")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    # Можно передать путь как аргумент или задать здесь
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "2025-05-27 02.44.20.jpg"  # Ваша новая фотография
    
    upscale_single_image(image_path) 