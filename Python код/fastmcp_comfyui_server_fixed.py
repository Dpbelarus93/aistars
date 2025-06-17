#!/usr/bin/env python3
"""
🚀 FastMCP ComfyUI Server (Fixed for Cursor)
Исправленная версия для корректной работы с Cursor IDE
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
mcp = FastMCP("ComfyUI-FastMCP-Server")

# Конфигурация
COMFYUI_URL = "http://127.0.0.1:8188"
UPLOAD_DIR = Path("./input_images")
OUTPUT_DIR = Path("./upscaled_images")

# Создаем директории если их нет
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Workflow для upscale с правильным именем модели
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
                    return model_name_info.get("values", ["4x_ESRGAN.pth"])  # Fallback
        return ["4x_ESRGAN.pth"]  # Fallback
    except Exception as e:
        print(f"❌ Ошибка получения моделей: {e}")
        return ["4x_ESRGAN.pth"]  # Fallback

@mcp.tool()
async def upscale_image(
    image_path: str,
    model_name: str = "4x_ESRGAN.pth",
    output_prefix: str = "upscaled_"
) -> str:
    """
    Увеличивает разрешение изображения с помощью ComfyUI
    
    Args:
        image_path: Путь к изображению для обработки
        model_name: Название модели для upscale (по умолчанию 4x_ESRGAN.pth)
        output_prefix: Префикс для выходного файла
    
    Returns:
        Результат обработки в виде строки
    """
    try:
        # Проверяем существование файла
        source_path = Path(image_path)
        if not source_path.exists():
            return f"❌ Файл не найден: {image_path}"
        
        # Копируем файл в input директорию
        input_file = UPLOAD_DIR / source_path.name
        async with aiofiles.open(source_path, 'rb') as src:
            content = await src.read()
            async with aiofiles.open(input_file, 'wb') as dst:
                await dst.write(content)
        
        # Загружаем изображение в ComfyUI
        if not await upload_image_to_comfyui(input_file):
            return "❌ Не удалось загрузить изображение в ComfyUI"
        
        # Подготавливаем workflow
        workflow = UPSCALE_WORKFLOW.copy()
        workflow["1"]["inputs"]["image"] = source_path.name
        workflow["2"]["inputs"]["model_name"] = model_name
        workflow["4"]["inputs"]["filename_prefix"] = output_prefix
        
        # Отправляем в очередь
        prompt_id = await queue_prompt(workflow)
        if not prompt_id:
            return "❌ Не удалось отправить задачу в очередь"
        
        # Ждем завершения
        if not await wait_for_completion(prompt_id):
            return "❌ Превышено время ожидания обработки"
        
        return f"✅ Изображение {image_path} успешно обработано! ID: {prompt_id}. Результат сохранен в ComfyUI/output/"
        
    except Exception as e:
        return f"❌ Ошибка обработки: {str(e)}"

@mcp.tool()
async def batch_upscale(
    input_directory: str,
    model_name: str = "4x_ESRGAN.pth"
) -> str:
    """
    Пакетное увеличение разрешения всех изображений в папке
    
    Args:
        input_directory: Путь к папке с изображениями
        model_name: Название модели для upscale
    
    Returns:
        Результат пакетной обработки в виде строки
    """
    try:
        input_dir = Path(input_directory)
        if not input_dir.exists():
            return f"❌ Папка не найдена: {input_directory}"
        
        # Находим все изображения
        file_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        image_files = []
        for ext in file_extensions:
            image_files.extend(input_dir.glob(f"*{ext}"))
            image_files.extend(input_dir.glob(f"*{ext.upper()}"))
        
        if not image_files:
            return "❌ В папке не найдено изображений"
        
        processed = 0
        failed = 0
        
        for image_file in image_files:
            result = await upscale_image(str(image_file), model_name)
            if "✅" in result:
                processed += 1
            else:
                failed += 1
        
        return f"✅ Пакетная обработка завершена! Обработано: {processed}, Ошибок: {failed} из {len(image_files)} файлов"
        
    except Exception as e:
        return f"❌ Ошибка пакетной обработки: {str(e)}"

@mcp.tool()
async def list_upscale_models() -> str:
    """
    Получает список доступных моделей для upscale
    
    Returns:
        Список доступных моделей в виде строки
    """
    try:
        models = await get_available_models()
        models_list = "\n".join([f"• {model}" for model in models])
        return f"📋 Доступные модели для upscale:\n{models_list}\n\nВсего найдено: {len(models)} моделей"
    except Exception as e:
        return f"❌ Ошибка получения списка моделей: {str(e)}"

@mcp.tool()
async def check_comfyui_status() -> str:
    """
    Проверяет статус ComfyUI сервера
    
    Returns:
        Информация о статусе сервера в виде строки
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/system_stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    system_info = stats.get("system", {})
                    return f"""✅ ComfyUI сервер работает!
🌐 URL: {COMFYUI_URL}
🐍 Python: {system_info.get('python_version', 'Unknown')}
🎨 ComfyUI: {system_info.get('comfyui_version', 'Unknown')}
🧠 RAM свободно: {system_info.get('ram_free', 0) // (1024**3)} ГБ
💻 OS: {system_info.get('os', 'Unknown')}"""
                else:
                    return f"❌ ComfyUI недоступен (HTTP {response.status})"
    except Exception as e:
        return f"❌ ComfyUI сервер недоступен: {str(e)}"

@mcp.tool()
async def get_queue_status() -> str:
    """
    Получает информацию о текущей очереди ComfyUI
    
    Returns:
        Информация о очереди задач в виде строки
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/queue") as response:
                if response.status == 200:
                    queue_data = await response.json()
                    running = len(queue_data.get("queue_running", []))
                    pending = len(queue_data.get("queue_pending", []))
                    return f"""📊 Статус очереди ComfyUI:
🔄 Выполняется: {running} задач
⏳ В ожидании: {pending} задач
📝 Общий статус: {'Загружен' if running > 0 else 'Свободен'}"""
                else:
                    return f"❌ Ошибка получения очереди (HTTP {response.status})"
    except Exception as e:
        return f"❌ Ошибка получения очереди: {str(e)}"

if __name__ == "__main__":
    # Запускаем сервер с правильным транспортом для Cursor
    mcp.run(transport="stdio") 