"""
Вариант main.py для работы в webhook режиме на Render
Используйте этот файл вместо обычного main.py при деплое на Render
"""
import asyncio
import logging
import sys
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

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

# Константы для webhook
WEBHOOK_PATH = "/webhook"
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL", "https://your-app.onrender.com")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Порт для Render (обязательно использовать переменную PORT)
PORT = int(os.getenv("PORT", 10000))


async def on_startup(app: web.Application):
    """Действия при запуске приложения"""
    bot: Bot = app["bot"]
    
    # Устанавливаем webhook
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )
    
    # Получаем информацию о боте
    bot_info = await bot.get_me()
    logger.info(f"Бот запущен: @{bot_info.username}")
    logger.info(f"ID бота: {bot_info.id}")
    logger.info(f"Webhook установлен: {WEBHOOK_URL}")


async def on_shutdown(app: web.Application):
    """Действия при остановке приложения"""
    bot: Bot = app["bot"]
    
    # Удаляем webhook
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    
    logger.info("Бот остановлен")


def create_app() -> web.Application:
    """Создание и настройка приложения"""
    
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
    
    # Создаем веб-приложение
    app = web.Application()
    
    # Добавляем бота в контекст приложения
    app["bot"] = bot
    
    # Регистрируем обработчики запуска и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    # Настраиваем webhook handler
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path=WEBHOOK_PATH)
    
    # Настраиваем приложение для работы с aiogram
    setup_application(app, dp, bot=bot)
    
    return app


# Обработчик для health check от Render
async def health_check(request):
    """Endpoint для проверки работоспособности"""
    return web.Response(text="OK", status=200)


def main():
    """Главная функция запуска бота"""
    try:
        # Создаем приложение
        app = create_app()
        
        # Добавляем health check endpoint
        app.router.add_get("/health", health_check)
        app.router.add_get("/", health_check)  # Для главной страницы
        
        logger.info(f"Запуск веб-сервера на порту {PORT}")
        
        # Запускаем сервер
        web.run_app(
            app,
            host="0.0.0.0",
            port=PORT
        )
        
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
