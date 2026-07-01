import asyncio

if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    )

import takodachi_bot.configs as configs
from takodachi_bot.modules.base_service import BaseService
from takodachi_bot.modules.discord_bot_module.discord_bot import DiscordBot


class DiscordBotService(BaseService):
    def __init__(self):
        super().__init__()
        self._discord_loop = asyncio.new_event_loop()
        self.discord_bot = DiscordBot()

    def start_service(self):
        if self.is_running():
            return
        super().start_service()
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.start(str(configs.BOT_TOKEN)), self._discord_loop
        )
        self._discord_loop.run_forever()

    def stop_service(self):
        if not self.is_running():
            return
        super().stop_service()
        asyncio.run_coroutine_threadsafe(
            self.discord_bot.close(), self._discord_loop
        ).result()
        self.discord_bot.clear()
        print("Discord bot stopped")
        self._discord_loop.stop()

    def is_running(self) -> bool:
        return super().is_running()

    def notify(self, message):
        if self.is_running():
            asyncio.run_coroutine_threadsafe(
                self.discord_bot.send_message_to_channel(
                    configs.DISCORD_EXCEPTION_CHANNEL_ID, message
                ),
                self._discord_loop,
            ).result()


if __name__ == "__main__":
    from logging.config import fileConfig

    fileConfig(
        configs.LOGGER_CONFIGS_PATH, disable_existing_loggers=False, encoding="utf-8"
    )
    discord_bot_service = DiscordBotService()
    try:
        discord_bot_service.start_service()
    except KeyboardInterrupt:
        discord_bot_service.stop_service()
