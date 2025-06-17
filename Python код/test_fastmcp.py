#!/usr/bin/env python3
"""
🧪 Тестовый скрипт для FastMCP ComfyUI Server
"""

import asyncio
import aiohttp
import json
from pathlib import Path

async def test_fastmcp_server():
    """Тестирует FastMCP сервер"""
    print("🧪 Тестирование FastMCP ComfyUI Server...")
    
    # Проверяем, что у нас есть тестовое изображение
    test_image = Path("0.jpg")
    if not test_image.exists():
        print("❌ Тестовое изображение 0.jpg не найдено")
        return
    
    print(f"✅ Найдено тестовое изображение: {test_image}")
    
    # Тестируем различные функции через прямой вызов
    try:
        # Импортируем наш сервер
        import sys
        sys.path.append('.')
        
        from fastmcp_comfyui_server import (
            check_comfyui_status,
            list_upscale_models,
            get_queue_status,
            upscale_image
        )
        
        print("\n🔍 Проверка статуса ComfyUI...")
        status = await check_comfyui_status()
        print(f"Статус: {status}")
        
        if status.get("success"):
            print("\n📋 Получение списка моделей...")
            models = await list_upscale_models()
            print(f"Модели: {models}")
            
            print("\n📊 Проверка очереди...")
            queue = await get_queue_status()
            print(f"Очередь: {queue}")
            
            print(f"\n🖼️ Тестирование upscale изображения {test_image}...")
            result = await upscale_image(str(test_image))
            print(f"Результат: {result}")
        else:
            print("❌ ComfyUI недоступен, пропускаем тесты обработки")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fastmcp_server()) 