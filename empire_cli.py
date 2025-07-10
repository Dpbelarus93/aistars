#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🏢 EMPIRE AI CORPORATION - КОМАНДНЫЙ ИНТЕРФЕЙС
👑 Управление корпоративной империей агентов
💻 Простые команды для сложных задач
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from empire_agents import EmpireCorporation

class EmpireCLI:
    """👑 Командный интерфейс для управления империей"""
    
    def __init__(self):
        self.empire = None
        self.workspace_path = Path("EMPIRE_WORKSPACE")
    
    def init_empire(self):
        """🏗️ Инициализация корпоративной империи"""
        print("👑" * 60)
        print("🏢 ИНИЦИАЛИЗАЦИЯ EMPIRE AI CORPORATION")
        print("👑" * 60)
        
        self.empire = EmpireCorporation()
        
        print("\n🚀 КОРПОРАТИВНАЯ ИМПЕРИЯ ГОТОВА К РАБОТЕ!")
        print("📋 Доступные агенты:")
        
        for agent_name, agent in self.empire.agents.items():
            print(f"  🤖 {agent_name}: {agent.role} ({agent.department})")
        
        return True
    
    def execute_project(self, project_file: str):
        """🚀 Выполнение проекта корпорацией"""
        
        if not self.empire:
            self.init_empire()
        
        # Загрузка требований к проекту
        if Path(project_file).exists():
            with open(project_file, 'r', encoding='utf-8') as f:
                project_requirements = json.load(f)
        else:
            print(f"❌ Файл проекта не найден: {project_file}")
            return
        
        print(f"🚀 Начинаю выполнение проекта: {project_requirements.get('name', 'Unnamed')}")
        
        # Выполнение проекта
        result = self.empire.execute_project(project_requirements)
        
        # Вывод результатов
        print(f"\n✅ ПРОЕКТ ЗАВЕРШЕН!")
        print(f"📋 ID: {result['project_id']}")
        print(f"📊 Статус: {result['completion_status']}")
        print(f"👑 Команда: {', '.join(result['strategy']['assigned_team'])}")
        print(f"🎯 Сложность: {result['strategy']['complexity_level']}")
        
        # Сохранение результатов
        self.save_project_results(result)
    
    def research_domain(self, domain: str):
        """🔬 Исследование предметной области"""
        
        if not self.empire:
            self.init_empire()
        
        print(f"🔬 ИССЛЕДОВАНИЕ ОБЛАСТИ: {domain}")
        print("=" * 50)
        
        # Запуск исследования
        research_result = self.empire.agents["RESEARCH"].research_best_solutions(domain)
        
        # Вывод результатов
        print(f"📊 Найдено решений: {len(research_result['top_solutions'])}")
        print(f"🎯 Уверенность исследования: {research_result['research_confidence']:.2f}")
        
        print("\n🔝 ТОП-5 РЕШЕНИЙ:")
        for i, solution in enumerate(research_result['top_solutions'][:5], 1):
            print(f"  {i}. {solution.get('title', 'N/A')}")
            print(f"     🌟 Рейтинг: {solution.get('stars', 0)}")
            print(f"     🔗 {solution.get('url', 'N/A')}")
            print()
        
        return research_result
    
    def mentor_session(self, junior_agent: str, task_type: str):
        """🎓 Менторская сессия"""
        
        if not self.empire:
            self.init_empire()
        
        print(f"🎓 МЕНТОРСКАЯ СЕССИЯ")
        print(f"👨‍🎓 Студент: {junior_agent}")
        print(f"📚 Тема: {task_type}")
        print("=" * 50)
        
        # Создание задачи для менторства
        task = {
            "type": task_type,
            "domain": "programming",
            "complexity": "medium"
        }
        
        # Проведение менторства
        guidance = self.empire.agents["SENIOR_DEV"].mentor_junior_agent(junior_agent, task)
        
        # Вывод рекомендаций
        print("💡 РЕКОМЕНДАЦИИ МЕНТОРА:")
        for recommendation in guidance.get("approach_recommendations", []):
            print(f"  • {recommendation}")
        
        print("\n📚 BEST PRACTICES:")
        for practice in guidance.get("best_practices", []):
            print(f"  ✅ {practice}")
        
        print("\n📖 РЕСУРСЫ ДЛЯ ИЗУЧЕНИЯ:")
        for resource in guidance.get("learning_resources", []):
            print(f"  📄 {resource}")
        
        return guidance
    
    def learning_session(self):
        """🧠 Сессия корпоративного обучения"""
        
        if not self.empire:
            self.init_empire()
        
        print("🧠 КОРПОРАТИВНОЕ ОБУЧЕНИЕ")
        print("=" * 50)
        
        # Запуск обучения
        learning_result = self.empire.agents["LEARNING"].learn_from_corporate_experience()
        
        # Вывод результатов
        print(f"📊 Проанализировано точек данных: {learning_result['data_points_analyzed']}")
        print(f"🎯 Паттернов успеха найдено: {len(learning_result['success_patterns'])}")
        print(f"❌ Паттернов неудач найдено: {len(learning_result['failure_patterns'])}")
        
        print("\n✅ КЛЮЧЕВЫЕ ПАТТЕРНЫ УСПЕХА:")
        for pattern in learning_result['success_patterns'][:3]:
            print(f"  • {pattern}")
        
        print("\n📈 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")
        for recommendation in learning_result['recommendations'][:3]:
            print(f"  🎯 {recommendation}")
        
        return learning_result
    
    def corporate_standup(self):
        """📊 Корпоративный standup"""
        
        if not self.empire:
            self.init_empire()
        
        print("📊 DAILY STANDUP - EMPIRE AI CORPORATION")
        print("=" * 60)
        
        standup_data = self.empire.daily_standup()
        
        for agent_name, data in standup_data.items():
            print(f"\n🤖 {agent_name}:")
            print(f"   📊 Статус: {data['status']}")
            print(f"   ⭐ Опыт: {data['experience_points']} XP")
            print(f"   🎯 Навыков: {len(data['current_skills'])}")
            
            if data['current_skills']:
                print("   💪 Топ навыки:")
                sorted_skills = sorted(data['current_skills'].items(), key=lambda x: x[1], reverse=True)
                for skill, level in sorted_skills[:3]:
                    print(f"      • {skill}: {level:.2f}")
    
    def create_sample_project(self, project_name: str):
        """📋 Создание примера проекта"""
        
        sample_projects = {
            "ai_video": {
                "name": "AI Video Generator",
                "domain": "artificial intelligence",
                "technical_requirements": [
                    "video generation",
                    "AI integration",
                    "real-time processing",
                    "user interface",
                    "cloud deployment"
                ],
                "deadline": "normal",
                "innovation": "breakthrough",
                "resources": "high",
                "description": "Создание AI системы для генерации видео из текста"
            },
            
            "crypto_bot": {
                "name": "Crypto Trading Bot",
                "domain": "financial technology",
                "technical_requirements": [
                    "real-time data processing",
                    "machine learning",
                    "API integration",
                    "risk management",
                    "backtesting"
                ],
                "deadline": "urgent",
                "innovation": "incremental",
                "resources": "medium",
                "description": "Автоматический бот для торговли криптовалютами"
            },
            
            "social_media": {
                "name": "Social Media Manager",
                "domain": "social media automation",
                "technical_requirements": [
                    "content generation",
                    "scheduling",
                    "analytics",
                    "multi-platform",
                    "AI writing"
                ],
                "deadline": "normal",
                "innovation": "incremental",
                "resources": "standard",
                "description": "Автоматизация управления социальными сетями"
            }
        }
        
        if project_name in sample_projects:
            project = sample_projects[project_name]
            filename = f"project_{project_name}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(project, f, ensure_ascii=False, indent=2)
            
            print(f"📋 Создан проект: {filename}")
            print(f"📄 Название: {project['name']}")
            print(f"🎯 Описание: {project['description']}")
            print(f"⚡ Сложность: {len(project['technical_requirements'])} требований")
            
        else:
            print(f"❌ Неизвестный тип проекта: {project_name}")
            print("📋 Доступные проекты:")
            for name, project in sample_projects.items():
                print(f"  • {name}: {project['name']}")
    
    def monitor_empire(self):
        """👁️ Мониторинг состояния империи"""
        
        if not self.empire:
            print("❌ Империя не инициализирована. Запустите --init-empire")
            return
        
        print("👁️ МОНИТОРИНГ EMPIRE AI CORPORATION")
        print("🔄 Обновление каждые 5 секунд. Ctrl+C для остановки")
        print("=" * 60)
        
        try:
            while True:
                # Очистка экрана
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Заголовок
                print("👑 EMPIRE AI CORPORATION - LIVE MONITOR")
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
                print("=" * 60)
                
                # Статус агентов
                standup_data = self.empire.daily_standup()
                
                print("🤖 СТАТУС АГЕНТОВ:")
                for agent_name, data in standup_data.items():
                    status_emoji = {"idle": "😴", "processing": "⚡", "completed": "✅"}
                    emoji = status_emoji.get(data['status'], "❓")
                    
                    print(f"  {emoji} {agent_name}: {data['status']} | XP: {data['experience_points']} | Навыков: {len(data['current_skills'])}")
                
                # Информация о рабочем пространстве
                print(f"\n📁 РАБОЧЕЕ ПРОСТРАНСТВО:")
                if self.workspace_path.exists():
                    departments = [d for d in self.workspace_path.iterdir() if d.is_dir()]
                    print(f"  📂 Отделов: {len(departments)}")
                    for dept in departments:
                        agents = [a for a in dept.iterdir() if a.is_dir()]
                        print(f"    • {dept.name}: {len(agents)} агентов")
                
                # База знаний
                kb_file = Path("empire_knowledge.db")
                if kb_file.exists():
                    size = kb_file.stat().st_size / 1024  # KB
                    print(f"\n🧠 БАЗА ЗНАНИЙ: {size:.1f} KB")
                
                print("\n" + "=" * 60)
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен")
    
    def save_project_results(self, result: dict):
        """💾 Сохранение результатов проекта"""
        
        results_dir = Path("project_results")
        results_dir.mkdir(exist_ok=True)
        
        filename = f"result_{result['project_id']}.json"
        filepath = results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"💾 Результаты сохранены: {filepath}")
    
    def show_empire_stats(self):
        """📈 Статистика империи"""
        
        if not self.empire:
            print("❌ Империя не инициализирована")
            return
        
        print("📈 СТАТИСТИКА EMPIRE AI CORPORATION")
        print("=" * 60)
        
        # Общая статистика
        total_xp = sum(agent.experience_points for agent in self.empire.agents.values())
        total_skills = sum(len(agent.skills) for agent in self.empire.agents.values())
        
        print(f"🏢 Агентов в корпорации: {len(self.empire.agents)}")
        print(f"⭐ Общий опыт: {total_xp} XP")
        print(f"🎯 Общих навыков: {total_skills}")
        
        # Топ агентов по опыту
        print("\n🏆 ТОП АГЕНТОВ ПО ОПЫТУ:")
        sorted_agents = sorted(
            self.empire.agents.items(), 
            key=lambda x: x[1].experience_points, 
            reverse=True
        )
        
        for i, (name, agent) in enumerate(sorted_agents[:3], 1):
            print(f"  {i}. {name}: {agent.experience_points} XP ({agent.role})")
        
        # База знаний
        kb_file = Path("empire_knowledge.db")
        if kb_file.exists():
            size = kb_file.stat().st_size / 1024
            print(f"\n🧠 Размер базы знаний: {size:.1f} KB")
            modified = datetime.fromtimestamp(kb_file.stat().st_mtime)
            print(f"📅 Последнее обновление: {modified.strftime('%Y-%m-%d %H:%M')}")

def main():
    """🚀 Главная функция CLI"""
    
    parser = argparse.ArgumentParser(
        description="👑 Empire AI Corporation - Командный интерфейс",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
👑 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

# Инициализация корпорации
python empire_cli.py --init-empire

# Создание и выполнение проекта
python empire_cli.py --create-project ai_video
python empire_cli.py --execute-project project_ai_video.json

# Исследование области
python empire_cli.py --research "machine learning"

# Менторство
python empire_cli.py --mentor junior_dev_001 --task python_optimization

# Корпоративное обучение
python empire_cli.py --learning-session

# Мониторинг
python empire_cli.py --monitor

# Статистика
python empire_cli.py --stats
        """
    )
    
    # Основные команды
    parser.add_argument("--init-empire", action="store_true",
                       help="🏗️ Инициализация корпоративной империи")
    
    parser.add_argument("--execute-project", metavar="FILE",
                       help="🚀 Выполнение проекта из JSON файла")
    
    parser.add_argument("--research", metavar="DOMAIN",
                       help="🔬 Исследование предметной области")
    
    parser.add_argument("--mentor", metavar="AGENT",
                       help="🎓 Менторство агента")
    
    parser.add_argument("--task", metavar="TYPE",
                       help="📚 Тип задачи для менторства")
    
    parser.add_argument("--learning-session", action="store_true",
                       help="🧠 Сессия корпоративного обучения")
    
    parser.add_argument("--standup", action="store_true",
                       help="📊 Ежедневный standup")
    
    parser.add_argument("--monitor", action="store_true",
                       help="👁️ Мониторинг состояния империи")
    
    parser.add_argument("--stats", action="store_true",
                       help="📈 Статистика империи")
    
    parser.add_argument("--create-project", metavar="TYPE",
                       help="📋 Создание примера проекта (ai_video, crypto_bot, social_media)")
    
    args = parser.parse_args()
    
    cli = EmpireCLI()
    
    # Обработка команд
    if args.init_empire:
        cli.init_empire()
    
    elif args.execute_project:
        cli.execute_project(args.execute_project)
    
    elif args.research:
        cli.research_domain(args.research)
    
    elif args.mentor and args.task:
        cli.mentor_session(args.mentor, args.task)
    
    elif args.mentor:
        print("❌ Для менторства укажите --task")
    
    elif args.learning_session:
        cli.learning_session()
    
    elif args.standup:
        cli.corporate_standup()
    
    elif args.monitor:
        cli.monitor_empire()
    
    elif args.stats:
        cli.show_empire_stats()
    
    elif args.create_project:
        cli.create_sample_project(args.create_project)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 