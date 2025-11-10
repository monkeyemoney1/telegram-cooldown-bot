# Примеры расширения функционала

Этот файл содержит примеры того, как можно расширить бота новыми функциями.

## Пример 1: Добавление команды с аргументами

Создайте новую команду в `handlers/commands.py`:

```python
from aiogram.filters import Command, CommandObject

@command_router.message(Command("settimeout"))
async def cmd_set_timeout(message: Message, command: CommandObject):
    """Установка cooldown (только для админов)"""
    # Проверка прав администратора
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["creator", "administrator"]:
        await message.answer("⛔️ Эта команда доступна только администраторам.")
        return
    
    # Получение аргумента команды
    if not command.args:
        await message.answer("Использование: /settimeout <секунды>")
        return
    
    try:
        timeout = int(command.args)
        if timeout < 1 or timeout > 60:
            await message.answer("Таймаут должен быть от 1 до 60 секунд.")
            return
        
        # Здесь можно обновить настройки cooldown
        await message.answer(f"✅ Таймаут установлен: {timeout} секунд")
    except ValueError:
        await message.answer("❌ Неверный формат. Укажите число.")
```

## Пример 2: Фильтр по типу чата

Добавьте обработчик только для групп в `handlers/group.py`:

```python
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.enums import ChatType

# Обработчик только для супергрупп
@group_router.message(F.chat.type.in_(["group", "supergroup"]))
async def handle_only_groups(message: Message):
    # Логика только для групп
    pass
```

## Пример 3: Middleware для логирования

Создайте `middlewares/logging.py`:

```python
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования всех сообщений"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger.info(
            f"Message from {event.from_user.id} "
            f"in chat {event.chat.id}: {event.text[:50]}"
        )
        return await handler(event, data)
```

Подключите в `main.py`:

```python
from middlewares.logging import LoggingMiddleware
dp.message.middleware(LoggingMiddleware())
```

## Пример 4: Обработка callback кнопок

Добавьте в `handlers/commands.py`:

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters.callback_data import CallbackData

class SettingsCallback(CallbackData, prefix="settings"):
    action: str
    value: int

@command_router.message(Command("settings"))
async def cmd_settings(message: Message):
    """Настройки с кнопками"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="5 сек",
                callback_data=SettingsCallback(action="timeout", value=5).pack()
            ),
            InlineKeyboardButton(
                text="10 сек",
                callback_data=SettingsCallback(action="timeout", value=10).pack()
            ),
            InlineKeyboardButton(
                text="30 сек",
                callback_data=SettingsCallback(action="timeout", value=30).pack()
            ),
        ]
    ])
    await message.answer("Выберите таймаут:", reply_markup=keyboard)

@command_router.callback_query(SettingsCallback.filter())
async def handle_settings(callback: CallbackQuery, callback_data: SettingsCallback):
    """Обработка нажатий на кнопки"""
    await callback.message.edit_text(
        f"Таймаут установлен: {callback_data.value} секунд"
    )
    await callback.answer()
```

## Пример 5: Фильтр слов (антиспам)

Создайте `handlers/moderation.py`:

```python
from aiogram import Router, F
from aiogram.types import Message
import re

moderation_router = Router(name="moderation")

# Список запрещенных слов
BANNED_WORDS = ["спам", "реклама", "купить"]

@moderation_router.message(F.text)
async def check_spam(message: Message):
    """Проверка на запрещенные слова"""
    if not message.text:
        return
    
    text_lower = message.text.lower()
    
    for word in BANNED_WORDS:
        if word in text_lower:
            await message.delete()
            warning = await message.answer(
                f"⚠️ Сообщение удалено: содержит запрещенное слово"
            )
            # Удаляем предупреждение через 5 секунд
            import asyncio
            await asyncio.sleep(5)
            await warning.delete()
            return
```

Не забудьте добавить в `main.py`:

```python
from handlers.moderation import moderation_router
dp.include_router(moderation_router)
```

## Пример 6: Сохранение статистики

Создайте `handlers/stats.py`:

```python
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from collections import defaultdict

stats_router = Router(name="stats")

# Хранилище статистики (в памяти)
message_stats = defaultdict(int)

@stats_router.message()
async def count_messages(message: Message):
    """Подсчет сообщений"""
    user_id = message.from_user.id
    message_stats[user_id] += 1

@stats_router.message(Command("mystats"))
async def show_stats(message: Message):
    """Показать статистику пользователя"""
    user_id = message.from_user.id
    count = message_stats.get(user_id, 0)
    await message.answer(
        f"📊 Ваша статистика:\n"
        f"Отправлено сообщений: {count}"
    )
```

## Пример 7: База данных (SQLite)

Создайте `database/db.py`:

```python
import sqlite3
from typing import Optional

class Database:
    def __init__(self, db_path: str = "bot.db"):
        self.db_path = db_path
        self.create_tables()
    
    def create_tables(self):
        """Создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    message_count INTEGER DEFAULT 0
                )
            """)
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Получить пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM users WHERE user_id = ?", 
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "user_id": row[0],
                    "username": row[1],
                    "message_count": row[2]
                }
        return None
    
    def add_user(self, user_id: int, username: str):
        """Добавить пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )
    
    def increment_messages(self, user_id: int):
        """Увеличить счетчик сообщений"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET message_count = message_count + 1 WHERE user_id = ?",
                (user_id,)
            )
```

Используйте в handlers:

```python
from database.db import Database

db = Database()

@router.message()
async def track_messages(message: Message):
    db.add_user(message.from_user.id, message.from_user.username)
    db.increment_messages(message.from_user.id)
```

## Пример 8: Расписание задач

Добавьте в `main.py`:

```python
import asyncio
from datetime import datetime

async def scheduled_task(bot: Bot):
    """Задача, выполняемая по расписанию"""
    while True:
        # Выполняем каждые 24 часа
        await asyncio.sleep(86400)
        
        # Отправка сообщения админу
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📊 Ежедневный отчет на {datetime.now()}"
        )

# В функции main():
asyncio.create_task(scheduled_task(bot))
```

---

Используйте эти примеры как основу для расширения вашего бота! 🚀
