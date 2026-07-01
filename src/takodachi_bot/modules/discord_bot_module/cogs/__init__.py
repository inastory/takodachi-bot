from takodachi_bot.modules.discord_bot_module.cogs import on_ready
from takodachi_bot.modules.discord_bot_module.cogs import test
from takodachi_bot.modules.discord_bot_module.cogs import sync_commands
from takodachi_bot.modules.discord_bot_module.cogs import archive

__all__ = [
    "on_ready",
    "test",
    "sync_commands",
    "archive",
]


def get_modules():
    return [on_ready, test, sync_commands, archive]
