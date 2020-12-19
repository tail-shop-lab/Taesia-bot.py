import discord
import asyncio
import random
import openpyxl
from discord import Member
from discord.ext import commands, tasks
import youtube_dl
from urllib.request import urlopen, Request
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import unicodedata
import json
import pickle
import sqlite3
from random import randint
from pytz import timezone
conn = sqlite3.connect(os.path.abspath("admin.db"))

cur = conn.cursor()
def RandomColor():
    return randint(0, 0xFFFFFF)


class admin(commands.Cog):
        def __init__(self, app):
            self.app = app

        @commands.command(name="유저메모")
        @commands.has_permissions(administrator=True)
        async def memo(self, ctx, member: discord.Member, *, content):
            cur.execute(f"SELECT * FROM memo WHERE user_id= {member.id}")
            check = cur.fetchone()

            if check == None:
                cur.execute(f"INSERT INTO memo VALUES (?, ?)", (member.id, content))
                conn.commit()
            else:
                cur.execute(f"UPDATE memo SET content = {content} WHERE user_id = {member.id}")
                conn.commit()

            await ctx.send("> 메모 등록이 완료되었습니다.", delete_after=3)

        @commands.command(name="메모삭제")
        @commands.has_permissions(administrator=True)
        async def delete_memo(self, ctx, member: discord.Member):
            cur.execute(f"DELETE FROM memo WHERE user_id= {member.id}")
            conn.commit()

            await ctx.send("> 메모가 삭제되었습니다.", delete_after=3)

        @commands.command(name="서버목록")
        @commands.has_permissions(administrator=True)
        async def serverlist(self,ctx):
            file = open("serverlist.txt", "w", encoding="utf-8")
            file.write(str(self.app.guilds))
            file.close()
            ctx.send("> 서버목록을 작성하였습니다.")
        @commands.command(name="유저정보")
        @commands.has_permissions(administrator=True)
        async def user_info(self, ctx, member: discord.Member):
            cur.execute(f"SELECT * FROM WARNS WHERE user_id= {member.id}")
            warns = cur.fetchall()

            warn_count = 0
            reasons = list()
            for i in warns:
                warn_count += 1
                reasons.append(f"( ID : {i[0]} )경고 {self.app.get_user(i[1])} {i[2]}")

            cur.execute(f"SELECT * FROM MUTES WHERE user_id= {member.id}")
            mutes = cur.fetchall()

            for i in mutes:
                reasons.append(f"채팅금지 {self.app.get_user(i[0])} {i[1]} {i[2]}")

            reasons = '\n'.join(reasons)
            memo = "등록된 메모가 없습니다."
            cur.execute(f"SELECT * FROM memo WHERE user_id= {member.id}")
            check_memo = cur.fetchone()

            if check_memo:
                memo = check_memo[1]

            cur.execute(f"SELECT * FROM ON_MUTED WHERE user_id= {member.id}")
            check_mute = cur.fetchone()

            try:
                check_mute = f"채팅금지 {check_mute[1]}"
            except:
                check_mute = "진행중인 처벌이 없습니다."
            date = datetime.datetime.utcfromtimestamp(((int(member.id) >> 22) + 1420070400000) / 1000)
            embed = discord.Embed(title=f"{member.display_name} 님의 정보", color=0x00ff00,
                                  timestamp=datetime.datetime.now())
            embed.add_field(name="이름", value=member.name, inline=True)
            embed.add_field(name="서버닉네임", value=member.display_name, inline=True)
            embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일",
                            inline=False)
            embed.add_field(name="아이디", value=member.id, inline=True)
            embed.add_field(name="현재 경고 횟수", value=f"{warn_count} / 5")
            embed.add_field(name="처벌 기록", value=f"```{reasons}```", inline=False)
            embed.add_field(name="받고있는 처벌", value=f"```{check_mute}```", inline=False)
            embed.add_field(name="메모", value=f"```{memo}```", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"{member.display_name} | {member.id}", icon_url=member.avatar_url)

            await ctx.send(embed=embed, delete_after=5)


        @commands.command(name="알림판")
        @commands.has_permissions(administrator=True)
        async def broadcast(self, ctx, channel: discord.TextChannel, *, title="알림"):
            await ctx.send("> 내용을 1분 이내에 작성해주세요.", delete_after=60)

            try:
                msg = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
            except asyncio.TimeoutError:
                await ctx.send("> 알림판 작성이 취소되었습니다.", delete_after=3)
            else:
                embed = discord.Embed(title=title, description=f"```{msg.content}```", colour=discord.Colour.blue(),
                                      timestamp=datetime.datetime.now())
                embed.set_footer(text=f'{ctx.author.name}|알림을 확인하셨다면 아래반응에 응답해주세요!', icon_url=ctx.author.avatar_url)
                embed.add_field(name="봇 초대",
                                value='[태시아봇 초대하기](<https://discord.com/api/oauth2/authorize?client_id=728820788278329424&permissions=1342352502&scope=bot>)',
                                inline=False)
                await channel.send("@everyone")
                msg = await channel.send(embed=embed)
                await msg.add_reaction("\U00002705")


        
        @commands.command(name="청소")
        @commands.has_permissions(administrator=True)
        async def clear(self, ctx, amount: int = 5):
            msg = await ctx.send("> :wastebasket:")
            await msg.edit(content="> :wastebasket: 청소준비중..")
            time.sleep(2)
            await msg.edit(content="> :wastebasket: 청소중..")
            time.sleep(2)
            await msg.edit(content="> :wastebasket: 청소끝!")
            time.sleep(1)
            await ctx.channel.purge(limit=amount + 2)

        @commands.command(name="밴")
        @commands.has_permissions(administrator=True)
        async def ban(self, ctx, member: discord.Member, *, reason="사유 미작성"):
            await member.ban(reason=reason)

            embed = discord.Embed(title="관리 로그", colour=discord.Colour.red(), timestamp=datetime.datetime.now())
            embed.add_field(name="처벌 내용", value="밴", inline=False)
            embed.add_field(name="유저", value=member.mention)
            embed.add_field(name="관리자", value=ctx.author.mention)
            embed.add_field(name="사유", value=reason, inline=False)

            await self.app.get_channel(749998827356029008).send(embed=embed)
            await self.app.get_channel(730016508859645992).send(embed=embed)

        @commands.command(name="언밴")
        @commands.has_permissions(administrator=True)
        async def unban(self, ctx, member: discord.Member, *, reason="사유 미작성"):
            await member.unban()

            embed = discord.Embed(title="관리 로그", colour=discord.Colour.blue(), timestamp=datetime.datetime.now())
            embed.add_field(name="관리 내용", value="언밴", inline=False)
            embed.add_field(name="유저", value=member.mention)
            embed.add_field(name="관리자", value=ctx.author.mention)
            embed.add_field(name="사유", value=reason, inline=False)

            await self.app.get_channel(749998827356029008).send(embed=embed)
            await self.app.get_channel(730016508859645992).send(embed=embed)

        @commands.command(name="킥")
        @commands.has_permissions(administrator=True)
        async def kick(self, ctx, member: discord.Member, *, reason="사유 미작성"):
            await member.kick(reason=reason)

            embed = discord.Embed(title="관리 로그", colour=discord.Colour.red(), timestamp=datetime.datetime.now())
            embed.add_field(name="처벌 내용", value="킥", inline=False)
            embed.add_field(name="유저", value=member.mention)
            embed.add_field(name="관리자", value=ctx.author.mention)
            embed.add_field(name="사유", value=reason, inline=False)

            await self.app.get_channel(749998827356029008).send(embed=embed)
            await self.app.get_channel(730016508859645992).send(embed=embed)

        @commands.command(name="경고")
        @commands.has_permissions(administrator=True)
        async def warn(self, ctx, member: discord.Member, *, reason="사유 미작성"):

            check = 1  # 경고 횟수 카운트
            cur.execute(f"SELECT * FROM WARNS WHERE user_id={member.id}")
            warnings = cur.fetchall()
            try:
                for j in warnings:
                    check += 1
            except:
                pass

            cur.execute(f"INSERT INTO WARNS(user_id, reason) VALUES(?, ?)", (member.id, reason))
            conn.commit()

            cur.execute(f"SELECT id FROM WARNS WHERE user_id={member.id}")
            ID = cur.fetchall()[-1][0]

            embed = discord.Embed(title="관리 로그", colour=discord.Colour.red(), timestamp=datetime.datetime.now())
            embed.add_field(name="처벌 내용", value="```경고```", inline=False)
            embed.add_field(name="유저", value=member.mention)
            embed.add_field(name="관리자", value=ctx.author.mention)
            embed.add_field(name="사유", value=f"```{reason}```", inline=False)
            embed.set_footer(text=f"경고 ID | {ID}")

            await self.app.get_channel(749998827356029008).send(embed=embed)
            await self.app.get_channel(730016508859645992).send(embed=embed)

            embed = discord.Embed(title="경고장발급됨",
                                  colour=discord.Colour.red(),
                                  timestamp=datetime.datetime.now())
            embed.add_field(name="처벌 내용", value="```경고```", inline=False)
            embed.add_field(name="유저", value=member.mention)
            embed.add_field(name="사유", value=f"```{reason}```", inline=False)
            embed.set_footer(text="경고5회 누적시 밴처리 되오니 주의바랍니다.")
            await ctx.send(embed=embed, delete_after=20)

            if check == 5:
                await member.ban(reason="경고 3회 누적")

                embed = discord.Embed(title="관리 로그", colour=discord.Colour.red(), timestamp=datetime.datetime.now())
                embed.add_field(name="처벌 내용", value="```밴```", inline=False)
                embed.add_field(name="유저", value=member.mention)
                embed.add_field(name="사유", value="```경고 5회 누적```", inline=False)

                await self.app.get_channel(749998827356029008).send(embed=embed)
                await self.app.get_channel(730016508859645992).send(embed=embed)

                return None

        @commands.command(name="경고삭제")
        @commands.has_permissions(administrator=True)
        async def delete_warns(self, ctx, _id: int):
            cur.execute(f"DELETE FROM WARNS WHERE id= {_id}")
            conn.commit()

            await ctx.send(f"> ID : {_id} 에 해당하는 경고가 삭제되었습니다.", delete_after=3)

        @commands.command(name="경고리셋")
        @commands.has_permissions(administrator=True)
        async def reset_warns(self, ctx, member: discord.Member):
            cur.execute(f"DELETE FROM WARNS WHERE user_id= {member.id}")
            conn.commit()

            await ctx.send(f"> {member.mention} 의 경고를 초기화 하였습니다.", delete_after=3)

        @commands.command(name="처벌기록리셋")
        @commands.has_permissions(administrator=True)
        async def reset_mute(self, ctx, member: discord.Member):
            cur.execute(f"DELETE FROM MUTES WHERE user_id= {member.id}")
            conn.commit()

            await ctx.send(f"> {member.mention} 의 처벌기록을 초기화 하였습니다.", delete_after=3)

        @commands.command(name="벙어리")
        @commands.has_permissions(administrator=True)
        async def mute(self, ctx, member: discord.Member, time: str, *, reason):
            role = discord.utils.get(ctx.guild.roles, name="mute")

            if role == None:
                role = await ctx.guild.create_role(name="mute")

                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False)

            hour = 0
            minute = 0
            second = 0

            a = [time]
            if time.find("h") != -1:
                a = a[0].split("h")
                hour = a.pop(0).strip()

            if time.find("m") != -1:
                a = a[0].split("m")
                minute = a.pop(0).strip()

            if time.find("s") != -1:
                a = a[0].split("s")
                second = a.pop(0).strip()

            await member.add_roles(role)

            ending = datetime.datetime.now() + datetime.timedelta(hours=int(hour), minutes=int(minute),
                                                                  seconds=int(second))
            ending = ending.strftime('%Y-%m-%d %H:%M:%S')

            cur.execute(f"INSERT INTO ON_MUTED VALUES (?, ?, ?)", (member.id, ending, ctx.guild.id))
            conn.commit()
            cur.execute(f"INSERT INTO MUTES VALUES (?, ?, ?)", (member.id, time, reason))
            conn.commit()

            embed = discord.Embed(title="관리 로그", colour=discord.Colour.red(), timestamp=datetime.datetime.now())
            embed.add_field(name="처벌 내용", value=f"{time}동안 채팅 금지", inline=False)
            embed.add_field(name="유저", value=member.mention)
            embed.add_field(name="관리자", value=ctx.author.mention)
            embed.add_field(name="사유", value=reason, inline=False)

            await self.app.get_channel(749998827356029008).send(embed=embed)
            await self.app.get_channel(730016508859645992).send(embed=embed)
            await ctx.send(f"> :ballot_box_with_check: {member.mention}님에게 일시적으로 입을 막았습니다", delete_after=3)

        @commands.command(name="영구벙어리")
        @commands.has_permissions(administrator=True)
        async def _mute(self, ctx, member: discord.Member = None):
            member = member
            role = discord.utils.get(ctx.guild.roles, name="mute")
            if role == None:
                role = await ctx.guild.create_role(name="mute")

                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, send_messages=False)
            await member.add_roles(role)
            await ctx.channel.send(f"> :ballot_box_with_check: `{member.display_name}` 님의 입을 영구적으로 막았습니다.", delete_after=3)

        @commands.command(name="벙어리종료")
        @commands.has_permissions(administrator=True)
        async def delete_mute(self, ctx, member: discord.Member):

            role = discord.utils.get(ctx.guild.roles, name="mute")

            await member.remove_roles(role)
            await ctx.send("> 채팅금지가 종료되었습니다.", delete_after=3)

        @commands.command(name="정신차려")
        @commands.has_permissions(administrator=True)
        async def reboot(self, ctx):
            await ctx.send("후에엥ㅜㅜ")
            await ctx.send("리붓하고올게요..ㅜ")
            python = sys.executable
            os.execl(python, python, *sys.argv)


        


def setup(app):
    app.add_cog(admin(app))