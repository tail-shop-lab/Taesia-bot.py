# import dbkrpy
import discord
from discord.ext import commands


class GuildCount(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = ''
        dbkrpy.UpdateGuilds(self.bot, self.token)


def setup(bot):
    bot.add_cog(GuildCount(bot))
