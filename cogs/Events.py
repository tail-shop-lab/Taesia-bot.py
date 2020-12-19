import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, BucketType, cooldown, CommandOnCooldown
from discord import Webhook, RequestsWebhookAdapter
from time import gmtime, strftime
from discord.utils import get
import youtube_dl
import logging
import random
import praw
import time
import json
import sys
import os
from random import randint
def RandomColor():
    return randint(0, 0xFFFFFF)
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print("[-]", error)
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"워워~진정하세요 잠시 쿨타임에 걸렸어요. {error.retry_after:,.2f} 초후에 다시 사용해주세요")
        elif isinstance(error, MissingPermissions):
            Denied = discord.Embed(title="⚠권한부족!", description="이 명령을 실행하실 권한이 없어요.자세한 사항은 관리자님께 문의하세요.", color=EmbedColor)
            await ctx.send(embed=Denied)


def setup(bot):
    bot.add_cog(Events(bot))
