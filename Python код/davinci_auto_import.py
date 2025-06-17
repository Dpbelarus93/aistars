#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DaVinci Resolve Auto Import Script
Автоматически импортирует обработанные кадры и создает timeline

Требования:
- DaVinci Resolve должен быть запущен
- Установлены переменные окружения для DaVinci API
"""

import os
import sys
import glob
from pathlib import Path

# Добавляем путь к DaVinci Resolve API
try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    # Попытка настроить пути для API
    if sys.platform == "darwin":  # macOS
        api_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
        lib_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    elif sys.platform == "win32":  # Windows
        api_path = r"%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
        lib_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    else:  # Linux
        api_path = "/opt/resolve/Developer/Scripting/Modules"
        lib_path = "/opt/resolve/libs/Fusion/fusionscript.so"
    
    sys.path.append(api_path)
    os.environ["RESOLVE_SCRIPT_LIB"] = lib_path
    
    try:
        import DaVinciResolveScript as dvr_script
    except ImportError as e:
        print(f"❌ Ошибка: Не удается подключиться к DaVinci Resolve API: {e}")
        print("Убедитесь что:")
        print("1. DaVinci Resolve запущен")
        print("2. Настроены переменные окружения")
        sys.exit(1)

class DaVinciAutoImporter:
    def __init__(self):
        """Инициализация подключения к DaVinci Resolve"""
        try:
            self.resolve = dvr_script.scriptapp("Resolve")
            self.project_manager = self.resolve.GetProjectManager()
            self.project = self.project_manager.GetCurrentProject()
            
            if not self.project:
                print("❌ Нет открытого проекта в DaVinci Resolve")
                # Создаем новый проект
                project_name = "AI_Video_Project"
                self.project = self.project_manager.CreateProject(project_name)
                if self.project:
                    print(f"✅ Создан новый проект: {project_name}")
                else:
                    raise Exception("Не удалось создать проект")
            
            self.media_pool = self.project.GetMediaPool()
            self.media_storage = self.resolve.GetMediaStorage()
            
            print(f"✅ Подключение к DaVinci Resolve успешно")
            print(f"📁 Текущий проект: {self.project.GetName()}")
            
        except Exception as e:
            print(f"❌ Ошибка подключения к DaVinci Resolve: {e}")
            # Вместо sys.exit(1) поднимаем исключение
            raise Exception(f"DaVinci Resolve недоступен: {e}")
    
    def import_image_sequence(self, image_folder, timeline_name="AI_Generated_Video", fps=24):
        """
        Импортирует последовательность изображений и создает timeline
        
        Args:
            image_folder (str): Путь к папке с изображениями
            timeline_name (str): Имя timeline
            fps (int): Частота кадров
        """
        try:
            image_folder = Path(image_folder).resolve()
            
            if not image_folder.exists():
                print(f"❌ Папка не найдена: {image_folder}")
                return False
            
            # Поиск PNG файлов
            png_files = sorted(list(image_folder.glob("upscaled__*.png")))
            
            if not png_files:
                print(f"❌ PNG файлы не найдены в: {image_folder}")
                return False
            
            print(f"📸 Найдено {len(png_files)} изображений")
            
            # Создаем папку в Media Pool
            root_folder = self.media_pool.GetRootFolder()
            subfolder = self.media_pool.AddSubFolder(root_folder, "AI_Upscaled_Images")
            self.media_pool.SetCurrentFolder(subfolder)
            
            # Импортируем как последовательность изображений
            first_file = str(png_files[0])
            
            # Определяем паттерн для последовательности
            # upscaled__00002_.png -> upscaled__%05d_.png
            import re
            pattern_match = re.search(r'upscaled__(\d+)_\.png', first_file)
            if pattern_match:
                # Создаем паттерн для последовательности
                base_path = first_file.replace(pattern_match.group(0), "upscaled__%05d_.png")
                start_frame = int(pattern_match.group(1))
                end_frame = start_frame + len(png_files) - 1
                
                clip_info = {
                    "FilePath": base_path,
                    "StartIndex": start_frame,
                    "EndIndex": end_frame
                }
                
                # Импортируем последовательность
                media_pool_items = self.media_pool.ImportMedia([clip_info])
                
                if media_pool_items:
                    print(f"✅ Импортирована последовательность: {len(media_pool_items)} элементов")
                    
                    # Создаем timeline
                    timeline = self.media_pool.CreateTimelineFromClips(timeline_name, media_pool_items)
                    
                    if timeline:
                        print(f"✅ Создан timeline: {timeline_name}")
                        
                        # Устанавливаем как текущий timeline
                        self.project.SetCurrentTimeline(timeline)
                        
                        # Устанавливаем FPS
                        timeline_settings = {
                            "timelineFrameRate": str(fps)
                        }
                        
                        # Переходим на страницу Edit
                        self.resolve.OpenPage("edit")
                        
                        print(f"🎬 Timeline готов! FPS: {fps}")
                        return True
                    else:
                        print("❌ Не удалось создать timeline")
                        return False
                else:
                    print("❌ Не удалось импортировать изображения")
                    return False
            else:
                print("❌ Не удалось определить паттерн файлов")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка импорта: {e}")
            return False
    
    def export_timeline(self, output_path, preset_name="H.264 Master"):
        """
        Экспортирует timeline в видеофайл
        
        Args:
            output_path (str): Путь для сохранения видео
            preset_name (str): Название пресета рендера
        """
        try:
            current_timeline = self.project.GetCurrentTimeline()
            if not current_timeline:
                print("❌ Нет активного timeline")
                return False
            
            # Настройки рендера
            render_settings = {
                "SelectAllFrames": True,
                "TargetDir": str(Path(output_path).parent),
                "CustomName": Path(output_path).stem,
                "VideoQuality": "High"
            }
            
            # Устанавливаем настройки
            if self.project.SetRenderSettings(render_settings):
                print("✅ Настройки рендера установлены")
                
                # Добавляем задачу рендера
                job_id = self.project.AddRenderJob()
                if job_id:
                    print(f"✅ Задача рендера добавлена: {job_id}")
                    
                    # Запускаем рендер
                    if self.project.StartRendering([job_id]):
                        print("🎬 Рендер запущен!")
                        return True
                    else:
                        print("❌ Не удалось запустить рендер")
                        return False
                else:
                    print("❌ Не удалось добавить задачу рендера")
                    return False
            else:
                print("❌ Не удалось установить настройки рендера")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка экспорта: {e}")
            return False

def main():
    """Основная функция"""
    print("🎬 DaVinci Resolve Auto Import Script")
    print("=" * 50)
    
    # Определяем пути
    current_dir = Path(__file__).parent.parent
    upscaled_dir = current_dir / "upscaled_images"
    output_dir = current_dir / "final_video"
    output_dir.mkdir(exist_ok=True)
    
    # Создаем импортер
    importer = DaVinciAutoImporter()
    
    # Импортируем изображения и создаем timeline
    success = importer.import_image_sequence(
        image_folder=upscaled_dir,
        timeline_name="AI_Generated_Scene",
        fps=24
    )
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Импорт завершен успешно!")
        print("🎬 Timeline создан в DaVinci Resolve")
        print("💡 Можете продолжить редактирование в DaVinci Resolve")
        
        # Опционально - автоматический экспорт
        export_choice = input("\n🤔 Хотите автоматически экспортировать видео? (y/n): ")
        if export_choice.lower() in ['y', 'yes', 'да']:
            output_file = output_dir / "ai_generated_video.mp4"
            importer.export_timeline(output_file)
    else:
        print("❌ Импорт не удался")
        sys.exit(1)

if __name__ == "__main__":
    main() 