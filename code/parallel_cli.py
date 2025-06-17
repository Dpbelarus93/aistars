#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
🔥 КОМАНДНЫЙ ИНТЕРФЕЙС ДЛЯ ПАРАЛЛЕЛЬНЫХ АГЕНТОВ
💻 Простое управление системой через команды
⚡ Быстрый запуск задач для пользователя
"""

import argparse
import json
import os
import sys
from pathlib import Path
from parallel_task_manager import ParallelTaskManager
import time

class ParallelCLI:
    """💻 Командный интерфейс для управления агентами"""
    
    def __init__(self):
        self.manager = None
        self.workspace_path = Path("PARALLEL_WORKSPACE")
    
    def init_system(self):
        """🏗️ Инициализация системы"""
        print("🔥" * 50)
        print("🤖 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ ПАРАЛЛЕЛЬНЫХ АГЕНТОВ")
        print("🔥" * 50)
        
        self.manager = ParallelTaskManager()
        
        # Создание основных агентов
        agents = ["video", "audio", "ai_generation", "analysis"]
        for agent_type in agents:
            self.manager.create_agent(agent_type)
            print(f"✅ Агент {agent_type} создан")
        
        print("\n🚀 Система готова к работе!")
        return True
    
    def assign_video_task(self, task_type, input_path, **kwargs):
        """🎬 Назначение видеозадачи"""
        
        if not self.manager:
            self.init_system()
        
        task_data = {
            "input": input_path,
            **kwargs
        }
        
        self.manager.assign_task(task_type, task_data)
        print(f"✅ Видеозадача '{task_type}' назначена")
        print(f"📁 Входной файл: {input_path}")
    
    def assign_audio_task(self, task_type, input_path, **kwargs):
        """🎵 Назначение аудиозадачи"""
        
        if not self.manager:
            self.init_system()
        
        task_data = {
            "input": input_path,
            **kwargs
        }
        
        self.manager.assign_task(task_type, task_data)
        print(f"✅ Аудиозадача '{task_type}' назначена")
        print(f"📁 Входной файл: {input_path}")
    
    def assign_ai_task(self, task_type, prompt, **kwargs):
        """🤖 Назначение AI задачи"""
        
        if not self.manager:
            self.init_system()
        
        task_data = {
            "prompt": prompt,
            **kwargs
        }
        
        self.manager.assign_task(task_type, task_data)
        print(f"✅ AI задача '{task_type}' назначена")
        print(f"💬 Промпт: {prompt}")
    
    def batch_assign_tasks(self, tasks_file):
        """📋 Пакетное назначение задач из файла"""
        
        if not self.manager:
            self.init_system()
        
        if not Path(tasks_file).exists():
            print(f"❌ Файл с задачами не найден: {tasks_file}")
            return
        
        with open(tasks_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        print(f"📋 Загружено {len(tasks)} задач из {tasks_file}")
        
        for i, task in enumerate(tasks, 1):
            task_type = task.get("type")
            task_data = task.get("data", {})
            priority = task.get("priority", "medium")
            
            self.manager.assign_task(task_type, task_data, priority)
            print(f"✅ Задача {i}/{len(tasks)}: {task_type} назначена")
        
        print("🚀 Все задачи назначены!")
    
    def monitor_dashboard(self, refresh_interval=5):
        """📊 Мониторинг дашборда"""
        
        if not self.manager:
            print("❌ Система не инициализирована. Запустите --init-system")
            return
        
        print("📊 Запуск дашборда мониторинга...")
        print("🛑 Нажмите Ctrl+C для остановки")
        
        try:
            while True:
                # Получение статуса системы
                system_info = self.get_system_status()
                
                # Очистка экрана
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Вывод дашборда
                self.print_status_dashboard(system_info)
                
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен")
    
    def get_system_status(self):
        """📋 Получение статуса системы"""
        
        status_file = self.workspace_path / "TASK_MANAGER" / "system_status.json"
        
        if status_file.exists():
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"error": "Статус не найден"}
    
    def print_status_dashboard(self, system_info):
        """🖥️ Вывод дашборда статуса"""
        
        print("🔥" * 60)
        print("🤖 PARALLEL AGENTS DASHBOARD")
        print("🔥" * 60)
        
        if "error" in system_info:
            print("❌ Ошибка получения статуса")
            return
        
        print(f"⏰ Обновлено: {system_info.get('timestamp', 'N/A')}")
        print()
        
        # Статус агентов
        agents_status = system_info.get("agents_status", {})
        print("🤖 АГЕНТЫ:")
        
        if not agents_status:
            print("  😴 Агенты не активны")
        else:
            for agent_id, status in agents_status.items():
                status_emoji = {
                    "idle": "😴", 
                    "processing": "⚡", 
                    "completed": "✅", 
                    "error": "❌"
                }
                emoji = status_emoji.get(status.get("status"), "❓")
                progress = status.get("progress", 0)
                load = status.get("load", 0)
                
                print(f"  {emoji} {agent_id}")
                print(f"     Статус: {status.get('status', 'unknown')}")
                print(f"     Прогресс: {progress}%")
                print(f"     Нагрузка: {load}")
                print()
        
        # Ресурсы системы
        resources = system_info.get("system_resources", {})
        print("💻 РЕСУРСЫ СИСТЕМЫ:")
        print(f"  🔥 CPU: {resources.get('cpu_percent', 'N/A')}%")
        print(f"  🧠 Memory: {resources.get('memory_percent', 'N/A')}%")
        print(f"  💾 Disk: {resources.get('disk_usage', 'N/A')}%")
        print(f"  🎮 GPU: {'✅' if resources.get('gpu_available') else '❌'}")
        print()
        
        # Статистика задач
        queue_size = system_info.get("task_queue_size", 0)
        completed = system_info.get("completed_tasks", 0)
        
        print("📊 ЗАДАЧИ:")
        print(f"  📋 В очереди: {queue_size}")
        print(f"  ✅ Завершено: {completed}")
        print()
        print("🔥" * 60)
    
    def sync_results(self):
        """🔄 Синхронизация результатов"""
        
        if not self.manager:
            print("❌ Система не инициализирована")
            return
        
        print("🔄 Начало синхронизации результатов...")
        self.manager.sync_all_results()
        print("✅ Синхронизация завершена!")
        
        # Копирование результатов на рабочий стол
        desktop_path = Path.home() / "Desktop" / "PARALLEL_RESULTS"
        final_output = self.workspace_path / "FINAL_OUTPUT"
        
        if final_output.exists():
            import shutil
            if desktop_path.exists():
                shutil.rmtree(desktop_path)
            shutil.copytree(final_output, desktop_path)
            print(f"📁 Результаты скопированы на рабочий стол: {desktop_path}")
    
    def list_agents(self):
        """📋 Список активных агентов"""
        
        status_file = self.workspace_path / "TASK_MANAGER" / "system_status.json"
        
        if not status_file.exists():
            print("❌ Система не запущена или статус не найден")
            return
        
        with open(status_file, 'r', encoding='utf-8') as f:
            system_info = json.load(f)
        
        agents_status = system_info.get("agents_status", {})
        
        print("🤖 АКТИВНЫЕ АГЕНТЫ:")
        print("-" * 50)
        
        for agent_id, status in agents_status.items():
            print(f"🤖 {agent_id}")
            print(f"   Статус: {status.get('status', 'unknown')}")
            print(f"   Прогресс: {status.get('progress', 0)}%")
            print(f"   Текущая задача: {status.get('current_task', 'None')}")
            print()
    
    def stop_system(self):
        """🛑 Остановка системы"""
        
        if self.manager:
            print("🛑 Остановка системы...")
            self.manager.sync_all_results()
            print("✅ Система остановлена!")
        else:
            print("❌ Система не запущена")

def create_sample_tasks_file():
    """📋 Создание примера файла с задачами"""
    
    sample_tasks = [
        {
            "type": "video_upscaling",
            "data": {"input": "video1.mp4", "target_resolution": "4K"},
            "priority": "high"
        },
        {
            "type": "audio_separation", 
            "data": {"input": "track1.mp3", "output_format": "wav"},
            "priority": "medium"
        },
        {
            "type": "image_generation",
            "data": {"prompt": "Ultra-realistic AI rapper character"},
            "priority": "medium"
        },
        {
            "type": "trend_analysis",
            "data": {"keywords": ["AI", "music", "video"]},
            "priority": "low"
        }
    ]
    
    with open("sample_tasks.json", 'w', encoding='utf-8') as f:
        json.dump(sample_tasks, f, ensure_ascii=False, indent=2)
    
    print("📋 Файл sample_tasks.json создан с примерами задач")

def main():
    """🚀 Главная функция CLI"""
    
    parser = argparse.ArgumentParser(
        description="🔥 Система параллельных агентов - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🔥 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

# Инициализация системы
python parallel_cli.py --init-system

# Назначение видео задач
python parallel_cli.py --video-upscale input.mp4
python parallel_cli.py --video-convert input.mp4 --format mp4

# Назначение аудио задач  
python parallel_cli.py --audio-separate track.mp3
python parallel_cli.py --audio-enhance track.wav

# AI генерация
python parallel_cli.py --ai-image "Ultra-realistic rapper"
python parallel_cli.py --ai-video "Music video scene"

# Пакетная обработка
python parallel_cli.py --batch-tasks sample_tasks.json

# Мониторинг
python parallel_cli.py --monitor

# Синхронизация результатов
python parallel_cli.py --sync-results
        """
    )
    
    # Основные команды
    parser.add_argument("--init-system", action="store_true", 
                       help="🏗️ Инициализация системы параллельных агентов")
    
    parser.add_argument("--monitor", action="store_true",
                       help="📊 Запуск дашборда мониторинга")
    
    parser.add_argument("--sync-results", action="store_true",
                       help="🔄 Синхронизация результатов всех агентов")
    
    parser.add_argument("--list-agents", action="store_true",
                       help="📋 Список активных агентов")
    
    parser.add_argument("--stop-system", action="store_true",
                       help="🛑 Остановка системы")
    
    # Видео задачи
    parser.add_argument("--video-upscale", metavar="FILE",
                       help="🎬 Апскейлинг видео файла")
    
    parser.add_argument("--video-convert", metavar="FILE",
                       help="🎬 Конвертация видео файла")
    
    parser.add_argument("--video-compress", metavar="FILE", 
                       help="🎬 Сжатие видео файла")
    
    # Аудио задачи
    parser.add_argument("--audio-separate", metavar="FILE",
                       help="🎵 Разделение аудио файла")
    
    parser.add_argument("--audio-enhance", metavar="FILE",
                       help="🎵 Улучшение качества аудио")
    
    parser.add_argument("--audio-cut", metavar="FILE",
                       help="🎵 Нарезка аудио файла")
    
    # AI задачи
    parser.add_argument("--ai-image", metavar="PROMPT",
                       help="🤖 Генерация изображения по промпту")
    
    parser.add_argument("--ai-video", metavar="PROMPT", 
                       help="🤖 Генерация видео по промпту")
    
    parser.add_argument("--ai-lipsync", metavar="PROMPT",
                       help="🤖 Создание lip-sync видео")
    
    # Пакетная обработка
    parser.add_argument("--batch-tasks", metavar="FILE",
                       help="📋 Пакетное назначение задач из JSON файла")
    
    parser.add_argument("--create-sample", action="store_true",
                       help="📋 Создать пример файла с задачами")
    
    # Дополнительные параметры
    parser.add_argument("--format", metavar="FORMAT",
                       help="🔧 Формат выходного файла")
    
    parser.add_argument("--quality", metavar="QUALITY",
                       help="🔧 Качество обработки")
    
    args = parser.parse_args()
    
    cli = ParallelCLI()
    
    # Обработка команд
    if args.init_system:
        cli.init_system()
    
    elif args.monitor:
        cli.monitor_dashboard()
    
    elif args.sync_results:
        cli.sync_results()
    
    elif args.list_agents:
        cli.list_agents()
    
    elif args.stop_system:
        cli.stop_system()
    
    elif args.create_sample:
        create_sample_tasks_file()
    
    # Видео задачи
    elif args.video_upscale:
        cli.assign_video_task("video_upscaling", args.video_upscale)
    
    elif args.video_convert:
        format_type = args.format or "mp4"
        cli.assign_video_task("video_conversion", args.video_convert, format=format_type)
    
    elif args.video_compress:
        quality = args.quality or "medium"
        cli.assign_video_task("video_compression", args.video_compress, quality=quality)
    
    # Аудио задачи
    elif args.audio_separate:
        cli.assign_audio_task("audio_separation", args.audio_separate)
    
    elif args.audio_enhance:
        cli.assign_audio_task("audio_enhancement", args.audio_enhance)
    
    elif args.audio_cut:
        cli.assign_audio_task("audio_cutting", args.audio_cut)
    
    # AI задачи
    elif args.ai_image:
        cli.assign_ai_task("image_generation", args.ai_image)
    
    elif args.ai_video:
        cli.assign_ai_task("video_generation", args.ai_video)
    
    elif args.ai_lipsync:
        cli.assign_ai_task("lip_sync", args.ai_lipsync)
    
    # Пакетная обработка
    elif args.batch_tasks:
        cli.batch_assign_tasks(args.batch_tasks)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 