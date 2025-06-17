#!/usr/bin/env python3
"""
🚀 ComfyUI MCP Server
Model Context Protocol сервер для интеграции ComfyUI с AI ассистентами
"""

import json
import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import os
from pathlib import Path

# Импортируем наш upscaler
from comfy_upscaler_fixed import ComfyUpscalerFixed

@dataclass
class MCPTool:
    """Описание инструмента MCP"""
    name: str
    description: str
    input_schema: Dict[str, Any]

class ComfyUIMCPServer:
    """MCP сервер для ComfyUI"""
    
    def __init__(self, comfyui_url: str = "http://localhost:8188"):
        self.comfyui_url = comfyui_url
        self.upscaler = ComfyUpscalerFixed(comfyui_url)
        self.tools = self._init_tools()
        
    def _init_tools(self) -> List[MCPTool]:
        """Инициализация доступных инструментов"""
        return [
            MCPTool(
                name="comfyui_upscale_image",
                description="Увеличивает одно изображение через ComfyUI",
                input_schema={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Путь к изображению для upscale"
                        },
                        "output_dir": {
                            "type": "string", 
                            "description": "Директория для сохранения результата",
                            "default": "upscaled_images"
                        },
                        "use_model": {
                            "type": "boolean",
                            "description": "Использовать ли AI модель для upscale",
                            "default": False
                        }
                    },
                    "required": ["image_path"]
                }
            ),
            MCPTool(
                name="comfyui_batch_upscale",
                description="Пакетное увеличение всех изображений в папке",
                input_schema={
                    "type": "object",
                    "properties": {
                        "input_dir": {
                            "type": "string",
                            "description": "Папка с исходными изображениями"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Папка для результатов",
                            "default": "upscaled_images"
                        },
                        "extensions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Поддерживаемые расширения файлов",
                            "default": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
                        }
                    },
                    "required": ["input_dir"]
                }
            ),
            MCPTool(
                name="comfyui_status",
                description="Проверяет статус ComfyUI сервера",
                input_schema={
                    "type": "object",
                    "properties": {}
                }
            ),
            MCPTool(
                name="comfyui_list_images",
                description="Показывает список изображений в папке",
                input_schema={
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Папка для просмотра",
                            "default": "."
                        }
                    }
                }
            ),
            MCPTool(
                name="comfyui_get_models",
                description="Получает список доступных upscale моделей",
                input_schema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка вызова инструмента"""
        try:
            if tool_name == "comfyui_upscale_image":
                return await self._upscale_image(arguments)
            elif tool_name == "comfyui_batch_upscale":
                return await self._batch_upscale(arguments)
            elif tool_name == "comfyui_status":
                return await self._get_status()
            elif tool_name == "comfyui_list_images":
                return await self._list_images(arguments)
            elif tool_name == "comfyui_get_models":
                return await self._get_models()
            else:
                return {"error": f"Неизвестный инструмент: {tool_name}"}
        except Exception as e:
            return {"error": f"Ошибка выполнения {tool_name}: {str(e)}"}
    
    async def _upscale_image(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Увеличение одного изображения"""
        image_path = args["image_path"]
        output_dir = args.get("output_dir", "upscaled_images")
        use_model = args.get("use_model", False)
        
        if not os.path.exists(image_path):
            return {"error": f"Файл не найден: {image_path}"}
        
        # Создаем выходную директорию
        os.makedirs(output_dir, exist_ok=True)
        
        # Выполняем upscale
        success = self.upscaler.upscale_image(image_path, output_dir, use_model)
        
        if success:
            return {
                "success": True,
                "message": f"Изображение {image_path} успешно увеличено",
                "output_dir": output_dir
            }
        else:
            return {"error": f"Ошибка при обработке {image_path}"}
    
    async def _batch_upscale(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Пакетное увеличение изображений"""
        input_dir = args["input_dir"]
        output_dir = args.get("output_dir", "upscaled_images")
        extensions = tuple(args.get("extensions", [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]))
        
        if not os.path.exists(input_dir):
            return {"error": f"Папка не найдена: {input_dir}"}
        
        # Находим изображения
        image_files = []
        for ext in extensions:
            image_files.extend(Path(input_dir).glob(f"*{ext}"))
            image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
        
        if not image_files:
            return {"error": f"Изображения не найдены в {input_dir}"}
        
        # Выполняем пакетную обработку
        self.upscaler.batch_upscale(input_dir, output_dir)
        
        return {
            "success": True,
            "message": f"Обработано {len(image_files)} изображений",
            "input_dir": input_dir,
            "output_dir": output_dir,
            "files_count": len(image_files)
        }
    
    async def _get_status(self) -> Dict[str, Any]:
        """Проверка статуса ComfyUI"""
        import requests
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            if response.status_code == 200:
                stats = response.json()
                return {
                    "success": True,
                    "status": "online",
                    "url": self.comfyui_url,
                    "stats": stats
                }
            else:
                return {
                    "success": False,
                    "status": "offline",
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "status": "offline", 
                "error": str(e)
            }
    
    async def _list_images(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Список изображений в папке"""
        directory = args.get("directory", ".")
        
        if not os.path.exists(directory):
            return {"error": f"Папка не найдена: {directory}"}
        
        extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        images = []
        
        for ext in extensions:
            images.extend([str(f) for f in Path(directory).glob(f"*{ext}")])
            images.extend([str(f) for f in Path(directory).glob(f"*{ext.upper()}")])
        
        return {
            "success": True,
            "directory": directory,
            "images": sorted(images),
            "count": len(images)
        }
    
    async def _get_models(self) -> Dict[str, Any]:
        """Получение списка доступных моделей"""
        models = self.upscaler.check_available_upscale_models()
        return {
            "success": True,
            "models": models,
            "count": len(models)
        }
    
    def get_tools_manifest(self) -> Dict[str, Any]:
        """Возвращает манифест доступных инструментов для MCP"""
        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema
                }
                for tool in self.tools
            ]
        }

# MCP протокол сервер
class MCPProtocolHandler:
    """Обработчик MCP протокола"""
    
    def __init__(self):
        self.comfyui_server = ComfyUIMCPServer()
        
    async def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Инициализация MCP соединения"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "comfyui-mcp-server",
                "version": "1.0.0"
            }
        }
    
    async def handle_tools_list(self) -> Dict[str, Any]:
        """Список доступных инструментов"""
        manifest = self.comfyui_server.get_tools_manifest()
        return {"tools": manifest["tools"]}
    
    async def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Вызов инструмента"""
        tool_name = params["name"]
        arguments = params.get("arguments", {})
        
        result = await self.comfyui_server.handle_tool_call(tool_name, arguments)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False, indent=2)
                }
            ]
        }

# Основная функция для запуска сервера
async def main():
    """Запуск MCP сервера"""
    handler = MCPProtocolHandler()
    
    print("🚀 ComfyUI MCP Server запущен!")
    print("📡 Ожидание подключений...")
    
    # Здесь должна быть реализация транспорта (stdio, websocket, etc.)
    # Для простоты создадим REST API сервер
    
    from aiohttp import web, web_request
    
    async def handle_mcp_request(request: web_request.Request):
        """Обработка MCP запросов"""
        try:
            data = await request.json()
            method = data.get("method")
            params = data.get("params", {})
            
            if method == "initialize":
                result = await handler.handle_initialize(params)
            elif method == "tools/list":
                result = await handler.handle_tools_list()
            elif method == "tools/call":
                result = await handler.handle_tools_call(params)
            else:
                result = {"error": f"Неизвестный метод: {method}"}
            
            return web.json_response({
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": result
            })
            
        except Exception as e:
            return web.json_response({
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {"code": -1, "message": str(e)}
            })
    
    # Создаем веб-приложение
    app = web.Application()
    app.router.add_post("/mcp", handle_mcp_request)
    
    # Добавляем CORS для Cursor
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
    
    print("🌐 MCP сервер запущен на http://localhost:3001/mcp")
    print("🔗 Используйте этот URL для подключения к Cursor")
    
    # Держим сервер активным
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("👋 Завершение работы MCP сервера...")

if __name__ == "__main__":
    asyncio.run(main()) 