#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DaVinci Resolve Environment Setup Script
Настройка переменных окружения для работы с DaVinci Resolve API
"""

import os
import sys
import platform
from pathlib import Path

def setup_davinci_environment():
    """Настройка переменных окружения для DaVinci Resolve API"""
    
    print("🔧 Настройка окружения DaVinci Resolve API")
    print("=" * 50)
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        api_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
        lib_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
        modules_path = f"{api_path}/Modules"
        
        print("🍎 Обнаружена macOS")
        
    elif system == "windows":  # Windows
        api_path = os.path.expandvars(r"%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting")
        lib_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
        modules_path = f"{api_path}\\Modules"
        
        print("🪟 Обнаружена Windows")
        
    elif system == "linux":  # Linux
        api_path = "/opt/resolve/Developer/Scripting"
        lib_path = "/opt/resolve/libs/Fusion/fusionscript.so"
        modules_path = f"{api_path}/Modules"
        
        print("🐧 Обнаружена Linux")
        
    else:
        print(f"❌ Неподдерживаемая система: {system}")
        return False
    
    # Проверяем существование файлов
    print(f"\n📁 Проверка путей DaVinci Resolve:")
    print(f"API Path: {api_path}")
    print(f"Lib Path: {lib_path}")
    print(f"Modules Path: {modules_path}")
    
    api_exists = Path(api_path).exists()
    lib_exists = Path(lib_path).exists()
    modules_exists = Path(modules_path).exists()
    
    print(f"\n✅ API Path существует: {api_exists}")
    print(f"✅ Lib Path существует: {lib_exists}")
    print(f"✅ Modules Path существует: {modules_exists}")
    
    if not all([api_exists, lib_exists, modules_exists]):
        print("\n❌ Некоторые компоненты DaVinci Resolve не найдены!")
        print("Убедитесь что DaVinci Resolve установлен правильно")
        return False
    
    # Устанавливаем переменные окружения
    os.environ["RESOLVE_SCRIPT_API"] = api_path
    os.environ["RESOLVE_SCRIPT_LIB"] = lib_path
    
    # Добавляем к PYTHONPATH
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    if modules_path not in current_pythonpath:
        if current_pythonpath:
            new_pythonpath = f"{current_pythonpath}{os.pathsep}{modules_path}"
        else:
            new_pythonpath = modules_path
        os.environ["PYTHONPATH"] = new_pythonpath
    
    # Добавляем к sys.path для текущей сессии
    if modules_path not in sys.path:
        sys.path.insert(0, modules_path)
    
    print(f"\n✅ Переменные окружения установлены:")
    print(f"RESOLVE_SCRIPT_API = {os.environ['RESOLVE_SCRIPT_API']}")
    print(f"RESOLVE_SCRIPT_LIB = {os.environ['RESOLVE_SCRIPT_LIB']}")
    print(f"PYTHONPATH обновлен")
    
    # Тестируем импорт
    try:
        import DaVinciResolveScript as dvr_script
        print("✅ DaVinciResolveScript успешно импортирован!")
        return True
    except ImportError as e:
        print(f"❌ Не удалось импортировать DaVinciResolveScript: {e}")
        return False

def create_shell_script():
    """Создает shell скрипт для постоянной настройки переменных"""
    
    system = platform.system().lower()
    
    if system == "darwin" or system == "linux":
        # Bash script для macOS/Linux
        script_content = '''#!/bin/bash
# DaVinci Resolve Environment Setup

export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

echo "✅ DaVinci Resolve environment variables set"
'''
        
        if system == "linux":
            script_content = script_content.replace(
                "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
                "/opt/resolve/Developer/Scripting"
            ).replace(
                "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
                "/opt/resolve/libs/Fusion/fusionscript.so"
            )
        
        script_path = Path("setup_davinci_env.sh")
        
    elif system == "windows":
        # Batch script для Windows
        script_content = '''@echo off
REM DaVinci Resolve Environment Setup

set RESOLVE_SCRIPT_API=%PROGRAMDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting
set RESOLVE_SCRIPT_LIB=C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll
set PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\\Modules\\

echo ✅ DaVinci Resolve environment variables set
'''
        script_path = Path("setup_davinci_env.bat")
    
    else:
        return False
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        if system != "windows":
            os.chmod(script_path, 0o755)  # Make executable
        
        print(f"\n📄 Создан скрипт настройки: {script_path}")
        print("💡 Запустите этот скрипт перед использованием DaVinci API")
        return True
        
    except Exception as e:
        print(f"❌ Не удалось создать скрипт: {e}")
        return False

def main():
    """Основная функция"""
    print("🎬 DaVinci Resolve Environment Setup")
    print("=" * 50)
    
    # Настраиваем окружение
    if setup_davinci_environment():
        print("\n✅ Окружение настроено успешно!")
        
        # Создаем shell скрипт для будущего использования
        create_shell_script()
        
        return True
    else:
        print("\n❌ Не удалось настроить окружение")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 