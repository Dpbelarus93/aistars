#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ComfyUI Batch Upscaler 🚀
Автоматический upscale изображений через ComfyUI API
"""

import os
import json
import requests
import base64
from pathlib import Path
import time
from typing import List, Optional
import websocket
import threading
import uuid

class ComfyUpscaler:
    def __init__(self, server_url: str = "http://localhost:8188"):
        """
        Инициализация ComfyUI Upscaler
        
        Args:
            server_url: URL сервера ComfyUI (по умолчанию локальный)
        """
        self.server_url = server_url.rstrip('/')
        self.client_id = str(uuid.uuid4())
        
    def get_workflow_template(self) -> dict:
        """
        Создает базовый workflow для upscale изображений
        """
        return {
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
                    "model_name": "RealESRGAN_x4plus.pth"
                },
                "class_type": "UpscaleModelLoader",
                "_meta": {
                    "title": "Upscale Model Loader"
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
    
    def upload_image(self, image_path: str) -> Optional[dict]:
        """
        Загружает изображение на сервер ComfyUI
        
        Args:
            image_path: Путь к изображению
            
        Returns:
            Информация о загруженном файле или None при ошибке
        """
        try:
            with open(image_path, 'rb') as f:
                files = {'image': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(
                    f"{self.server_url}/upload/image",
                    files=files
                )
                
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Ошибка загрузки {image_path}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при загрузке {image_path}: {e}")
            return None
    
    def queue_workflow(self, workflow: dict) -> Optional[str]:
        """
        Добавляет workflow в очередь выполнения
        
        Args:
            workflow: Словарь с workflow
            
        Returns:
            ID промпта или None при ошибке
        """
        try:
            data = {
                "prompt": workflow,
                "client_id": self.client_id
            }
            
            response = requests.post(
                f"{self.server_url}/prompt",
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("prompt_id")
            else:
                print(f"❌ Ошибка добавления в очередь: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ошибка при добавлении в очередь: {e}")
            return None
    
    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> bool:
        """
        Ожидает завершения обработки
        
        Args:
            prompt_id: ID промпта
            timeout: Таймаут в секундах
            
        Returns:
            True если обработка завершена успешно
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.server_url}/history/{prompt_id}")
                
                if response.status_code == 200:
                    history = response.json()
                    if prompt_id in history:
                        return True
                        
                time.sleep(2)  # Проверяем каждые 2 секунды
                
            except Exception as e:
                print(f"⚠️ Ошибка при проверке статуса: {e}")
                time.sleep(5)
        
        print(f"⏰ Таймаут при обработке {prompt_id}")
        return False
    
    def get_output_images(self, prompt_id: str) -> List[str]:
        """
        Получает список выходных изображений
        
        Args:
            prompt_id: ID промпта
            
        Returns:
            Список путей к выходным изображениям
        """
        try:
            response = requests.get(f"{self.server_url}/history/{prompt_id}")
            
            if response.status_code == 200:
                history = response.json()
                
                if prompt_id in history:
                    outputs = history[prompt_id].get("outputs", {})
                    
                    image_files = []
                    for node_id, node_output in outputs.items():
                        if "images" in node_output:
                            for img in node_output["images"]:
                                image_files.append(img["filename"])
                    
                    return image_files
                    
        except Exception as e:
            print(f"❌ Ошибка при получении выходных изображений: {e}")
            
        return []
    
    def download_image(self, filename: str, output_dir: str) -> bool:
        """
        Скачивает обработанное изображение
        
        Args:
            filename: Имя файла на сервере
            output_dir: Директория для сохранения
            
        Returns:
            True если скачивание успешно
        """
        try:
            response = requests.get(f"{self.server_url}/view", params={
                "filename": filename,
                "type": "output"
            })
            
            if response.status_code == 200:
                output_path = os.path.join(output_dir, filename)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"❌ Ошибка скачивания {filename}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при скачивании {filename}: {e}")
            return False
    
    def upscale_image(self, image_path: str, output_dir: str) -> bool:
        """
        Выполняет upscale одного изображения
        
        Args:
            image_path: Путь к исходному изображению
            output_dir: Директория для сохранения результата
            
        Returns:
            True если upscale выполнен успешно
        """
        print(f"🚀 Обрабатываем: {os.path.basename(image_path)}")
        
        # 1. Загружаем изображение
        upload_result = self.upload_image(image_path)
        if not upload_result:
            return False
        
        # 2. Создаем workflow
        workflow = self.get_workflow_template()
        workflow["1"]["inputs"]["image"] = upload_result["name"]
        
        # 3. Добавляем в очередь
        prompt_id = self.queue_workflow(workflow)
        if not prompt_id:
            return False
        
        print(f"📋 Задача в очереди: {prompt_id}")
        
        # 4. Ждем завершения
        if not self.wait_for_completion(prompt_id):
            return False
        
        # 5. Получаем результаты
        output_files = self.get_output_images(prompt_id)
        
        if not output_files:
            print(f"❌ Нет выходных файлов для {image_path}")
            return False
        
        # 6. Скачиваем результаты
        success = True
        for filename in output_files:
            if not self.download_image(filename, output_dir):
                success = False
        
        if success:
            print(f"✅ Успешно обработан: {os.path.basename(image_path)}")
        
        return success
    
    def batch_upscale(self, input_dir: str, output_dir: str, 
                     image_extensions: tuple = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
        """
        Выполняет пакетный upscale изображений
        
        Args:
            input_dir: Директория с исходными изображениями
            output_dir: Директория для сохранения результатов
            image_extensions: Поддерживаемые расширения файлов
        """
        # Создаем выходную директорию
        os.makedirs(output_dir, exist_ok=True)
        
        # Находим все изображения
        image_files = []
        for ext in image_extensions:
            image_files.extend(Path(input_dir).glob(f"*{ext}"))
            image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"❌ Изображения не найдены в {input_dir}")
            return
        
        print(f"📁 Найдено изображений: {len(image_files)}")
        print(f"📤 Входная папка: {input_dir}")
        print(f"📥 Выходная папка: {output_dir}")
        print("=" * 50)
        
        # Обрабатываем каждое изображение
        successful = 0
        failed = 0
        
        for i, image_path in enumerate(image_files, 1):
            print(f"\n[{i}/{len(image_files)}] ", end="")
            
            try:
                if self.upscale_image(str(image_path), output_dir):
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"❌ Критическая ошибка при обработке {image_path}: {e}")
                failed += 1
        
        print("\n" + "=" * 50)
        print(f"✅ Успешно обработано: {successful}")
        print(f"❌ Ошибок: {failed}")
        print(f"📊 Всего файлов: {len(image_files)}")


def main():
    """Основная функция"""
    print("🚀 ComfyUI Batch Upscaler 🚀")
    print("=" * 50)
    
    # Настройки
    INPUT_DIR = "."  # Текущая папка с фотографиями
    OUTPUT_DIR = "upscaled_images"  # Папка для результатов
    SERVER_URL = "http://localhost:8188"  # ComfyUI сервер
    
    # Создаем upscaler
    upscaler = ComfyUpscaler(SERVER_URL)
    
    # Проверяем подключение к серверу
    try:
        response = requests.get(f"{SERVER_URL}/system_stats", timeout=5)
        if response.status_code == 200:
            print(f"✅ Подключение к ComfyUI: {SERVER_URL}")
        else:
            print(f"❌ ComfyUI недоступен: {SERVER_URL}")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к ComfyUI: {e}")
        print("💡 Убедитесь, что ComfyUI запущен на http://localhost:8188")
        return
    
    # Запускаем пакетную обработку
    upscaler.batch_upscale(INPUT_DIR, OUTPUT_DIR)
    
    print(f"\n🎉 Обработка завершена! Результаты сохранены в папке '{OUTPUT_DIR}'")


if __name__ == "__main__":
    main() 