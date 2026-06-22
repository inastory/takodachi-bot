from discord import __version__, Activity, ActivityType
from discord.ext.commands import Cog
from platform import python_version

class OnReady(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print('--------')
        print('Good morning, after noon, evening! It is tako time. Wah! How are you today?')
        print('--------')
        print('Logged in as ' + self.bot.user.name + ' (ID:' + str(self.bot.user.id) + ') | Connected to '
                + str(len(self.bot.guilds)) + ' servers | Connected to ' + str(len(set(self.bot.get_all_members()))) + ' users')
        print('--------')
        print('Current Discord.py Version: {} | Current Python Version: {}'.format(
            __version__, python_version()))
        print('--------')
        print('Use this link to invite {}:'.format(self.bot.user.name))
        print('https://discordapp.com/oauth2/authorize?self.bot_id={}&scope=self.bot&permissions=8'.format(self.bot.user.id))
        print('--------')
        print('Github Link: --')
        print('--------')
        print('Reference: https://github.com/CedArctic/Chimera')
        print('--------')
        return await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name="Ina's back"))

async def setup(bot):
    await bot.add_cog(OnReady(bot))