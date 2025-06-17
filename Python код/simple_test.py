#!/usr/bin/env python3
"""
🔍 Simple ComfyUI API Test
Тестируем подключение к ComfyUI и изучаем доступные функции
"""

import requests
import json

def test_comfyui_connection():
    """Тестируем подключение к ComfyUI"""
    server_url = "http://localhost:8188"
    
    print("🚀 Тестируем ComfyUI API...")
    
    # 1. Проверяем статус сервера
    try:
        response = requests.get(f"{server_url}/system_stats")
        if response.status_code == 200:
            print("✅ ComfyUI сервер работает!")
            stats = response.json()
            print(f"📊 Статистика: {json.dumps(stats, indent=2)}")
        else:
            print(f"❌ Ошибка статуса: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    # 2. Получаем информацию о доступных нодах
    try:
        response = requests.get(f"{server_url}/object_info")
        if response.status_code == 200:
            print("✅ Получены доступные ноды!")
            nodes = response.json()
            
            # Ищем ноды для upscale
            upscale_nodes = []
            for node_name, node_info in nodes.items():
                if 'upscale' in node_name.lower() or 'scale' in node_name.lower():
                    upscale_nodes.append(node_name)
            
            print(f"🔍 Найдено upscale нодов: {len(upscale_nodes)}")
            for node in upscale_nodes[:10]:  # Показываем первые 10
                print(f"   📦 {node}")
                
            # Ищем LoadImage ноду
            if "LoadImage" in nodes:
                print("✅ LoadImage нода найдена!")
                print(f"📋 Параметры LoadImage: {json.dumps(nodes['LoadImage'], indent=2)}")
            else:
                print("❌ LoadImage нода не найдена")
                
            # Ищем SaveImage ноду
            if "SaveImage" in nodes:
                print("✅ SaveImage нода найдена!")
            else:
                print("❌ SaveImage нода не найдена")
                
        else:
            print(f"❌ Ошибка получения нодов: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении нодов: {e}")
    
    # 3. Проверяем очередь
    try:
        response = requests.get(f"{server_url}/queue")
        if response.status_code == 200:
            print("✅ Очередь доступна!")
            queue_info = response.json()
            print(f"📋 Информация об очереди: {json.dumps(queue_info, indent=2)}")
        else:
            print(f"❌ Ошибка очереди: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при проверке очереди: {e}")
    
    # 4. Проверяем историю
    try:
        response = requests.get(f"{server_url}/history")
        if response.status_code == 200:
            print("✅ История доступна!")
            history = response.json()
            print(f"📚 Записей в истории: {len(history)}")
        else:
            print(f"❌ Ошибка истории: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при проверке истории: {e}")

if __name__ == "__main__":
    test_comfyui_connection() 