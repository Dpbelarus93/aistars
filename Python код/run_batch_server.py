#!/usr/bin/env python3
"""
🚀 Запуск Photo Batch Processing Server
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    print("🚀 Запуск Photo Batch Processing Server...")
    print("📁 Создание необходимых директорий...")
    
    # Создаем необходимые директории
    directories = ["batch_input", "batch_output", "temp", "templates"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}")
    
    print(f"\n🌐 Сервер будет доступен по адресу: http://localhost:8000")
    print(f"📊 API документация: http://localhost:8000/docs")
    print(f"🔄 Убедитесь, что ComfyUI запущен на http://localhost:8188")
    print(f"\n🚀 Запуск сервера...\n")
    
    try:
        uvicorn.run(
            "photo_batch_server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=[".", "templates"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 