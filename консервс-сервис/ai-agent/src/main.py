from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import asyncio
import uvicorn
import os
from dotenv import load_dotenv

from core.ai_engine import AIEngine
from core.order_dispatcher import OrderDispatcher
from core.partner_matcher import PartnerMatcher
from core.database import get_db
from core.auth import get_current_user
from models.schemas import (
    AIRequest, 
    AIResponse, 
    OrderAnalysisRequest, 
    OrderAnalysisResponse,
    PartnerRecommendationRequest,
    PartnerRecommendationResponse,
    AutoAssignRequest,
    AutoAssignResponse
)

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai-agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title="Консервс-Сервис AI Agent",
    description="AI-агент для автоматизации заказов и перенаправления к исполнителям",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация компонентов AI
ai_engine = AIEngine()
order_dispatcher = OrderDispatcher()
partner_matcher = PartnerMatcher()

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    logger.info("Запуск AI-агента консервс-сервиса")
    await ai_engine.initialize()
    await order_dispatcher.initialize()
    await partner_matcher.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    """Очистка ресурсов при остановке"""
    logger.info("Остановка AI-агента")
    await ai_engine.cleanup()

@app.get("/")
async def root():
    """Главная страница API"""
    return {
        "message": "Консервс-Сервис AI Agent",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {
        "status": "healthy",
        "ai_engine": ai_engine.is_ready(),
        "order_dispatcher": order_dispatcher.is_ready(),
        "partner_matcher": partner_matcher.is_ready(),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/ai/chat", response_model=AIResponse)
async def ai_chat(
    request: AIRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Основной чат с AI-ассистентом
    
    Обрабатывает запросы пользователей и предоставляет:
    - Помощь в поиске услуг
    - Создание заказов
    - Поддержку клиентов
    - Навигацию по платформе
    """
    try:
        logger.info(f"AI чат запрос от пользователя {current_user['id']}: {request.message}")
        
        # Обработка запроса через AI движок
        response = await ai_engine.process_message(
            message=request.message,
            user_id=current_user['id'],
            context=request.context,
            message_type=request.type
        )
        
        # Логирование ответа
        logger.info(f"AI ответ для пользователя {current_user['id']}: {response.message}")
        
        return response
        
    except Exception as e:
        logger.error(f"Ошибка в AI чате: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка AI: {str(e)}")

@app.post("/api/ai/analyze-order", response_model=OrderAnalysisResponse)
async def analyze_order(
    request: OrderAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Анализ заказа с помощью AI
    
    Анализирует описание заказа и предоставляет:
    - Категорию услуги
    - Примерную стоимость
    - Время выполнения
    - Требования к исполнителю
    """
    try:
        logger.info(f"Анализ заказа от пользователя {current_user['id']}")
        
        # Анализ заказа через AI
        analysis = await ai_engine.analyze_order(
            title=request.title,
            description=request.description,
            location=request.location,
            budget=request.budget,
            user_id=current_user['id']
        )
        
        return analysis
        
    except Exception as e:
        logger.error(f"Ошибка при анализе заказа: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")

@app.post("/api/ai/recommend-partners", response_model=PartnerRecommendationResponse)
async def recommend_partners(
    request: PartnerRecommendationRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Рекомендация партнеров для заказа
    
    Находит наиболее подходящих исполнителей на основе:
    - Категории услуги
    - Местоположения
    - Рейтинга и опыта
    - Доступности
    """
    try:
        logger.info(f"Поиск партнеров для заказа {request.order_id}")
        
        # Поиск подходящих партнеров
        recommendations = await partner_matcher.find_best_partners(
            category=request.category,
            location=request.location,
            requirements=request.requirements,
            budget=request.budget,
            urgency=request.urgency
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Ошибка при поиске партнеров: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")

@app.post("/api/ai/auto-assign", response_model=AutoAssignResponse)
async def auto_assign_order(
    request: AutoAssignRequest,
    current_user: dict = Depends(get_current_user),
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Автоматическое назначение заказа исполнителю
    
    Автоматически находит и назначает лучшего исполнителя:
    - Анализирует требования заказа
    - Находит подходящих партнеров
    - Выбирает оптимального исполнителя
    - Уведомляет стороны
    """
    try:
        logger.info(f"Автоназначение заказа {request.order_id}")
        
        # Запуск автоматического назначения
        result = await order_dispatcher.auto_assign_order(
            order_id=request.order_id,
            preferences=request.preferences,
            force_assign=request.force_assign
        )
        
        # Запуск фоновых задач уведомлений
        if result.success:
            background_tasks.add_task(
                order_dispatcher.notify_assignment,
                order_id=request.order_id,
                partner_id=result.assigned_partner_id,
                client_id=current_user['id']
            )
        
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при автоназначении: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка назначения: {str(e)}")

@app.get("/api/ai/orders/{order_id}/suggestions")
async def get_order_suggestions(
    order_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение AI-предложений для заказа
    
    Предоставляет умные предложения:
    - Улучшения описания заказа
    - Оптимизация бюджета
    - Рекомендации по срокам
    """
    try:
        suggestions = await ai_engine.get_order_suggestions(
            order_id=order_id,
            user_id=current_user['id']
        )
        
        return {"suggestions": suggestions}
        
    except Exception as e:
        logger.error(f"Ошибка при получении предложений: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@app.post("/api/ai/train")
async def train_ai_model(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обучение AI модели на новых данных
    
    Доступно только для администраторов
    """
    if current_user.get('role') != 'ADMIN':
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    try:
        logger.info("Запуск обучения AI модели")
        
        # Запуск обучения
        training_result = await ai_engine.train_model()
        
        return {
            "status": "success",
            "message": "Обучение модели запущено",
            "training_id": training_result.id,
            "estimated_time": training_result.estimated_minutes
        }
        
    except Exception as e:
        logger.error(f"Ошибка при обучении модели: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка обучения: {str(e)}")

@app.get("/api/ai/metrics")
async def get_ai_metrics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение метрик работы AI-агента
    
    Доступно для менеджеров и администраторов
    """
    if current_user.get('role') not in ['MANAGER', 'ADMIN']:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    try:
        metrics = await ai_engine.get_metrics()
        
        return {
            "total_requests": metrics.total_requests,
            "successful_assignments": metrics.successful_assignments,
            "average_response_time": metrics.average_response_time,
            "user_satisfaction": metrics.user_satisfaction,
            "top_categories": metrics.top_categories,
            "partner_performance": metrics.partner_performance
        }
        
    except Exception as e:
        logger.error(f"Ошибка при получении метрик: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@app.websocket("/ws/ai-chat/{user_id}")
async def websocket_ai_chat(websocket, user_id: str):
    """
    WebSocket для real-time чата с AI
    """
    await websocket.accept()
    logger.info(f"WebSocket соединение установлено для пользователя {user_id}")
    
    try:
        while True:
            # Получение сообщения от клиента
            data = await websocket.receive_json()
            
            # Обработка через AI
            response = await ai_engine.process_message(
                message=data['message'],
                user_id=user_id,
                context=data.get('context', {}),
                message_type=data.get('type', 'GENERAL')
            )
            
            # Отправка ответа
            await websocket.send_json({
                "type": "ai_response",
                "data": response.dict()
            })
            
    except Exception as e:
        logger.error(f"Ошибка WebSocket: {str(e)}")
    finally:
        logger.info(f"WebSocket соединение закрыто для пользователя {user_id}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("AI_AGENT_PORT", 8000)),
        reload=True,
        log_level="info"
    )