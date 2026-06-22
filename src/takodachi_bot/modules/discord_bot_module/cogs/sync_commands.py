from discord.ext.commands import Cog, command, has_permissions

class SyncCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    @has_permissions(administrator=True)
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("同步完成")

async def setup(bot):
    await bot.add_cog(SyncCommands(bot))