from discord import Intents
from discord.ext import commands
import asyncio

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../..')))

from takodachi_bot.modules.discord_bot_module import cogs
import takodachi_bot.configs as configs

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        super().__init__(description=configs.BOT_DESCRIPTION,command_prefix=configs.BOT_PREFIX, intents=intents)
        asyncio.run(self.set_cogs())
    
    async def setup_cog(self, cog):
        await cog.setup(self)

    async def set_cogs(self):
        tasks = [self.setup_cog(cog) for cog in cogs.get_modules()]
        await asyncio.gather(*tasks)

    async def start_bot(self):
        await self.start(token=str(configs.BOT_TOKEN))

    def run_bot(self):
        self.run(str(configs.BOT_TOKEN), log_level=20)

    async def stop_bot(self):
        await self.close()

    async def send_message_to_channel(self, channel_id, message):
        channel = self.get_channel(channel_id)
        
        if channel:
            await channel.send(message)
        else:
            print(f"Channel with ID {channel_id} not found.")

if __name__ == "__main__":
    discord_bot = DiscordBot()
    try:
        discord_bot.run_bot()
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.run(discord_bot.stop_bot())
        if discord_bot.is_closed():
            print("Discord Bot closed")