#!/usr/bin/env python3
"""
🚀 Simple ComfyUI MCP Server
Упрощенная версия MCP сервера для интеграции ComfyUI с Cursor
"""

import json
import asyncio
import os
import requests
from pathlib import Path
from aiohttp import web
from typing import Dict, Any, List

class SimpleComfyUIMCP:
    """Простой MCP сервер для ComfyUI"""
    
    def __init__(self, comfyui_url: str = "http://localhost:8188"):
        self.comfyui_url = comfyui_url
        
    async def handle_request(self, request):
        """Обработка MCP запросов"""
        try:
            data = await request.json()
            method = data.get("method")
            params = data.get("params", {})
            request_id = data.get("id", 1)
            
            print(f"📨 Получен запрос: {method}")
            
            if method == "initialize":
                result = await self._initialize(params)
            elif method == "tools/list":
                result = await self._list_tools()
            elif method == "tools/call":
                result = await self._call_tool(params)
            else:
                result = {"error": f"Неизвестный метод: {method}"}
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
            return web.json_response(response)
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return web.json_response({
                "jsonrpc": "2.0",
                "id": data.get("id", 1) if 'data' in locals() else 1,
                "error": {"code": -1, "message": str(e)}
            })
    
    async def _initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Инициализация MCP соединения"""
        print("🔗 Инициализация MCP соединения")
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "simple-comfyui-mcp",
                "version": "1.0.0"
            }
        }
    
    async def _list_tools(self) -> Dict[str, Any]:
        """Список доступных инструментов"""
        print("📋 Запрос списка инструментов")
        return {
            "tools": [
                {
                    "name": "comfyui_status",
                    "description": "Проверяет статус ComfyUI сервера",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "comfyui_list_images",
                    "description": "Показывает список изображений в папке",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Папка для просмотра",
                                "default": "."
                            }
                        }
                    }
                },
                {
                    "name": "comfyui_upscale_single",
                    "description": "Увеличивает одно изображение через ComfyUI",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "image_path": {
                                "type": "string",
                                "description": "Путь к изображению"
                            }
                        },
                        "required": ["image_path"]
                    }
                }
            ]
        }
    
    async def _call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Вызов инструмента"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        print(f"🔧 Вызов инструмента: {tool_name}")
        
        if tool_name == "comfyui_status":
            return await self._check_status()
        elif tool_name == "comfyui_list_images":
            return await self._list_images(arguments)
        elif tool_name == "comfyui_upscale_single":
            return await self._upscale_single(arguments)
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"❌ Неизвестный инструмент: {tool_name}"
                    }
                ]
            }
    
    async def _check_status(self) -> Dict[str, Any]:
        """Проверка статуса ComfyUI"""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                result_text = f"✅ ComfyUI работает!\n🌐 URL: {self.comfyui_url}\n📊 Статистика: {json.dumps(stats, indent=2, ensure_ascii=False)}"
            else:
                result_text = f"❌ ComfyUI недоступен (HTTP {response.status_code})"
        except Exception as e:
            result_text = f"❌ Ошибка подключения к ComfyUI: {e}"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }
    
    async def _list_images(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Список изображений в папке"""
        directory = args.get("directory", ".")
        
        if not os.path.exists(directory):
            result_text = f"❌ Папка не найдена: {directory}"
        else:
            extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
            images = []
            
            for ext in extensions:
                images.extend([str(f) for f in Path(directory).glob(f"*{ext}")])
                images.extend([str(f) for f in Path(directory).glob(f"*{ext.upper()}")])
            
            images = sorted(images)
            result_text = f"📁 Папка: {directory}\n📸 Найдено изображений: {len(images)}\n\n"
            
            if images:
                result_text += "📋 Список файлов:\n"
                for i, img in enumerate(images[:10], 1):  # Показываем первые 10
                    result_text += f"{i}. {img}\n"
                if len(images) > 10:
                    result_text += f"... и еще {len(images) - 10} файлов"
            else:
                result_text += "❌ Изображения не найдены"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }
    
    async def _upscale_single(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Увеличение одного изображения"""
        image_path = args.get("image_path")
        
        if not image_path:
            result_text = "❌ Не указан путь к изображению"
        elif not os.path.exists(image_path):
            result_text = f"❌ Файл не найден: {image_path}"
        else:
            # Здесь должен быть вызов нашего upscaler
            # Для простоты пока просто сообщаем о получении запроса
            result_text = f"🚀 Запрос на upscale получен!\n📸 Файл: {image_path}\n⏳ Для полной обработки используйте скрипт upscale_single.py"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": result_text
                }
            ]
        }

async def main():
    """Запуск MCP сервера"""
    print("🚀 Запуск Simple ComfyUI MCP Server...")
    
    mcp_server = SimpleComfyUIMCP()
    
    # Создаем веб-приложение
    app = web.Application()
    app.router.add_post("/mcp", mcp_server.handle_request)
    app.router.add_options("/mcp", lambda r: web.Response(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }))
    
    # Добавляем CORS
    async def add_cors(request, handler):
        response = await handler(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    app.middlewares.append(add_cors)
    
    # Запускаем сервер
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 3001)
    await site.start()
    
    print("✅ MCP сервер запущен!")
    print("🌐 URL: http://localhost:3001/mcp")
    print("🔗 Готов к подключению с Cursor")
    print("📡 Ожидание запросов...")
    
    # Держим сервер активным
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Завершение работы MCP сервера...")

if __name__ == "__main__":
    asyncio.run(main()) 