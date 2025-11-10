"""
Обработчики общих команд
"""
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)

# Создаем роутер для команд
command_router = Router(name="commands")


@command_router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start"""
    welcome_text = (
        "👋 Привет! Я бот для управления группами.\n\n"
        "Основные функции:\n"
        "⏱ Контроль частоты сообщений (cooldown)\n"
        "🛡 Защита от спама\n\n"
        "Добавь меня в группу и дай права администратора "
        "для полноценной работы!"
    )
    await message.answer(welcome_text)


@command_router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработка команды /help"""
    help_text = (
        "📚 Помощь по использованию бота\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/status - Показать статус бота (только для админов)\n\n"
        "В группах бот автоматически:\n"
        "• Ограничивает частоту сообщений от пользователей\n"
        "• Удаляет сообщения, отправленные слишком часто\n"
        "• Уведомляет пользователей о необходимости подождать\n"
    )
    await message.answer(help_text)


@command_router.message(Command("status"))
async def cmd_status(message: Message):
    """Обработка команды /status (для админов)"""
    # Проверяем, является ли пользователь администратором
    if message.chat.type == "private":
        await message.answer("Эта команда работает только в группах.")
        return
    
    try:
        member = await message.chat.get_member(message.from_user.id)
        is_admin = member.status in ["creator", "administrator"]
        
        if not is_admin:
            await message.answer("⛔️ Эта команда доступна только администраторам.")
            return
        
        status_text = (
            "✅ Бот работает нормально\n\n"
            f"📊 Статус:\n"
            f"• Чат: {message.chat.title}\n"
            f"• ID чата: {message.chat.id}\n"
            f"• Cooldown: активен\n"
        )
        await message.answer(status_text)
        
    except Exception as e:
        logger.error(f"Ошибка при проверке статуса: {e}")
        await message.answer("❌ Ошибка при получении статуса.")
