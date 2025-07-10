# ⚡ Быстрый Старт - 5 Минут до Работы

## 🚀 Супер Быстрая Настройка

### 1. Подготовка (1 минута)
```bash
# Создать папку и перейти в неё
mkdir telegram_parser && cd telegram_parser

# Скачать все файлы проекта (или склонировать с GitHub)
```

### 2. Установка (2 минуты)
```bash
# Создать виртуальное окружение
python -m venv env

# Активировать (macOS/Linux)
source env/bin/activate
# Или для Windows: env\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

### 3. Настройка API (1 минута)
```bash
# Создать файл .env
touch .env
```

Добавить в `.env`:
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

**Где взять API ключи:**
1. Идти на https://my.telegram.org/apps
2. Войти в аккаунт Telegram
3. Создать новое приложение
4. Скопировать API ID и API Hash

### 4. Запуск (1 минута)
```bash
python telegram_parser_mvp.py
```

**Готово!** Открыть http://localhost:8000

---

## 🎯 Первое Использование

### Шаг 1: Авторизация
1. Открыть веб-интерфейс
2. Ввести номер телефона
3. Ввести код из SMS
4. Готово к парсингу!

### Шаг 2: Первый Парсинг
1. Ввести имя канала (например: `@durov`)
2. Выбрать количество сообщений (100-1000)
3. Нажать "Начать парсинг"
4. Дождаться результатов

### Шаг 3: Анализ Результатов
- Статистика по активности
- Топ ключевых слов
- Анализ тональности
- Экспорт в Excel/JSON

---

## 🔧 Для Команды

### GitHub Настройка
```bash
# Создать репозиторий
git init
git add .
git commit -m "Initial setup"

# Подключить к GitHub
git remote add origin https://github.com/YOUR_USERNAME/telegram-parser.git
git push -u origin main
```

### Командная Работа
```bash
# Каждый участник команды:
git clone https://github.com/YOUR_USERNAME/telegram-parser.git
cd telegram-parser
python -m venv env
source env/bin/activate  # или env\Scripts\activate
pip install -r requirements.txt
python telegram_parser_mvp.py
```

---

## 🆘 Если Что-то Не Работает

### Проблема: Ошибка установки
```bash
# Обновить pip
pip install --upgrade pip

# Переустановить зависимости
pip install -r requirements.txt --force-reinstall
```

### Проблема: Не запускается
```bash
# Проверить Python версию (нужна 3.8+)
python --version

# Проверить активацию окружения
which python  # должен показать путь к env/bin/python
```

### Проблема: Telegram API
- Проверить правильность API ID и Hash
- Убедиться, что файл `.env` в корне проекта
- Проверить интернет соединение

---

## 📞 Помощь
- Полная документация: `README.md`
- Подробное руководство: `DEPLOYMENT_GUIDE.md`
- Техническая информация: `TELEGRAM_PARSER_MVP_ANALYSIS.md` 