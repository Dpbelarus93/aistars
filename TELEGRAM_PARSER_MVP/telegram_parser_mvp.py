#!/usr/bin/env python3
"""
🕉️ Telegram Parser MVP - Универсальный парсер для Telegram
Создан с мудростью Вед и современными технологиями

Автор: НейроКодер
Версия: 1.0.0
"""

import asyncio
import json
import logging
import os
import re
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import aiohttp
from urllib.parse import urlparse

# Telegram клиенты
try:
    from pyrogram import Client, filters
    from pyrogram.types import Message, Chat, User
    from pyrogram.errors import FloodWait, UserDeactivated, UserDeactivatedBan
    PYROGRAM_AVAILABLE = True
except ImportError:
    PYROGRAM_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    from telethon.tl.types import Channel, Chat as TelethonChat, User as TelethonUser
    from telethon.errors import FloodWaitError, UserDeactivatedError
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

# ИИ и анализ данных
try:
    from textblob import TextBlob
    import nltk
    from collections import Counter
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Веб-фреймворк
try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_parser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ParsedMessage:
    """Структура распарсенного сообщения"""
    id: int
    text: str
    date: datetime
    author: str
    author_id: int
    channel_id: int
    channel_name: str
    message_type: str
    media_type: Optional[str] = None
    media_url: Optional[str] = None
    reply_to: Optional[int] = None
    views: Optional[int] = None
    forwards: Optional[int] = None
    sentiment: Optional[str] = None
    keywords: Optional[List[str]] = None
    language: Optional[str] = None

@dataclass
class ParseConfig:
    """Конфигурация парсинга"""
    target: str  # Канал или группа
    max_messages: int = 1000
    days_back: int = 7
    keywords: List[str] = None
    exclude_keywords: List[str] = None
    include_media: bool = True
    analyze_sentiment: bool = True
    extract_keywords: bool = True
    min_message_length: int = 10
    rate_limit_delay: float = 1.0

class TelegramParserMVP:
    """
    🕉️ Основной класс парсера Telegram
    
    Объединяет мудрость древних писаний с современными технологиями
    для этичного и эффективного анализа публичных данных.
    """
    
    def __init__(self, config_file: str = "config.json"):
        """Инициализация парсера"""
        self.config = self._load_config(config_file)
        self.db_path = "telegram_data.db"
        self.pyrogram_client = None
        self.telethon_client = None
        self.current_engine = None
        self.stats = {
            'parsed_messages': 0,
            'errors': 0,
            'start_time': None,
            'channels_processed': 0
        }
        
        # Инициализация базы данных
        self._init_database()
        
        logger.info("🕉️ Telegram Parser MVP инициализирован")
    
    def _load_config(self, config_file: str) -> Dict:
        """Загрузка конфигурации"""
        default_config = {
            "telegram": {
                "api_id": "",
                "api_hash": "",
                "phone_number": "",
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
                "sentiment_analysis": True,
                "keyword_extraction": True,
                "language_detection": True
            },
            "privacy": {
                "anonymize_users": True,
                "exclude_private_data": True,
                "hash_user_ids": True
            }
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.error(f"Ошибка загрузки конфигурации: {e}")
        else:
            # Создаем файл конфигурации по умолчанию
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            logger.info(f"Создан файл конфигурации: {config_file}")
        
        return default_config
    
    def _init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Таблица сообщений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                message_id INTEGER,
                text TEXT,
                date TIMESTAMP,
                author TEXT,
                author_id_hash TEXT,
                channel_id INTEGER,
                channel_name TEXT,
                message_type TEXT,
                media_type TEXT,
                media_url TEXT,
                reply_to INTEGER,
                views INTEGER,
                forwards INTEGER,
                sentiment TEXT,
                keywords TEXT,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица каналов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY,
                channel_id INTEGER UNIQUE,
                channel_name TEXT,
                title TEXT,
                description TEXT,
                members_count INTEGER,
                type TEXT,
                is_verified BOOLEAN,
                is_scam BOOLEAN,
                is_fake BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица статистики
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parsing_stats (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                channel_name TEXT,
                messages_parsed INTEGER,
                errors_count INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                config TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("База данных инициализирована")
    
    async def _init_pyrogram_client(self):
        """Инициализация Pyrogram клиента"""
        if not PYROGRAM_AVAILABLE:
            logger.error("Pyrogram не установлен")
            return False
        
        try:
            self.pyrogram_client = Client(
                self.config['telegram']['session_name'],
                api_id=self.config['telegram']['api_id'],
                api_hash=self.config['telegram']['api_hash'],
                phone_number=self.config['telegram']['phone_number']
            )
            await self.pyrogram_client.start()
            logger.info("✅ Pyrogram клиент инициализирован")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации Pyrogram: {e}")
            return False
    
    async def _init_telethon_client(self):
        """Инициализация Telethon клиента"""
        if not TELETHON_AVAILABLE:
            logger.error("Telethon не установлен")
            return False
        
        try:
            self.telethon_client = TelegramClient(
                self.config['telegram']['session_name'] + '_telethon',
                self.config['telegram']['api_id'],
                self.config['telegram']['api_hash']
            )
            await self.telethon_client.start(phone=self.config['telegram']['phone_number'])
            logger.info("✅ Telethon клиент инициализирован")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации Telethon: {e}")
            return False
    
    async def initialize_clients(self):
        """Инициализация клиентов с fallback"""
        # Попытка инициализации Pyrogram (предпочтительный)
        if await self._init_pyrogram_client():
            self.current_engine = "pyrogram"
            return True
        
        # Fallback на Telethon
        if await self._init_telethon_client():
            self.current_engine = "telethon"
            return True
        
        logger.error("❌ Не удалось инициализировать ни один клиент")
        return False
    
    def _anonymize_user_data(self, user_id: int, username: str) -> Dict:
        """Анонимизация пользовательских данных"""
        if not self.config['privacy']['anonymize_users']:
            return {'id': user_id, 'username': username}
        
        # Хэширование ID пользователя
        user_id_hash = hashlib.sha256(str(user_id).encode()).hexdigest()[:16]
        
        # Анонимизация username
        if username and self.config['privacy']['hash_user_ids']:
            username = f"user_{user_id_hash}"
        
        return {
            'id_hash': user_id_hash,
            'username': username if username else f"user_{user_id_hash}"
        }
    
    def _analyze_sentiment(self, text: str) -> Optional[str]:
        """Анализ тональности текста"""
        if not AI_AVAILABLE or not self.config['ai']['sentiment_analysis']:
            return None
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return "positive"
            elif polarity < -0.1:
                return "negative"
            else:
                return "neutral"
        except Exception as e:
            logger.warning(f"Ошибка анализа тональности: {e}")
            return None
    
    def _extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Извлечение ключевых слов"""
        if not AI_AVAILABLE or not self.config['ai']['keyword_extraction']:
            return []
        
        try:
            # Простое извлечение ключевых слов
            words = re.findall(r'\b[а-яё]{3,}\b', text.lower())
            word_freq = Counter(words)
            return [word for word, _ in word_freq.most_common(top_n)]
        except Exception as e:
            logger.warning(f"Ошибка извлечения ключевых слов: {e}")
            return []
    
    def _detect_language(self, text: str) -> Optional[str]:
        """Определение языка текста"""
        if not AI_AVAILABLE or not self.config['ai']['language_detection']:
            return None
        
        try:
            blob = TextBlob(text)
            return blob.detect_language()
        except Exception as e:
            logger.warning(f"Ошибка определения языка: {e}")
            return None
    
    def _filter_message(self, text: str, config: ParseConfig) -> bool:
        """Фильтрация сообщений по критериям"""
        # Проверка минимальной длины
        if len(text) < config.min_message_length:
            return False
        
        # Проверка ключевых слов
        if config.keywords:
            text_lower = text.lower()
            if not any(keyword.lower() in text_lower for keyword in config.keywords):
                return False
        
        # Проверка исключающих слов
        if config.exclude_keywords:
            text_lower = text.lower()
            if any(keyword.lower() in text_lower for keyword in config.exclude_keywords):
                return False
        
        return True
    
    async def _parse_with_pyrogram(self, config: ParseConfig) -> List[ParsedMessage]:
        """Парсинг с использованием Pyrogram"""
        messages = []
        
        try:
            # Получение информации о канале
            chat = await self.pyrogram_client.get_chat(config.target)
            
            # Сохранение информации о канале
            await self._save_channel_info(chat)
            
            # Вычисление даты начала
            start_date = datetime.now() - timedelta(days=config.days_back)
            
            # Получение сообщений
            async for message in self.pyrogram_client.get_chat_history(
                config.target, 
                limit=config.max_messages
            ):
                if message.date < start_date:
                    break
                
                if not message.text:
                    continue
                
                # Фильтрация сообщений
                if not self._filter_message(message.text, config):
                    continue
                
                # Анонимизация данных пользователя
                user_data = self._anonymize_user_data(
                    message.from_user.id if message.from_user else 0,
                    message.from_user.username if message.from_user else "unknown"
                )
                
                # Анализ текста
                sentiment = self._analyze_sentiment(message.text) if config.analyze_sentiment else None
                keywords = self._extract_keywords(message.text) if config.extract_keywords else []
                language = self._detect_language(message.text)
                
                # Создание объекта сообщения
                parsed_msg = ParsedMessage(
                    id=message.id,
                    text=message.text,
                    date=message.date,
                    author=user_data['username'],
                    author_id=user_data.get('id_hash', user_data.get('id', 0)),
                    channel_id=chat.id,
                    channel_name=chat.username or chat.title,
                    message_type="text",
                    media_type=message.media.value if message.media else None,
                    views=message.views,
                    sentiment=sentiment,
                    keywords=keywords,
                    language=language
                )
                
                messages.append(parsed_msg)
                self.stats['parsed_messages'] += 1
                
                # Rate limiting
                await asyncio.sleep(config.rate_limit_delay)
                
                if len(messages) % 100 == 0:
                    logger.info(f"Обработано {len(messages)} сообщений")
        
        except Exception as e:
            logger.error(f"Ошибка парсинга с Pyrogram: {e}")
            self.stats['errors'] += 1
        
        return messages
    
    async def _parse_with_telethon(self, config: ParseConfig) -> List[ParsedMessage]:
        """Парсинг с использованием Telethon"""
        messages = []
        
        try:
            # Получение информации о канале
            entity = await self.telethon_client.get_entity(config.target)
            
            # Вычисление даты начала
            start_date = datetime.now() - timedelta(days=config.days_back)
            
            # Получение сообщений
            async for message in self.telethon_client.iter_messages(
                entity,
                limit=config.max_messages
            ):
                if message.date < start_date:
                    break
                
                if not message.text:
                    continue
                
                # Фильтрация сообщений
                if not self._filter_message(message.text, config):
                    continue
                
                # Анонимизация данных пользователя
                user_data = self._anonymize_user_data(
                    message.sender_id or 0,
                    getattr(message.sender, 'username', 'unknown') if message.sender else 'unknown'
                )
                
                # Анализ текста
                sentiment = self._analyze_sentiment(message.text) if config.analyze_sentiment else None
                keywords = self._extract_keywords(message.text) if config.extract_keywords else []
                language = self._detect_language(message.text)
                
                # Создание объекта сообщения
                parsed_msg = ParsedMessage(
                    id=message.id,
                    text=message.text,
                    date=message.date,
                    author=user_data['username'],
                    author_id=user_data.get('id_hash', user_data.get('id', 0)),
                    channel_id=entity.id,
                    channel_name=getattr(entity, 'username', None) or getattr(entity, 'title', 'unknown'),
                    message_type="text",
                    media_type=str(type(message.media).__name__) if message.media else None,
                    views=getattr(message, 'views', None),
                    sentiment=sentiment,
                    keywords=keywords,
                    language=language
                )
                
                messages.append(parsed_msg)
                self.stats['parsed_messages'] += 1
                
                # Rate limiting
                await asyncio.sleep(config.rate_limit_delay)
                
                if len(messages) % 100 == 0:
                    logger.info(f"Обработано {len(messages)} сообщений")
        
        except Exception as e:
            logger.error(f"Ошибка парсинга с Telethon: {e}")
            self.stats['errors'] += 1
        
        return messages
    
    async def _save_channel_info(self, chat):
        """Сохранение информации о канале"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO channels 
                (channel_id, channel_name, title, description, members_count, type, is_verified, is_scam, is_fake)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                chat.id,
                getattr(chat, 'username', None),
                getattr(chat, 'title', None),
                getattr(chat, 'description', None),
                getattr(chat, 'members_count', None),
                str(chat.type),
                getattr(chat, 'is_verified', False),
                getattr(chat, 'is_scam', False),
                getattr(chat, 'is_fake', False)
            ))
            conn.commit()
        except Exception as e:
            logger.error(f"Ошибка сохранения информации о канале: {e}")
        finally:
            conn.close()
    
    async def _save_messages(self, messages: List[ParsedMessage]):
        """Сохранение сообщений в базу данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for msg in messages:
                cursor.execute('''
                    INSERT OR REPLACE INTO messages 
                    (message_id, text, date, author, author_id_hash, channel_id, channel_name, 
                     message_type, media_type, media_url, reply_to, views, forwards, 
                     sentiment, keywords, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    msg.id, msg.text, msg.date, msg.author, msg.author_id,
                    msg.channel_id, msg.channel_name, msg.message_type,
                    msg.media_type, msg.media_url, msg.reply_to, msg.views,
                    msg.forwards, msg.sentiment, json.dumps(msg.keywords),
                    msg.language
                ))
            
            conn.commit()
            logger.info(f"Сохранено {len(messages)} сообщений в базу данных")
        
        except Exception as e:
            logger.error(f"Ошибка сохранения сообщений: {e}")
        finally:
            conn.close()
    
    async def parse_channel(self, config: ParseConfig) -> Dict:
        """Основной метод парсинга канала"""
        logger.info(f"🚀 Начинаем парсинг: {config.target}")
        self.stats['start_time'] = datetime.now()
        
        # Инициализация клиентов если не сделано
        if not self.current_engine:
            if not await self.initialize_clients():
                return {"error": "Не удалось инициализировать клиенты"}
        
        messages = []
        
        try:
            # Выбор движка для парсинга
            if self.current_engine == "pyrogram":
                messages = await self._parse_with_pyrogram(config)
            elif self.current_engine == "telethon":
                messages = await self._parse_with_telethon(config)
            else:
                return {"error": "Нет доступных движков для парсинга"}
            
            # Сохранение сообщений
            if messages:
                await self._save_messages(messages)
            
            # Обновление статистики
            self.stats['channels_processed'] += 1
            
            result = {
                "success": True,
                "channel": config.target,
                "messages_parsed": len(messages),
                "engine_used": self.current_engine,
                "stats": self.stats.copy(),
                "messages_sample": [asdict(msg) for msg in messages[:5]]  # Первые 5 сообщений
            }
            
            logger.info(f"✅ Парсинг завершен: {len(messages)} сообщений")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка парсинга: {e}")
            return {"error": str(e)}
    
    def export_data(self, format_type: str = "json", filename: str = None) -> str:
        """Экспорт данных в различных форматах"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"telegram_export_{timestamp}.{format_type}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Получение всех сообщений
            cursor.execute('''
                SELECT * FROM messages 
                ORDER BY date DESC
            ''')
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            if format_type == "json":
                data = [dict(zip(columns, row)) for row in rows]
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            elif format_type == "csv":
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    writer.writerows(rows)
            
            logger.info(f"Данные экспортированы в файл: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Ошибка экспорта данных: {e}")
            return None
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """Получение статистики парсинга"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Общая статистика
            cursor.execute("SELECT COUNT(*) FROM messages")
            total_messages = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT channel_name) FROM messages")
            total_channels = cursor.fetchone()[0]
            
            # Статистика по каналам
            cursor.execute('''
                SELECT channel_name, COUNT(*) as message_count 
                FROM messages 
                GROUP BY channel_name 
                ORDER BY message_count DESC
            ''')
            channels_stats = cursor.fetchall()
            
            # Статистика по тональности
            cursor.execute('''
                SELECT sentiment, COUNT(*) as count 
                FROM messages 
                WHERE sentiment IS NOT NULL 
                GROUP BY sentiment
            ''')
            sentiment_stats = cursor.fetchall()
            
            # Статистика по языкам
            cursor.execute('''
                SELECT language, COUNT(*) as count 
                FROM messages 
                WHERE language IS NOT NULL 
                GROUP BY language 
                ORDER BY count DESC
            ''')
            language_stats = cursor.fetchall()
            
            return {
                "total_messages": total_messages,
                "total_channels": total_channels,
                "channels": dict(channels_stats),
                "sentiment": dict(sentiment_stats),
                "languages": dict(language_stats),
                "parsing_stats": self.stats
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}
        finally:
            conn.close()
    
    async def cleanup(self):
        """Очистка ресурсов"""
        try:
            if self.pyrogram_client:
                await self.pyrogram_client.stop()
            if self.telethon_client:
                await self.telethon_client.disconnect()
            logger.info("🧹 Ресурсы очищены")
        except Exception as e:
            logger.error(f"Ошибка очистки ресурсов: {e}")

# Веб-интерфейс (если доступен FastAPI)
if WEB_AVAILABLE:
    app = FastAPI(title="Telegram Parser MVP", version="1.0.0")
    parser = TelegramParserMVP()
    
    class ParseRequest(BaseModel):
        target: str
        max_messages: int = 1000
        days_back: int = 7
        keywords: Optional[List[str]] = None
        exclude_keywords: Optional[List[str]] = None
        analyze_sentiment: bool = True
        extract_keywords: bool = True
    
    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        """Главная страница дашборда"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🕉️ Telegram Parser MVP</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { background: #2196F3; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .card { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, textarea, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
                button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #45a049; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
                .stat-card { background: #fff; padding: 20px; border-radius: 10px; text-align: center; }
                .stat-number { font-size: 2em; font-weight: bold; color: #2196F3; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🕉️ Telegram Parser MVP</h1>
                    <p>Универсальный парсер для анализа Telegram каналов и групп</p>
                </div>
                
                <div class="card">
                    <h2>📊 Статистика</h2>
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-number" id="total-messages">0</div>
                            <div>Сообщений</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="total-channels">0</div>
                            <div>Каналов</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="parsing-sessions">0</div>
                            <div>Сессий</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🚀 Новая задача парсинга</h2>
                    <form id="parse-form">
                        <div class="form-group">
                            <label for="target">Канал или группа:</label>
                            <input type="text" id="target" name="target" placeholder="@channel_name или https://t.me/channel_name" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="max_messages">Максимум сообщений:</label>
                            <input type="number" id="max_messages" name="max_messages" value="1000" min="1" max="10000">
                        </div>
                        
                        <div class="form-group">
                            <label for="days_back">Дней назад:</label>
                            <input type="number" id="days_back" name="days_back" value="7" min="1" max="365">
                        </div>
                        
                        <div class="form-group">
                            <label for="keywords">Ключевые слова (через запятую):</label>
                            <input type="text" id="keywords" name="keywords" placeholder="биткоин, криптовалюта, блокчейн">
                        </div>
                        
                        <div class="form-group">
                            <label for="exclude_keywords">Исключить слова (через запятую):</label>
                            <input type="text" id="exclude_keywords" name="exclude_keywords" placeholder="реклама, спам">
                        </div>
                        
                        <div class="form-group">
                            <label>
                                <input type="checkbox" id="analyze_sentiment" name="analyze_sentiment" checked>
                                Анализ тональности
                            </label>
                        </div>
                        
                        <div class="form-group">
                            <label>
                                <input type="checkbox" id="extract_keywords" name="extract_keywords" checked>
                                Извлечение ключевых слов
                            </label>
                        </div>
                        
                        <button type="submit">🚀 Запустить парсинг</button>
                    </form>
                </div>
                
                <div class="card">
                    <h2>📈 Результаты</h2>
                    <div id="results"></div>
                </div>
            </div>
            
            <script>
                // Загрузка статистики
                async function loadStats() {
                    try {
                        const response = await fetch('/api/stats');
                        const stats = await response.json();
                        
                        document.getElementById('total-messages').textContent = stats.total_messages || 0;
                        document.getElementById('total-channels').textContent = stats.total_channels || 0;
                        document.getElementById('parsing-sessions').textContent = stats.parsing_stats?.channels_processed || 0;
                    } catch (error) {
                        console.error('Ошибка загрузки статистики:', error);
                    }
                }
                
                // Обработка формы
                document.getElementById('parse-form').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const formData = new FormData(e.target);
                    const data = {
                        target: formData.get('target'),
                        max_messages: parseInt(formData.get('max_messages')),
                        days_back: parseInt(formData.get('days_back')),
                        keywords: formData.get('keywords') ? formData.get('keywords').split(',').map(k => k.trim()) : null,
                        exclude_keywords: formData.get('exclude_keywords') ? formData.get('exclude_keywords').split(',').map(k => k.trim()) : null,
                        analyze_sentiment: formData.get('analyze_sentiment') === 'on',
                        extract_keywords: formData.get('extract_keywords') === 'on'
                    };
                    
                    const resultsDiv = document.getElementById('results');
                    resultsDiv.innerHTML = '<p>⏳ Парсинг в процессе...</p>';
                    
                    try {
                        const response = await fetch('/api/parse', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            resultsDiv.innerHTML = `
                                <h3>✅ Парсинг завершен успешно!</h3>
                                <p><strong>Канал:</strong> ${result.channel}</p>
                                <p><strong>Сообщений обработано:</strong> ${result.messages_parsed}</p>
                                <p><strong>Движок:</strong> ${result.engine_used}</p>
                                <p><strong>Время:</strong> ${new Date().toLocaleString()}</p>
                                <button onclick="downloadData()">📥 Скачать данные</button>
                            `;
                            loadStats(); // Обновить статистику
                        } else {
                            resultsDiv.innerHTML = `<p style="color: red;">❌ Ошибка: ${result.error}</p>`;
                        }
                    } catch (error) {
                        resultsDiv.innerHTML = `<p style="color: red;">❌ Ошибка: ${error.message}</p>`;
                    }
                });
                
                // Скачивание данных
                async function downloadData() {
                    window.open('/api/export?format=json', '_blank');
                }
                
                // Загрузить статистику при загрузке страницы
                loadStats();
            </script>
        </body>
        </html>
        """
        return html_content
    
    @app.post("/api/parse")
    async def parse_endpoint(request: ParseRequest, background_tasks: BackgroundTasks):
        """API endpoint для парсинга"""
        try:
            config = ParseConfig(
                target=request.target,
                max_messages=request.max_messages,
                days_back=request.days_back,
                keywords=request.keywords,
                exclude_keywords=request.exclude_keywords,
                analyze_sentiment=request.analyze_sentiment,
                extract_keywords=request.extract_keywords
            )
            
            # Запуск парсинга в фоне
            result = await parser.parse_channel(config)
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/stats")
    async def get_stats():
        """API endpoint для получения статистики"""
        return parser.get_statistics()
    
    @app.get("/api/export")
    async def export_data_endpoint(format: str = "json"):
        """API endpoint для экспорта данных"""
        filename = parser.export_data(format)
        if filename:
            return {"filename": filename, "download_url": f"/download/{filename}"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка экспорта данных")

# CLI интерфейс
async def main():
    """Основная функция для CLI"""
    print("🕉️ Telegram Parser MVP - Запуск CLI режима")
    
    parser = TelegramParserMVP()
    
    try:
        # Инициализация клиентов
        if not await parser.initialize_clients():
            print("❌ Не удалось инициализировать клиенты")
            return
        
        # Интерактивный ввод параметров
        target = input("Введите канал или группу (@channel_name): ").strip()
        if not target:
            print("❌ Не указан канал")
            return
        
        max_messages = int(input("Максимум сообщений (по умолчанию 1000): ") or "1000")
        days_back = int(input("Дней назад (по умолчанию 7): ") or "7")
        
        keywords_input = input("Ключевые слова через запятую (необязательно): ").strip()
        keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else None
        
        # Создание конфигурации
        config = ParseConfig(
            target=target,
            max_messages=max_messages,
            days_back=days_back,
            keywords=keywords,
            analyze_sentiment=True,
            extract_keywords=True
        )
        
        # Запуск парсинга
        result = await parser.parse_channel(config)
        
        if result.get("success"):
            print(f"✅ Парсинг завершен успешно!")
            print(f"📊 Обработано сообщений: {result['messages_parsed']}")
            print(f"🔧 Использованный движок: {result['engine_used']}")
            
            # Экспорт данных
            export_choice = input("Экспортировать данные? (y/n): ").lower()
            if export_choice == 'y':
                format_choice = input("Формат (json/csv): ").lower() or "json"
                filename = parser.export_data(format_choice)
                if filename:
                    print(f"📁 Данные экспортированы в файл: {filename}")
            
            # Показать статистику
            stats = parser.get_statistics()
            print(f"\n📈 Общая статистика:")
            print(f"   Всего сообщений: {stats['total_messages']}")
            print(f"   Всего каналов: {stats['total_channels']}")
            
        else:
            print(f"❌ Ошибка парсинга: {result.get('error')}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Парсинг прерван пользователем")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    finally:
        await parser.cleanup()

if __name__ == "__main__":
    if WEB_AVAILABLE:
        print("🌐 Запуск веб-сервера...")
        print("Откройте http://localhost:8000 в браузере")
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("🖥️ Запуск CLI режима...")
        asyncio.run(main()) 