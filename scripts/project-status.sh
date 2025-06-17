#!/bin/bash

# 🕉️ Священный Скрипт Проверки Статуса Проекта
# Быстрая диагностика текущего состояния

echo "🕉️ СТАТУС ПРОЕКТА 'ХОЧУ ЕЩЕ'"
echo "================================"
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================"

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# 1. HEYGEN МИКСЫ
echo -e "${BLUE}🎬 HEYGEN МИКСЫ:${NC}"
if [ -d "HEYGEN_READY_BATCH" ]; then
    mix_count=$(find HEYGEN_READY_BATCH -name "heygen_mix_*" -type d | wc -l)
    echo -e "${GREEN}   ✅ Готово: $mix_count/20 миксов${NC}"
    
    # Проверка каждого микса
    for i in $(seq -f "%02g" 1 20); do
        mix_dir="HEYGEN_READY_BATCH/heygen_mix_$i"
        if [ -d "$mix_dir" ]; then
            audio_file="$mix_dir/audio_$i.wav"
            photo_file=$(find "$mix_dir" -name "photo_$i.*" | head -1)
            json_file="$mix_dir/heygen_instruction.json"
            
            if [ -f "$audio_file" ] && [ -f "$photo_file" ] && [ -f "$json_file" ]; then
                echo -e "${GREEN}   ✅ Микс $i: Полный${NC}"
            else
                echo -e "${RED}   ❌ Микс $i: Неполный${NC}"
            fi
        else
            echo -e "${RED}   ❌ Микс $i: Отсутствует${NC}"
        fi
    done
else
    echo -e "${RED}   ❌ Папка HEYGEN_READY_BATCH не найдена${NC}"
fi

echo ""

# 2. ГОТОВЫЕ ВИДЕО
echo -e "${BLUE}🎥 ГОТОВЫЕ ВИДЕО:${NC}"
if [ -d "lipsync" ]; then
    video_count=$(find lipsync -name "*.mp4" -not -path "*/4k_upscaled/*" | wc -l)
    echo -e "${GREEN}   ✅ Готово: $video_count видео${NC}"
    
    # 4K версии
    if [ -d "lipsync/4k_upscaled" ]; then
        upscaled_count=$(find lipsync/4k_upscaled -name "*.mp4" | wc -l)
        echo -e "${GREEN}   ✅ 4K версии: $upscaled_count видео${NC}"
    fi
    
    # Размеры файлов
    echo -e "${BLUE}   📊 Размеры видео:${NC}"
    find lipsync -name "*.mp4" -not -path "*/4k_upscaled/*" -exec ls -lh {} \; | awk '{print "      " $5 " - " $9}' | head -5
    if [ $video_count -gt 5 ]; then
        echo "      ... и еще $((video_count - 5)) видео"
    fi
else
    echo -e "${RED}   ❌ Папка lipsync не найдена${NC}"
fi

echo ""

# 3. МЕДИА БИБЛИОТЕКА
echo -e "${BLUE}📚 МЕДИА БИБЛИОТЕКА:${NC}"
if [ -d "ALL_TRACK_PHOTOS" ]; then
    photo_count=$(find ALL_TRACK_PHOTOS -name "*.jpg" -o -name "*.png" | wc -l)
    echo -e "${GREEN}   ✅ Фотографии: $photo_count файлов${NC}"
else
    echo -e "${RED}   ❌ Папка ALL_TRACK_PHOTOS не найдена${NC}"
fi

if [ -d "VOICE_TRACKS" ]; then
    audio_count=$(find VOICE_TRACKS -name "*.wav" -o -name "*.mp3" | wc -l)
    echo -e "${GREEN}   ✅ Аудио треки: $audio_count файлов${NC}"
else
    echo -e "${RED}   ❌ Папка VOICE_TRACKS не найдена${NC}"
fi

echo ""

# 4. АВТОМАТИЗАЦИЯ
echo -e "${BLUE}🔧 АВТОМАТИЗАЦИЯ:${NC}"
if [ -d "code" ]; then
    script_count=$(find code -name "*.py" | wc -l)
    echo -e "${GREEN}   ✅ Python скрипты: $script_count файлов${NC}"
    
    # Критические скрипты
    critical_scripts=(
        "code/heygen_api_automator.py"
        "code/professional_lip_sync_automation.py"
        "code/comfy_upscaler_fixed.py"
        "code/create_heygen_batch.py"
    )
    
    echo -e "${BLUE}   🎯 Критические скрипты:${NC}"
    for script in "${critical_scripts[@]}"; do
        if [ -f "$script" ]; then
            echo -e "${GREEN}      ✅ $(basename "$script")${NC}"
        else
            echo -e "${RED}      ❌ $(basename "$script")${NC}"
        fi
    done
else
    echo -e "${RED}   ❌ Папка code не найдена${NC}"
fi

echo ""

# 5. ПРОГРЕСС ПРОЕКТА
echo -e "${BLUE}📈 ПРОГРЕСС ПРОЕКТА:${NC}"
total_progress=0

# HeyGen миксы (25%)
if [ -d "HEYGEN_READY_BATCH" ]; then
    mix_count=$(find HEYGEN_READY_BATCH -name "heygen_mix_*" -type d | wc -l)
    mix_progress=$((mix_count * 25 / 20))
    total_progress=$((total_progress + mix_progress))
    echo -e "${GREEN}   ✅ HeyGen миксы: $mix_count/20 ($mix_progress%)${NC}"
fi

# Готовые видео (50%)
if [ -d "lipsync" ]; then
    video_count=$(find lipsync -name "*.mp4" -not -path "*/4k_upscaled/*" | wc -l)
    video_progress=$((video_count * 50 / 20))
    total_progress=$((total_progress + video_progress))
    echo -e "${GREEN}   ✅ Готовые видео: $video_count/20 ($video_progress%)${NC}"
fi

# 4K апскейлинг (15%)
if [ -d "lipsync/4k_upscaled" ]; then
    upscaled_count=$(find lipsync/4k_upscaled -name "*.mp4" | wc -l)
    upscaled_progress=$((upscaled_count * 15 / 20))
    total_progress=$((total_progress + upscaled_progress))
    echo -e "${GREEN}   ✅ 4K апскейлинг: $upscaled_count/20 ($upscaled_progress%)${NC}"
fi

# Автоматизация (10%)
if [ -d "code" ]; then
    total_progress=$((total_progress + 10))
    echo -e "${GREEN}   ✅ Автоматизация: 100% (10%)${NC}"
fi

echo ""
echo -e "${BLUE}🎯 ОБЩИЙ ПРОГРЕСС: ${total_progress}%${NC}"

# Прогресс бар
progress_bar=""
for i in $(seq 1 10); do
    if [ $((i * 10)) -le $total_progress ]; then
        progress_bar="${progress_bar}█"
    else
        progress_bar="${progress_bar}░"
    fi
done
echo -e "${GREEN}   [$progress_bar] $total_progress%${NC}"

echo ""

# 6. СЛЕДУЮЩИЕ ШАГИ
echo -e "${BLUE}🚀 СЛЕДУЮЩИЕ ШАГИ:${NC}"
if [ $total_progress -lt 100 ]; then
    if [ -d "HEYGEN_READY_BATCH" ]; then
        mix_count=$(find HEYGEN_READY_BATCH -name "heygen_mix_*" -type d | wc -l)
        if [ $mix_count -eq 20 ]; then
            video_count=$(find lipsync -name "*.mp4" -not -path "*/4k_upscaled/*" | wc -l)
            if [ $video_count -lt 20 ]; then
                remaining=$((20 - video_count))
                echo -e "${YELLOW}   🎬 Генерация видео: осталось $remaining видео${NC}"
                echo -e "${BLUE}   💡 Команда: cd code && python heygen_api_automator.py${NC}"
            fi
        fi
    fi
    
    if [ -d "lipsync" ]; then
        video_count=$(find lipsync -name "*.mp4" -not -path "*/4k_upscaled/*" | wc -l)
        if [ -d "lipsync/4k_upscaled" ]; then
            upscaled_count=$(find lipsync/4k_upscaled -name "*.mp4" | wc -l)
            if [ $upscaled_count -lt $video_count ]; then
                remaining=$((video_count - upscaled_count))
                echo -e "${YELLOW}   🔧 4K апскейлинг: осталось $remaining видео${NC}"
                echo -e "${BLUE}   💡 Команда: cd code && python comfy_upscaler_fixed.py${NC}"
            fi
        fi
    fi
else
    echo -e "${GREEN}   🎉 ПРОЕКТ ЗАВЕРШЕН! Все задачи выполнены!${NC}"
    echo -e "${BLUE}   📦 Создать финальный релиз${NC}"
fi

echo ""
echo "================================"
echo -e "${GREEN}🕉️ Ом Шанти. Путь ясен.${NC}"
echo "================================" 