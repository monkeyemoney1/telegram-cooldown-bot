"""
Middleware для контроля таймаута между сообщениями пользователей
"""
import time
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)


class CooldownMiddleware(BaseMiddleware):
    """
    Middleware для ограничения частоты сообщений от пользователей в группах.
    
    Хранит время последнего сообщения каждого пользователя в каждом чате.
    Если пользователь пытается отправить сообщение раньше cooldown периода,
    сообщение удаляется и отправляется предупреждение.
    """
    
    def __init__(self, cooldown_seconds: int = 10):
        """
        Args:
            cooldown_seconds: Минимальное время между сообщениями в секундах
        """
        super().__init__()
        self.cooldown_seconds = cooldown_seconds
        # Словарь для хранения времени последнего сообщения
        # Структура: {chat_id: {user_id: timestamp}}
        self.user_last_message: Dict[int, Dict[int, float]] = {}
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обработка входящего сообщения
        
        Args:
            handler: Следующий обработчик в цепочке
            event: Объект сообщения
            data: Дополнительные данные
        
        Returns:
            Результат обработки или None если сообщение заблокировано
        """
        # Пропускаем обработку для приватных чатов
        if event.chat.type == "private":
            return await handler(event, data)
        
        # Пропускаем служебные сообщения
        if not event.from_user:
            return await handler(event, data)
        
        chat_id = event.chat.id
        user_id = event.from_user.id
        current_time = time.time()
        
        # Инициализируем словарь для чата если его нет
        if chat_id not in self.user_last_message:
            self.user_last_message[chat_id] = {}
        
        # Проверяем время последнего сообщения пользователя
        if user_id in self.user_last_message[chat_id]:
            last_message_time = self.user_last_message[chat_id][user_id]
            time_passed = current_time - last_message_time
            
            # Если прошло меньше времени чем cooldown
            if time_passed < self.cooldown_seconds:
                try:
                    # Удаляем сообщение пользователя
                    await event.delete()
                    
                    # Отправляем предупреждение с обратным отсчетом
                    wait_time = int(self.cooldown_seconds - time_passed)
                    
                    # Имя пользователя для персонализации
                    user_name = event.from_user.first_name or "Пользователь"
                    
                    warning_msg = await event.answer(
                        f"⏱ {user_name}, подожди еще <b>{wait_time}</b> сек.",
                        reply_to_message_id=None
                    )
                    
                    # Обновляем сообщение каждую секунду
                    import asyncio
                    for remaining in range(wait_time - 1, 0, -1):
                        await asyncio.sleep(1)
                        try:
                            await warning_msg.edit_text(
                                f"⏱ {user_name}, подожди еще <b>{remaining}</b> сек."
                            )
                        except Exception:
                            break  # Если сообщение удалено, прекращаем обновление
                    
                    # Финальное сообщение
                    await asyncio.sleep(1)
                    try:
                        await warning_msg.edit_text(
                            f"✅ {user_name}, теперь можешь отправлять сообщения!"
                        )
                        # Удаляем через 3 секунды
                        await asyncio.sleep(3)
                        await warning_msg.delete()
                    except Exception:
                        pass
                    
                    logger.info(
                        f"Сообщение от {user_id} в чате {chat_id} "
                        f"заблокировано (cooldown: {wait_time}s)"
                    )
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке cooldown: {e}")
                
                # Блокируем дальнейшую обработку
                return None
        
        # Обновляем время последнего сообщения
        self.user_last_message[chat_id][user_id] = current_time
        
        # Продолжаем обработку
        return await handler(event, data)
    
    def clear_user_cooldown(self, chat_id: int, user_id: int) -> None:
        """
        Очистка cooldown для конкретного пользователя
        
        Args:
            chat_id: ID чата
            user_id: ID пользователя
        """
        if chat_id in self.user_last_message:
            self.user_last_message[chat_id].pop(user_id, None)
    
    def clear_chat_cooldowns(self, chat_id: int) -> None:
        """
        Очистка всех cooldown в чате
        
        Args:
            chat_id: ID чата
        """
        self.user_last_message.pop(chat_id, None)


# Расширение для Message для удаления с задержкой
async def delete_with_delay(message: Message, delay: int = 5):
    """
    Удалить сообщение с задержкой
    
    Args:
        message: Сообщение для удаления
        delay: Задержка в секундах
    """
    import asyncio
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass  # Игнорируем ошибки при удалении


# Добавляем метод к классу Message
Message.delete_with_delay = delete_with_delay
