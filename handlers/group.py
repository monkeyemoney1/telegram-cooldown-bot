"""
Обработчики для групповых чатов
"""
import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER

logger = logging.getLogger(__name__)

# Создаем роутер для групповых чатов
group_router = Router(name="group")


@group_router.message()
async def handle_group_message(message: Message):
    """
    Базовый обработчик всех сообщений в группах.
    Cooldown middleware автоматически обрабатывает ограничения.
    
    Здесь можно добавить дополнительную логику обработки сообщений.
    """
    # Пропускаем служебные сообщения
    if not message.text:
        return
    
    # Логируем сообщение
    logger.debug(
        f"Сообщение от {message.from_user.id} "
        f"в чате {message.chat.id}: {message.text[:50]}"
    )
    
    # Здесь можно добавить дополнительную логику:
    # - Модерация контента
    # - Автоответы
    # - Команды
    # - Статистика и т.д.
