import aiohttp
import discord
import asyncio
import random
#import openpyxl
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
from jamostoolkit import JamosSeparator
from tools.checker import Checker,Embed
from Naver_Api.Api import Naver
def RandomColor():
    return randint(0, 0xFFFFFF)
# Naver Open API application ID
client_id = ""
# Naver Open API application token
client_secret = ""
tierScore = {
    'default': 0,
    'iron': 1,
    'bronze': 2,
    'silver': 3,
    'gold': 4,
    'platinum': 5,
    'diamond': 6,
    'master': 7,
    'grandmaster': 8,
    'challenger': 9
}


def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2

warnings.filterwarnings(action='ignore')

opggsummonersearch = 'https://www.op.gg/summoner/userName='
def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls
daily = sqlite3.connect("daily.db")

daily_cur = daily.cursor()

client_id2 = ""
client_secret2 = ""

N = Naver(client_id2, client_secret2)
def daily_embed(name, value):
    D = discord.Embed(colour=discord.Colour.blue())
    D.add_field(name=name, value=value)
    return D
class etc(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name='강제데일리')
    @commands.has_permissions(administrator=True)
    async def 강제데일리(self, ctx):
        tg = await ctx.send(ctx.author.mention + " 강제로 데일리발송을 진행합니다. 보내시겠습니까?")
        await tg.add_reaction("⭕")
        await tg.add_reaction("❌")

        def notice_check(reaction, user):
            return (
                    user == ctx.author
                    and str(reaction) in ["⭕", "❌"]
                    and tg.id == reaction.message.id
            )

        try:
            reaction, user = await self.app.wait_for(
                "reaction_add", timeout=60.0, check=notice_check
            )
            if str(reaction) == "⭕":
                await self.app.get_channel(782261035377229845).send('<@300535826088067072>')
                await self.app.get_channel(782261035377229845).send(
                    embed=daily_embed(name='START!', value=f'데일리 발송을 시작합니다!'))
                daily_cur.execute(f"SELECT * FROM daily")
                sel = daily_cur.fetchall()
                day = discord.Embed(colour=discord.Colour.blue())
                num = 0
                fail = 0
                success = 0
                for show in sel:
                    temp = []
                    news = []
                    url = f"http://sujang.dothome.co.kr/API/weather.php?place={show[1]}"
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(url) as res:
                            pr = await res.read()
                            sid = pr.decode('utf-8')
                            answer = json.loads(sid)
                            temp.append(answer["현재온도"])
                            temp.append(answer["최저온도"])
                            temp.append(answer["최고온도"])
                            temp.append(answer["미세먼지"])
                            temp.append(answer["초미세먼지"])
                            print(temp)
                    a = await N.News(query=show[2])
                    for i in a["items"][:1]:
                        title = i["title"]
                        tit = str(title).replace("<b>", "")
                        ti = tit.replace("</b>", "")
                        T = ti.replace("&quot;", "")
                        link = i["originallink"]
                        des = i["description"]
                        d_e = des.replace("</b>", "")
                        d = d_e.replace("<b>", "")
                        D = d.replace("&quot;", "")
                        DE = D.replace("&amp;", "")
                        news.append(T)
                        news.append(link)
                        news.append(DE)
                        print(news)
                    day.add_field(name=f'지역: {show[1]}', value="** **", inline=False)
                    day.add_field(name=f'현재온도: {temp[0]}', value="** **")
                    day.add_field(name=f'최저온도: {temp[1]}', value="** **")
                    day.add_field(name=f'최고온도: {temp[2]}', value="** **")
                    dust = []
                    if int(temp[3][:-3]) <= 30:
                        m = '오늘 미세먼지는 좋아요!'
                        dust.append(m)
                    elif int(temp[3][:-3]) >= 31 and int(temp[3][:-3]) <= 80:
                        m = '오늘 미세먼지는 보통이에요!'
                        dust.append(m)
                    elif int(temp[3][:-3]) >= 81 and int(temp[3][:-3]) <= 150:
                        m = '오늘 미세먼지는 나쁨이에요!,마스크착용이 필요해요!'
                        dust.append(m)
                    elif int(temp[3][:-3]) >= 151:
                        m = '오늘 미세먼지는 매우나빠요!, 마스크를 꼭! 착용하세요!'
                        dust.append(m)
                    day.add_field(name=f'미세먼지: {temp[3]}', value=dust[0])
                    smalldust = []
                    if int(temp[4][:-3]) <= 15:
                        mm = '오늘 초미세먼지는 좋아요!'
                        smalldust.append(mm)
                    elif int(temp[4][:-3]) >= 16 and int(temp[4][:-3]) <= 35:
                        mm = '오늘 초미세먼지는 보통이에요!'
                        smalldust.append(mm)
                    elif int(temp[4][:-3]) >= 36 and int(temp[4][:-3]) <= 75:
                        mm = '오늘 초미세먼지는 나쁨이에요!,마스크착용이 필요하거나 외출을 자제해주세요!'
                        smalldust.append(mm)
                    elif int(temp[4][:-3]) >= 76:
                        mm = '오늘 초미세먼지는 매우나빠요!, 외출을 자제해주세요!'
                        smalldust.append(mm)
                    day.add_field(name=f'초미세먼지: {temp[4]}', value=smalldust[0])
                    day.add_field(name=f"{'-----' * 10}\n검색된 주제: {str(show[2])}", value=f'기사제목- {str(news[0])}', inline=False)
                    day.add_field(name="미리보기", value=str(news[2]), inline=False)
                    day.add_field(name="** **", value=f"[자세한 내용 보러가기](<{str(news[1])}>)\n{'-----' * 10}", inline=False)
                    day.set_footer(text='이 발송은 관리자의 의해 강제로 발송된 메시지입니다. 강제로 보낸 사유는 대부분 오류로 발송되지않았을때 해당됩니다.')
                    try:
                        await self.app.get_user(int(show[0])).send(embed=day)
                        print(show[0])
                        num += 1
                        success += 1
                        await self.app.get_channel(782261035377229845).send(
                            embed=daily_embed(name='SUCCESS!', value=f'{str(num)}번째 데일리발송을 성공했습니다!'))
                        temp.clear()
                        news.clear()
                        dust.clear()
                        smalldust.clear()
                        print('List clear complete!')
                    except:
                        fail += 1
                        num += 1
                        await self.app.get_channel(782261035377229845).send('<@300535826088067072>')
                        await self.app.get_channel(782261035377229845).send(embed=daily_embed(name='ERROR!',value=f'{str(num)}번째 데일리 발송중 에러가 발생했습니다.\n발생된 유저ID: {show[0]}'))
                        print(show[0])
                        temp.clear()
                        news.clear()
                        dust.clear()
                        smalldust.clear()
                        print('List clear complete!')
                        pass
                await self.app.get_channel(782261035377229845).send('<@300535826088067072>')
                await self.app.get_channel(782261035377229845).send(embed=daily_embed(name='DONE!',value=f'데일리 발송을 모두 마쳤습니다! \n발송시도한 DM총갯수: {str(num)}\n성공: {str(success)}\n실패: {str(fail)}'))
            else:
                return await ctx.send('취소하셨습니다.')
        except asyncio.TimeoutError:
            return await ctx.send('취소되었습니다.')
    @commands.command(name='데일리상태')
    @commands.has_permissions(administrator=True)
    async def 데일리상태(self, ctx):
        daily_cur.execute(f"SELECT * FROM daily")
        sel = daily_cur.fetchall()
        num = 0
        for show in sel:
            num += 1
        await ctx.send(ctx.author.mention)
        await ctx.send(f'총 {str(num)}명이 등록해있습니다.')

    @commands.command(name='나의데일리')
    async def 나의데일리(self, ctx):
        ser = str(ctx.author.id)
        daily_cur.execute(f"SELECT * FROM daily WHERE user= {ser}")
        P_T = daily_cur.fetchone()
        if P_T == None:
            await ctx.send(ctx.author.mention)
            return await ctx.send(embed=daily_embed(name='ERROR!',value='가입되어있지않으셔요! `ㅌ데일리셋업`을 요청하셔서 가입하세요!'))
        await ctx.send(ctx.author.mention)
        await ctx.send(embed=daily_embed(name=f'{ctx.author.display_name}님의 데일리 가입상태',value=f'날씨지역: {P_T[1]}\n뉴스주제: {P_T[2]}\n수정하실려면 `ㅌ데일리탈퇴`하신후 다시 `ㅌ데일리등록`을 요청해주세요.'))
    @commands.command(name='데일리삭제', aliases=['데일리탈퇴'])
    async def 데일리탈퇴(self, ctx):
        ser = str(ctx.author.id)
        daily_cur.execute(f"SELECT * FROM daily WHERE user= {ser}")
        P_T = daily_cur.fetchone()
        if P_T == None:
            await ctx.send(ctx.author.mention)
            return await ctx.send(embed=daily_embed(name='ERROR!',value='가입되어있지않으셔요! `ㅌ데일리셋업`을 요청하셔서 가입하세요!'))
        else:
            pass
        mt = await ctx.send(ctx.author.mention)
        MG = await ctx.send(embed=daily_embed(name='진짜로 탈퇴 하시겠습니까?탈퇴하시면 가입된 정보가 삭제됩니다!', value=f'날씨지역: {P_T[1]}\n뉴스주제: {P_T[2]}\n반응을 클릭해주세요.\n✅:동의, 🚫: 취소'))
        reaction_list = ['✅', '🚫']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.app.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                daily_cur.execute(f"DELETE FROM daily WHERE user= {ser}")
                daily.commit()
                await MG.delete()
                await mt.delete()
                await ctx.send(ctx.author.mention)
                return await ctx.send(embed=daily_embed(name='성---공!', value='성공적으로 탈퇴처리되었습니다!'))
            else:
                await MG.delete()
                await ctx.send(ctx.author.mention)
                return await ctx.send(embed=daily_embed(name='거---부!', value='탈퇴작업을 거---부하셨습니다.'))
        except asyncio.TimeoutError:
            await MG.delete()
            await ctx.send(ctx.author.mention)
            return await ctx.send(embed=daily_embed(name='타---임아웃', value='탈퇴작업이 취---소되었습니다.'))
    @commands.command(name='데일리셋업', aliases=['데일리등록','데일리가입'])
    async def 데일리셋업(self,ctx):
        ser = str(ctx.author.id)
        daily_cur.execute(f"SELECT * FROM daily WHERE user= {ser}")
        P_T = daily_cur.fetchone()
        if P_T is not None:
            await ctx.send(ctx.author.mention)
            return await ctx.send(embed=daily_embed(name='이미 가입되어있으셔요!', value=f'날씨지역: {P_T[1]}\n뉴스주제: {P_T[2]}'))
        global loc, new
        mt = await ctx.send(ctx.author.mention)
        msg = await ctx.send(embed=daily_embed(name='지역설정', value='날씨를 알아볼 지역을 어디로 하시겠습니까?(예: 서울) __지역이름__만채팅으로 적어주세요.'))
        try:
            loc = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send(ctx.author.mention)
            return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))
        mt2 = await ctx.send(ctx.author.mention)
        MG = await ctx.send(embed=daily_embed(name=f'지역을 {loc.content}로 하시겠습니까?', value='✅:동의 \n❎:다시설정\n🚫: 취소'))
        await msg.delete()
        await mt.delete()
        reaction_list = ['✅', '❎', '🚫']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.app.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                await MG.delete()
                await mt2.delete()
                mt3 = await ctx.send(ctx.author.mention)
                msg2 = await ctx.send(embed=daily_embed(name='뉴스주제 설정', value='뉴스 주제를 무엇으로 하시겠습니까?(예: 코로나) __뉴스주제__만채팅으로 적어주세요.'))
                try:
                    new = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                except asyncio.TimeoutError:
                    await ctx.send(ctx.author.mention)
                    return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))
                mt4 = await ctx.send(ctx.author.mention)
                MG = await ctx.send(embed=daily_embed(name=f'뉴스주제를 {new.content}로 하시겠습니까?', value='✅:동의 \n❎:다시설정\n🚫: 취소'))
                await msg2.delete()
                await mt3.delete()
                reaction_list = ['✅', '❎', '🚫']
                for r in reaction_list:
                    await MG.add_reaction(r)

                def check(reaction, user):
                    return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

                try:
                    reaction, user = await self.app.wait_for('reaction_add', timeout=60, check=check)
                    if str(reaction) == "✅":
                        await MG.delete()
                        await mt4.delete()
                        daily_cur.execute("INSERT INTO daily VALUES (?, ?, ?)", (ctx.author.id, loc.content, new.content))
                        daily.commit()
                        user = ctx.message.author
                        DM = await user.create_dm()
                        await DM.send('매일아침마다 DM을 보내기위해 DM채널을 생성하였어요! 이제부터 매일아침 7시에 발송해드릴게요! 거부하실려면 `ㅌ데일리탈퇴`를 요청해주세요.')
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=daily_embed(name='성공!', value=f'날씨지역: {loc.content}\n뉴스주제: {new.content}\n셋업완료!'))
                    elif str(reaction) == "❎":
                        await MG.delete()
                        mt5 = await ctx.send(ctx.author.mention)
                        msg3 = await ctx.send(embed=daily_embed(name='재입력', value='다시입력해주세요.'))
                        try:
                            new = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                        except asyncio.TimeoutError:
                            await ctx.send(ctx.author.mention)
                            await ctx.send('시간초과로 취소되었습니다.')
                        daily_cur.execute("INSERT INTO daily VALUES (?, ?, ?)", (ctx.author.id, loc.content, new.content))
                        daily.commit()
                        await msg3.delete()
                        await mt5.delete()
                        user = ctx.message.author
                        DM = await user.create_dm()
                        await DM.send('매일아침마다 DM을 보내기위해 DM채널을 생성하였어요! 이제부터 매일아침 7시에 발송해드릴게요! 거부하실려면 `ㅌ데일리탈퇴`를 요청해주세요.')
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=daily_embed(name='성공!', value=f'날씨지역: {loc.content}\n뉴스주제: {new.content}\n셋업완료!'))
                    else:
                        await MG.delete()
                        await ctx.send(ctx.author.mention)
                        return await ctx.send(embed=daily_embed(name='취---소', value='취---소되었습니다.'))
                except asyncio.TimeoutError:
                    await MG.delete()
                    await ctx.send(ctx.author.mention)
                    return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))
            elif str(reaction) == "❎":
                mt6 = await ctx.send(ctx.author.mention)
                msg4 = await ctx.send(embed=daily_embed(name='재입력', value='다시입력해주세요.'))
                try:
                    loc = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                except asyncio.TimeoutError:
                    await ctx.send(ctx.author.mention)
                    return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))
                await msg4.delete()
                await mt6.delete()
                mt7 = await ctx.send(ctx.author.mention)
                msg5 = await ctx.send(embed=daily_embed(name='뉴스주제 설정', value='뉴스 주제를 무엇으로 하시겠습니까?(예: 코로나) __뉴스주제__만채팅으로 적어주세요.'))
                try:
                    new = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                except asyncio.TimeoutError:
                    await ctx.send(ctx.author.mention)
                    return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))
                await ctx.send(ctx.author.mention)
                MG = await ctx.send(embed=daily_embed(name=f'뉴스주제를 {new.content}로 하시겠습니까?', value='✅:동의 \n❎:다시설정\n🚫: 취소'))
                await msg5.delete()
                await mt7.delete()
                reaction_list = ['✅', '❎', '🚫']
                for r in reaction_list:
                    await MG.add_reaction(r)

                def check(reaction, user):
                    return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

                try:
                    reaction, user = await self.app.wait_for('reaction_add', timeout=60, check=check)
                    if str(reaction) == "✅":
                        await MG.delete()
                        daily_cur.execute("INSERT INTO daily VALUES (?, ?, ?)", (ctx.author.id, loc.content, new.content))
                        daily.commit()
                        user = ctx.message.author
                        DM = await user.create_dm()
                        await DM.send('매일아침마다 DM을 보내기위해 DM채널을 생성하였어요! 이제부터 매일아침 7시에 발송해드릴게요! 거부하실려면 `ㅌ데일리탈퇴`를 요청해주세요.')
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=daily_embed(name='성공!', value=f'날씨지역: {loc.content}\n뉴스주제: {new.content}\n셋업완료!'))
                    elif str(reaction) == "❎":
                        mt8 = await ctx.send(ctx.author.mention)
                        msg6 = await ctx.send('다시입력해주세요.')
                        try:
                            new = await self.app.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                        except asyncio.TimeoutError:
                            await ctx.send(ctx.author.mention)
                            await ctx.send('시간초과로 취소되었습니다.')
                        daily_cur.execute("INSERT INTO daily VALUES (?, ?, ?)", (ctx.author.id, loc.content, new.content))
                        daily.commit()
                        await msg6.delete()
                        await MG.delete()
                        await mt8.delete()
                        user = ctx.message.author
                        DM = await user.create_dm()
                        await DM.send('매일아침마다 DM을 보내기위해 DM채널을 생성하였어요! 이제부터 매일아침 7시에 발송해드릴게요! 거부하실려면 `ㅌ데일리탈퇴`를 요청해주세요.')
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=daily_embed(name='성공!', value=f'날씨지역: {loc.content}\n뉴스주제: {new.content}\n셋업완료!'))
                    else:
                        await MG.delete()
                        await ctx.send(ctx.author.mention)
                        return await ctx.send(embed=daily_embed(name='취---소', value='취---소되었습니다.'))
                except asyncio.TimeoutError:
                    await MG.delete()
                    await ctx.send(ctx.author.mention)
                    return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))
            else:
                await MG.delete()
                await ctx.send(ctx.author.mention)
                return await ctx.send(embed=daily_embed(name='취---소', value='취---소되었습니다.'))
        except asyncio.TimeoutError:
            await MG.delete()
            await ctx.send(ctx.author.mention)
            return await ctx.send(embed=daily_embed(name='타---임아웃', value='취---소되었습니다.'))

    @commands.command(name='도움', aliases=['help', '도움말'])
    async def help(self, ctx):

        e = discord.Embed(title='태시아봇 도움말',
                          description='프리픽스: **ㅌ**\n 개발자 : 가위#1111')
        e.add_field(name='1페이지', value='목차', inline=False)
        e.add_field(name='2페이지', value='음악', inline=False)
        e.add_field(name='3페이지', value='이코노미 1/3', inline=False)
        e.add_field(name='4페이지', value='이코노미 2/3', inline=False)
        e.add_field(name='5페이지', value='이코노미 3/3', inline=False)
        e.add_field(name='6페이지', value='서버관리', inline=False)
        e.add_field(name='7페이지', value='기타', inline=False)
        e.set_footer(text='[ 1 / 7 ]')

        e1 = discord.Embed(title='태시아봇 음악 도움말', description='음악소스는 `STORM#0001`님이 제공해주셨습니다.')
        e1.add_field(name='ㅌ재생 [검색어 or URL]', value='음악을 재생해요', inline=False)
        e1.add_field(name='ㅌ나가', value='통화방에서 나가요', inline=False)
        e1.add_field(name='ㅌ재생목록', value='지금 플레이리스트를 보여줘요', inline=False)
        e1.add_field(name='ㅌ스킵', value='음악을 하나 스킵해요', inline=False)
        e1.add_field(name='ㅌ지금곡', value='지금 플레이중인 곡을 보여줘요', inline=False)
        e1.add_field(name='ㅌ시간스킵 [초]', value='초만큼 시간을 스킵해요', inline=False)
        e1.add_field(name='ㅌ일시정지', value='재생중이던 음악을 일시정지해요, 일시정지상태에서 한번더 입력하면 다시 재생해요', inline=False)
        e1.add_field(name='ㅌ볼륨 [설정할 볼륨]', value='설정한 볼륨만큼 소리크기를 조정해요, 만약 볼륨값을 입력하지않으면 현재 볼륨값을 알려줘요', inline=False)
        e1.add_field(name='ㅌ셔플', value='대기목록의 순서를 랜덤으로 바꿔 재생해요', inline=False)
        e1.add_field(name='ㅌ반복', value='최근재생한 곡을 반복재생해요', inline=False)
        e1.add_field(name='ㅌ삭제 [대기번호]', value='대기목록의 번호를 대기열에서 삭제시켜요', inline=False)
        e1.add_field(name='ㅌ시간스킵 [초]', value='초만큼 시간을 스킵해요', inline=False)
        e1.set_footer(text='[ 2 / 7 ]')

        e2 = discord.Embed(title='태시아봇 이코노미 도움말 1/3')
        e2.add_field(name='ㅌ가입',value='모든서비스에 가입해요',
                     inline=False)
        e2.add_field(name='ㅌ직업', value='직업리스트를 보여줘요', inline=False)
        e2.add_field(name='ㅌ취직 [직업이름]', value='직업리스트에 있는 직업이름을 입력하면 해당 직업으로 취직해요', inline=False)
        e2.add_field(name='ㅌ지갑', value='자기가 가진 현금을 보여줘요', inline=False)
        e2.add_field(name='ㅌ통장', value='자기가 입금한 돈을 보여줘요', inline=False)
        e2.add_field(name='ㅌ가방', value='가방내용물을 보여줘요', inline=False)
        e2.add_field(name='ㅌ탈퇴', value='전체서비스에서 탈퇴해요', inline=False)
        e2.add_field(name='ㅌ통장', value='자기가 입금한 돈을 보여줘요', inline=False)
        e2.add_field(name='ㅌ로또구매', value='복권을 구매해요', inline=False)
        e2.add_field(name='ㅌ당첨확인', value='구매한 복권의 당첨유무를 확인해요', inline=False)
        e2.add_field(name='ㅌ랜덤입양', value='펫을 랜덤으로 입양해요', inline=False)
        e2.add_field(name='ㅌ유저입양', value='다른 유저가 분양중인 펫을 입양해요', inline=False)
        e2.set_footer(text='[ 3 / 7 ]')

        e3 = discord.Embed(title='태시아봇 이코노미 도움말 2/3')
        e3.add_field(name='ㅌ자판기', value='자판기에서 펫사료를 구매해요', inline=False)
        e3.add_field(name='ㅌ펫이름변경', value='펫이름을 번경해요', inline=False)
        e3.add_field(name='ㅌ파양', value='펫을 파양(소유권포기)해요', inline=False)
        e3.add_field(name='ㅌ펫분양', value='펫을 분양게시글에 등록해요', inline=False)
        e3.add_field(name='ㅌ펫상태', value='펫상태를 알려줘요', inline=False)
        e3.add_field(name='ㅌ길들이기', value='펫을 길들여요', inline=False)
        e3.add_field(name='ㅌ파양', value='펫을 파양(소유권포기)해요', inline=False)
        e3.set_footer(text='[ 4 / 7 ]')

        e4 = discord.Embed(title='태시아봇 이코노미 도움말 3/3')
        e4.add_field(name='ㅌ입금 [금액]', value='현금을 통장에 입금해요', inline=False)
        e4.add_field(name='ㅌ출금 [금액]', value='통장에서 돈을 뽑아요', inline=False)
        e4.add_field(name='ㅌ도박 [금액]', value='도박을 하여 랜덤으로 돈을 얻거나 잃어요', inline=False)
        e4.add_field(name='ㅌ나무', value='나무를 캐서 돈을 벌어요', inline=False)
        e4.add_field(name='ㅌ지원금', value='지원금을 받아요', inline=False)
        e4.add_field(name='ㅌ송금 [돈을 보낼 유저;@user]', value='지정한 상대에게 돈을 보내요', inline=False)
        e4.add_field(name='ㅌ일하기', value='일해서 돈을 벌어요', inline=False)
        e4.add_field(name='ㅌ파양', value='펫을 파양(소유권포기)해요', inline=False)
        e4.set_footer(text='[ 5 / 7 ]')

        e5 = discord.Embed(title='태시아봇 서버관리 도움말')
        e5.add_field(name='ㅌ유저메모 [유저;@user] [내용]', value='지정한 상대에게 간단한 메모를 남겨요', inline=False)
        e5.add_field(name='ㅌ메모삭제 [유저;@user]', value='지정한 상대에게 남긴 메모를 삭제해요', inline=False)
        e5.add_field(name='ㅌ유저정보 [유저;@user]', value='지정한 상대의 정보를 확인해요', inline=False)
        e5.add_field(name='ㅌ알림판 [채널;#channel]', value='지정한 채널에 공지를 등록해요(everyone멘션포함되어있아요)', inline=False)
        e5.add_field(name='ㅌ청소 [갯수]', value='설정한 갯수만큼 채팅을 지워요', inline=False)
        e5.add_field(name='ㅌ밴 [유저;@user]', value='지정한 상대를 서버에서 밴해요', inline=False)
        e5.add_field(name='ㅌ언밴 [유저;@user]', value='지정한 상대를 서버에서 언밴해요', inline=False)
        e5.add_field(name='ㅌ킥 [유저;@user]', value='지정한 상대를 서버에서 강제퇴장시켜요', inline=False)
        e5.add_field(name='ㅌ경고 [유저;@user]', value='지정한 상대에게 경고를 부여해요', inline=False)
        e5.add_field(name='ㅌ경고리셋 [유저;@user]', value='지정한 상대에게 부여된 경고를 초기화해요', inline=False)
        e5.add_field(name='ㅌ처벌기록리셋 [유저;@user]', value='지정한 상대에게 기록된 처벌기록을 초기화해요', inline=False)
        e5.set_footer(text='[ 6 / 7 ]')

        e6 = discord.Embed(title='태시아봇 기타 도움말')
        e6.add_field(name='ㅌ설명', value='간단한 설명을 해줘요', inline=False)
        e6.add_field(name='ㅌ크레딧', value='봇제작에 도움을 주신 정보를 알려줘요', inline=False)
        e6.add_field(name='ㅌ봇정보', value='봇의 상태를 알려줘요', inline=False)
        e6.add_field(name='ㅌ정보카드 [유저;@user]', value='지정한 상대의 정보를 이미지화 하여 알려주거나 상대를 지정하지않으면 자신의 정보로 알려줘요', inline=False)
        e6.add_field(name='ㅌ날씨 [지역]', value='지정한 지역의 날씨정보를 알려줘요', inline=False)
        e6.add_field(name='ㅌ인벤', value='인벤에서 핫뉴스를 알려줘요', inline=False)
        e6.add_field(name='ㅌ노래순위', value='실시간 노래순위를 알려줘요', inline=False)
        e6.add_field(name='ㅌ실검', value='실시간 실검을 알려줘요', inline=False)
        e6.add_field(name='ㅌ뉴스 [검색할 뉴스]', value='뉴스를 검색해요', inline=False)
        e6.add_field(name='ㅌ웹 [검색할 주제]', value='네이버로 검색해요', inline=False)
        e6.add_field(name='ㅌ카페 [검색할 게시글]', value='카페에서 게시글을 검색해요', inline=False)
        e6.add_field(name='ㅌ한강(이미지)', value='한강온도를 알려줘요', inline=False)
        e6.add_field(name='ㅌ데일리셋업', value='매일 아침7시에 날씨와 뉴스를 포함해 DM을 보내주는 서비스에 가입해요', inline=False)
        e6.add_field(name='ㅌ데일리삭제', value='데일리서비스에서 자신의 가입정보를 삭제해요', inline=False)
        e6.set_footer(text='[ 7 / 7 ]')

        es = [e, e1, e2, e3, e4, e5, e6]
        print(e1.to_dict())
        msg = await ctx.send(embed=e)
        page = Paginator(self.app, msg, embeds=es, only=ctx.author,use_more= True)
        await page.start()





    @commands.command(name="롤도움말")
    async def lolhelp(self,message):

        embed = discord.Embed(title="명령어 사용방법!", description="ㅌ롤전적 (소환사 이름 - 띄어쓰기 붙여쓰기 상관없습니다)",
                              color=0x5CD1E5)
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("도움말!", embed=embed)



    @commands.command(name="코로나")
    async def corona(self,message):

        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        # 주요 브리핑 및 뉴스링크
        briefTasks = []
        mainbrief = bs.findAll('a', {'href': re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)
        print(briefTasks)

        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
        lethatRate = round((int(statNum[3]) / int(tpInt)) * 100, 2)
        embed = discord.Embed(title="Covid-19 Virus Korea Status", description="", color=0x5CD1E5)
        embed.add_field(name="Data source : Ministry of Health and Welfare of Korea",
                        value="http://ncov.mohw.go.kr/index.jsp", inline=False)
        embed.add_field(name="Latest data refred time",
                        value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 " +
                              latestupdateTime[
                                  2] + " 자료입니다.", inline=False)
        embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1] + "(" + beforeNum[0] + ")",
                        inline=True)
        embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        embed.add_field(name="누적확진률", value=statNum[6], inline=True)
        embed.add_field(name="치사율", value=str(lethatRate) + " %", inline=True)
        embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0], value="Link : " + briefTasks[0][1],
                        inline=False)
        embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1],
                        inline=False)
        embed.set_thumbnail(
            url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("Covid-19 Virus Korea Status", embed=embed)

    

def setup(app):
    app.add_cog(etc(app))
