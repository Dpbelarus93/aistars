#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔥 ЦЕНТРАЛЬНЫЙ МЕНЕДЖЕР ПАРАЛЛЕЛЬНЫХ ЗАДАЧ
🤖 Управление множественными агентами и задачами
⚡ Параллельная обработка в отдельных директориях
"""

import os
import json
import time
import threading
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - 🤖 [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('parallel_task_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ParallelTaskManager:
    """🎯 Главный менеджер параллельных задач"""
    
    def __init__(self, workspace_path="PARALLEL_WORKSPACE"):
        self.workspace_path = Path(workspace_path)
        self.active_agents = {}
        self.task_queue = Queue()
        self.completed_tasks = []
        self.communication_hub = AgentCommunication()
        
        # Создание рабочего пространства
        self.setup_workspace()
        logger.info("🚀 ParallelTaskManager инициализирован!")
    
    def setup_workspace(self):
        """🏗️ Создание структуры рабочего пространства"""
        
        # Основные директории
        directories = [
            "TASK_MANAGER",
            "AGENT_01_VIDEO",
            "AGENT_02_AUDIO", 
            "AGENT_03_AI_GEN",
            "AGENT_04_ANALYSIS",
            "SYNC_RESULTS",
            "FINAL_OUTPUT"
        ]
        
        for directory in directories:
            dir_path = self.workspace_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Создание подпапок для агентов
            if directory.startswith("AGENT_"):
                for subfolder in ["input", "output", "scripts", "logs"]:
                    (dir_path / subfolder).mkdir(exist_ok=True)
        
        logger.info(f"📁 Рабочее пространство создано: {self.workspace_path}")
    
    def create_agent(self, agent_type):
        """🤖 Создание нового агента"""
        
        agent_classes = {
            "video": VideoAgent,
            "audio": AudioAgent,
            "ai_generation": AIGenerationAgent,
            "analysis": AnalysisAgent
        }
        
        if agent_type in agent_classes:
            agent_id = f"AGENT_{agent_type.upper()}_{len(self.active_agents) + 1}"
            agent = agent_classes[agent_type](agent_id, self.workspace_path)
            self.active_agents[agent_id] = agent
            
            logger.info(f"🤖 Агент создан: {agent_id}")
            return agent
        else:
            logger.error(f"❌ Неизвестный тип агента: {agent_type}")
            return None
    
    def assign_task(self, task_type, task_data, priority="medium"):
        """🎯 Назначение задачи агенту"""
        
        # Поиск подходящего агента
        suitable_agents = [agent for agent in self.active_agents.values() 
                          if agent.can_handle_task(task_type) and agent.status == "idle"]
        
        if suitable_agents:
            # Выбор наименее загруженного агента
            chosen_agent = min(suitable_agents, key=lambda x: x.current_load)
            
            # Назначение задачи
            task = {
                "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": task_type,
                "data": task_data,
                "priority": priority,
                "assigned_to": chosen_agent.agent_id,
                "created_at": datetime.now(),
                "status": "assigned"
            }
            
            chosen_agent.assign_task(task)
            logger.info(f"✅ Задача {task['id']} назначена агенту {chosen_agent.agent_id}")
            
        else:
            # Добавление в очередь
            task = {
                "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": task_type,
                "data": task_data,
                "priority": priority,
                "status": "queued"
            }
            
            self.task_queue.put(task)
            logger.info(f"📋 Задача {task['id']} добавлена в очередь")
    
    def monitor_system(self):
        """📊 Мониторинг системы и агентов"""
        
        while True:
            system_info = {
                "timestamp": datetime.now(),
                "agents_status": {},
                "system_resources": self.get_system_resources(),
                "task_queue_size": self.task_queue.qsize(),
                "completed_tasks": len(self.completed_tasks)
            }
            
            # Статус каждого агента
            for agent_id, agent in self.active_agents.items():
                system_info["agents_status"][agent_id] = {
                    "status": agent.status,
                    "current_task": agent.current_task,
                    "progress": agent.get_progress(),
                    "load": agent.current_load
                }
            
            # Сохранение статуса
            self.save_system_status(system_info)
            
            # Вывод в консоль
            self.print_dashboard(system_info)
            
            time.sleep(10)  # Обновление каждые 10 секунд
    
    def get_system_resources(self):
        """💻 Получение информации о ресурсах системы"""
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "gpu_available": self.check_gpu_availability()
        }
    
    def check_gpu_availability(self):
        """🎮 Проверка доступности GPU"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def print_dashboard(self, system_info):
        """🖥️ Вывод дашборда в консоль"""
        
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🔥" * 60)
        print("🤖 СИСТЕМА ПАРАЛЛЕЛЬНЫХ АГЕНТОВ - DASHBOARD")
        print("🔥" * 60)
        print(f"⏰ Время: {system_info['timestamp'].strftime('%H:%M:%S')}")
        print()
        
        # Статус агентов
        print("🤖 АГЕНТЫ:")
        for agent_id, status in system_info["agents_status"].items():
            status_emoji = {"idle": "😴", "processing": "⚡", "completed": "✅", "error": "❌"}
            emoji = status_emoji.get(status["status"], "❓")
            print(f"  {emoji} {agent_id}: {status['status']} | Прогресс: {status['progress']}% | Нагрузка: {status['load']}")
        
        print()
        
        # Ресурсы системы
        resources = system_info["system_resources"]
        print(f"💻 РЕСУРСЫ:")
        print(f"  🔥 CPU: {resources['cpu_percent']}%")
        print(f"  🧠 Memory: {resources['memory_percent']}%") 
        print(f"  💾 Disk: {resources['disk_usage']}%")
        print(f"  🎮 GPU: {'✅' if resources['gpu_available'] else '❌'}")
        
        print()
        print(f"📋 Задач в очереди: {system_info['task_queue_size']}")
        print(f"✅ Завершенных задач: {system_info['completed_tasks']}")
        print()
        print("🔥" * 60)
    
    def save_system_status(self, system_info):
        """💾 Сохранение статуса системы"""
        
        status_file = self.workspace_path / "TASK_MANAGER" / "system_status.json"
        
        # Конвертация datetime для JSON
        system_info_json = system_info.copy()
        system_info_json["timestamp"] = system_info["timestamp"].isoformat()
        
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(system_info_json, f, ensure_ascii=False, indent=2)
    
    def sync_all_results(self):
        """🔄 Синхронизация результатов всех агентов"""
        
        sync_folder = self.workspace_path / "SYNC_RESULTS"
        final_folder = self.workspace_path / "FINAL_OUTPUT"
        
        logger.info("🔄 Начало синхронизации результатов...")
        
        # Копирование результатов каждого агента
        for agent_id, agent in self.active_agents.items():
            if agent.status == "completed":
                agent_output = agent.workspace / "output"
                sync_agent_folder = sync_folder / agent_id
                sync_agent_folder.mkdir(exist_ok=True)
                
                # Копирование файлов
                if agent_output.exists():
                    subprocess.run(['cp', '-r', str(agent_output / "*"), str(sync_agent_folder)], shell=True)
                    logger.info(f"📁 Результаты {agent_id} синхронизированы")
        
        # Создание финального результата
        self.create_final_output()
        
        logger.info("✅ Синхронизация завершена!")
    
    def create_final_output(self):
        """📦 Создание финального результата"""
        
        final_folder = self.workspace_path / "FINAL_OUTPUT"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Создание сводного отчета
        report = {
            "project_name": "PARALLEL_PROCESSING",
            "completed_at": timestamp,
            "agents_used": list(self.active_agents.keys()),
            "total_tasks": len(self.completed_tasks),
            "processing_time": self.calculate_total_time(),
            "results_location": str(final_folder)
        }
        
        report_file = final_folder / f"project_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📦 Финальный отчет создан: {report_file}")
    
    def calculate_total_time(self):
        """⏱️ Расчет общего времени обработки"""
        
        if self.completed_tasks:
            start_times = [task.get("started_at") for task in self.completed_tasks if task.get("started_at")]
            end_times = [task.get("completed_at") for task in self.completed_tasks if task.get("completed_at")]
            
            if start_times and end_times:
                total_start = min(start_times)
                total_end = max(end_times)
                return (total_end - total_start).total_seconds()
        
        return 0

class BaseAgent:
    """🤖 Базовый класс для всех агентов"""
    
    def __init__(self, agent_id, workspace_path):
        self.agent_id = agent_id
        self.workspace = workspace_path / agent_id
        self.status = "idle"
        self.current_task = None
        self.current_load = 0
        self.task_history = []
        
        # Создание логгера для агента
        self.logger = logging.getLogger(agent_id)
        handler = logging.FileHandler(self.workspace / "logs" / f"{agent_id}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        self.logger.info(f"🤖 Агент {agent_id} инициализирован")
    
    def can_handle_task(self, task_type):
        """❓ Проверка возможности выполнения задачи"""
        return task_type in self.supported_tasks
    
    def assign_task(self, task):
        """📋 Назначение задачи агенту"""
        self.current_task = task
        self.status = "processing"
        
        # Запуск задачи в отдельном потоке
        threading.Thread(target=self.execute_task, args=(task,)).start()
        
        self.logger.info(f"📋 Задача {task['id']} назначена")
    
    def execute_task(self, task):
        """⚡ Выполнение задачи"""
        try:
            self.logger.info(f"🚀 Начало выполнения задачи {task['id']}")
            
            # Выполнение специфичной логики агента
            result = self.process_task(task)
            
            # Сохранение результата
            self.save_result(task, result)
            
            # Обновление статуса
            self.status = "completed"
            self.current_task = None
            
            self.logger.info(f"✅ Задача {task['id']} завершена")
            
        except Exception as e:
            self.status = "error"
            self.logger.error(f"❌ Ошибка в задаче {task['id']}: {str(e)}")
    
    def process_task(self, task):
        """🔧 Основная логика обработки задачи (переопределяется в подклассах)"""
        raise NotImplementedError("Метод должен быть переопределен в подклассе")
    
    def save_result(self, task, result):
        """💾 Сохранение результата задачи"""
        
        result_file = self.workspace / "output" / f"{task['id']}_result.json"
        result_data = {
            "task_id": task['id'],
            "result": result,
            "completed_at": datetime.now().isoformat(),
            "agent_id": self.agent_id
        }
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    def get_progress(self):
        """📊 Получение прогресса выполнения"""
        if self.current_task:
            # Здесь может быть более сложная логика подсчета прогресса
            return 50  # Заглушка
        return 0

class VideoAgent(BaseAgent):
    """🎬 Агент для обработки видео"""
    
    def __init__(self, agent_id, workspace_path):
        super().__init__(agent_id, workspace_path)
        self.supported_tasks = ["video_upscaling", "video_conversion", "video_compression"]
    
    def process_task(self, task):
        """🎬 Обработка видео задач"""
        
        task_type = task['type']
        
        if task_type == "video_upscaling":
            return self.upscale_video(task['data'])
        elif task_type == "video_conversion":
            return self.convert_video(task['data'])
        elif task_type == "video_compression":
            return self.compress_video(task['data'])
    
    def upscale_video(self, data):
        """📈 Апскейлинг видео"""
        self.logger.info("🚀 Начало апскейлинга видео")
        
        # Имитация обработки
        time.sleep(5)
        
        return {"status": "success", "output_file": "upscaled_video.mp4"}

class AudioAgent(BaseAgent):
    """🎵 Агент для обработки аудио"""
    
    def __init__(self, agent_id, workspace_path):
        super().__init__(agent_id, workspace_path)
        self.supported_tasks = ["audio_separation", "audio_enhancement", "audio_cutting"]
    
    def process_task(self, task):
        """🎵 Обработка аудио задач"""
        
        task_type = task['type']
        
        if task_type == "audio_separation":
            return self.separate_audio(task['data'])
        elif task_type == "audio_enhancement":
            return self.enhance_audio(task['data'])
        elif task_type == "audio_cutting":
            return self.cut_audio(task['data'])
    
    def separate_audio(self, data):
        """🎤 Разделение аудио"""
        self.logger.info("🚀 Начало разделения аудио")
        
        # Имитация обработки
        time.sleep(3)
        
        return {"status": "success", "vocals": "vocals.wav", "instruments": "instruments.wav"}

class AIGenerationAgent(BaseAgent):
    """🤖 Агент для AI генерации"""
    
    def __init__(self, agent_id, workspace_path):
        super().__init__(agent_id, workspace_path)
        self.supported_tasks = ["image_generation", "video_generation", "lip_sync"]
    
    def process_task(self, task):
        """🤖 AI генерация"""
        
        task_type = task['type']
        
        if task_type == "image_generation":
            return self.generate_image(task['data'])
        elif task_type == "video_generation":
            return self.generate_video(task['data'])
        elif task_type == "lip_sync":
            return self.create_lip_sync(task['data'])
    
    def generate_image(self, data):
        """🎨 Генерация изображения"""
        self.logger.info("🚀 Начало генерации изображения")
        
        # Имитация обработки
        time.sleep(4)
        
        return {"status": "success", "output_file": "generated_image.png"}

class AnalysisAgent(BaseAgent):
    """📊 Агент для аналитики"""
    
    def __init__(self, agent_id, workspace_path):
        super().__init__(agent_id, workspace_path)
        self.supported_tasks = ["trend_analysis", "performance_analysis", "quality_check"]
    
    def process_task(self, task):
        """📊 Аналитические задачи"""
        
        task_type = task['type']
        
        if task_type == "trend_analysis":
            return self.analyze_trends(task['data'])
        elif task_type == "performance_analysis":
            return self.analyze_performance(task['data'])
        elif task_type == "quality_check":
            return self.check_quality(task['data'])
    
    def analyze_trends(self, data):
        """📈 Анализ трендов"""
        self.logger.info("🚀 Начало анализа трендов")
        
        # Имитация обработки
        time.sleep(2)
        
        return {"status": "success", "trends": ["trend1", "trend2", "trend3"]}

class AgentCommunication:
    """📡 Система коммуникации между агентами"""
    
    def __init__(self):
        self.message_queue = Queue()
        self.status_board = {}
    
    def send_message(self, from_agent, to_agent, message):
        """📤 Отправка сообщения"""
        msg = {
            'from': from_agent,
            'to': to_agent,
            'message': message,
            'timestamp': datetime.now()
        }
        self.message_queue.put(msg)
    
    def broadcast_status(self, agent_id, status):
        """📢 Рассылка статуса"""
        self.status_board[agent_id] = {
            'status': status,
            'updated': datetime.now()
        }

def main():
    """🚀 Главная функция запуска"""
    
    print("🔥" * 60)
    print("🤖 ЗАПУСК СИСТЕМЫ ПАРАЛЛЕЛЬНЫХ АГЕНТОВ")
    print("🔥" * 60)
    
    # Создание менеджера
    manager = ParallelTaskManager()
    
    # Создание агентов
    manager.create_agent("video")
    manager.create_agent("audio")
    manager.create_agent("ai_generation")
    manager.create_agent("analysis")
    
    # Запуск мониторинга в отдельном потоке
    monitoring_thread = threading.Thread(target=manager.monitor_system)
    monitoring_thread.daemon = True
    monitoring_thread.start()
    
    # Пример назначения задач
    manager.assign_task("video_upscaling", {"input": "video.mp4"})
    manager.assign_task("audio_separation", {"input": "audio.mp3"})
    manager.assign_task("image_generation", {"prompt": "AI star character"})
    
    print("✅ Система запущена! Нажмите Ctrl+C для остановки")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Остановка системы...")
        manager.sync_all_results()
        print("✅ Система остановлена!")

if __name__ == "__main__":
    main() 