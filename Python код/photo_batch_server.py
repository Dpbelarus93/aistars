#!/usr/bin/env python3
"""
🚀 Photo Batch Processing Server
FastAPI сервер для батчевой обработки фотографий через ComfyUI API
"""

import asyncio
import json
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import aiofiles
import aiohttp
from PIL import Image
import io
import base64

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Инициализация FastAPI
app = FastAPI(
    title="Photo Batch Processor",
    description="Батчевая обработка фотографий через ComfyUI API",
    version="1.0.0"
)

# Настройка шаблонов и статических файлов
templates = Jinja2Templates(directory="templates")

# Конфигурация
COMFYUI_URL = "http://127.0.0.1:8188"
UPLOAD_DIR = Path("./batch_input")
OUTPUT_DIR = Path("./batch_output")
TEMP_DIR = Path("./temp")

# Создаем директории
for directory in [UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# Модели данных
class ProcessingTask(BaseModel):
    task_id: str
    status: str  # pending, processing, completed, failed
    files: List[str]
    parameters: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime] = None
    results: Optional[List[str]] = None
    error: Optional[str] = None

class BatchConfig(BaseModel):
    upscale_model: str = "4x_ESRGAN.pth"
    upscale_factor: float = 4.0
    output_format: str = "png"
    quality: int = 95
    noise_reduction: bool = True
    enhance_details: bool = True
    batch_size: int = 5

# Глобальное хранилище задач
active_tasks: Dict[str, ProcessingTask] = {}

# Workflow шаблоны для разных типов обработки
WORKFLOWS = {
    "upscale": {
        "1": {
            "inputs": {
                "image": "input_image.jpg",
                "upload": "image"
            },
            "class_type": "LoadImage",
            "_meta": {"title": "Load Image"}
        },
        "2": {
            "inputs": {
                "model_name": "4x_ESRGAN.pth"
            },
            "class_type": "UpscaleModelLoader",
            "_meta": {"title": "Load Upscale Model"}
        },
        "3": {
            "inputs": {
                "upscale_model": ["2", 0],
                "image": ["1", 0]
            },
            "class_type": "ImageUpscaleWithModel",
            "_meta": {"title": "Upscale Image"}
        },
        "4": {
            "inputs": {
                "filename_prefix": "upscaled_",
                "images": ["3", 0]
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"}
        }
    },
    "enhance": {
        "1": {
            "inputs": {
                "image": "input_image.jpg",
                "upload": "image"
            },
            "class_type": "LoadImage",
            "_meta": {"title": "Load Image"}
        },
        "2": {
            "inputs": {
                "denoise": 0.7,
                "image": ["1", 0]
            },
            "class_type": "ImageDenoise",
            "_meta": {"title": "Denoise"}
        },
        "3": {
            "inputs": {
                "sharpen": 0.5,
                "image": ["2", 0]
            },
            "class_type": "ImageSharpen",
            "_meta": {"title": "Sharpen"}
        },
        "4": {
            "inputs": {
                "filename_prefix": "enhanced_",
                "images": ["3", 0]
            },
            "class_type": "SaveImage",
            "_meta": {"title": "Save Image"}
        }
    }
}

# Утилиты для работы с ComfyUI API
async def check_comfyui_connection() -> bool:
    """Проверяет подключение к ComfyUI"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/system_stats") as response:
                return response.status == 200
    except Exception:
        return False

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
        print(f"Ошибка загрузки изображения: {e}")
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
        print(f"Ошибка отправки workflow: {e}")
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
        print(f"Ошибка ожидания завершения: {e}")
        return False

async def get_available_models() -> List[str]:
    """Получает список доступных моделей"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{COMFYUI_URL}/object_info") as response:
                if response.status == 200:
                    data = await response.json()
                    upscale_loader = data.get("UpscaleModelLoader", {})
                    input_info = upscale_loader.get("input", {})
                    model_name_info = input_info.get("model_name", {})
                    return model_name_info.get("values", ["4x_ESRGAN.pth"])
        return ["4x_ESRGAN.pth"]
    except Exception:
        return ["4x_ESRGAN.pth"]

# API Routes
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    """Главная страница с интерфейсом"""
    models = await get_available_models()
    comfyui_status = await check_comfyui_connection()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "models": models,
        "comfyui_status": comfyui_status,
        "active_tasks": len(active_tasks)
    })

@app.get("/api/status")
async def get_server_status():
    """Статус сервера и подключения к ComfyUI"""
    return {
        "server_status": "running",
        "comfyui_connected": await check_comfyui_connection(),
        "active_tasks": len(active_tasks),
        "available_models": await get_available_models()
    }

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Загрузка файлов для обработки"""
    uploaded_files = []
    
    for file in files:
        if not file.content_type.startswith('image/'):
            continue
            
        # Генерируем уникальное имя файла
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Сохраняем файл
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        uploaded_files.append(unique_filename)
    
    return {"uploaded_files": uploaded_files, "count": len(uploaded_files)}

@app.post("/api/process")
async def start_batch_processing(
    background_tasks: BackgroundTasks,
    files: List[str] = Form(...),
    workflow_type: str = Form("upscale"),
    upscale_model: str = Form("4x_ESRGAN.pth"),
    output_format: str = Form("png"),
    batch_size: int = Form(5)
):
    """Запуск батчевой обработки"""
    
    task_id = str(uuid.uuid4())
    
    # Создаем задачу
    task = ProcessingTask(
        task_id=task_id,
        status="pending",
        files=files,
        parameters={
            "workflow_type": workflow_type,
            "upscale_model": upscale_model,
            "output_format": output_format,
            "batch_size": batch_size
        },
        created_at=datetime.now()
    )
    
    active_tasks[task_id] = task
    
    # Запускаем обработку в фоне
    background_tasks.add_task(process_batch, task_id)
    
    return {"task_id": task_id, "status": "started"}

@app.get("/api/task/{task_id}")
async def get_task_status(task_id: str):
    """Получить статус задачи"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return active_tasks[task_id]

@app.get("/api/tasks")
async def get_all_tasks():
    """Получить все задачи"""
    return list(active_tasks.values())

@app.get("/api/download/{task_id}")
async def download_results(task_id: str):
    """Скачать результаты обработки"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    if task.status != "completed" or not task.results:
        raise HTTPException(status_code=400, detail="Task not completed or no results")
    
    # Создаем архив с результатами
    import zipfile
    archive_path = TEMP_DIR / f"results_{task_id}.zip"
    
    with zipfile.ZipFile(archive_path, 'w') as zipf:
        for result_file in task.results:
            result_path = OUTPUT_DIR / result_file
            if result_path.exists():
                zipf.write(result_path, result_file)
    
    return FileResponse(
        archive_path,
        media_type='application/zip',
        filename=f"processed_images_{task_id}.zip"
    )

# Функция фоновой обработки
async def process_batch(task_id: str):
    """Фоновая обработка батча изображений"""
    task = active_tasks[task_id]
    task.status = "processing"
    
    try:
        workflow_type = task.parameters["workflow_type"]
        upscale_model = task.parameters["upscale_model"]
        batch_size = task.parameters["batch_size"]
        
        processed_files = []
        
        # Обрабатываем файлы батчами
        for i in range(0, len(task.files), batch_size):
            batch_files = task.files[i:i + batch_size]
            
            for filename in batch_files:
                input_path = UPLOAD_DIR / filename
                
                if not input_path.exists():
                    continue
                
                # Загружаем в ComfyUI
                if not await upload_image_to_comfyui(input_path):
                    continue
                
                # Подготавливаем workflow
                workflow = WORKFLOWS[workflow_type].copy()
                workflow["1"]["inputs"]["image"] = filename
                
                if workflow_type == "upscale":
                    workflow["2"]["inputs"]["model_name"] = upscale_model
                
                # Отправляем в очередь
                prompt_id = await queue_prompt(workflow)
                if not prompt_id:
                    continue
                
                # Ждем завершения
                if await wait_for_completion(prompt_id):
                    processed_files.append(f"processed_{filename}")
            
            # Небольшая пауза между батчами
            await asyncio.sleep(2)
        
        task.results = processed_files
        task.status = "completed"
        task.completed_at = datetime.now()
        
    except Exception as e:
        task.status = "failed"
        task.error = str(e)
        task.completed_at = datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 