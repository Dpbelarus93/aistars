import openai
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import os

from ..models.schemas import AIResponse, OrderAnalysisResponse
from ..utils.text_processor import TextProcessor
from ..utils.category_classifier import CategoryClassifier
from ..utils.price_estimator import PriceEstimator

logger = logging.getLogger(__name__)

class AIEngine:
    """
    Основной AI движок для обработки запросов пользователей
    """
    
    def __init__(self):
        self.openai_client = None
        self.text_processor = TextProcessor()
        self.category_classifier = CategoryClassifier()
        self.price_estimator = PriceEstimator()
        self.is_initialized = False
        
        # Промпты для разных типов запросов
        self.system_prompts = {
            'GENERAL': """
            Ты - AI-ассистент консервс-сервиса, платформы для заказа услуг.
            Твоя задача - помочь пользователям найти нужные услуги, создать заказы, 
            и получить поддержку. Отвечай дружелюбно и профессионально на русском языке.
            
            Доступные услуги включают:
            - Аренда велосипедов
            - Доставка еды и товаров
            - Уборка и клининг
            - Ремонт и обслуживание
            - Транспортные услуги
            - И многое другое
            
            Если пользователь хочет заказать услугу, предложи ему создать заказ.
            """,
            
            'ORDER_HELP': """
            Ты помогаешь пользователям с созданием и управлением заказами.
            Задавай уточняющие вопросы о деталях заказа:
            - Точное описание услуги
            - Местоположение
            - Бюджет
            - Сроки выполнения
            - Особые требования
            
            Предлагай улучшения и оптимизацию заказа.
            """,
            
            'SERVICE_SEARCH': """
            Ты помогаешь пользователям найти подходящие услуги.
            Используй информацию о местоположении, бюджете и предпочтениях.
            Рекомендуй проверенных исполнителей и объясняй преимущества.
            """,
            
            'SUPPORT': """
            Ты предоставляешь техническую поддержку пользователям.
            Помогай решать проблемы с заказами, платежами, аккаунтом.
            Если не можешь решить проблему - предложи связаться с человеком-оператором.
            """
        }
    
    async def initialize(self):
        """Инициализация AI движка"""
        try:
            # Настройка OpenAI
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.openai_client = openai
            
            # Инициализация компонентов
            await self.text_processor.initialize()
            await self.category_classifier.initialize()
            await self.price_estimator.initialize()
            
            self.is_initialized = True
            logger.info("AI движок инициализирован")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации AI движка: {str(e)}")
            raise
    
    async def cleanup(self):
        """Очистка ресурсов"""
        self.is_initialized = False
        logger.info("AI движок остановлен")
    
    def is_ready(self) -> bool:
        """Проверка готовности AI движка"""
        return self.is_initialized
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None,
        message_type: str = 'GENERAL'
    ) -> AIResponse:
        """
        Обработка сообщения пользователя
        """
        try:
            # Подготовка контекста
            system_prompt = self.system_prompts.get(message_type, self.system_prompts['GENERAL'])
            
            # Анализ намерений пользователя
            intent = await self._analyze_intent(message, context)
            
            # Генерация ответа
            response_text = await self._generate_response(
                message, system_prompt, intent, context
            )
            
            # Генерация предложений и действий
            suggestions = await self._generate_suggestions(intent, context)
            actions = await self._generate_actions(intent, context)
            
            return AIResponse(
                message=response_text,
                suggestions=suggestions,
                actions=actions,
                metadata={
                    'intent': intent,
                    'confidence': 0.85,
                    'processed_at': datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {str(e)}")
            return AIResponse(
                message="Извините, произошла ошибка при обработке вашего запроса. Попробуйте еще раз.",
                suggestions=[],
                actions=[],
                metadata={'error': str(e)}
            )
    
    async def analyze_order(
        self,
        title: str,
        description: str,
        location: Optional[str] = None,
        budget: Optional[float] = None,
        user_id: str = None
    ) -> OrderAnalysisResponse:
        """
        Анализ заказа с помощью AI
        """
        try:
            # Классификация категории
            category = await self.category_classifier.classify(title, description)
            
            # Оценка стоимости
            price_estimate = await self.price_estimator.estimate(
                category, description, location, budget
            )
            
            # Анализ сложности и времени
            complexity = await self._analyze_complexity(description)
            estimated_time = await self._estimate_duration(category, description, complexity)
            
            # Требования к исполнителю
            requirements = await self._analyze_requirements(description, category)
            
            # Рекомендации по улучшению
            improvements = await self._suggest_improvements(title, description)
            
            return OrderAnalysisResponse(
                category=category,
                estimated_price=price_estimate,
                estimated_duration=estimated_time,
                complexity=complexity,
                requirements=requirements,
                improvements=improvements,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Ошибка анализа заказа: {str(e)}")
            raise
    
    async def get_order_suggestions(
        self,
        order_id: str,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """
        Получение предложений по улучшению заказа
        """
        try:
            # Здесь будет загрузка заказа из базы данных
            # order = await self.db.get_order(order_id)
            
            suggestions = [
                {
                    'type': 'description',
                    'title': 'Улучшить описание',
                    'suggestion': 'Добавьте больше деталей о требованиях к работе',
                    'priority': 'high'
                },
                {
                    'type': 'budget',
                    'title': 'Оптимизировать бюджет',
                    'suggestion': 'Рассмотрите увеличение бюджета на 15% для привлечения лучших исполнителей',
                    'priority': 'medium'
                },
                {
                    'type': 'timing',
                    'title': 'Скорректировать сроки',
                    'suggestion': 'Добавьте 2-3 дня к срокам для обеспечения качества',
                    'priority': 'low'
                }
            ]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Ошибка получения предложений: {str(e)}")
            return []
    
    async def train_model(self):
        """
        Обучение AI модели на новых данных
        """
        try:
            # Здесь будет логика обучения модели
            # на основе новых заказов, отзывов и взаимодействий
            
            training_result = {
                'id': 'training_' + datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
                'estimated_minutes': 30,
                'status': 'started'
            }
            
            logger.info("Запуск обучения AI модели")
            return training_result
            
        except Exception as e:
            logger.error(f"Ошибка обучения модели: {str(e)}")
            raise
    
    async def get_metrics(self):
        """
        Получение метрик работы AI
        """
        try:
            # Здесь будет сбор реальных метрик из базы данных
            metrics = {
                'total_requests': 1247,
                'successful_assignments': 892,
                'average_response_time': 1.2,
                'user_satisfaction': 4.6,
                'top_categories': [
                    {'category': 'Доставка', 'count': 456},
                    {'category': 'Уборка', 'count': 234},
                    {'category': 'Ремонт', 'count': 189}
                ],
                'partner_performance': {
                    'avg_rating': 4.5,
                    'completion_rate': 0.94,
                    'response_time_hours': 2.3
                }
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Ошибка получения метрик: {str(e)}")
            raise
    
    async def _analyze_intent(self, message: str, context: Optional[Dict]) -> str:
        """Анализ намерений пользователя"""
        try:
            # Простейший анализ намерений на основе ключевых слов
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['заказать', 'нужна услуга', 'хочу', 'требуется']):
                return 'create_order'
            elif any(word in message_lower for word in ['найти', 'поиск', 'где', 'какие услуги']):
                return 'search_services'
            elif any(word in message_lower for word in ['проблема', 'не работает', 'ошибка', 'помощь']):
                return 'support'
            elif any(word in message_lower for word in ['статус', 'заказ', 'исполнитель']):
                return 'order_status'
            else:
                return 'general_chat'
                
        except Exception as e:
            logger.error(f"Ошибка анализа намерений: {str(e)}")
            return 'general_chat'
    
    async def _generate_response(
        self,
        message: str,
        system_prompt: str,
        intent: str,
        context: Optional[Dict]
    ) -> str:
        """Генерация ответа с помощью OpenAI"""
        try:
            # Формирование запроса к OpenAI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {str(e)}")
            return "Извините, не могу обработать ваш запрос прямо сейчас. Попробуйте позже."
    
    async def _generate_suggestions(self, intent: str, context: Optional[Dict]) -> List[str]:
        """Генерация предложений для пользователя"""
        suggestions_map = {
            'create_order': [
                "Создать новый заказ",
                "Посмотреть каталог услуг",
                "Найти исполнителя"
            ],
            'search_services': [
                "Показать все услуги",
                "Фильтр по городу",
                "Популярные услуги"
            ],
            'support': [
                "Связаться с оператором",
                "Часто задаваемые вопросы",
                "Сообщить о проблеме"
            ],
            'general_chat': [
                "Показать мои заказы",
                "Найти услуги",
                "Стать партнером"
            ]
        }
        
        return suggestions_map.get(intent, [])
    
    async def _generate_actions(self, intent: str, context: Optional[Dict]) -> List[Dict]:
        """Генерация действий для пользователя"""
        actions_map = {
            'create_order': [
                {
                    'type': 'REDIRECT',
                    'label': 'Создать заказ',
                    'url': '/orders/create'
                }
            ],
            'search_services': [
                {
                    'type': 'SEARCH_SERVICES',
                    'label': 'Поиск услуг',
                    'url': '/services'
                }
            ],
            'support': [
                {
                    'type': 'CONTACT_SUPPORT',
                    'label': 'Связаться с поддержкой',
                    'url': '/support'
                }
            ]
        }
        
        return actions_map.get(intent, [])
    
    async def _analyze_complexity(self, description: str) -> str:
        """Анализ сложности заказа"""
        # Простейший анализ сложности
        if len(description.split()) > 50:
            return 'high'
        elif len(description.split()) > 20:
            return 'medium'
        else:
            return 'low'
    
    async def _estimate_duration(self, category: str, description: str, complexity: str) -> int:
        """Оценка времени выполнения в минутах"""
        base_times = {
            'delivery': 60,
            'cleaning': 180,
            'repair': 240,
            'transport': 120,
            'other': 120
        }
        
        base_time = base_times.get(category, 120)
        
        if complexity == 'high':
            return base_time * 2
        elif complexity == 'medium':
            return int(base_time * 1.5)
        else:
            return base_time
    
    async def _analyze_requirements(self, description: str, category: str) -> List[str]:
        """Анализ требований к исполнителю"""
        requirements = ['Опыт работы', 'Положительные отзывы']
        
        if 'срочно' in description.lower():
            requirements.append('Быстрое реагирование')
        
        if category == 'repair':
            requirements.append('Специализированные инструменты')
        
        return requirements
    
    async def _suggest_improvements(self, title: str, description: str) -> List[str]:
        """Предложения по улучшению заказа"""
        improvements = []
        
        if len(description) < 50:
            improvements.append('Добавьте больше деталей в описание')
        
        if 'срочно' in description.lower():
            improvements.append('Укажите конкретные сроки выполнения')
        
        if not any(word in description.lower() for word in ['адрес', 'место', 'где']):
            improvements.append('Уточните местоположение')
        
        return improvements