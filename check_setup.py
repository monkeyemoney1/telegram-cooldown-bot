"""
Скрипт для проверки окружения и зависимостей
"""
import sys
import os

def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    print(f"✓ Python версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("⚠ Рекомендуется Python 3.11 или выше")
        return False
    return True

def check_dependencies():
    """Проверка установленных зависимостей"""
    dependencies = {
        'aiogram': '3.4.0',
        'dotenv': '1.0.0',
    }
    
    all_ok = True
    for package, min_version in dependencies.items():
        try:
            if package == 'dotenv':
                import importlib
                mod = importlib.import_module('dotenv')
            else:
                mod = __import__(package)
            
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {package} установлен (версия: {version})")
        except ImportError:
            print(f"✗ {package} НЕ установлен")
            all_ok = False
    
    return all_ok

def check_env_file():
    """Проверка наличия .env файла"""
    if os.path.exists('.env'):
        print("✓ Файл .env найден")
        
        # Проверка наличия BOT_TOKEN
        with open('.env', 'r') as f:
            content = f.read()
            if 'BOT_TOKEN=' in content and 'your_bot_token_here' not in content:
                print("✓ BOT_TOKEN настроен")
                return True
            else:
                print("⚠ BOT_TOKEN не настроен в .env")
                return False
    else:
        print("✗ Файл .env не найден")
        print("  Скопируйте .env.example в .env и настройте токен")
        return False

def check_structure():
    """Проверка структуры проекта"""
    required_dirs = ['config', 'handlers', 'middlewares']
    required_files = ['main.py', 'requirements.txt']
    
    all_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Папка {directory}/ найдена")
        else:
            print(f"✗ Папка {directory}/ НЕ найдена")
            all_ok = False
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ Файл {file} найден")
        else:
            print(f"✗ Файл {file} НЕ найден")
            all_ok = False
    
    return all_ok

def main():
    """Главная функция проверки"""
    print("=" * 50)
    print("Проверка окружения Telegram бота")
    print("=" * 50)
    
    print("\n1. Проверка Python:")
    python_ok = check_python_version()
    
    print("\n2. Проверка зависимостей:")
    deps_ok = check_dependencies()
    
    print("\n3. Проверка конфигурации:")
    env_ok = check_env_file()
    
    print("\n4. Проверка структуры проекта:")
    structure_ok = check_structure()
    
    print("\n" + "=" * 50)
    
    if python_ok and deps_ok and env_ok and structure_ok:
        print("✅ Все проверки пройдены!")
        print("\nМожете запустить бота командой:")
        print("  python main.py")
    else:
        print("⚠ Обнаружены проблемы!")
        
        if not deps_ok:
            print("\nУстановите зависимости:")
            print("  pip install -r requirements.txt")
        
        if not env_ok:
            print("\nНастройте файл .env:")
            print("  1. Скопируйте .env.example в .env")
            print("  2. Получите токен у @BotFather в Telegram")
            print("  3. Укажите токен в .env")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
