from discord.ext import commands
from ..views.play import PlayView

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello_command(self, ctx):
        await ctx.send('Hello from the Cog!')

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(name='play')
    async def play(self, ctx):
        await ctx.send("Start game", view=PlayView())

async def setup(bot):
    await bot.add_cog(Test(bot))