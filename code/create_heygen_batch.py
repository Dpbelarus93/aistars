#!/usr/bin/env python3
"""
🎬 HEYGEN BATCH CREATOR - СОЗДАНИЕ 20 РЕЗУЛЬТАТОВ
================================================================

Автоматически создает 20 комбинаций фото + аудио для HeyGen
на основе плана из rap_mix_plan.txt

Автор: AI Assistant
Дата: 2025-01-07
"""

import os
import shutil
import json
from pathlib import Path

def create_heygen_batch():
    """Создает 20 готовых комбинаций для HeyGen"""
    
    # Пути к материалам
    base_path = Path("хочу еще/LIP_SYNC_WORKSPACE")
    photos_path = base_path / "input_photos"
    audio_path = base_path / "input_audio"
    output_path = Path("HEYGEN_READY_BATCH")
    
    # Создаем выходную папку
    output_path.mkdir(exist_ok=True)
    
    # План миксов из rap_mix_plan.txt
    mix_plan = [
        {"id": 1, "audio": "track_01_rap_5sec_015_70s-75s.wav", "photo": "photo_08_upscaled__00013_.png"},
        {"id": 2, "audio": "track_01_rap_5sec_015_70s-75s.wav", "photo": "photo_05_2025-05-24 23.48.19.jpg"},
        {"id": 3, "audio": "track_02_rap_5sec_012_55s-60s.wav", "photo": "photo_02_2025-05-27 02.27.10.jpg"},
        {"id": 4, "audio": "track_02_rap_5sec_012_55s-60s.wav", "photo": "photo_08_upscaled__00013_.png"},
        {"id": 5, "audio": "track_03_rap_5sec_003_10s-15s.wav", "photo": "photo_01_2025-05-27 00.17.18.jpg"},
        {"id": 6, "audio": "track_03_rap_5sec_003_10s-15s.wav", "photo": "photo_03_2025-05-26 17.52.42.jpg"},
        {"id": 7, "audio": "track_04_rap_5sec_022_105s-110s.wav", "photo": "photo_04_2025-05-27 01.30.37.jpg"},
        {"id": 8, "audio": "track_04_rap_5sec_022_105s-110s.wav", "photo": "photo_01_2025-05-27 00.17.18.jpg"},
        {"id": 9, "audio": "track_05_rap_10sec_03.wav", "photo": "photo_01_2025-05-27 00.17.18.jpg"},
        {"id": 10, "audio": "track_05_rap_10sec_03.wav", "photo": "photo_05_2025-05-24 23.48.19.jpg"},
        {"id": 11, "audio": "track_06_rap_10sec_01.wav", "photo": "photo_08_upscaled__00013_.png"},
        {"id": 12, "audio": "track_06_rap_10sec_01.wav", "photo": "photo_09_upscaled__00070_.png"},
        {"id": 13, "audio": "track_07_rap_5sec_008_35s-40s.wav", "photo": "photo_03_2025-05-26 17.52.42.jpg"},
        {"id": 14, "audio": "track_07_rap_5sec_008_35s-40s.wav", "photo": "photo_02_2025-05-27 02.27.10.jpg"},
        {"id": 15, "audio": "track_08_rap_10sec_02.wav", "photo": "photo_06_upscaled__00006_.png"},
        {"id": 16, "audio": "track_08_rap_10sec_02.wav", "photo": "photo_02_2025-05-27 02.27.10.jpg"},
        {"id": 17, "audio": "track_09_rap_5sec_020_95s-100s.wav", "photo": "photo_06_upscaled__00006_.png"},
        {"id": 18, "audio": "track_09_rap_5sec_020_95s-100s.wav", "photo": "photo_10_upscaled__00078_.png"},
        {"id": 19, "audio": "track_10_rap_5sec_018_85s-90s.wav", "photo": "photo_04_2025-05-27 01.30.37.jpg"},
        {"id": 20, "audio": "track_10_rap_5sec_018_85s-90s.wav", "photo": "photo_09_upscaled__00070_.png"},
    ]
    
    # Создаем результаты
    results = []
    success_count = 0
    
    print("🎬 СОЗДАНИЕ HEYGEN BATCH...")
    print("=" * 50)
    
    for mix in mix_plan:
        try:
            # Пути к файлам
            audio_file = audio_path / mix["audio"]
            photo_file = photos_path / mix["photo"]
            
            # Проверяем существование файлов
            if not audio_file.exists():
                print(f"❌ Аудио не найдено: {mix['audio']}")
                continue
                
            if not photo_file.exists():
                print(f"❌ Фото не найдено: {mix['photo']}")
                continue
            
            # Создаем папку для микса
            mix_folder = output_path / f"heygen_mix_{mix['id']:02d}"
            mix_folder.mkdir(exist_ok=True)
            
            # Копируем файлы с понятными именами
            new_audio = mix_folder / f"audio_{mix['id']:02d}.wav"
            new_photo = mix_folder / f"photo_{mix['id']:02d}{photo_file.suffix}"
            
            shutil.copy2(audio_file, new_audio)
            shutil.copy2(photo_file, new_photo)
            
            # Создаем инструкцию для HeyGen
            instruction = {
                "mix_id": mix["id"],
                "audio_file": f"audio_{mix['id']:02d}.wav",
                "photo_file": f"photo_{mix['id']:02d}{photo_file.suffix}",
                "original_audio": mix["audio"],
                "original_photo": mix["photo"],
                "heygen_settings": {
                    "quality": "high",
                    "voice_clone": True,
                    "lip_sync": "precise",
                    "background": "remove"
                }
            }
            
            # Сохраняем инструкцию
            with open(mix_folder / "heygen_instruction.json", "w", encoding="utf-8") as f:
                json.dump(instruction, f, indent=2, ensure_ascii=False)
            
            # Создаем README для каждого микса
            readme_content = f"""# 🎬 HEYGEN MIX {mix['id']:02d}

## 📁 ФАЙЛЫ:
- `audio_{mix['id']:02d}.wav` - аудио трек
- `photo_{mix['id']:02d}{photo_file.suffix}` - фотография
- `heygen_instruction.json` - настройки

## 🚀 ИНСТРУКЦИЯ ДЛЯ HEYGEN:
1. Загрузи фото: `photo_{mix['id']:02d}{photo_file.suffix}`
2. Загрузи аудио: `audio_{mix['id']:02d}.wav`
3. Настройки: High Quality, Precise Lip-Sync
4. Генерируй видео
5. Скачай результат как `heygen_result_{mix['id']:02d}.mp4`

## 📊 ДЕТАЛИ:
- Оригинальное аудио: {mix['audio']}
- Оригинальное фото: {mix['photo']}
- Длительность: {"5 сек" if "5sec" in mix['audio'] else "10 сек"}
"""
            
            with open(mix_folder / "README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            results.append({
                "mix_id": mix["id"],
                "status": "ready",
                "folder": str(mix_folder),
                "audio": str(new_audio),
                "photo": str(new_photo)
            })
            
            success_count += 1
            print(f"✅ Mix {mix['id']:02d}: {mix['audio']} + {mix['photo']}")
            
        except Exception as e:
            print(f"❌ Ошибка Mix {mix['id']}: {e}")
            results.append({
                "mix_id": mix["id"],
                "status": "error",
                "error": str(e)
            })
    
    # Создаем общий отчет
    report = {
        "total_mixes": len(mix_plan),
        "successful": success_count,
        "failed": len(mix_plan) - success_count,
        "output_folder": str(output_path),
        "results": results,
        "next_steps": [
            "1. Открой каждую папку heygen_mix_XX",
            "2. Загрузи файлы в HeyGen",
            "3. Генерируй видео с настройками из JSON",
            "4. Скачай результаты",
            "5. Создай вирусный контент!"
        ]
    }
    
    # Сохраняем отчет
    with open(output_path / "BATCH_REPORT.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Создаем главный README
    main_readme = f"""# 🎬 HEYGEN READY BATCH - 20 РЕЗУЛЬТАТОВ

## 📊 СТАТИСТИКА:
- Всего миксов: {len(mix_plan)}
- Готовых: {success_count}
- Ошибок: {len(mix_plan) - success_count}

## 📁 СТРУКТУРА:
```
HEYGEN_READY_BATCH/
├── heygen_mix_01/          # Mix 1
│   ├── audio_01.wav
│   ├── photo_01.jpg/png
│   ├── heygen_instruction.json
│   └── README.md
├── heygen_mix_02/          # Mix 2
│   └── ...
├── ...
├── heygen_mix_20/          # Mix 20
└── BATCH_REPORT.json       # Этот отчет
```

## 🚀 КАК ИСПОЛЬЗОВАТЬ:

### Шаг 1: Открой HeyGen
- Перейди на https://heygen.com
- Войди в аккаунт

### Шаг 2: Для каждого микса
1. Открой папку `heygen_mix_XX`
2. Загрузи фото в HeyGen
3. Загрузи аудио в HeyGen
4. Настройки: High Quality + Precise Lip-Sync
5. Генерируй видео
6. Скачай как `heygen_result_XX.mp4`

### Шаг 3: Результат
- 20 готовых lip-sync видео
- Идеально для TikTok, Instagram, YouTube
- Вирусный контент гарантирован! 🔥

## 💡 СОВЕТЫ:
- Используй высокое качество в HeyGen
- Включи точную синхронизацию губ
- Убери фон если нужно
- Сохраняй результаты в отдельную папку

---
**Создано:** {success_count} из {len(mix_plan)} миксов готовы к HeyGen! 🎯
"""
    
    with open(output_path / "README.md", "w", encoding="utf-8") as f:
        f.write(main_readme)
    
    print("\n" + "=" * 50)
    print(f"🎯 РЕЗУЛЬТАТ:")
    print(f"✅ Готово: {success_count} из {len(mix_plan)} миксов")
    print(f"📁 Папка: {output_path}")
    print(f"📋 Отчет: {output_path}/BATCH_REPORT.json")
    print("\n🚀 СЛЕДУЮЩИЙ ШАГ: Открой HeyGen и создавай видео!")
    
    return output_path, success_count

if __name__ == "__main__":
    create_heygen_batch() 