#!/bin/bash

# Функция для форматирования времени
timestamp() {
  date "+%Y-%m-%d %H:%M:%S"
}

echo "[$(timestamp)] 🕉️ Начинаем синхронизацию с GitHub..."

# Проверяем статус SUCCESS_HISTORY.md
if git diff --quiet SUCCESS_HISTORY.md; then
    echo "[$(timestamp)] ℹ️ Нет новых успешных задач для синхронизации"
else
    echo "[$(timestamp)] 📝 Обнаружены новые успешные задачи"
    
    # Добавляем SUCCESS_HISTORY.md и связанные файлы
    git add SUCCESS_HISTORY.md
    git add .cursor/rules/*.mdc
    
    # Создаем коммит с эмодзи и timestamp
    git commit -m "📈 Автоматическое обновление успешных задач [$(timestamp)]"
    
    # Пушим изменения
    git push origin main
    
    echo "[$(timestamp)] ✅ Успешно синхронизировано с GitHub"
fi

# Проверяем наличие других изменений в проекте
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[$(timestamp)] 🔄 Обнаружены другие изменения в проекте"
    echo "Для синхронизации всех изменений используйте команды:"
    echo "git add ."
    echo "git commit -m \"Ваше сообщение\""
    echo "git push origin main"
fi
