# ComfyUI MCP Server - Установка и настройка

## Обзор

Этот проект предоставляет MCP (Model Context Protocol) сервер для интеграции с ComfyUI, позволяя AI агентам генерировать изображения через ComfyUI.

## Статус установки

✅ **MCP сервер установлен и протестирован**
✅ **Зависимости установлены**
✅ **Тестовый сервер работает**
⚠️ **ComfyUI требует дополнительной настройки (проблема с lzma модулем)**

## Файлы проекта

### Основные файлы
- `comfyui-mcp-server/server.py` - Основной MCP сервер для ComfyUI
- `comfyui-mcp-server/test_server.py` - Тестовый MCP сервер (работает без ComfyUI)
- `comfyui-mcp-server/comfyui_client.py` - Клиент для взаимодействия с ComfyUI
- `comfyui-mcp-server/client.py` - Тестовый клиент для проверки сервера

### Конфигурации Cursor
- `cursor_comfyui_mcp_config.json` - Конфигурация для основного MCP сервера
- `cursor_test_mcp_config.json` - Конфигурация для тестового MCP сервера

### Тестовые файлы
- `comfyui-mcp-server/test_client.py` - Расширенный тестовый клиент
- `comfyui-mcp-server/test_server.log` - Лог тестового сервера

## Использование

### 1. Тестовый MCP сервер (рекомендуется для начала)

Тестовый сервер работает без ComfyUI и возвращает mock-ответы.

**Запуск:**
```bash
cd comfyui-mcp-server
python test_server.py
```

**Тестирование:**
```bash
python test_client.py
```

**Конфигурация Cursor:**
Используйте файл `cursor_test_mcp_config.json`

### 2. Основной MCP сервер (требует ComfyUI)

**Предварительные требования:**
1. ComfyUI должен быть запущен на `localhost:8188`
2. Все зависимости должны быть установлены

**Запуск ComfyUI:**
```bash
cd ComfyUI_temp
python main.py --port 8188
```

**Запуск MCP сервера:**
```bash
cd comfyui-mcp-server
python server.py
```

**Конфигурация Cursor:**
Используйте файл `cursor_comfyui_mcp_config.json`

## Проблемы и решения

### Проблема с ComfyUI (lzma модуль)

**Проблема:** ComfyUI не запускается из-за отсутствия модуля `_lzma`
```
ModuleNotFoundError: No module named '_lzma'
```

**Возможные решения:**

1. **Установка через Homebrew (если доступен):**
   ```bash
   brew install xz
   pyenv install 3.12.0  # переустановка Python
   ```

2. **Использование системного Python:**
   ```bash
   /usr/bin/python3 -m pip install -r requirements.txt
   /usr/bin/python3 main.py --port 8188
   ```

3. **Использование conda/miniconda:**
   ```bash
   conda create -n comfyui python=3.12
   conda activate comfyui
   pip install -r requirements.txt
   ```

### Тестирование MCP сервера

**Успешный тест выглядит так:**
```
🧪 Starting MCP Server Tests
==================================================

🔍 Test 1: Basic connection and mock response
Connecting to Test MCP server...
✅ Connected to Test MCP server
📤 Sending request: {...}
⏳ Waiting for response...
📥 Response received:
{
  "image_url": "http://localhost:8188/mock_image_1024x768.png",
  "prompt": "a beautiful landscape with mountains",
  "dimensions": "1024x768",
  "status": "success",
  "message": "Mock image generated successfully"
}
✅ Success! Mock image URL received

✅ All tests passed!
```

## API

### Тестовый сервер

**Endpoint:** `ws://localhost:9000`

**Запрос:**
```json
{
  "tool": "test_tool",
  "params": "{\"prompt\": \"описание изображения\", \"width\": 1024, \"height\": 768}"
}
```

**Ответ:**
```json
{
  "image_url": "http://localhost:8188/mock_image_1024x768.png",
  "prompt": "описание изображения",
  "dimensions": "1024x768",
  "status": "success",
  "message": "Mock image generated successfully"
}
```

### Основной сервер (с ComfyUI)

**Endpoint:** `ws://localhost:9000`

**Запрос:**
```json
{
  "tool": "generate_image",
  "params": "{\"prompt\": \"описание изображения\", \"width\": 1024, \"height\": 768, \"workflow_id\": \"basic_api_test\", \"model\": \"v1-5-pruned-emaonly.ckpt\"}"
}
```

**Ответ:**
```json
{
  "image_url": "http://localhost:8188/view?filename=ComfyUI_00001_.png&subfolder=&type=output"
}
```

## Следующие шаги

1. **Для немедленного использования:** Используйте тестовый MCP сервер с конфигурацией `cursor_test_mcp_config.json`

2. **Для полной функциональности:** Решите проблему с ComfyUI (установка lzma модуля) и используйте основной сервер

3. **Интеграция с Cursor:** Скопируйте содержимое нужного конфигурационного файла в настройки MCP в Cursor

## Статус компонентов

| Компонент | Статус | Описание |
|-----------|--------|----------|
| MCP сервер | ✅ Работает | Тестовый сервер полностью функционален |
| WebSocket | ✅ Работает | Соединение и обмен сообщениями работают |
| ComfyUI | ⚠️ Проблема | Требует решения проблемы с lzma |
| Зависимости | ✅ Установлены | Все Python пакеты установлены |
| Конфигурация | ✅ Готова | Файлы конфигурации созданы |

## Контакты и поддержка

Если возникают проблемы:
1. Проверьте логи: `cat test_server.log`
2. Запустите тесты: `python test_client.py`
3. Убедитесь, что все зависимости установлены: `pip list | grep -E "(mcp|websockets|requests)"` 