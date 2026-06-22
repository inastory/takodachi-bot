# Declare top-level shortcuts
from .base_service import BaseService

from .app_module.service import AppIconService

from .discord_bot_module.service import DiscordBotService
from .volume_control_module.service import VolumeControlService

from .services_manager import ServicesManager

__all__=[
    "ServicesManager",
    "BaseService",
    "AppIconService",
    "DiscordBotService",
    "VolumeControlService",
]