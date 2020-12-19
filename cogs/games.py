import os
import random
import asyncio
import sqlite3

import fortune
import aiopentdb
import xkcd
import ksoftapi
import json
import datetime
import discord
from discord.ext import commands
from async_timeout import timeout
from random import randint
from tools.checker import Checker,Embed
KSoft_Token = ""


conn = sqlite3.connect("main.db")

cur = conn.cursor()


def RandomColor():
    return randint(0, 0xFFFFFF)


class Games(commands.Cog):
    """Play various Games"""

    def __init__(self, bot):
        self.client = None
        self.bot = bot
        self.kclient = ksoftapi.Client(KSoft_Token)

    @commands.command(name='투표')
    async def quickpoll(self, ctx, question, time: str, *options: str):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        cur.execute(f"SELECT * FROM license WHERE user= {ser}")
        L_i = cur.fetchone()
        print(ser)
        if L_i == None:
            sv = discord.Embed(title="⛔명령어 거부됨", colour=discord.colour.Colour.dark_purple())
            sv.add_field(
                name="이런..서비스에 가입하지 않으셨네요..가입을 원하시면 아래반응에 응답해주세요.\n\n가입할시 **__정보제공(서버ID,유저ID,유저닉네임)__**에 동의하시는것으로 간주됩니다.",
                value="** **", inline=False)
            msg = await ctx.send(embed=sv)
            reaction_list = ['✅', '❎']
            for r in reaction_list:
                await msg.add_reaction(r)

            def check(reaction, user):
                return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == msg.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                if str(reaction) == "✅":
                    tm = datetime.datetime.utcnow()
                    cur.execute("INSERT INTO license VALUES (?, ?)", (ser, tm))
                    conn.commit()
                    return await ctx.send("✅가입되었습니다.\n탈퇴를 원하신다면 'ㅌ전체탈퇴'를 명령해주세요.")
                elif str(reaction) == "❎":
                    conn.commit()
                    return await ctx.send("❌가입을 거부하셨습니다.")
            except asyncio.TimeoutError:
                conn.commit()
                return await ctx.send("시간초과로 가입이 취소되었습니다.")
        else:
            if len(options) <= 1:
                await ctx.send('2개이상의 선택지를 만들어주세요!')
                return
            if len(options) > 10:
                await ctx.send('선택지는 최대10개까지에요! 10개 이하로 낮추어주세요.')
                return

            if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
                reactions = ['✅', '❌']
            else:
                reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

            description = []
            for x, option in enumerate(options):
                description += '\n {} {}'.format(reactions[x], option)
            embed = discord.Embed(title="**투표주제:** " + "**" + question + "**", description=''.join(description),
                                  color=discord.Colour(0xFF355E))
            react_message = await ctx.send(embed=embed)
            for reaction in reactions[:len(options)]:
                await react_message.add_reaction(reaction)
            print(react_message.id)
            Day = 0
            Hour = 0
            Minute = 0
            Second = 0

            a = [time]
            if time.find("d") != -1:
                a = a[0].split("d")
                day = a.pop(0).strip()
                Day = int(day)

            if time.find("h") != -1:
                a = a[0].split("h")
                hour = a.pop(0).strip()
                Hour = int(hour)

            if time.find("m") != -1:
                a = a[0].split("m")
                minute = a.pop(0).strip()
                Minute = int(minute)

            if time.find("s") != -1:
                a = a[0].split("s")
                second = a.pop(0).strip()
                Second = int(second)

            embed.add_field(
                name='투표종료까지:',
                value="로딩..")
            react_message.edit(embed=embed)

            while True:
                embed.remove_field(index=0)
                embed.add_field(
                    name='투표종료까지:',
                    value=f"{str(Day)}일 {str(Hour)}시간 {str(Minute)}분 {str(Second)}초 남았습니다."
                )
                await react_message.edit(embed=embed)
                if Second <= 0 and Minute > 0:
                    Minute -= 1
                    Second = 60
                if Minute <= 0 and Hour > 0:
                    Hour -= 1
                    Minute = 59
                if Hour <= 0 and Day > 0:
                    Day -= 1
                    Hour = 23
                await asyncio.sleep(5)
                if Second > 0:
                    Second -= 5
                if Day == 0 and Hour == 0 and Minute == 0 and Second == 0:
                    embed.remove_field(index=0)
                    embed.add_field(
                        name='투표종료까지:',
                        value="투표마감")
                    await react_message.edit(embed=embed)
                    id = react_message.id
                    poll_message = await ctx.message.channel.fetch_message(id)
                    if not poll_message.embeds:
                        return
                    embed = poll_message.embeds[0]
                    if poll_message.author != self.bot.user:
                        return
                    unformatted_options = [x.strip() for x in embed.description.split('\n')]
                    opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
                        else {x[:1]: x[2:] for x in unformatted_options}
                    # check if we're using numbers for the poll, or x/checkmark, parse accordingly
                    voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes

                    tally = {x: 0 for x in opt_dict.keys()}
                    for reaction in poll_message.reactions:
                        if reaction.emoji in opt_dict.keys():
                            reactors = await reaction.users().flatten()
                            for reactor in reactors:
                                if reactor.id not in voters:
                                    tally[reaction.emoji] += 1
                                    voters.append(reactor.id)
                    output = discord.Embed(title='투표결과! \n\n{}\n'.format(embed.title) + \
                                                 '\n'.join(
                                                     ['{}: {}표'.format(opt_dict[key], tally[key]) for key in
                                                      tally.keys()]), color=discord.Colour(0xFF355E))
                    await ctx.send(ctx.author.mention, embed=output)
                    embed = discord.Embed(title="투표주제:\n만료된 투표입니다.")
                    await react_message.edit(embed=embed)
                    break

    


def setup(bot):
    bot.add_cog(Games(bot))
