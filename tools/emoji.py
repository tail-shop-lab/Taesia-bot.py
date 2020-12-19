import datetime

import discord
import sqlite3
import asyncio
money = sqlite3.connect("animal.db")

money_cur = money.cursor()
class Checker:
    def __init__(self, bot, ctx, join: bool,message: discord.message,timeout: int = 30):
        self.ctx = ctx
        self.join = join
        self.reactions = ["✅", "⛔"]
        self.message = message
        self.timeout = timeout
    async def licence(self):
        ser = str(self.ctx.author.id)
        money_cur.execute(f"SELECT * FROM license WHERE user= {ser}")
        L_i = money_cur.fetchone()
        if L_i == None:
            if self.join == True:
                await self.add_reactions()
            else:
                pass
            return 0
        else:
            return 1

    async def no_(self):
        no = discord.Embed(title="⛔명령어 거부됨", colour=discord.colour.Colour.dark_purple())
        no.add_field(
            name="이런..서비스에 가입하지 않으셨네요..가입을 원하시면 `ㅌ가입`을 요청해주세요.\n\n가입할시 **__정보제공(서버ID,유저ID,유저닉네임)__**에 동의하시는것으로 간주됩니다.",
            value="** **", inline=False)
        no.set_footer(text=f'{self.ctx.author}', icon_url=self.ctx.author.avatar_url)
        return no
    async def ok_(self):
        ok = discord.Embed(title="✅가입승인됨", colour=discord.colour.Colour.dark_purple())
        ok.add_field(
            name="가입요청이 승인되었습니다!\n\n탈퇴를 원하실경우 `ㅌ전체탈퇴`를 입력해주세요.",
            value="** **", inline=False)
        ok.set_footer(text=f'{self.ctx.author}', icon_url=self.ctx.author.avatar_url)
        return await self.ctx.send(embed=ok)
    async def add_reactions(self):
        for i in self.reactions:
            await self.message.add_reaction(i)

    def emoji_checker(self, payload):
        if payload.user_id == self.ctx.author.id:
            return False

        if payload.message_id != self.message.id:
            return False


        if str(payload.emoji) in self.reactions:
            return True
        return False

    async def start(self):
        await self.add_reactions()

        while True:
            try:
                add_reaction = asyncio.ensure_future(
                    self.bot.wait_for(
                        "raw_reaction_add", check=self.emoji_checker
                    )
                )
                remove_reaction = asyncio.ensure_future(
                    self.ctx.wait_for(
                        "raw_reaction_remove", check=self.emoji_checker
                    )
                )

                done, pending = await asyncio.wait(
                    (add_reaction, remove_reaction),
                    return_when=asyncio.FIRST_COMPLETED,
                    timeout=self.timeout,
                )

                for i in pending:
                    i.cancel()

                if len(done) == 0:
                    raise asyncio.TimeoutError()

                payload = done.pop().result()  ## done : set
                await self.pagination(payload.emoji)

            except asyncio.TimeoutError:
                try:
                    await self.message.clear_reactions()
                    break
                except:
                    break
    async def pagination(self, emoji):
        if str(emoji) == "✅":
            '''tm = datetime.datetime.utcnow()
            money_cur.execute("INSERT INTO license VALUES (?, ?)", (self.ctx.id, tm))
            money.commit()'''
            print('ok')
            await self.ok_()

        elif str(emoji) == "⛔":
            pass