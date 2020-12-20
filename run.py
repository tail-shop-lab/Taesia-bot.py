import datetime
import sqlite3
import urllib
import asyncio
import aiohttp
import bs4
import discord
import time
import requests
from discord.ext import commands
from config import TOKEN
from tools.autocogs import AutoCogs
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib import parse
from cogs.Economy import Economy

conn = sqlite3.connect("level.db")

cur = conn.cursor()
INTENTS = discord.Intents.default()
INTENTS.members = True


class Taesia(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=["ㅌ", 't'], INTENTS=INTENTS)
        self.remove_command("help")
        AutoCogs(self)

    async def on_ready(self):
        print(f"{self.user.name}#{self.user.discriminator} 준비 완료!")

    async def on_message(self, message):
        if message.author.bot:
            return

        async def makeembed(title):
            embed = discord.Embed(
                title=title,
                colour=0x00f000
            )
            await message.channel.send(embed=embed)

        async def req(url: str, header=None):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=header) as r:
                    data = await r.json()
            return data

        async def makeembed2(title, description):
            embed = discord.Embed(
                title=title,
                description=description,
                colour=0x00e2ff
            )
            await message.channel.send(embed=embed)

        if message.content.startswith("") and message.author.id != 766932365426819092:
            # ser = str(message.author.id)
            cur.execute(f"SELECT * FROM level WHERE user = {message.author.id} AND guild_id = {message.guild.id}")
            level = cur.fetchone()
            if level == None:
                cur.execute("INSERT INTO level VALUES (?, ?, ?, ?, ?, ?)",
                            (message.author.id, 0, 1, 0, message.guild.id, message.author.display_name))
                conn.commit()
            exp = [100, 220, 350, 480, 610, 740, 870, 1100, 1230, 1360, 1490, 1620, 1750, 2000, 2500, 3000, 3500, 4000,
                   6000, 8000, 10000]
            await asyncio.sleep(0.3)
            cur.execute(
                f"UPDATE level SET exp = exp + 1 WHERE user = {message.author.id} AND guild_id = {message.guild.id}")
            conn.commit()
            cur.execute(f"SELECT * FROM level WHERE user = {message.author.id} AND guild_id = {message.guild.id}")
            level2 = cur.fetchone()
            if level2[3] == 1:
                return
            elif level2[1] >= exp[level2[2] - 1]:
                try:
                    cur.execute(
                        f"UPDATE level SET lv = lv + 1 WHERE user = {message.author.id} AND guild_id = {message.guild.id}")
                    conn.commit()
                    embed = discord.Embed(title="레벨업!🆙", colour=discord.Colour.gold())
                    embed.add_field(name="축하드립니다!",
                                    value="현재 레벨:" + str(level2[2]) + ".Lv" "\n현재 경험치: " + str(
                                        level2[1]) + ".exp" + "\n다음 레벨업까지:" + str(
                                        int(exp[level2[2]]) - int(level2[1])) + ".Exp 이상 필요해요!")
                    embed.set_footer(text="아나타... 좀 고여가시는군요?")
                    await message.channel.send(f"{message.author.mention}", embed=embed)
                except IndexError:
                    cur.execute(
                        f"UPDATE level SET lv = lv + 1 WHERE user = {message.author.id} AND guild_id = {message.guild.id}")
                    cur.execute(
                        f"UPDATE level SET max = 1 WHERE user = {message.author.id} AND guild_id = {message.guild.id}")
                    conn.commit()
                    embed = discord.Embed(title="레벨업!🆙", colour=discord.Colour.gold())
                    embed.add_field(name="축하드립니다!",
                                    value="현재 레벨: " + str(level2[2]) + ".Lv MAX!🏆" "\n현재 경험치: " + str(
                                        level2[1]) + ".Exp MAX!🏆" + "\n~~다음레벨업까지~~: 최고 레벨 달성!🏆")
                    embed.set_footer(text="아나타... 고이다 못해 썩었군요?")
                    await message.channel.send(f"{message.author.mention}님! 최고 레벨을 달성하셨어요!🎉🎉", embed=embed)

        if message.content.startswith('ㅌ뉴스'):
            await message.channel.send("오늘의 주요 네이버뉴스입니다. (총 5개 나옴)")
            req = Request('https://news.naver.com/', headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            # print(html)
            bsObj = bs4.BeautifulSoup(webpage, "html.parser")
            news = bsObj.select('#today_main_news > div.hdline_news > ul > li > div.hdline_article_tit > a')
            splitted_str = ["`" + a.text.strip() + "`" for a in news]
            await message.channel.send("\n".join(splitted_str))

        if message.content.startswith('ㅌ영화순위'):
            url = urlopen("https://movie.naver.com/movie/running/current.nhn")
            bs = BeautifulSoup(url, 'html.parser')
            body = bs.body
            now = datetime.datetime.now()
            target = body.find(class_="lst_detail_t1")
            embed = discord.Embed(title="영화 순위", description="영화 순위입니다.", colour=0x00f000).set_footer(
                icon_url=message.author.avatar_url,
                text=f' {str(message.author.display_name)}에게 요청받음 | {str(now.year)}년 {str(now.month)}월 {str(now.day)}일')
            list = target.find_all('li')
            no = 0
            for n in range(0, 10):
                no += 1
                title = list[n].find(class_="tit").find("a").text
                try:
                    director = list[n].find(class_="info_txt1").find_all("dd")[1].find("span").find_all("a")
                    directorList = [director.text.strip() for director in director]
                except IndexError:
                    directorList = "정보 없음"
                try:
                    cast = list[n].find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(
                        class_="link_txt").find_all("a")
                    castList = [cast.text.strip() for cast in cast]
                except IndexError:
                    castList = "정보 없음"
                embed.add_field(name=f'{no}등', value=f"영화 제목:  {title}\n제작 감독:  {directorList}\n출연 배우:  {castList}",
                                inline=False)
                embed.set_thumbnail(url="https://img.vogue.co.kr/vogue/2016/03/style_56d7c79069e99.png")
            await message.channel.send(embed=embed)
        if message.content.startswith('ㅌ한디리순위'):
            data = await req(f'https://api.koreanbots.cf/bots/get')
            a = str()
            n = 1
            for i in data['data']:
                a += f"{n}위 -{i['name']} : {i['servers']}서버 ❤️{i['votes']}\n"
                n += 1
            await makeembed2('한국 디스코드봇 순위', f'{a}')


        else:
            await self.process_commands(message)


bot = Taesia()
bot.run(TOKEN, bot=True)
