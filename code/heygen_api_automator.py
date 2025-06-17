#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 HEYGEN API AUTOMATOR - ПОЛНАЯ АВТОМАТИЗАЦИЯ
============================================================

Этот скрипт автоматически создает видео в HeyGen, используя API.

ВАЖНО: Этот скрипт НЕ загружает файлы напрямую. Он использует
заранее созданные Photo Avatars и аудио, доступные по URL.

Автор: AI Assistant (Джимми)
Дата: 2025-01-07
"""

import os
import time
import requests
import json
from pathlib import Path

# --- ⚙️ НАСТРОЙКИ - ЗАПОЛНИТЕ ВРУЧНУЮ ⚙️ ---

# 1. Ваш API ключ из HeyGen (Настройки -> Subscriptions -> HeyGen API)
HEYGEN_API_KEY = "YOUR_HEYGEN_API_KEY_HERE"

# 2. ID ваших Photo Avatars (Нужно загрузить фото в HeyGen и получить ID)
#    Замените 'photo_name.jpg' на имя файла, а 'avatar_id_goes_here' на ID из HeyGen
AVATAR_IDS = {
    "photo_01_2025-05-27 00.17.18.jpg": "avatar_id_goes_here",
    "photo_02_2025-05-27 02.27.10.jpg": "avatar_id_goes_here",
    "photo_03_2025-05-26 17.52.42.jpg": "avatar_id_goes_here",
    "photo_04_2025-05-27 01.30.37.jpg": "avatar_id_goes_here",
    "photo_05_2025-05-24 23.48.19.jpg": "avatar_id_goes_here",
    "photo_06_upscaled__00006_.png": "avatar_id_goes_here",
    "photo_08_upscaled__00013_.png": "avatar_id_goes_here",
    "photo_09_upscaled__00070_.png": "avatar_id_goes_here",
    "photo_10_upscaled__00078_.png": "avatar_id_goes_here",
}

# 3. URL, где будут временно храниться аудиофайлы.
#    ВАЖНО: Аудиофайлы должны быть доступны по публичной ссылке!
#    Например, вы можете загрузить их на Amazon S3, Google Cloud Storage
#    или любой другой хостинг.
#    Пример: "https://your-temp-storage.com/audio/"
BASE_AUDIO_URL = "YOUR_PUBLIC_AUDIO_URL_HERE" 

# ----------------------------------------------------

API_BASE_URL = "https://api.heygen.com"
HEADERS = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json"
}

def generate_video(mix_info):
    """
    Отправляет запрос на генерацию видео в HeyGen.
    """
    avatar_id = AVATAR_IDS.get(mix_info["photo"])
    if not avatar_id or "avatar_id_goes_here" in avatar_id:
        print(f"❌ Ошибка: Не найден или не указан Avatar ID для фото {mix_info['photo']}")
        return None, f"Avatar ID not configured for {mix_info['photo']}"

    audio_url = f"{BASE_AUDIO_URL.rstrip('/')}/{mix_info['audio']}"
    
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                },
                "voice": {
                    "type": "audio",
                    "audio_url": audio_url
                }
            }
        ],
        "test": True,  # Создает тестовое видео (обычно быстрее и не тратит кредиты)
        "dimension": {
            "width": 1080,
            "height": 1920 # Вертикальный формат для соцсетей
        }
    }

    try:
        response = requests.post(f"{API_BASE_URL}/v2/video/generate", headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            return None, data["error"]["message"]
        
        video_id = data["data"]["video_id"]
        print(f"✅ Запрос на генерацию отправлен. Mix ID: {mix_info['id']}, Video ID: {video_id}")
        return video_id, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка API запроса: {e}")
        return None, str(e)


def check_video_status(video_id):
    """
    Проверяет статус генерации видео и скачивает его по готовности.
    """
    status_url = f"{API_BASE_URL}/v1/video_status.get?video_id={video_id}"
    
    while True:
        try:
            response = requests.get(status_url, headers={"X-Api-Key": HEYGEN_API_KEY})
            response.raise_for_status()
            data = response.json().get("data", {})
            status = data.get("status")

            if status == "completed":
                print(f"✅ Видео {video_id} готово! Скачиваю...")
                video_url = data.get("video_url")
                if video_url:
                    video_content = requests.get(video_url).content
                    return video_content, None
                else:
                    return None, "Video URL not found in completed status."
            elif status in ("processing", "pending"):
                print(f"⏳ Видео {video_id} в обработке. Статус: {status}. Жду 15 секунд...")
                time.sleep(15)
            elif status == "failed":
                error_message = data.get("error", {}).get("message", "Unknown error")
                print(f"❌ Генерация видео {video_id} провалена. Ошибка: {error_message}")
                return None, error_message
            else:
                print(f"❓ Неизвестный статус {status} для видео {video_id}.")
                time.sleep(15)
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при проверке статуса: {e}")
            return None, str(e)


def main():
    """
    Основной цикл для автоматизации создания 20 видео.
    """
    if "YOUR_HEYGEN_API_KEY_HERE" in HEYGEN_API_KEY or "YOUR_PUBLIC_AUDIO_URL_HERE" in BASE_AUDIO_URL:
        print("🛑 ОСТАНОВКА: Пожалуйста, укажите ваш HEYGEN_API_KEY и BASE_AUDIO_URL в настройках скрипта.")
        return

    # Загружаем план из HEYGEN_READY_BATCH
    report_path = Path("HEYGEN_READY_BATCH/BATCH_REPORT.json")
    if not report_path.exists():
        print(f"❌ Не найден файл отчета: {report_path}")
        return
        
    with open(report_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)

    mix_plan = [
        {"id": mix["mix_id"], "audio": Path(mix["audio"]).name, "photo": Path(mix["photo"]).name}
        for mix in report_data.get("results", []) if mix["status"] == "ready"
    ]

    output_dir = Path("HEYGEN_API_RESULTS")
    output_dir.mkdir(exist_ok=True)
    
    print(f"🚀 Начинаю автоматическую генерацию {len(mix_plan)} видео...")
    print("=" * 60)
    
    for mix in mix_plan:
        print(f"\n--- Работаю над Mix #{mix['id']} ---")
        
        # 1. Отправляем запрос на генерацию
        video_id, error = generate_video(mix)
        if error:
            print(f"❌ Не удалось запустить генерацию для Mix #{mix['id']}. Причина: {error}")
            continue
            
        # 2. Ждем и скачиваем видео
        video_data, error = check_video_status(video_id)
        if error:
            print(f"❌ Не удалось получить видео для Mix #{mix['id']}. Причина: {error}")
            continue
            
        # 3. Сохраняем результат
        output_file = output_dir / f"heygen_result_{mix['id']:02d}.mp4"
        with open(output_file, 'wb') as f:
            f.write(video_data)
        print(f"💾 Видео для Mix #{mix['id']} сохранено в: {output_file}")
        
    print("\n" + "=" * 60)
    print("🎉 Все задачи выполнены!")
    print(f"📂 Готовые видео находятся в папке: {output_dir}")


if __name__ == "__main__":
    main() 