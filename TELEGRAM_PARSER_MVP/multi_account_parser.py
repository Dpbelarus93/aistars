#!/usr/bin/env python3
"""
🕉️ Multi-Account Telegram Parser - Масштабируемый парсер
Коммерческая версия с поддержкой множественных аккаунтов

Автор: НейроКодер
Версия: 2.0.0
"""

import asyncio
import json
import logging
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import aiohttp

# Telegram клиенты
try:
    from pyrogram import Client
    from telethon import TelegramClient
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class AccountConfig:
    """Конфигурация одного аккаунта"""
    account_id: str
    api_id: str
    api_hash: str
    phone_number: str
    session_name: str
    is_active: bool = True
    daily_requests: int = 0
    last_request_time: Optional[datetime] = None
    max_daily_requests: int = 5000  # Безопасный лимит
    rate_limit_delay: float = 1.0

@dataclass
class ScalingConfig:
    """Конфигурация масштабирования"""
    max_concurrent_accounts: int = 5
    max_daily_requests_per_account: int = 5000
    global_rate_limit: float = 0.5  # секунды между запросами
    account_rotation_interval: int = 100  # сообщений
    retry_delay: float = 60.0  # секунды при ошибках
    max_retries: int = 3

class MultiAccountParser:
    """Масштабируемый парсер с множественными аккаунтами"""
    
    def __init__(self, config_file: str = "multi_account_config.json"):
        self.config_file = config_file
        self.accounts: Dict[str, AccountConfig] = {}
        self.scaling_config = ScalingConfig()
        self.active_accounts: List[str] = []
        self.current_account_index = 0
        self.global_stats = {
            "total_messages_parsed": 0,
            "total_accounts_used": 0,
            "total_errors": 0,
            "start_time": datetime.now()
        }
        
        self._load_config()
        self._init_database()
    
    def _load_config(self):
        """Загрузка конфигурации множественных аккаунтов"""
        default_config = {
            "scaling": {
                "max_concurrent_accounts": 5,
                "max_daily_requests_per_account": 5000,
                "global_rate_limit": 0.5,
                "account_rotation_interval": 100,
                "retry_delay": 60.0,
                "max_retries": 3
            },
            "accounts": []
        }
        
        if Path(self.config_file).exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                logger.error(f"Ошибка загрузки конфигурации: {e}")
        else:
            # Создаем пример конфигурации
            default_config["accounts"] = [
                {
                    "account_id": "account_1",
                    "api_id": "YOUR_API_ID_1",
                    "api_hash": "YOUR_API_HASH_1", 
                    "phone_number": "+1234567890",
                    "session_name": "parser_session_1",
                    "is_active": True,
                    "max_daily_requests": 5000,
                    "rate_limit_delay": 1.0
                },
                {
                    "account_id": "account_2", 
                    "api_id": "YOUR_API_ID_2",
                    "api_hash": "YOUR_API_HASH_2",
                    "phone_number": "+0987654321", 
                    "session_name": "parser_session_2",
                    "is_active": True,
                    "max_daily_requests": 5000,
                    "rate_limit_delay": 1.0
                }
            ]
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            logger.info(f"Создан файл конфигурации: {self.config_file}")
        
        # Загрузка аккаунтов
        for acc_data in default_config["accounts"]:
            account = AccountConfig(**acc_data)
            self.accounts[account.account_id] = account
            if account.is_active:
                self.active_accounts.append(account.account_id)
        
        # Загрузка настроек масштабирования
        scaling_data = default_config.get("scaling", {})
        self.scaling_config = ScalingConfig(**scaling_data)
        
        logger.info(f"Загружено {len(self.accounts)} аккаунтов, активных: {len(self.active_accounts)}")
    
    def _init_database(self):
        """Инициализация базы данных для множественных аккаунтов"""
        conn = sqlite3.connect("multi_account_parser.db")
        cursor = conn.cursor()
        
        # Таблица аккаунтов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                api_id TEXT,
                phone_number TEXT,
                daily_requests INTEGER DEFAULT 0,
                last_request_time TIMESTAMP,
                total_requests INTEGER DEFAULT 0,
                errors_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица статистики парсинга
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parsing_sessions (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                account_id TEXT,
                target_channel TEXT,
                messages_parsed INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT,
                error_message TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            )
        ''')
        
        # Таблица лимитов и мониторинга
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rate_limits (
                id INTEGER PRIMARY KEY,
                account_id TEXT,
                request_type TEXT,
                timestamp TIMESTAMP,
                response_time FLOAT,
                success BOOLEAN,
                error_type TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts (account_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_next_available_account(self) -> Optional[AccountConfig]:
        """Получение следующего доступного аккаунта"""
        if not self.active_accounts:
            return None
        
        # Ротация аккаунтов
        account_id = self.active_accounts[self.current_account_index]
        account = self.accounts[account_id]
        
        # Проверка дневных лимитов
        if account.daily_requests >= account.max_daily_requests:
            logger.warning(f"Аккаунт {account_id} достиг дневного лимита")
            return None
        
        # Проверка времени последнего запроса
        if account.last_request_time:
            time_since_last = (datetime.now() - account.last_request_time).total_seconds()
            if time_since_last < account.rate_limit_delay:
                return None
        
        # Переход к следующему аккаунту
        self.current_account_index = (self.current_account_index + 1) % len(self.active_accounts)
        
        return account
    
    async def parse_with_account_rotation(self, target: str, max_messages: int = 1000) -> Dict:
        """Парсинг с автоматической ротацией аккаунтов"""
        logger.info(f"🚀 Начинаем масштабированный парсинг: {target}")
        
        all_messages = []
        accounts_used = set()
        errors = []
        
        messages_parsed = 0
        account_rotation_count = 0
        
        while messages_parsed < max_messages:
            account = self.get_next_available_account()
            
            if not account:
                logger.warning("Нет доступных аккаунтов, ожидание...")
                await asyncio.sleep(self.scaling_config.retry_delay)
                continue
            
            # Парсинг с текущим аккаунтом
            try:
                messages_batch = await self._parse_batch_with_account(
                    account, target, 
                    min(max_messages - messages_parsed, self.scaling_config.account_rotation_interval)
                )
                
                if messages_batch:
                    all_messages.extend(messages_batch)
                    messages_parsed += len(messages_batch)
                    accounts_used.add(account.account_id)
                    account_rotation_count += 1
                    
                    # Обновление статистики аккаунта
                    account.daily_requests += len(messages_batch)
                    account.last_request_time = datetime.now()
                    
                    logger.info(f"✅ Аккаунт {account.account_id}: {len(messages_batch)} сообщений")
                
                # Глобальный rate limiting
                await asyncio.sleep(self.scaling_config.global_rate_limit)
                
            except Exception as e:
                error_msg = f"Ошибка аккаунта {account.account_id}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                
                # Временная деактивация проблемного аккаунта
                account.is_active = False
                if account.account_id in self.active_accounts:
                    self.active_accounts.remove(account.account_id)
        
        # Сохранение статистики
        self._save_session_stats(target, accounts_used, messages_parsed, errors)
        
        return {
            "success": True,
            "target": target,
            "messages_parsed": messages_parsed,
            "accounts_used": list(accounts_used),
            "account_rotations": account_rotation_count,
            "errors": errors,
            "global_stats": self.global_stats
        }
    
    async def _parse_batch_with_account(self, account: AccountConfig, target: str, limit: int) -> List[Dict]:
        """Парсинг батча сообщений с конкретным аккаунтом"""
        # Здесь будет логика парсинга с Pyrogram/Telethon
        # Пока заглушка для демонстрации
        await asyncio.sleep(account.rate_limit_delay)
        
        # Симуляция парсинга
        messages = []
        for i in range(min(limit, 50)):  # Максимум 50 сообщений за раз
            messages.append({
                "id": f"{account.account_id}_{i}",
                "text": f"Сообщение {i} от аккаунта {account.account_id}",
                "date": datetime.now().isoformat(),
                "account_id": account.account_id
            })
        
        return messages
    
    def _save_session_stats(self, target: str, accounts_used: set, messages_parsed: int, errors: List[str]):
        """Сохранение статистики сессии"""
        conn = sqlite3.connect("multi_account_parser.db")
        cursor = conn.cursor()
        
        try:
            session_id = f"session_{int(time.time())}"
            
            cursor.execute('''
                INSERT INTO parsing_sessions 
                (session_id, account_id, target_channel, messages_parsed, start_time, end_time, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                ",".join(accounts_used),
                target,
                messages_parsed,
                self.global_stats["start_time"],
                datetime.now(),
                "completed" if not errors else "completed_with_errors",
                "; ".join(errors) if errors else None
            ))
            
            conn.commit()
        except Exception as e:
            logger.error(f"Ошибка сохранения статистики: {e}")
        finally:
            conn.close()
    
    def get_accounts_status(self) -> Dict:
        """Получение статуса всех аккаунтов"""
        status = {
            "total_accounts": len(self.accounts),
            "active_accounts": len(self.active_accounts),
            "accounts_details": {}
        }
        
        for account_id, account in self.accounts.items():
            status["accounts_details"][account_id] = {
                "is_active": account.is_active,
                "daily_requests": account.daily_requests,
                "max_daily_requests": account.max_daily_requests,
                "last_request_time": account.last_request_time.isoformat() if account.last_request_time else None,
                "usage_percentage": (account.daily_requests / account.max_daily_requests) * 100
            }
        
        return status
    
    def reset_daily_limits(self):
        """Сброс дневных лимитов (вызывать раз в день)"""
        for account in self.accounts.values():
            account.daily_requests = 0
            account.last_request_time = None
        
        logger.info("Дневные лимиты сброшены")

# Пример использования
async def main():
    parser = MultiAccountParser()
    
    # Проверка статуса аккаунтов
    status = parser.get_accounts_status()
    print("Статус аккаунтов:", json.dumps(status, indent=2, ensure_ascii=False))
    
    # Парсинг с ротацией аккаунтов
    result = await parser.parse_with_account_rotation("@test_channel", 1000)
    print("Результат парсинга:", json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main()) 