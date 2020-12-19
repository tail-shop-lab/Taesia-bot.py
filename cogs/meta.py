from discord.ext import commands
import discord
from datetime import datetime
from src import util
from tools.checker import Checker,Embed

class Meta(commands.Cog):
    """Commands relating to the bot itself."""

    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        bot.remove_command("help")



    @commands.command(name="업타임")
    async def uptime(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        """Tells how long the bot has been running."""
        uptime_seconds = round(
            (datetime.now() - self.start_time).total_seconds())
        await ctx.send(f"> 봇이 작동한시간: {util.format_seconds(uptime_seconds)}"
                       )
def setup(bot):
    bot.add_cog(Meta(bot))