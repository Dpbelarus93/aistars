# 🚀 Quick Video Pipeline - Быстрый Старт

Автоматический пайплайн для создания высококачественных видео из AI-сгенерированных изображений с интеграцией DaVinci Resolve.

## 📋 Что у нас есть

- ✅ **96 обработанных кадров** в папке `upscaled_images/`
- ✅ **Python скрипты** для автоматизации
- ✅ **DaVinci Resolve интеграция** 
- ✅ **Альтернативный FFmpeg** путь

## 🚀 Быстрый запуск (3 команды)

### 1. Установка зависимостей
```bash
cd "Python код"
pip install -r requirements.txt
```

### 2. Запуск полного пайплайна
```bash
python quick_video_pipeline.py
```

### 3. Готово! 🎉
Видео будет создано автоматически через DaVinci Resolve или FFmpeg.

## 🎬 Опции запуска

### Только DaVinci Resolve
```bash
python "Python код/davinci_auto_import.py"
```

### Только настройка окружения DaVinci
```bash
python "Python код/setup_davinci_env.py"
```

### FFmpeg альтернатива (если DaVinci недоступен)
```bash
ffmpeg -framerate 24 -i "upscaled_images/upscaled_%05d_.png" -c:v libx264 -pix_fmt yuv420p -crf 18 "final_video/output.mp4"
```

## 📁 Структура файлов

```
📁 upscaled_images/          # 96 готовых кадров
   ├── upscaled__00002_.png
   ├── upscaled__00003_.png
   └── ... (до 00096_.png)

📁 Python код/               # Все скрипты
   ├── davinci_auto_import.py      # Главный DaVinci скрипт
   ├── setup_davinci_env.py       # Настройка окружения
   └── requirements.txt            # Зависимости

📁 final_video/              # Результат (создается автоматически)
   └── ai_generated_video.mp4     # Готовое видео

📄 quick_video_pipeline.py   # 🚀 ГЛАВНЫЙ СКРИПТ
```

## ⚙️ Требования

### Для DaVinci Resolve
- DaVinci Resolve установлен и запущен
- Python 3.6+ (у вас 3.12.0 ✅)

### Для FFmpeg альтернативы
- FFmpeg установлен в системе

## 🎯 Что происходит автоматически

1. **Проверка** - Скрипт находит ваши 96 обработанных изображений
2. **DaVinci подключение** - Автоматическая настройка API
3. **Импорт** - Изображения импортируются как последовательность 
4. **Timeline** - Создается timeline с именем "AI_Generated_Scene"
5. **Настройки** - 24 FPS, высокое качество
6. **Экспорт** - Опциональный автоматический рендер

## 🔧 Если что-то не работает

### DaVinci Resolve не подключается
```bash
# Убедитесь что DaVinci запущен, затем:
python "Python код/setup_davinci_env.py"
```

### Нет FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian  
sudo apt install ffmpeg

# Windows
# Скачайте с https://ffmpeg.org/download.html
```

### Python ошибки
```bash
cd "Python код"
pip install --upgrade -r requirements.txt
```

## 🎬 Результат

- **Входные данные**: 96 PNG изображений (1-2MB каждое)
- **Выходные данные**: MP4 видео 24 FPS, ~4 секунды
- **Качество**: Высокое (настраиваемое)
- **Время обработки**: 1-2 минуты

## 💡 Продвинутые настройки

### Изменить FPS
В `davinci_auto_import.py` найдите:
```python
fps=24  # Измените на нужное значение
```

### Изменить качество FFmpeg
В `quick_video_pipeline.py` найдите:
```python
"-crf", "18"  # Уменьшите для лучшего качества (15-18)
```

### Настроить DaVinci рендер
В `davinci_auto_import.py` в функции `export_timeline()` настройте `render_settings`

---

## 🚀 TL;DR - Самый быстрый способ

```bash
python quick_video_pipeline.py
```

Всё остальное произойдет автоматически! 🎉 