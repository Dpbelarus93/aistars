#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
👔 CORPORATE DIRECTOR CLI - Интерфейс управления корпорацией
🏢 Командная строка для анализа, найма и управления задачами
"""

import argparse
import json
import time
from datetime import datetime
from empire_agents import EmpireCorporation

def main():
    parser = argparse.ArgumentParser(
        description="👔 Corporate Director CLI - Управление EMPIRE AI Corporation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🏢 Примеры использования:

📊 Анализ состояния корпорации:
  python director_cli.py --analyze

👥 План найма новых агентов:
  python director_cli.py --hiring-plan

⚡ Управляемое выполнение проекта:
  python director_cli.py --manage-project --domain "ai automation"

🎯 Выполнение кастомных задач:
  python director_cli.py --execute-tasks --tasks "task1,task2,task3"

📈 Полный отчет корпорации:
  python director_cli.py --full-report

👔 Все возможности Директора:
  python director_cli.py --demo
        """
    )
    
    # Основные команды
    parser.add_argument('--analyze', action='store_true',
                       help='📊 Анализ текущего состояния корпорации')
    
    parser.add_argument('--hiring-plan', action='store_true',
                       help='👥 Создание плана найма новых агентов')
    
    parser.add_argument('--manage-project', action='store_true',
                       help='⚡ Управляемое выполнение проекта')
    
    parser.add_argument('--execute-tasks', action='store_true',
                       help='🎯 Выполнение кастомных задач')
    
    parser.add_argument('--full-report', action='store_true',
                       help='📈 Полный отчет о корпорации')
    
    parser.add_argument('--demo', action='store_true',
                       help='👔 Демонстрация всех возможностей Директора')
    
    # Параметры
    parser.add_argument('--domain', type=str, default='general',
                       help='🎯 Область проекта (ai, automation, web, etc.)')
    
    parser.add_argument('--tasks', type=str,
                       help='📋 Список задач через запятую')
    
    parser.add_argument('--output', type=str,
                       help='💾 Файл для сохранения результатов')
    
    args = parser.parse_args()
    
    print("👔" * 60)
    print("🏢 CORPORATE DIRECTOR - УПРАВЛЕНИЕ КОРПОРАЦИЕЙ")
    print("👔" * 60)
    
    # Инициализация корпорации
    print("🏗️ Инициализация EMPIRE AI Corporation...")
    corporation = EmpireCorporation()
    director = corporation.director
    
    print(f"✅ Корпорация готова: {len(corporation.agents)} агентов + Директор")
    print()
    
    results = {}
    
    # Выполнение команд
    if args.analyze or args.demo:
        print("📊 АНАЛИЗ СОСТОЯНИЯ КОРПОРАЦИИ")
        print("=" * 50)
        
        start_time = time.time()
        analysis = corporation.run_corporate_analysis()
        analysis_time = time.time() - start_time
        
        print(f"👥 Общий штат: {analysis['total_agents']} агентов")
        print(f"⚡ Эффективность: {analysis['operational_efficiency']}%")
        print(f"📈 Время анализа: {analysis_time:.2f}с")
        print()
        
        print("🤖 ТЕКУЩИЕ АГЕНТЫ:")
        for agent_name, agent_info in analysis['current_agents'].items():
            efficiency = agent_info['efficiency_rating']
            specialization = agent_info['specialization']
            experience = agent_info['experience_points']
            
            print(f"  • {agent_name:<15} | {specialization:<20} | Эффективность: {efficiency:.1%} | Опыт: {experience}")
        
        print()
        results['analysis'] = analysis
    
    if args.hiring_plan or args.demo:
        print("👥 ПЛАН НАЙМА НОВЫХ АГЕНТОВ")
        print("=" * 50)
        
        analysis = corporation.run_corporate_analysis()
        hiring_plan = analysis['hiring_recommendations']
        
        print("🚨 КРИТИЧЕСКИЕ ПОТРЕБНОСТИ (немедленно):")
        for need in hiring_plan['immediate_needs']:
            print(f"  • {need['role']:<25} | {need['skills'][0]:<20} | {need['estimated_cost']}")
        
        print("\n📅 КРАТКОСРОЧНЫЕ ПЛАНЫ (1-2 месяца):")
        for need in hiring_plan['short_term']:
            print(f"  • {need['role']:<25} | {need['skills'][0]:<20} | {need['estimated_cost']}")
        
        print("\n🔮 ДОЛГОСРОЧНЫЕ ПЛАНЫ (3-6 месяцев):")
        for need in hiring_plan['long_term']:
            print(f"  • {need['role']:<25} | {need['skills'][0]:<20} | {need['estimated_cost']}")
        
        print()
        results['hiring_plan'] = hiring_plan
    
    if args.manage_project or args.demo:
        print("⚡ УПРАВЛЯЕМОЕ ВЫПОЛНЕНИЕ ПРОЕКТА")
        print("=" * 50)
        
        project_requirements = {
            "name": f"AI Project in {args.domain}",
            "domain": args.domain,
            "technical_requirements": ["automation", "intelligence", "scalability"],
            "deadline": "normal",
            "innovation": "high"
        }
        
        print(f"🎯 Проект: {project_requirements['name']}")
        print(f"🌐 Область: {args.domain}")
        
        start_time = time.time()
        managed_result = corporation.execute_managed_project(project_requirements)
        execution_time = time.time() - start_time
        
        director_result = managed_result['director_management']
        
        print(f"📊 Результат:")
        print(f"  • Задач выполнено: {director_result['successful_tasks']}/{director_result['total_tasks']}")
        print(f"  • Эффективность: {director_result['efficiency_score']:.1f}%")
        print(f"  • Время выполнения: {execution_time:.2f}с")
        print(f"  • Статус: {managed_result['completion_status']}")
        
        if director_result['lessons_learned']:
            print("📚 Извлеченные уроки:")
            for lesson in director_result['lessons_learned']:
                print(f"  • {lesson}")
        
        print()
        results['managed_project'] = managed_result
    
    if args.execute_tasks:
        print("🎯 ВЫПОЛНЕНИЕ КАСТОМНЫХ ЗАДАЧ")
        print("=" * 50)
        
        if args.tasks:
            task_names = [t.strip() for t in args.tasks.split(',')]
            
            # Создание задач
            custom_tasks = []
            for task_name in task_names:
                custom_tasks.append({
                    "name": task_name,
                    "type": "custom",
                    "domain": args.domain,
                    "required_skills": ["general"],
                    "priority": "medium"
                })
            
            print(f"📋 Выполняю {len(custom_tasks)} задач:")
            for task in custom_tasks:
                print(f"  • {task['name']}")
            
            start_time = time.time()
            task_result = director.manage_task_execution(custom_tasks)
            execution_time = time.time() - start_time
            
            print(f"\n📊 Результат:")
            print(f"  • Успешно: {task_result['successful_tasks']}/{task_result['total_tasks']}")
            print(f"  • Эффективность: {task_result['efficiency_score']:.1f}%") 
            print(f"  • Время: {execution_time:.2f}с")
            
            results['custom_tasks'] = task_result
        else:
            print("❌ Не указаны задачи. Используйте --tasks \"task1,task2,task3\"")
    
    if args.full_report or args.demo:
        print("📈 ПОЛНЫЙ ОТЧЕТ КОРПОРАЦИИ")
        print("=" * 50)
        
        analysis = corporation.run_corporate_analysis()
        
        # Общая статистика
        print("📊 ОБЩАЯ СТАТИСТИКА:")
        print(f"  • Всего агентов: {analysis['total_agents']}")
        print(f"  • Операционная эффективность: {analysis['operational_efficiency']}%")
        print(f"  • Средний опыт агентов: {analysis['performance_metrics']['average_experience']:.1f}")
        print(f"  • Общее количество навыков: {analysis['performance_metrics']['total_skills']}")
        print(f"  • Активность обучения: {analysis['performance_metrics']['learning_activity']}")
        
        # Пробелы в навыках
        skill_gaps = analysis['skill_gaps']
        critical_gaps = [gap for gap in skill_gaps if gap['priority'] >= 0.8]
        
        print(f"\n⚠️ КРИТИЧЕСКИЕ ПРОБЕЛЫ В НАВЫКАХ: {len(critical_gaps)}")
        for gap in critical_gaps[:5]:  # Топ-5
            print(f"  • {gap['skill']:<25} | Приоритет: {gap['priority']:.1%} | Тип агента: {gap['recommended_agent_type']}")
        
        # Области для улучшения
        print("\n💡 РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ:")
        for improvement in analysis['areas_for_improvement']:
            print(f"  • {improvement}")
        
        print()
        results['full_report'] = analysis
    
    # Сохранение результатов
    if args.output and results:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"💾 Результаты сохранены в {args.output}")
    
    print("\n👔 Управление корпорацией завершено!")

if __name__ == "__main__":
    main() 