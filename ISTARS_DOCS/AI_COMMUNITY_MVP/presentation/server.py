#!/usr/bin/env python3
"""
Простой веб-сервер для презентации AI STARS
Запуск: python server.py
URL: http://localhost:8080
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Настройки сервера
PORT = 8080
HOST = 'localhost'

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def end_headers(self):
        # Добавляем заголовки для корректной работы
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    # Переходим в директорию с презентацией
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Создаем сервер
    with socketserver.TCPServer((HOST, PORT), CustomHandler) as httpd:
        url = f"http://{HOST}:{PORT}"
        
        print(f"🚀 AI STARS Презентация запущена!")
        print(f"📊 URL: {url}")
        print(f"🔗 Откройте в браузере: {url}")
        print(f"⏹️  Остановка: Ctrl+C")
        print("-" * 50)
        
        # Автоматически открываем браузер
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"⚠️  Не удалось открыть браузер автоматически: {e}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")
            sys.exit(0)

if __name__ == "__main__":
    main() 