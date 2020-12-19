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
from urllib.parse import quote
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
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import unicodedata
import json
import pickle
import sqlite3
import requests as rq
from random import randint
from tools.checker import Checker,Embed
from Naver_Api.Api import Naver
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
conn = sqlite3.connect(os.path.abspath("main.db"))

cur = conn.cursor()
colour = discord.Colour.blue()

opggsummonersearch = 'https://www.op.gg/summoner/userName='

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

r6URL = "https://r6stats.com"
playerSite = 'https://www.r6stats.com/search/'


def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls


def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2

warnings.filterwarnings(action='ignore')

client_id = ""
client_secret = ""

N = Naver(client_id, client_secret)
def RandomColor():
    return randint(0, 0xFFFFFF)
class 크롤링(commands.Cog):
    """웹크롤링을 활용한 기능들을 보여줍니다"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def 한강(self,ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        url = "https://api.winsub.kr/hangang/?key=$2y$10$hb02LEbU05.z0Eq8gQDjyuvVsI1xgdBhB9RP8WdjcYgsXizyDZE9i"
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request)
        response_body = response.read()
        sid = response_body.decode('utf-8')
        answer = json.loads(sid)
        a = answer["temp"]
        b = answer["time"]
        c = answer["notify"]
        d = answer["quote"]
        embed = discord.Embed(colour=discord.colour.Colour.blue())
        embed.add_field(name=f'현재온도: {a}', value=f'온도측정한시간: {b}', inline=False)
        embed.add_field(name='살아가는데있어 도움이 되는글', value=f'{d}', inline=False)
        embed.add_field(name='안내글', value=f'{c}', inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def 한강이미지(self,ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        url = "https://api.winsub.kr/hangang/?key=$2y$10$hb02LEbU05.z0Eq8gQDjyuvVsI1xgdBhB9RP8WdjcYgsXizyDZE9i"
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request)
        response_body = response.read()
        sid = response_body.decode('utf-8')
        answer = json.loads(sid)
        print(answer)
        a = answer["temp"]
        b = answer["time"]
        c = answer["notify"]
        d = answer["quote"]
        D = d.replace("\n", "")
        print(d)
        img = Image.open("한강석양.png")  # Replace infoimgimg.png with your background image.
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("etc.otf", 30)  # Make sure you insert a valid font from your folder.
        fontbig = ImageFont.truetype("temp.otf", 100)  # Make sure you insert a valid font from your folder.
        #    (x,y)::↓ ↓ ↓ (text)::↓ ↓     (r,g,b)::↓ ↓ ↓
        draw.text((275, 200), f'{a}', (255, 255, 255), font=fontbig)  # draws Information
        draw.text((95, 435), f'"{D}"', (255, 255, 255), font=font)  # draws the Username of the user
        img.save('한강석양_result.png')  # Change infoimg2.png if needed.
        await ctx.send(file=discord.File('한강석양_result.png'))

    @commands.command()
    async def 단축(self,ctx, *, orgurl):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        encText = urllib.parse.quote(orgurl)
        data = "url=" + encText
        url = "https://openapi.naver.com/v1/util/shorturl"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
            sid = response_body.decode('utf-8')
            answer = json.loads(sid)
            a = answer["result"]
            embed = discord.Embed(title="단축성공! ✅")
            if len(orgurl) > 100:
                call_url = f'{orgurl[:100]}...'
            else:
                call_url = orgurl
            embed.add_field(name=f"요청한 원본링크: {call_url}", value="** **", inline=False)
            embed.add_field(name=f"단축된 링크: {a['url']}", value="\n** **", inline=False)
            embed.add_field(name="단축된 링크QR이미지", value="** **", inline=False)
            embed.set_image(url=f"{a['url']}.qr")
            await ctx.send(embed=embed)
        else:
            print("Error Code:" + rescode)
            embed = discord.Embed(title=f"ERROR..단축실패 ❌\n에러코드: {rescode}")
            if len(orgurl) > 100:
                call_url = f'{orgurl[:100]}...'
            else:
                call_url = orgurl
            embed.add_field(name=f"요청한 원본링크: {call_url}", value="** **", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def 영화(self,ctx, *, query):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        global emoji_star, ST_AR1, AC
        a = await N.Movie(query=query)
        print(a)
        embed = discord.Embed(colour=discord.Colour.blue())
        num = 0
        for i in a["items"][:3]:
            director = i["director"]
            direct = str(director).replace("|", "\n")
            actor = i["actor"]
            act = str(actor).replace("|", "\n")
            if i["subtitle"] == '':
                sub = 'ERROR! (정보없음)'
            else:
                sub = i["subtitle"]
            title = i["title"]
            tit = title.replace("<b>", "")
            ti = tit.replace("</b>", "")
            embed.add_field(name=f'#{str(num)}\n제목: **{ti}({sub})**', value='** **', inline=False)
            embed.add_field(name="개봉일", value=i["pubDate"])
            if act == '':
                ac = 'ERROR! (정보없음)'
            else:
                ac = act
            if len(ac) > 15:
                AC = f'{ac[:15]}...'
            dire = f'{ac[:10]}...'
            num += 1


            star = i["userRating"]
            STAR1 = star[:1]
            STAR2 = star[2:3]
            if int(STAR2) >= 5:
                ST_AR1 = int(STAR1) + 1
                print(ST_AR1)
            elif int(STAR2) <= 4:
                ST_AR1 = int(STAR1) + 0
                print(ST_AR1)

            if ST_AR1 == 0:
                emoji_star = '☆☆☆☆☆'
                print('0')
            elif ST_AR1 == 1 or ST_AR1 == 2:
                emoji_star = '★☆☆☆☆'
                print('1')
            elif ST_AR1 == 3 or ST_AR1 == 4:
                emoji_star = '★★☆☆☆'
                print('2')
            elif ST_AR1 == 5 or ST_AR1 == 6:
                emoji_star = '★★★☆☆'
                print('3')
            elif ST_AR1 == 7 or ST_AR1 == 8:
                emoji_star = '★★★★☆'
                print('4')
            elif ST_AR1 == 9 or ST_AR1 == 10:
                emoji_star = '★★★★★'
                print('5')
            print(STAR1)
            embed.add_field(name="평점", value=f'{STAR1}.{STAR2}점, 별점: {emoji_star}({ST_AR1}점)')
            embed.add_field(name="감독", value=dire, inline=False)
            embed.add_field(name="배우", value=AC, inline=False)
            embed.add_field(name="바로가기", value=f"[자세한 내용 보러가기]({i['link']})\n[포스터보러가기]({i['image']})\n{'-----' * 10}")
            embed.set_footer(text='별점은 소숫점1의 자리에서 반올림한 값으로 계산합니다.')
            print(i["userRating"])
        await ctx.send(embed=embed)

    @commands.command()
    async def 뉴스(self,ctx, *, search):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        a = await N.News(query=search)
        print(a)
        embed = discord.Embed(title='뉴스 검색결과!')
        num = 0
        for i in a["items"][:3]:
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
            num += 1
            '''b = str(a["total"])
            c = b[:1]
            d = b[2:5]
            e = b[6:9]'''
            embed.add_field(name=f"#{str(num)}", value=f'기사제목- {str(T)}', inline=False)
            embed.add_field(name="미리보기", value=str(DE), inline=False)
            embed.add_field(name="게시일", value=i["pubDate"][:-6])
            embed.add_field(name="** **", value=f"[자세한 내용 보러가기](<{str(link)}>)\n{'-----' * 10}", inline=False)
            embed.set_footer(text=f'검색된 뉴스 기사 총갯수: {a["total"]}개')
        await ctx.send(embed=embed)
        # await ctx.send(f'{title}\n{link}\n{des}')

    @commands.command()
    async def 카페(self,ctx, *, search):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        a = await N.Cafe(query=search)
        print(a)
        embed = discord.Embed(title=f'카페 게시글 검색결과!\n{"-----" * 10}')
        num = 0
        for i in a["items"][:3]:
            title = i["title"]
            tit = str(title).replace("<b>", "")
            ti = tit.replace("</b>", "")
            T = ti.replace("&quot;", "")
            link = i["link"]
            des = i["description"]
            d_e = des.replace("</b>", "")
            d = d_e.replace("<b>", "")
            D = d.replace("&quot;", "")
            DE = D.replace("&amp;", "")
            num += 1
            embed.add_field(name=f"#{str(num)}\n제목", value=str(T), inline=False)
            embed.add_field(name="미리보기", value=str(DE), inline=False)
            embed.add_field(name="바로가기", value=f"[자세한 내용 보러가기](<{str(link)}>)", inline=False)
            embed.set_footer(text=f'검색된 카페 게시글 총갯수: {a["total"]}개')
        await ctx.send(embed=embed)

    @commands.command()
    async def 웹(self,ctx, *, search):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        a = await N.Webkr(query=search)
        print(a)
        embed = discord.Embed(title=f'네이버 검색결과!\n{"-----" * 10}')
        num = 0
        for i in a["items"][:3]:
            title = i["title"]
            tit = str(title).replace("<b>", "")
            ti = tit.replace("</b>", "")
            T = ti.replace("&quot;", "")
            link = i["link"]
            des = i["description"]
            d_e = des.replace("</b>", "")
            d = d_e.replace("<b>", "")
            D = d.replace("&quot;", "")
            DE = D.replace("&amp;", "")
            num += 1
            embed.add_field(name=f"#{str(num)}\n제목", value=str(T), inline=False)
            embed.add_field(name="미리보기", value=str(DE), inline=False)
            embed.add_field(name="바로가기", value=f"[자세한 내용 보러가기](<{str(link)}>)", inline=False)
            embed.set_footer(text=f'검색된 총갯수: {a["total"]}개')
        await ctx.send(embed=embed)

    @commands.command(name="날씨", pass_context=True)
    async def weather(self, ctx, location):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        embed = discord.Embed(
            title="날씨",
            colour=colour
        )
        Finallocation = location + '날씨'
        LocationInfo = ""
        NowTemp = ""
        CheckDust = []
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + Finallocation
        hdr = {'User-Agent': (
            'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36')}
        req = requests.get(url, headers=hdr)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        bsObj = bs4.BeautifulSoup(html, "html.parser")

        # 오류 체크
        ErrorCheck = soup.find('span', {'class': 'btn_select'})

        if 'None' in str(ErrorCheck):
            await ctx.send('검색 오류발생')
        else:
            # 지역 정보
            for i in soup.select('span[class=btn_select]'):
                LocationInfo = i.text

            NowTemp = soup.find('span', {'class': 'todaytemp'}).text + soup.find('span',
                                                                                 {'class': 'tempmark'}).text[2:]

            WeatherCast = soup.find('p', {'class': 'cast_txt'}).text

            TodayMorningTemp = soup.find('span', {'class': 'min'}).text
            TodayAfternoonTemp = soup.find('span', {'class': 'max'}).text
            TodayFeelTemp = soup.find('span', {'class': 'sensible'}).text[5:]

            TodayUV = soup.find('span', {'class': 'indicator'}).text[4:-2] + " " + soup.find('span', {
                'class': 'indicator'}).text[-2:]

            CheckDust1 = soup.find('div', {'class': 'sub_info'})
            CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'})
            for i in CheckDust2.select('dd'):
                CheckDust.append(i.text)
            FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:]
            UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:]
            Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]
            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
            tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
            tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
            print(tomorrowMoring)

            tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
            tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
            print(tomorrowValue)

            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
            tomorrowAfter1 = tomorrowAllFind[1]
            tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
            tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
            tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
            print(tomorrowAfterTemp)

            tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
            tomorrowAfterValue = tomorrowAfterValue1.text.strip()

            print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지

            embed.add_field(name="|🗺️지역", value=f"{LocationInfo}")
            embed.add_field(name="|🌡️현재온도", value=f"|{NowTemp}", inline=True)
            embed.add_field(name="|🧍🏻체감온도", value=f"|{TodayFeelTemp}", inline=True)
            embed.add_field(name="|ℹ️현재날씨", value=f"{WeatherCast}", inline=True)
            embed.add_field(name="|☀️자외선", value=f"|{TodayUV}", inline=True)
            embed.add_field(name="|🌡️최저온도/최고온도", value=f"|{TodayMorningTemp}/{TodayAfternoonTemp}",
                            inline=True)
            embed.add_field(name="|🌫️미세먼지", value=f"{FineDust}", inline=True)
            embed.add_field(name="|🌫️초미세먼지", value=f"|{UltraFineDust}", inline=True)
            embed.add_field(name="|☀오존 지수", value=f"|{Ozon}", inline=True)
            embed.add_field(name='|🌡내일 오전/오후온도', value='|' + tomorrowMoring + '˚/' + tomorrowAfterTemp + '˚',
                            inline=True)  # 내일오전날씨
            embed.add_field(name='|☀내일 오전날씨상태', value='|' + tomorrowValue, inline=True)  # 내일오전 날씨상태
            embed.add_field(name='|☀내일 오후날씨상태', value='|' + tomorrowAfterValue, inline=True)  # 내일오후 날씨상태
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)



    @commands.command(name="인벤", pass_context=True)
    async def inven(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        embed = discord.Embed(
            title="인벤 주요뉴스",
            colour=colour
        )
        targetSite = 'http://www.inven.co.kr/webzine/news/?hotnews=1'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = rq.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = bs(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'title'})
        titles = melonsp.findAll('span', {'class': 'summary'})
        for i in range(len(titles)):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}".format(i + 1), value='제목:{0} - 내용:{1}'.format(artist, title),
                            inline=False)
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


    @commands.command(name="노래순위", pass_context=True)
    async def music(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        embed = discord.Embed(
            title="노래순위",
            description="노래순위입니다.",
            colour=colour
        )
        targetSite = 'https://www.melon.com/chart/index.htm'

        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        melonrqRetry = rq.get(targetSite, headers=header)
        melonht = melonrqRetry.text
        melonsp = bs(melonht, 'html.parser')
        artists = melonsp.findAll('span', {'class': 'checkEllipsis'})
        titles = melonsp.findAll('div', {'class': 'ellipsis rank01'})
        for i in range(len(titles)):
            artist = artists[i].text.strip()
            title = titles[i].text.strip()
            embed.add_field(name="{0:3d}위".format(i + 1), value='🎶{0} - {1}'.format(artist, title),
                            inline=True)
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


    @commands.command(name="실검", pass_context=True)
    async def sc(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        embed = discord.Embed(
            title="실시간 검색어",
            description="실시간 검색어입니다.",
            colour=colour
        )
        targetSite = 'https://datalab.naver.com/keyword/realtimeList.naver?groupingLevel=3&where=main'
        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        source = rq.get(targetSite, headers=header).text
        soup = BeautifulSoup(source, "html.parser")
        hotKeys = soup.select("span.item_title")
        index = 0
        for key in hotKeys:
            index += 1
            embed.add_field(name="{}위".format(index), value=key.text, inline=True)
            embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(크롤링(client))
