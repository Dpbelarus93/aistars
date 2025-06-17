#!/bin/bash

# 🕉️ Ритуал Проверки Чистоты Кода
# Священный скрипт для проверки качества Python кода

echo "🕉️ Начинаю ритуал проверки чистоты кода..."
echo "================================================"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Счетчики ошибок
ERRORS=0
WARNINGS=0

# Функция логирования
log_error() {
    echo -e "${RED}❌ ОШИБКА: $1${NC}"
    ((ERRORS++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  ПРЕДУПРЕЖДЕНИЕ: $1${NC}"
    ((WARNINGS++))
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 1. Проверка структуры проекта
echo "🔍 Проверка структуры проекта..."
if [ ! -d "code" ]; then
    log_error "Отсутствует папка 'code' с основными скриптами"
else
    log_success "Папка 'code' найдена"
fi

if [ ! -d "HEYGEN_READY_BATCH" ]; then
    log_warning "Отсутствует папка 'HEYGEN_READY_BATCH'"
else
    log_success "Папка 'HEYGEN_READY_BATCH' найдена"
fi

# 2. Проверка Python файлов на синтаксис
echo "🐍 Проверка синтаксиса Python файлов..."
python_files=$(find . -name "*.py" -not -path "./photo_batch_env/*" -not -path "./__pycache__/*")

if [ -z "$python_files" ]; then
    log_warning "Python файлы не найдены"
else
    for file in $python_files; do
        if python -m py_compile "$file" 2>/dev/null; then
            log_success "Синтаксис корректен: $file"
        else
            log_error "Ошибка синтаксиса в файле: $file"
        fi
    done
fi

# 3. Проверка кодировки файлов
echo "📝 Проверка кодировки файлов..."
for file in $python_files; do
    if file "$file" | grep -q "UTF-8"; then
        log_success "UTF-8 кодировка: $file"
    else
        log_warning "Возможные проблемы с кодировкой: $file"
    fi
done

# 4. Проверка наличия основных скриптов
echo "🔧 Проверка критических скриптов..."
critical_scripts=(
    "code/heygen_api_automator.py"
    "code/professional_lip_sync_automation.py"
    "code/comfy_upscaler_fixed.py"
)

for script in "${critical_scripts[@]}"; do
    if [ -f "$script" ]; then
        log_success "Найден критический скрипт: $script"
    else
        log_error "Отсутствует критический скрипт: $script"
    fi
done

# 5. Проверка размеров медиа файлов
echo "🎬 Проверка медиа библиотеки..."
if [ -d "ALL_TRACK_PHOTOS" ]; then
    photo_count=$(find ALL_TRACK_PHOTOS -name "*.jpg" -o -name "*.png" | wc -l)
    log_success "Найдено $photo_count фотографий"
else
    log_warning "Папка ALL_TRACK_PHOTOS не найдена"
fi

if [ -d "VOICE_TRACKS" ]; then
    audio_count=$(find VOICE_TRACKS -name "*.wav" -o -name "*.mp3" | wc -l)
    log_success "Найдено $audio_count аудио файлов"
else
    log_warning "Папка VOICE_TRACKS не найдена"
fi

# 6. Проверка готовых результатов
echo "🎯 Проверка готовых результатов..."
if [ -d "lipsync" ]; then
    video_count=$(find lipsync -name "*.mp4" | wc -l)
    log_success "Найдено $video_count готовых видео"
else
    log_warning "Папка lipsync не найдена"
fi

if [ -d "HEYGEN_READY_BATCH" ]; then
    mix_count=$(find HEYGEN_READY_BATCH -name "heygen_mix_*" -type d | wc -l)
    log_success "Найдено $mix_count HeyGen миксов"
else
    log_warning "Папка HEYGEN_READY_BATCH не найдена"
fi

# 7. Проверка свободного места на диске
echo "💾 Проверка свободного места..."
free_space=$(df -h . | awk 'NR==2 {print $4}')
log_success "Свободное место: $free_space"

# Итоговый отчет
echo "================================================"
echo "🕉️ Ритуал проверки завершен"
echo "================================================"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✨ КОД ЧИСТ И ГАРМОНИЧЕН ✨${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Найдено $WARNINGS предупреждений${NC}"
    echo -e "${GREEN}✅ Критических ошибок нет${NC}"
    exit 0
else
    echo -e "${RED}❌ Найдено $ERRORS ошибок и $WARNINGS предупреждений${NC}"
    echo -e "${RED}🔥 ТРЕБУЕТСЯ ОЧИЩЕНИЕ КОДА${NC}"
    exit 1
fi 