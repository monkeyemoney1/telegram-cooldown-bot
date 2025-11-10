"""
Основной файл приложения Telegram бота
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.settings import get_settings
from middlewares import CooldownMiddleware
from handlers import command_router, group_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    
    # Загружаем настройки
    try:
        settings = get_settings()
        logger.info("Настройки успешно загружены")
    except ValueError as e:
        logger.error(f"Ошибка загрузки настроек: {e}")
        sys.exit(1)
    
    # Устанавливаем уровень логирования
    if settings.DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Режим отладки включен")
    
    # Инициализируем бот и диспетчер
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    # Подключаем middleware для cooldown
    cooldown_middleware = CooldownMiddleware(
        cooldown_seconds=settings.MESSAGE_COOLDOWN
    )
    dp.message.middleware(cooldown_middleware)
    logger.info(f"Cooldown middleware подключен ({settings.MESSAGE_COOLDOWN}s)")
    
    # Регистрируем роутеры
    dp.include_router(command_router)
    dp.include_router(group_router)
    logger.info("Роутеры зарегистрированы")
    
    # Удаляем webhook и запускаем polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook удален")
        
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        logger.info(f"Бот запущен: @{bot_info.username}")
        logger.info(f"ID бота: {bot_info.id}")
        
        # Запускаем polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)
