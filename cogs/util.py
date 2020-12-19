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
import pytz
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from EZPaginator import Paginator
from pytz import timezone
from random import randint
from tools.checker import Checker,Embed
level = sqlite3.connect("level.db")

level_cur = level.cursor()
def RandomColor():
    return randint(0, 0xFFFFFF)


class util(commands.Cog):
    def __init__(self, app):
        self.app = app




    @commands.command(name="설명")
    async def tmi(self, ctx):
        await ctx.send("> 'ㅌ도움말'으로 구체적인 사용법을 보실수있어요!\n> 기능추가나 업데이트되면 공지발송해드릴게요!")

    @commands.command(name="랭크")
    async def my_rank(self,ctx, member: discord.Member=None):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        if member == None:
            member = ctx.author
            level_cur.execute(f"SELECT * FROM level WHERE user= {member.id} AND guild_id = {ctx.guild.id}")
            L_V = level_cur.fetchone()
            path = r"C:\Users\Administrator\Desktop\teasia2.0\LV.png"
            with requests.get(member.avatar_url) as r:
                img_data = r.content
            with open('profile.jpg', 'wb') as handler:
                handler.write(img_data)
            if L_V is not None:
                im1 = Image.open("background.png")
                im2 = Image.open("profile.jpg")

                draw = ImageDraw.Draw(im1)
                font = ImageFont.truetype("2.TTF", 28)
                font1 = ImageFont.truetype("1.TTF", 28)

                draw.text((145, 15), f"{member.display_name}", (255, 255, 255), font=font)
                draw.text((160, 50), str(L_V[2]) + ".Lv", (255, 255, 255), font=font1)
                draw.text((160, 80), str(L_V[1]) + ".exp", (255, 255, 255), font=font1)

                size = 129

                im2 = im2.resize((size, size), resample=0)

                mask_im = Image.new("L", im2.size, 0)
                draw = ImageDraw.Draw(mask_im)
                draw.ellipse((0, 0, size, size), fill=255)

                mask_im.save('mask_circle.png', quality=100)

                back_im = im1.copy()
                back_im.paste(im2, (11, 11), mask_im)

                back_im.save('LV.png', quality=100)

                f = discord.File(path, filename="LV.png")

                await ctx.send(file=f)
                conn.commit()
            else:
                await ctx.send('이런..당신의 레벨정보가 존재하지않아요!')
                conn.commit()
            conn.commit()
        else:
            cur.execute(f"SELECT * FROM level WHERE user= {member.id} AND guild_id = {ctx.guild.id}")
            L_V = cur.fetchone()
            path = r"C:\Users\Administrator\Desktop\teasia2.0\LV.png"
            with requests.get(member.avatar_url) as r:
                img_data = r.content
            with open('profile.jpg', 'wb') as handler:
                handler.write(img_data)
            if L_V is not None:
                im1 = Image.open("background.png")
                im2 = Image.open("profile.jpg")

                draw = ImageDraw.Draw(im1)
                font = ImageFont.truetype("2.TTF", 28)
                font1 = ImageFont.truetype("1.TTF", 28)

                draw.text((145, 15), f"{member.display_name}", (255, 255, 255), font=font)
                draw.text((160, 50), str(L_V[2]) + ".Lv", (255, 255, 255), font=font1)
                draw.text((160, 80), str(L_V[1]) + ".exp", (255, 255, 255), font=font1)

                size = 129

                im2 = im2.resize((size, size), resample=0)

                mask_im = Image.new("L", im2.size, 0)
                draw = ImageDraw.Draw(mask_im)
                draw.ellipse((0, 0, size, size), fill=255)

                mask_im.save('mask_circle.png', quality=100)

                back_im = im1.copy()
                back_im.paste(im2, (11, 11), mask_im)

                back_im.save('LV.png', quality=100)

                f = discord.File(path, filename="LV.png")

                await ctx.send(file=f)
                conn.commit()
            else:
                await ctx.send('이런..지정한 상대의 레벨정보가 존재하지않아요!')
                conn.commit()
            conn.commit()


    




    @commands.command(name="크레딧")
        # 봇에 메시지가 오면 수행 될 액션
    async def dev(self,ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        embed = discord.Embed(title="크레딧", color=0x00ff56)
        embed.add_field(name="개발자", value="가위#1111\n트위터:```https://twitter.com/tfam_is_love```\n유튜브:```https://bit.ly/2Z0550F```")
        embed.add_field(name="베타테스터", value="공식서버에 계신 모든분들.", inline=False)
        embed.add_field(name="후원", value="테일러(서버운영비용)", inline=False)
        embed.add_field(name="참고한 오픈소스", value="[깃허브1](<https://github.com/hands8142/discord-bot>)\n[깃허브2](<https://github.com/SAHYUN/Pulse-Group_Moderation-Bot>)\n[깃허브3](<https://github.com/Puilin/Puilin-Bot>)\n[깃허브4](<https://github.com/minibox24/MiniBOT>)", inline=False)
        embed.set_footer(text="도움을 주신분들 모두 감사합니다😁")
        await ctx.send(embed=embed)


    @commands.command(name="봇정보")
    async  def botinfo(self,ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        if (self.app.latency * 1000) > 210:
            embed = discord.Embed(title="봇정보", color=0xff0000, timestamp=datetime.datetime.now())
            embed.add_field(name="이름", value="태시아", inline=True)
            embed.add_field(name="핑", value="""
                                    현재 핑: {0}ms
                                    상태: 불안정⛔""".format(round(self.app.latency * 1000)))
            embed.add_field(name="접속한 서버수", value=f"{len(self.app.guilds)}개의 서버에 접속함", inline=False)
            embed.add_field(name="접속한 서버들의 멤버수", value=f"{len(self.app.users)}명의 멤버", inline=True)
            embed.set_footer(text=f"태시아봇 | 2.0", icon_url="https://i.imgur.com/TRxVv4X.png")
            embed.set_thumbnail(url="https://i.imgur.com/TRxVv4X.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="봇정보", color=0xff0000, timestamp=datetime.datetime.now())
            embed.add_field(name="이름", value="태시아", inline=True)
            embed.add_field(name="핑", value="""
                                    현재 핑: {0}ms
                                    상태: 양호✅""".format(round(self.app.latency * 1000)))
            embed.add_field(name="접속한 서버수", value=f"{len(self.app.guilds)}개의 서버에 접속함", inline=False)
            embed.add_field(name="접속한 서버들의 멤버수", value=f"{len(self.app.users)}명의 멤버", inline=True)
            embed.set_footer(text=f"태시아봇 | 2.0", icon_url="https://i.imgur.com/TRxVv4X.png")
            embed.set_thumbnail(url="https://i.imgur.com/TRxVv4X.png")
            await ctx.send(embed=embed)




    @commands.command(name="정보카드")
    async def info(self,ctx, user: discord.Member=None):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        if user is None:
            user = ctx.author
            img = Image.open("infoimgimg.png")  # Replace infoimgimg.png with your background image.
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("1.ttf", 55)  # Make sure you insert a valid font from your folder.
            fontbig = ImageFont.truetype("2.TTF", 100)  # Make sure you insert a valid font from your folder.
            #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
            draw.text((370, 25), "유저정보 카드", (255, 255, 255), font=fontbig)  # draws Information
            draw.text((50, 150), "유저이름: {}".format(user.name), (255, 255, 255),
                      font=font)  # draws the Username of the user
            draw.text((50, 220), "ID:  {}".format(user.id), (255, 255, 255), font=font)  # draws the user ID
            draw.text((50, 290), "유저상태:{}".format(user.status), (255, 255, 255),
                      font=font)  # draws the user status
            draw.text((50, 360), "디코가입일: {}".format(user.created_at), (255, 255, 255),
                      font=font)  # When the account was created
            draw.text((50, 430), "서버별명:{}".format(user.display_name), (255, 255, 255),
                      font=font)  # Nickname of the user
            draw.text((50, 500), "최고역할:{}".format(user.top_role), (255, 255, 255),
                      font=font)  # draws the top rome
            draw.text((50, 570), "서버가입일:{}".format(user.joined_at), (255, 255, 255),
                      font=font)  # draws info about when the user joined
            img.save('infoimg2.png')  # Change infoimg2.png if needed.
            await ctx.send(file=discord.File('infoimg2.png'))
        else:
            img = Image.open("infoimgimg.png")  # Replace infoimgimg.png with your background image.
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("1.ttf", 55)  # Make sure you insert a valid font from your folder.
            fontbig = ImageFont.truetype("2.TTF", 100)  # Make sure you insert a valid font from your folder.
            #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
            draw.text((370, 25), "유저정보 카드", (255, 255, 255), font=fontbig)  # draws Information
            draw.text((50, 150), "유저이름: {}".format(user.name), (255, 255, 255),
                      font=font)  # draws the Username of the user
            draw.text((50, 220), "ID:  {}".format(user.id), (255, 255, 255), font=font)  # draws the user ID
            draw.text((50, 290), "유저상태:{}".format(user.status), (255, 255, 255),
                      font=font)  # draws the user status
            draw.text((50, 360), "디코가입일: {}".format(user.created_at), (255, 255, 255),
                      font=font)  # When the account was created
            draw.text((50, 430), "서버별명:{}".format(user.display_name), (255, 255, 255),
                      font=font)  # Nickname of the user
            draw.text((50, 500), "최고역할:{}".format(user.top_role), (255, 255, 255),
                      font=font)  # draws the top rome
            draw.text((50, 570), "서버가입일:{}".format(user.joined_at), (255, 255, 255),
                      font=font)  # draws info about when the user joined
            img.save('infoimg2.png')  # Change infoimg2.png if needed.
            await ctx.send(file=discord.File('infoimg2.png'))





    

def setup(app):
    app.add_cog(util(app))