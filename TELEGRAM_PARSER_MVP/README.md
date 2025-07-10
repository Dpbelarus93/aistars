# 🕉️ Telegram Parser MVP

> *"सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः। सर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्॥"*
> 
> *"Пусть все будут счастливы, пусть все будут здоровы. Пусть все видят благополучие, пусть никто не страдает."*

Универсальный парсер для Telegram каналов и групп с ИИ-анализом, веб-интерфейсом и соблюдением этических принципов.

## ✨ Особенности

### 🚀 Технические возможности
- **Гибридная архитектура** - автоматическое переключение между Pyrogram и Telethon
- **ИИ-анализ** - тональность, ключевые слова, определение языка
- **Веб-дашборд** - современный интерфейс для управления
- **REST API** - интеграция с внешними системами
- **Экспорт данных** - JSON, CSV, Excel форматы
- **Анонимизация** - автоматическая защита персональных данных

### 🛡️ Безопасность и соответствие
- **GDPR/CCPA** - соответствие требованиям защиты данных
- **Этичный парсинг** - только публичные данные
- **Rate limiting** - защита от блокировок
- **Шифрование** - безопасное хранение данных

### 📊 Аналитика
- **Статистика в реальном времени** - мониторинг процесса
- **Визуализация данных** - графики и диаграммы
- **Трендовый анализ** - выявление популярных тем
- **Отчеты** - детальная аналитика

## 🚀 Быстрый старт

### 1. Установка

```bash
# Клонирование репозитория
git clone https://github.com/your-username/telegram-parser-mvp.git
cd telegram-parser-mvp

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка Telegram API

1. Перейдите на [my.telegram.org](https://my.telegram.org)
2. Войдите с помощью номера телефона
3. Создайте новое приложение в разделе "API Development Tools"
4. Получите `api_id` и `api_hash`

### 3. Конфигурация

Создайте файл `config.json`:

```json
{
  "telegram": {
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH",
    "phone_number": "+1234567890",
    "session_name": "parser_session"
  },
  "database": {
    "path": "telegram_data.db"
  },
  "parsing": {
    "rate_limit": 1.0,
    "max_retries": 3,
    "timeout": 30
  },
  "ai": {
    "sentiment_analysis": true,
    "keyword_extraction": true,
    "language_detection": true
  },
  "privacy": {
    "anonymize_users": true,
    "exclude_private_data": true,
    "hash_user_ids": true
  }
}
```

### 4. Запуск

#### Веб-интерфейс (рекомендуется)
```bash
python telegram_parser_mvp.py
```
Откройте http://localhost:8000 в браузере

#### CLI режим
```bash
# Если FastAPI не установлен
pip uninstall fastapi uvicorn
python telegram_parser_mvp.py
```

## 📖 Использование

### 🌐 Веб-интерфейс

1. **Главная страница** - обзор статистики и активных задач
2. **Новая задача** - настройка параметров парсинга
3. **Результаты** - просмотр и экспорт данных
4. **Аналитика** - визуализация и инсайты

#### Создание задачи парсинга:

1. Укажите канал: `@channel_name` или `https://t.me/channel_name`
2. Настройте параметры:
   - Максимум сообщений (1-10000)
   - Период времени (дни назад)
   - Ключевые слова для фильтрации
   - Слова для исключения
3. Выберите типы анализа:
   - ✅ Анализ тональности
   - ✅ Извлечение ключевых слов
   - ✅ Определение языка
4. Запустите парсинг

### 🖥️ CLI режим

```bash
python telegram_parser_mvp.py
```

Интерактивный ввод параметров:
- Канал или группа
- Количество сообщений
- Период времени
- Ключевые слова

### 📡 API

#### Запуск парсинга
```bash
curl -X POST "http://localhost:8000/api/parse" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "@crypto_news",
    "max_messages": 1000,
    "days_back": 7,
    "keywords": ["биткоин", "криптовалюта"],
    "analyze_sentiment": true
  }'
```

#### Получение статистики
```bash
curl "http://localhost:8000/api/stats"
```

#### Экспорт данных
```bash
curl "http://localhost:8000/api/export?format=json"
```

## 🎯 Примеры использования

### 1. Анализ криптовалютных каналов

```python
from telegram_parser_mvp import TelegramParserMVP, ParseConfig

parser = TelegramParserMVP()
await parser.initialize_clients()

config = ParseConfig(
    target="@crypto_news",
    max_messages=5000,
    days_back=30,
    keywords=["биткоин", "эфириум", "NFT", "DeFi"],
    exclude_keywords=["реклама", "спам"],
    analyze_sentiment=True,
    extract_keywords=True
)

result = await parser.parse_channel(config)
print(f"Обработано {result['messages_parsed']} сообщений")

# Экспорт данных
parser.export_data("json", "crypto_analysis.json")
```

### 2. Мониторинг новостных каналов

```python
config = ParseConfig(
    target="@news_channel",
    max_messages=2000,
    days_back=7,
    keywords=["политика", "экономика", "технологии"],
    analyze_sentiment=True
)

result = await parser.parse_channel(config)
stats = parser.get_statistics()

print(f"Тональность сообщений: {stats['sentiment']}")
print(f"Популярные темы: {stats['languages']}")
```

### 3. Исследование сообществ

```python
config = ParseConfig(
    target="@community_group",
    max_messages=1000,
    days_back=14,
    min_message_length=50,
    extract_keywords=True,
    analyze_sentiment=True
)

result = await parser.parse_channel(config)

# Анализ результатов
for msg in result['messages_sample']:
    print(f"Сообщение: {msg['text'][:100]}...")
    print(f"Тональность: {msg['sentiment']}")
    print(f"Ключевые слова: {msg['keywords']}")
    print("---")
```

## 🔧 Конфигурация

### Основные параметры

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `rate_limit` | Задержка между запросами (сек) | 1.0 |
| `max_retries` | Максимум попыток при ошибке | 3 |
| `timeout` | Таймаут запроса (сек) | 30 |
| `anonymize_users` | Анонимизация пользователей | true |
| `hash_user_ids` | Хэширование ID пользователей | true |

### ИИ-анализ

| Параметр | Описание | Библиотека |
|----------|----------|------------|
| `sentiment_analysis` | Анализ тональности | TextBlob |
| `keyword_extraction` | Извлечение ключевых слов | NLTK |
| `language_detection` | Определение языка | TextBlob |

### Фильтрация

| Параметр | Описание | Тип |
|----------|----------|-----|
| `keywords` | Ключевые слова (ИЛИ) | List[str] |
| `exclude_keywords` | Исключающие слова | List[str] |
| `min_message_length` | Минимальная длина | int |
| `include_media` | Включать медиа | bool |

## 📊 База данных

### Структура таблиц

#### messages
- `id` - уникальный ID
- `message_id` - ID сообщения в Telegram
- `text` - текст сообщения
- `date` - дата создания
- `author` - автор (анонимизирован)
- `author_id_hash` - хэш ID автора
- `channel_id` - ID канала
- `channel_name` - имя канала
- `sentiment` - тональность
- `keywords` - ключевые слова (JSON)
- `language` - язык сообщения

#### channels
- `channel_id` - ID канала
- `channel_name` - имя канала
- `title` - заголовок
- `description` - описание
- `members_count` - количество участников
- `type` - тип канала

#### parsing_stats
- `session_id` - ID сессии
- `channel_name` - имя канала
- `messages_parsed` - обработано сообщений
- `errors_count` - количество ошибок
- `start_time` / `end_time` - время начала/окончания

## 🚨 Важные замечания

### ⚖️ Правовые аспекты

1. **Только публичные данные** - парсинг только открытых каналов и групп
2. **Соблюдение ToS** - следование правилам Telegram
3. **Анонимизация** - защита персональных данных
4. **Rate limiting** - предотвращение блокировок

### 🛡️ Этические принципы

1. **Прозрачность** - четкое объяснение целей
2. **Минимизация** - сбор только необходимых данных
3. **Безопасность** - защищенное хранение
4. **Уважение** - соблюдение приватности

### 🔐 Безопасность

1. **Не делитесь** `api_id` и `api_hash`
2. **Используйте** виртуальные окружения
3. **Регулярно обновляйте** зависимости
4. **Мониторьте** логи на предмет ошибок

## 🐛 Устранение неполадок

### Частые проблемы

#### 1. Ошибка авторизации
```
pyrogram.errors.exceptions.unauthorized_401.AuthKeyUnregistered
```
**Решение:** Удалите файл сессии и повторите авторизацию

#### 2. Ошибка FloodWait
```
pyrogram.errors.exceptions.flood_420.FloodWait
```
**Решение:** Увеличьте `rate_limit` в конфигурации

#### 3. Канал не найден
```
pyrogram.errors.exceptions.bad_request_400.UsernameNotOccupied
```
**Решение:** Проверьте правильность имени канала

#### 4. Нет доступа к каналу
```
pyrogram.errors.exceptions.forbidden_403.ChatWriteForbidden
```
**Решение:** Убедитесь, что канал публичный или вы являетесь участником

### Логирование

Логи сохраняются в файл `telegram_parser.log`:

```bash
# Просмотр последних логов
tail -f telegram_parser.log

# Поиск ошибок
grep ERROR telegram_parser.log
```

### Отладка

Включите детальное логирование:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📈 Производительность

### Оптимизация

1. **Используйте SSD** для базы данных
2. **Настройте rate_limit** под ваши нужды
3. **Ограничьте max_messages** для больших каналов
4. **Используйте фильтры** для уменьшения объема данных

### Мониторинг

```python
# Получение статистики производительности
stats = parser.get_statistics()
print(f"Скорость парсинга: {stats['parsing_stats']['parsed_messages']} сообщений")
print(f"Ошибки: {stats['parsing_stats']['errors']}")
```

## 🤝 Участие в разработке

### Структура проекта

```
telegram_parser_mvp/
├── telegram_parser_mvp.py      # Основной код
├── config.json                 # Конфигурация
├── requirements.txt            # Зависимости
├── README.md                   # Документация
├── tests/                      # Тесты
├── docs/                       # Дополнительная документация
└── examples/                   # Примеры использования
```

### Разработка

```bash
# Установка dev зависимостей
pip install -r requirements-dev.txt

# Форматирование кода
black telegram_parser_mvp.py
isort telegram_parser_mvp.py

# Проверка стиля
flake8 telegram_parser_mvp.py

# Запуск тестов
pytest tests/
```

### Создание Pull Request

1. Форкните репозиторий
2. Создайте ветку для функции: `git checkout -b feature/new-feature`
3. Зафиксируйте изменения: `git commit -am 'Add new feature'`
4. Отправьте в ветку: `git push origin feature/new-feature`
5. Создайте Pull Request

## 📜 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🙏 Благодарности

- **Telegram** - за открытое API
- **Pyrogram** и **Telethon** - за отличные библиотеки
- **FastAPI** - за современный веб-фреймворк
- **Сообщество разработчиков** - за вклад и поддержку

## 📞 Поддержка

- **GitHub Issues** - для багов и предложений
- **Telegram** - @your_telegram для вопросов
- **Email** - your.email@example.com
- **Discord** - ссылка на сервер сообщества

---

*Создано с мудростью Вед и современными технологиями* 🕉️

**Помните:** Используйте этот инструмент ответственно и этично. Уважайте приватность пользователей и соблюдайте законы вашей юрисдикции.
