#!/usr/bin/env python3
"""
🚀 FastMCP ComfyUI Server
Современный MCP сервер для работы с ComfyUI с использованием FastMCP
"""

import asyncio
import json
import os
import base64
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
import aiofiles
import aiohttp
from PIL import Image
import io

from fastmcp import FastMCP

# Инициализация FastMCP сервера
mcp = FastMCP("ComfyUI FastMCP Server")

# Конфигурация
COMFYUI_URL = "http://127.0.0.1:8188"
UPLOAD_DIR = Path("./input_images")
OUTPUT_DIR = Path("./upscaled_images")

# Создаем директории если их нет
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Workflow для upscale
UPSCALE_WORKFLOW = {
    "1": {
        "inputs": {
            "image": "input_image.jpg",
            "upload": "image"
        },
        "class_type": "LoadImage",
        "_meta": {
            "title": "Load Image"
        }
    },
    "2": {
        "inputs": {
            "model_name": "4x_ESRGAN.pth"
        },
        "class_type": "UpscaleModelLoader",
        "_meta": {
            "title": "Load Upscale Model"
        }
    },
    "3": {
        "inputs": {
            "upscale_model": ["2", 0],
            "image": ["1", 0]
        },
        "class_type": "ImageUpscaleWithModel",
        "_meta": {
            "title": "Upscale Image (using Model)"
        }
    },
    "4": {
        "inputs": {
            "filename_prefix": "upscaled_",
            "images": ["3", 0]
        },
        "class_type": "SaveImage",
        "_meta": {
            "title": "Save Image"
        }
    }
}

async def upload_image_to_comfyui(image_path: Path) -> bool:
    """Загружает изображение в ComfyUI"""
    try:
        async with aiohttp.ClientSession() as session:
            with open(image_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('image', f, filename=image_path.name)
                
                async with session.post(f"{COMFYUI_URL}/upload/image", data=data) as response:
                    return response.status == 200
    except Exception as e:
        print(f"❌ Ошибка загрузки изображения: {e}")
        return False

async def queue_prompt(workflow: Dict) -> Optional[str]:
    """Отправляет workflow в очередь ComfyUI"""
    try:
        async with aiohttp.ClientSession() as session:
            prompt_data = {"prompt": workflow}
            async with session.post(f"{COMFYUI_URL}/prompt", json=prompt_data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("prompt_id")
                return None
    except Exception as e:
        print(f"❌ Ошибка отправки workflow: {e}")
        return None

async def wait_for_completion(prompt_id: str, timeout: int = 300) -> bool:
    """Ждет завершения обработки"""
    try:
        async with aiohttp.ClientSession() as session:
            for _ in range(timeout):
                async with session.get(f"{COMFYUI_URL}/history/{prompt_id}") as response:
                    if response.status == 200:
                        history = await response.json()
                        if prompt_id in history:
                            return True
                await asyncio.sleep(1)
        return False
    except Exception as e:
        print(f"❌ Ошибка ожидания завершения: {e}")
        return False

async def get_available_models() -> List[str]:
    """Получает список доступных моделей upscale"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/object_info") as response:
                if response.status == 200:
                    data = await response.json()
                    upscale_loader = data.get("UpscaleModelLoader", {})
                    input_info = upscale_loader.get("input", {})
                    model_name_info = input_info.get("model_name", {})
                    return model_name_info.get("values", [])
        return []
    except Exception as e:
        print(f"❌ Ошибка получения моделей: {e}")
        return []

@mcp.tool()
async def upscale_image(
    image_path: str,
    model_name: str = "4x_ESRGAN.pth",
    output_prefix: str = "upscaled_"
) -> Dict[str, Any]:
    """
    Увеличивает разрешение изображения с помощью ComfyUI
    
    Args:
        image_path: Путь к изображению для обработки
        model_name: Название модели для upscale (по умолчанию 4x_ESRGAN.pth)
        output_prefix: Префикс для выходного файла
    
    Returns:
        Результат обработки с информацией о файле
    """
    try:
        # Проверяем существование файла
        source_path = Path(image_path)
        if not source_path.exists():
            return {
                "success": False,
                "error": f"Файл не найден: {image_path}"
            }
        
        # Копируем файл в input директорию
        input_file = UPLOAD_DIR / source_path.name
        async with aiofiles.open(source_path, 'rb') as src:
            content = await src.read()
            async with aiofiles.open(input_file, 'wb') as dst:
                await dst.write(content)
        
        # Загружаем изображение в ComfyUI
        if not await upload_image_to_comfyui(input_file):
            return {
                "success": False,
                "error": "Не удалось загрузить изображение в ComfyUI"
            }
        
        # Подготавливаем workflow
        workflow = UPSCALE_WORKFLOW.copy()
        workflow["1"]["inputs"]["image"] = source_path.name
        workflow["2"]["inputs"]["model_name"] = model_name
        workflow["4"]["inputs"]["filename_prefix"] = output_prefix
        
        # Отправляем в очередь
        prompt_id = await queue_prompt(workflow)
        if not prompt_id:
            return {
                "success": False,
                "error": "Не удалось отправить задачу в очередь"
            }
        
        # Ждем завершения
        if not await wait_for_completion(prompt_id):
            return {
                "success": False,
                "error": "Превышено время ожидания обработки"
            }
        
        return {
            "success": True,
            "prompt_id": prompt_id,
            "input_file": str(source_path),
            "model_used": model_name,
            "message": f"✅ Изображение успешно обработано! ID: {prompt_id}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка обработки: {str(e)}"
        }

@mcp.tool()
async def batch_upscale(
    input_directory: str,
    model_name: str = "4x_ESRGAN.pth",
    file_extensions: List[str] = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
) -> Dict[str, Any]:
    """
    Пакетное увеличение разрешения всех изображений в папке
    
    Args:
        input_directory: Путь к папке с изображениями
        model_name: Название модели для upscale
        file_extensions: Список поддерживаемых расширений файлов
    
    Returns:
        Результат пакетной обработки
    """
    try:
        input_dir = Path(input_directory)
        if not input_dir.exists():
            return {
                "success": False,
                "error": f"Папка не найдена: {input_directory}"
            }
        
        # Находим все изображения
        image_files = []
        for ext in file_extensions:
            image_files.extend(input_dir.glob(f"*{ext}"))
            image_files.extend(input_dir.glob(f"*{ext.upper()}"))
        
        if not image_files:
            return {
                "success": False,
                "error": "В папке не найдено изображений"
            }
        
        results = []
        processed = 0
        failed = 0
        
        for image_file in image_files:
            print(f"🔄 Обрабатываем: {image_file.name}")
            result = await upscale_image(str(image_file), model_name)
            
            if result["success"]:
                processed += 1
                print(f"✅ Готово: {image_file.name}")
            else:
                failed += 1
                print(f"❌ Ошибка: {image_file.name} - {result['error']}")
            
            results.append({
                "file": image_file.name,
                "result": result
            })
        
        return {
            "success": True,
            "total_files": len(image_files),
            "processed": processed,
            "failed": failed,
            "model_used": model_name,
            "results": results,
            "message": f"✅ Обработано {processed} из {len(image_files)} файлов"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка пакетной обработки: {str(e)}"
        }

@mcp.tool()
async def list_upscale_models() -> Dict[str, Any]:
    """
    Получает список доступных моделей для upscale
    
    Returns:
        Список доступных моделей
    """
    try:
        models = await get_available_models()
        return {
            "success": True,
            "models": models,
            "count": len(models),
            "message": f"Найдено {len(models)} моделей для upscale"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка получения списка моделей: {str(e)}"
        }

@mcp.tool()
async def check_comfyui_status() -> Dict[str, Any]:
    """
    Проверяет статус ComfyUI сервера
    
    Returns:
        Информация о статусе сервера
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/system_stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    return {
                        "success": True,
                        "status": "online",
                        "url": COMFYUI_URL,
                        "stats": stats,
                        "message": "✅ ComfyUI сервер работает"
                    }
                else:
                    return {
                        "success": False,
                        "status": "error",
                        "url": COMFYUI_URL,
                        "error": f"HTTP {response.status}"
                    }
    except Exception as e:
        return {
            "success": False,
            "status": "offline",
            "url": COMFYUI_URL,
            "error": f"Сервер недоступен: {str(e)}"
        }

@mcp.tool()
async def get_queue_status() -> Dict[str, Any]:
    """
    Получает информацию о текущей очереди ComfyUI
    
    Returns:
        Информация о очереди задач
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/queue") as response:
                if response.status == 200:
                    queue_data = await response.json()
                    return {
                        "success": True,
                        "queue": queue_data,
                        "running": len(queue_data.get("queue_running", [])),
                        "pending": len(queue_data.get("queue_pending", [])),
                        "message": f"В очереди: {len(queue_data.get('queue_pending', []))} задач"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}"
                    }
    except Exception as e:
        return {
            "success": False,
            "error": f"Ошибка получения очереди: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 Запуск FastMCP ComfyUI Server...")
    print(f"🌐 ComfyUI URL: {COMFYUI_URL}")
    print(f"📁 Input Directory: {UPLOAD_DIR}")
    print(f"📁 Output Directory: {OUTPUT_DIR}")
    print("🔧 Доступные инструменты:")
    print("   • upscale_image - Увеличение одного изображения")
    print("   • batch_upscale - Пакетное увеличение изображений")
    print("   • list_upscale_models - Список доступных моделей")
    print("   • check_comfyui_status - Проверка статуса ComfyUI")
    print("   • get_queue_status - Статус очереди задач")
    print("✅ Сервер готов к работе!")
    
    # Запускаем сервер
    mcp.run() 