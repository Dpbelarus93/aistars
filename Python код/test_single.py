#!/usr/bin/env python3
"""
Тест upscale одного изображения
"""

from comfy_upscaler_fixed import ComfyUpscalerFixed
import requests

def test_single_image():
    print("🧪 Тестируем upscale одного изображения...")
    
    # Создаем upscaler
    upscaler = ComfyUpscalerFixed("http://localhost:8188")
    
    # Проверяем подключение
    try:
        response = requests.get("http://localhost:8188/system_stats", timeout=5)
        if response.status_code != 200:
            print("❌ ComfyUI недоступен")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    print("✅ ComfyUI доступен")
    
    # Тестируем с одним файлом
    test_image = "0.jpg"  # Используем существующий файл
    output_dir = "test_output"
    
    try:
        success = upscaler.upscale_image(test_image, output_dir, use_model=False)
        if success:
            print("🎉 Тест прошел успешно!")
        else:
            print("❌ Тест не удался")
    except Exception as e:
        print(f"❌ Ошибка в тесте: {e}")

if __name__ == "__main__":
    test_single_image() 