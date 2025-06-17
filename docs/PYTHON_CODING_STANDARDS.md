# 🐍 СТАНДАРТЫ PYTHON КОДИРОВАНИЯ

## 🎯 **ОСНОВНЫЕ ПРИНЦИПЫ:**

### 🔥 **КАЧЕСТВО КОДА:**
- **Простые имена** без спецсимволов и пробелов
- **Подробные логи** каждой операции
- **Обработка ошибок** в каждой функции
- **Автоматические тесты** основного функционала

### ⚡ **СКОРОСТЬ РАЗРАБОТКИ:**
- **Готовые шаблоны** для типовых задач
- **Переиспользуемые функции** в отдельных модулях
- **Минимум зависимостей** - только необходимые пакеты
- **Максимум автоматизации** рутинных задач

## 📋 **ОБЯЗАТЕЛЬНАЯ СТРУКТУРА СКРИПТА:**

```python
#!/usr/bin/env python3
"""
📄 НАЗВАНИЕ СКРИПТА
🎯 Краткое описание что делает
📅 Дата создания: 2024
🔧 Автор: AI Assistant
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# 📊 НАСТРОЙКА ЛОГИРОВАНИЯ
def setup_logging():
    """Настройка детального логирования"""
    log_format = "%(asctime)s | %(levelname)s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f"logs/{Path(__file__).stem}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

# 🛠️ ГЛАВНАЯ ФУНКЦИЯ
def main():
    """Основная логика программы"""
    logger = setup_logging()
    
    try:
        logger.info("🚀 Запуск программы")
        
        # Проверка системных требований
        check_requirements()
        
        # Основная логика
        result = process_main_task()
        
        # Вывод результатов
        display_results(result)
        
        logger.info("✅ Программа завершена успешно")
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 🔧 **ОБЯЗАТЕЛЬНЫЕ ФУНКЦИИ:**

### 📊 **ПРОВЕРКА СИСТЕМЫ:**
```python
def check_requirements():
    """Проверка всех системных требований"""
    logger = logging.getLogger(__name__)
    
    # Проверка Python версии
    if sys.version_info < (3, 8):
        raise Exception("Нужен Python 3.8+")
    
    # Проверка свободного места
    free_space = get_free_disk_space()
    if free_space < 1024:  # 1GB
        logger.warning(f"⚠️ Мало места: {free_space}MB")
    
    # Проверка пакетов
    required_packages = ["requests", "pathlib"]
    check_packages(required_packages)
    
    logger.info("✅ Системные требования проверены")

def get_free_disk_space():
    """Получить свободное место на диске в MB"""
    statvfs = os.statvfs('.')
    return (statvfs.f_frsize * statvfs.f_bavail) // (1024 * 1024)
```

### 📈 **СТАТИСТИКА И ПРОГРЕСС:**
```python
def track_progress(current, total, operation_name="Обработка"):
    """Отслеживание прогресса операций"""
    percent = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f'\r{operation_name}: |{bar}| {percent:.1f}% ({current}/{total})', end='')
    
    if current == total:
        print()  # Новая строка после завершения

def collect_statistics(results):
    """Сбор и отображение статистики"""
    stats = {
        'total_processed': len(results),
        'successful': sum(1 for r in results if r['success']),
        'failed': sum(1 for r in results if not r['success']),
        'total_time': sum(r['processing_time'] for r in results),
        'average_time': sum(r['processing_time'] for r in results) / len(results)
    }
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"✅ Обработано: {stats['successful']}/{stats['total_processed']}")
    print(f"❌ Ошибок: {stats['failed']}")
    print(f"⏱️ Общее время: {stats['total_time']:.2f} сек")
    print(f"📈 Среднее время: {stats['average_time']:.2f} сек")
    
    return stats
```

### 🗂️ **РАБОТА С ФАЙЛАМИ:**
```python
def safe_file_operation(filepath, operation_func, *args, **kwargs):
    """Безопасная операция с файлом с обработкой ошибок"""
    logger = logging.getLogger(__name__)
    
    try:
        # Проверка существования файла
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        # Выполнение операции
        result = operation_func(filepath, *args, **kwargs)
        logger.info(f"✅ Операция выполнена: {filepath}")
        return result
        
    except PermissionError:
        logger.error(f"❌ Нет прав доступа: {filepath}")
        return None
    except Exception as e:
        logger.error(f"❌ Ошибка операции с файлом {filepath}: {str(e)}")
        return None

def clean_filename(filename):
    """Очистка имени файла от недопустимых символов"""
    import re
    # Удаляем недопустимые символы
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Удаляем множественные подчеркивания
    cleaned = re.sub(r'_{2,}', '_', cleaned)
    return cleaned.strip('_')
```

## 🚀 **ГОТОВЫЕ ШАБЛОНЫ:**

### 🎬 **ДЛЯ МЕДИА ОБРАБОТКИ:**
```python
def process_media_batch(input_dir, output_dir, process_func):
    """Шаблон для batch обработки медиа файлов"""
    logger = logging.getLogger(__name__)
    
    # Поиск файлов
    media_files = find_media_files(input_dir)
    total_files = len(media_files)
    
    if total_files == 0:
        logger.warning("⚠️ Медиа файлы не найдены")
        return []
    
    logger.info(f"📁 Найдено файлов: {total_files}")
    
    # Создание выходной папки
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for i, filepath in enumerate(media_files, 1):
        start_time = time.time()
        
        try:
            # Обработка файла
            result = process_func(filepath, output_dir)
            processing_time = time.time() - start_time
            
            results.append({
                'file': filepath,
                'success': True,
                'processing_time': processing_time,
                'output': result
            })
            
            # Обновление прогресса
            track_progress(i, total_files, "Обработка медиа")
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки {filepath}: {str(e)}")
            results.append({
                'file': filepath,
                'success': False,
                'processing_time': time.time() - start_time,
                'error': str(e)
            })
    
    # Статистика
    stats = collect_statistics(results)
    return results, stats
```

### 🤖 **ДЛЯ AI ОБРАБОТКИ:**
```python
def ai_processing_pipeline(input_data, model_config):
    """Шаблон для AI обработки с проверками"""
    logger = logging.getLogger(__name__)
    
    # Проверка входных данных
    if not validate_input_data(input_data):
        raise ValueError("Неверные входные данные")
    
    # Инициализация модели
    model = initialize_model(model_config)
    
    # Предобработка
    preprocessed_data = preprocess_data(input_data)
    
    # AI обработка
    logger.info("🤖 Запуск AI обработки...")
    results = model.process(preprocessed_data)
    
    # Постобработка
    final_results = postprocess_results(results)
    
    logger.info("✅ AI обработка завершена")
    return final_results
```

## 📦 **СТАНДАРТНЫЙ requirements.txt:**

```txt
# 🐍 ОСНОВНЫЕ ПАКЕТЫ
requests>=2.28.0
pathlib2>=2.3.0
pillow>=9.0.0

# 📊 ДАННЫЕ И АНАЛИЗ  
pandas>=1.5.0
numpy>=1.21.0

# 🎬 МЕДИА ОБРАБОТКА
moviepy>=1.0.3
opencv-python>=4.6.0

# 🔧 УТИЛИТЫ
tqdm>=4.64.0
colorama>=0.4.5
```

## 🎯 **ЧЕКЛИСТ ГОТОВОГО СКРИПТА:**

### ✅ **ОБЯЗАТЕЛЬНЫЕ ЭЛЕМЕНТЫ:**
- [ ] Подробный docstring с описанием
- [ ] Настройка логирования в файл и консоль
- [ ] Проверка системных требований
- [ ] Обработка всех исключений
- [ ] Отслеживание прогресса операций
- [ ] Сбор и вывод статистики
- [ ] Простые имена файлов без спецсимволов
- [ ] Создание необходимых папок
- [ ] Финальный отчет о результатах

### 🚀 **ДОПОЛНИТЕЛЬНЫЕ ПЛЮСЫ:**
- [ ] Параллельная обработка где возможно
- [ ] Автоматическое резервное копирование
- [ ] Конфигурационный файл для настроек
- [ ] Командная строка с аргументами
- [ ] Интеграция с системными уведомлениями 