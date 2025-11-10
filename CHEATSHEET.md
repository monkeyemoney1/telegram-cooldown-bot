# Шпаргалка команд

## 🚀 Быстрый старт

```bash
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
cp .env.example .env
# Затем отредактируйте .env и добавьте BOT_TOKEN

# 5. Проверить установку
python check_setup.py

# 6. Запустить бота
python main.py
```

## 📝 Git команды

```bash
# Инициализация репозитория
git init
git add .
git commit -m "Initial commit"

# Добавление удаленного репозитория
git remote add origin https://github.com/username/repo.git
git branch -M main
git push -u origin main

# Обновление кода
git add .
git commit -m "Описание изменений"
git push
```

## 🔧 Работа с виртуальным окружением

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1
deactivate

# Windows CMD
venv\Scripts\activate.bat
deactivate

# Linux/Mac
source venv/bin/activate
deactivate
```

## 📦 Управление зависимостями

```bash
# Установка всех зависимостей
pip install -r requirements.txt

# Добавление новой зависимости
pip install package_name
pip freeze > requirements.txt

# Обновление зависимостей
pip install --upgrade -r requirements.txt
```

## 🤖 Telegram BotFather команды

```
/newbot          - Создать нового бота
/mybots          - Список ваших ботов
/token           - Получить токен бота
/setdescription  - Установить описание
/setabouttext    - Установить текст "О боте"
/setcommands     - Установить список команд
/deletebot       - Удалить бота
```

## 🌐 Render команды (через CLI)

```bash
# Установка Render CLI
npm install -g render

# Вход
render login

# Деплой
render deploy

# Просмотр логов
render logs

# Список сервисов
render services list
```

## 🐛 Отладка

```bash
# Запуск с отладкой
# Установите в .env: DEBUG=True
python main.py

# Проверка переменных окружения (Windows)
echo $env:BOT_TOKEN

# Проверка переменных окружения (Linux/Mac)
echo $BOT_TOKEN

# Просмотр логов в реальном времени
# На Render: Dashboard → Logs
```

## 📊 Полезные Python команды

```bash
# Проверка версии Python
python --version

# Проверка установленных пакетов
pip list

# Информация о пакете
pip show aiogram

# Создание requirements.txt из установленных пакетов
pip freeze > requirements.txt

# Очистка кеша pip
pip cache purge
```

## 🔍 Проверка проекта

```bash
# Проверка окружения
python check_setup.py

# Проверка синтаксиса Python
python -m py_compile main.py

# Проверка импортов
python -c "import aiogram; print(aiogram.__version__)"
```

## 🎯 Структура команд бота

В Telegram отправьте боту:

```
/start    - Приветствие
/help     - Справка
/status   - Статус (только админы)
```

## 📁 Навигация по файлам проекта

```
main.py              - Основной файл (polling)
main_webhook.py      - Webhook версия (для Render)
config/settings.py   - Настройки и конфигурация
handlers/commands.py - Обработчики команд
handlers/group.py    - Обработчики для групп
middlewares/cooldown.py - Middleware таймера
```

## 🔐 Переменные окружения (.env)

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MESSAGE_COOLDOWN=10
DEBUG=False
```

## 🚨 Частые проблемы

### "BOT_TOKEN не установлен"
```bash
# Проверьте .env файл
cat .env  # Linux/Mac
type .env # Windows

# Убедитесь что venv активирован
# Должно быть (venv) в начале строки
```

### "Не удается разрешить импорт aiogram"
```bash
# Переустановите зависимости
pip install --force-reinstall -r requirements.txt
```

### Бот не удаляет сообщения в группе
```
1. Сделайте бота администратором группы
2. Дайте права "Delete messages"
```

### Render: приложение не запускается
```
1. Проверьте логи на Render
2. Убедитесь что BOT_TOKEN установлен в Environment
3. Проверьте Start Command (должен быть: python main.py)
```

## 📚 Документация

- **README.md** - Полная документация
- **QUICKSTART.md** - Быстрый старт для новичков
- **RENDER_DEPLOY.md** - Деплой на Render
- **EXAMPLES.md** - Примеры расширения
- **PROJECT_STRUCTURE.md** - Структура проекта

## 🔗 Полезные ссылки

- Aiogram Docs: https://docs.aiogram.dev/
- Telegram Bot API: https://core.telegram.org/bots/api
- Render Docs: https://render.com/docs
- Python Docs: https://docs.python.org/

## 💡 Советы

```bash
# Всегда работайте в виртуальном окружении
python -m venv venv

# Храните секреты в .env, не в коде
# НИКОГДА не коммитьте .env в git

# Используйте осмысленные commit messages
git commit -m "Add spam filter feature"

# Регулярно обновляйте зависимости
pip install --upgrade aiogram
```

## ⚡ Быстрые тесты

```bash
# Тест 1: Проверка Python
python --version
# Ожидается: Python 3.11+

# Тест 2: Проверка aiogram
python -c "import aiogram; print('OK')"
# Ожидается: OK

# Тест 3: Проверка .env
python -c "from config.settings import get_settings; s = get_settings(); print('OK')"
# Ожидается: OK

# Тест 4: Запуск бота (Ctrl+C для остановки)
python main.py
# Ожидается: "Бот запущен: @..."
```

---

**Сохраните эту шпаргалку для быстрого доступа к командам! 📌**
