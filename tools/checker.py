import datetime

import discord
from discord.ext import commands
import sqlite3
import asyncio
money = sqlite3.connect("animal.db")

money_cur = money.cursor()
class Checker:
    def __init__(self, ctx):
        self.ctx = ctx
    async def licence(self):
        ser = str(self.ctx.author.id)
        money_cur.execute(f"SELECT * FROM license WHERE user= {ser}")
        L_i = money_cur.fetchone()
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        E_C = money_cur.fetchone()
        if L_i or E_C == None:
            return 400
        else:
            return 200
class Embed:
    def __init__(self,ctx):
        self.ctx = ctx
    def no_(self):
        no = discord.Embed(title="⛔명령어 거부됨", colour=discord.colour.Colour.dark_purple())
        no.add_field(
            name="이런..서비스에 가입하지 않으셨네요..가입을 원하시면 `ㅌ가입`을 요청해주세요.\n\n가입할시 **__정보제공(서버ID,유저ID,유저닉네임)__**에 동의하시는것으로 간주됩니다.",
            value="** **", inline=False)
        no.set_footer(text=f'{self.ctx.author}', icon_url=self.ctx.author.avatar_url)
        return no
    def ok_(self):
        ok = discord.Embed(title="✅가입승인됨", colour=discord.colour.Colour.dark_purple())
        ok.add_field(
            name="가입요청이 승인되었습니다!\n\n탈퇴를 원하실경우 `ㅌ전체탈퇴`를 입력해주세요.",
            value="** **", inline=False)
        ok.set_footer(text=f'{self.ctx.author}', icon_url=self.ctx.author.avatar_url)
        return ok
class emoji:
    def __init__(self, message: discord.Message, join: bool = False):
        self.join = join
        self.message = message
        self.reactions = ["✅", "⛔"]

    async def add_reactions(self):
        if self.join == True:
            for i in self.reactions:
                await self.message.add_reaction(i)
        else:
            pass
