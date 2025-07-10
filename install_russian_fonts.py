#!/usr/bin/env python3
"""
Установщик топовых русских креативных шрифтов для Figma
Автоматически скачивает и устанавливает лучшие коллекции русских шрифтов
"""

import os
import requests
import zipfile
import platform
from pathlib import Path
import shutil

class RussianFontsInstaller:
    def __init__(self):
        self.system = platform.system()
        self.font_dir = self.get_font_directory()
        self.temp_dir = Path("temp_fonts")
        self.temp_dir.mkdir(exist_ok=True)
    
    def get_font_directory(self):
        """Определяет директорию для установки шрифтов"""
        if self.system == "Darwin":  # macOS
            return Path.home() / "Library" / "Fonts"
        elif self.system == "Windows":
            return Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"
        else:  # Linux
            return Path.home() / ".local" / "share" / "fonts"
    
    def download_font_collection(self, url, filename):
        """Скачивает коллекцию шрифтов"""
        print(f"📥 Скачиваю {filename}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            file_path = self.temp_dir / filename
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Скачано: {filename}")
            return file_path
        except Exception as e:
            print(f"❌ Ошибка скачивания {filename}: {e}")
            return None
    
    def install_font_files(self, font_files):
        """Устанавливает файлы шрифтов"""
        installed_count = 0
        for font_file in font_files:
            try:
                if font_file.suffix.lower() in ['.ttf', '.otf']:
                    dest_path = self.font_dir / font_file.name
                    shutil.copy2(font_file, dest_path)
                    print(f"✅ Установлен: {font_file.name}")
                    installed_count += 1
            except Exception as e:
                print(f"❌ Ошибка установки {font_file.name}: {e}")
        
        return installed_count
    
    def install_top_russian_fonts(self):
        """Устанавливает топовые русские шрифты"""
        print("🎨 Установка топовых русских креативных шрифтов для Figma")
        print("=" * 60)
        
        # Список лучших русских шрифтов с прямыми ссылками
        font_collections = [
            {
                "name": "Базовая коллекция русских шрифтов",
                "fonts": [
                    "https://fonts.gstatic.com/s/ptsans/v17/jizaRExUiTo99u79D0KExcOPIDU.woff2",
                    "https://fonts.gstatic.com/s/ptserif/v18/EJRVQgYoZZs2vCFuvAFWzr-_dSb_nco.woff2",
                    "https://fonts.gstatic.com/s/philosopher/v20/vEFV2_5QCwIS4_Dhez5jcWBuT0s.woff2",
                    "https://fonts.gstatic.com/s/comfortaa/v45/1Pt_g8LJRfWJmhDAuUsSQamb1W0lwk4S4WjNPrQVIT9c2c8.woff2",
                    "https://fonts.gstatic.com/s/play/v19/6xKtrZULGlNBfMHgAaMC9Ow.woff2",
                ]
            }
        ]
        
        # Создаем локальные файлы с лучшими русскими шрифтами
        self.create_local_font_files()
        
        # Устанавливаем все найденные шрифты
        font_files = list(self.temp_dir.glob("*.ttf")) + list(self.temp_dir.glob("*.otf"))
        if font_files:
            installed = self.install_font_files(font_files)
            print(f"\n🎉 Установлено {installed} русских шрифтов!")
        
        # Очистка временных файлов
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        print("\n📋 Инструкция для Figma:")
        print("1. Перезапустите Figma")
        print("2. Шрифты появятся в списке доступных шрифтов")
        print("3. Ищите по названиям: PT Sans, PT Serif, Philosopher, Comfortaa, Play")
        
        if self.system == "Darwin":
            print("\n💡 Для macOS: Также можете использовать Font Book для управления шрифтами")
        
        return True
    
    def create_local_font_files(self):
        """Создает локальные файлы с популярными русскими шрифтами"""
        # Список ссылок на популярные русские шрифты
        font_urls = {
            # Из коллекции Google Fonts с поддержкой кириллицы
            "PT_Sans.ttf": "https://github.com/google/fonts/raw/main/ofl/ptsans/PTSans-Regular.ttf",
            "PT_Sans_Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/ptsans/PTSans-Bold.ttf",
            "PT_Serif.ttf": "https://github.com/google/fonts/raw/main/ofl/ptserif/PTSerif-Regular.ttf",
            "PT_Serif_Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/ptserif/PTSerif-Bold.ttf",
            "Philosopher.ttf": "https://github.com/google/fonts/raw/main/ofl/philosopher/Philosopher-Regular.ttf",
            "Philosopher_Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/philosopher/Philosopher-Bold.ttf",
            "Comfortaa.ttf": "https://github.com/google/fonts/raw/main/ofl/comfortaa/Comfortaa%5Bwght%5D.ttf",
            "Play.ttf": "https://github.com/google/fonts/raw/main/ofl/play/Play-Regular.ttf",
            "Play_Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/play/Play-Bold.ttf",
            "Neucha.ttf": "https://github.com/google/fonts/raw/main/ofl/neucha/Neucha-Regular.ttf",
            "BadScript.ttf": "https://github.com/google/fonts/raw/main/ofl/badscript/BadScript-Regular.ttf",
            "Cuprum.ttf": "https://github.com/google/fonts/raw/main/ofl/cuprum/Cuprum%5Bwght%5D.ttf",
        }
        
        print("📥 Скачиваю топовые русские шрифты...")
        for filename, url in font_urls.items():
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(self.temp_dir / filename, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ {filename}")
                else:
                    print(f"⚠️ Не удалось скачать {filename}")
            except Exception as e:
                print(f"❌ Ошибка {filename}: {e}")

def main():
    installer = RussianFontsInstaller()
    
    print("🎨 УСТАНОВЩИК ТОПОВЫХ РУССКИХ ШРИФТОВ")
    print("=" * 50)
    print("Этот скрипт установит лучшие русские креативные шрифты для Figma")
    print("Включает: PT Sans, PT Serif, Philosopher, Comfortaa, Play, Neucha и другие")
    print()
    
    confirm = input("Продолжить установку? (y/n): ").lower().strip()
    if confirm in ['y', 'yes', 'да', 'д']:
        installer.install_top_russian_fonts()
        print("\n🎉 Установка завершена! Перезапустите Figma для использования новых шрифтов.")
    else:
        print("Установка отменена.")

if __name__ == "__main__":
    main() 