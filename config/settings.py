"""
Конфигурация бота
"""
import os
from dataclasses import dataclass
from typing import Optional

# Загрузка переменных окружения из .env файла
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv не обязателен, переменные могут быть установлены в системе
    pass


@dataclass
class Settings:
    """Настройки приложения"""
    
    # Telegram Bot Token
    BOT_TOKEN: str
    
    # Настройки cooldown
    MESSAGE_COOLDOWN: int = 10  # секунд
    
    # Режим отладки
    DEBUG: bool = False
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Загрузка настроек из переменных окружения"""
        bot_token = os.getenv('BOT_TOKEN')
        
        if not bot_token:
            raise ValueError(
                "BOT_TOKEN не установлен! "
                "Установите переменную окружения BOT_TOKEN"
            )
        
        return cls(
            BOT_TOKEN=bot_token,
            MESSAGE_COOLDOWN=int(os.getenv('MESSAGE_COOLDOWN', '10')),
            DEBUG=os.getenv('DEBUG', 'False').lower() == 'true'
        )


# Глобальный экземпляр настроек
settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Получить настройки приложения"""
    global settings
    if settings is None:
        settings = Settings.from_env()
    return settings
