import json
import random
import sqlite3
import datetime
import discord
import asyncio
from discord.ext import commands, tasks
import aiohttp
from Naver_Api.Api import Naver
money = sqlite3.connect("animal.db")

money_cur = money.cursor()
premium = sqlite3.connect("premium.db")

premium_cur = premium.cursor()
daily = sqlite3.connect("daily.db")

daily_cur = daily.cursor()
client_id = ""
client_secret = ""

N = Naver(client_id, client_secret)
def daily_embed(name, value):
    D = discord.Embed(colour=discord.Colour.blue())
    D.add_field(name=name, value=value)
    return D
class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = ['ㅌ도움말', '주인| 가위#1111', 'Team Project A']
        asyncio.get_event_loop().create_task(self.on_load())

    @tasks.loop(seconds=10)
    async def status_loop(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=self.messages[0],
                                                                                               type=discord.ActivityType.playing))
        self.messages.append(self.messages.pop(0))
        await asyncio.sleep(10)

    @tasks.loop(hours=1)
    async def daily_loop(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H")
        print("daily Current Time =", current_time)
        if (current_time == '07'):
            await self.bot.get_channel(782261035377229845).send('<@300535826088067072>')
            await self.bot.get_channel(782261035377229845).send(embed=daily_embed(name='START!', value=f'데일리 발송을 시작합니다!'))
            daily_cur.execute(f"SELECT * FROM daily")
            sel = daily_cur.fetchall()
            day = discord.Embed(colour=discord.Colour.blue())
            temp = []
            news = []
            sh = []
            num = 0
            fail = 0
            success = 0
            for show in sel:
                sh.append(show[0])
                sh.append(show[1])
                sh.append(show[2])
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
                print(a)
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
                day.add_field(name=f'지역: {sh[1]}', value="** **", inline=False)
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
                day.add_field(name=f"검색된 주제: {str(sh[2])}", value=f'기사제목- {str(news[0])}', inline=False)
                day.add_field(name="미리보기", value=str(news[2]), inline=False)
                day.add_field(name="** **", value=f"[자세한 내용 보러가기](<{str(news[1])}>)\n{'-----' * 10}", inline=False)
                try:
                    await self.bot.get_user(int(sh[0])).send(embed=day)
                    num += 1
                    success += 1
                    await self.bot.get_channel(782261035377229845).send(embed=daily_embed(name='SUCCESS!', value=f'{str(num)}번째 데일리발송을 성공했습니다!'))
                except:
                    fail += 1
                    num += 1
                    await self.bot.get_channel(782261035377229845).send('<@300535826088067072>')
                    await self.bot.get_channel(782261035377229845).send(embed=daily_embed(name='ERROR!',value=f'{str(num)}번째 데일리 발송중 에러가 발생했습니다.\n발생된 유저ID: {show[0]}'))
                    pass
                temp.clear()
                news.clear()
                sh.clear()
                dust.clear()
                smalldust.clear()
            await self.bot.get_channel(782261035377229845).send('<@300535826088067072>')
            await self.bot.get_channel(782261035377229845).send(embed=daily_embed(name='DONE!', value=f'데일리 발송을 모두 마쳤습니다! \n발송시도한 DM: {str(num)}\n성공: {str(success)}\n실패: {str(fail)}'))


    @tasks.loop(seconds=2)
    async def premium_loop(self):
        premium_cur.execute("SELECT * FROM premium")
        vip = premium_cur.fetchall()
        for i in vip:

            date = datetime.datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S')

            if date < datetime.datetime.now():
                money_cur.execute("DELETE FROM premium WHERE user=" + str(i[0]))
                money.commit()
                print('complete premium deleted!')

    @tasks.loop(hours=1)
    async def automachine_loop(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H")
        print("automachine Current Time =", current_time)
        await asyncio.sleep(3600)
        if (current_time == '06'):
            print('automachine reload start!')
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(강아지용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(고양이용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(앵무새용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(여우용)'")
            money.commit()
            print('automachine reload complete!')
        elif (current_time == '12'):
            print('automachine reload start!')
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(강아지용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(고양이용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(앵무새용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(여우용)'")
            money.commit()
            print('automachine reload complete!')
        elif (current_time == '18'):
            print('automachine reload start!')
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(강아지용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(고양이용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(앵무새용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(여우용)'")
            money.commit()
            print('automachine reload complete!')
        elif (current_time == '23'):
            print('automachine reload start!')
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(강아지용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(고양이용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(앵무새용)'")
            money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(여우용)'")
            money.commit()
            print('automachine reload complete!')

    async def on_load(self):
        await self.bot.wait_until_ready()
        self.status_loop.start()
        print('statue loop started!')
        self.premium_loop.start()
        print('premium checker started!')
        self.automachine_loop.start()
        print('automachine checker started!')
        self.daily_loop.start()
        print('dailyloop started!')
        print('automachine reload start!')
        money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(강아지용)'")
        money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(고양이용)'")
        money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(앵무새용)'")
        money_cur.execute("UPDATE automachine SET 수량 = 1000 WHERE 물건 = '사료(여우용)'")
        money.commit()
        print('automachine reload complete!')
        print('AD function started!')


def setup(bot):
    bot.add_cog(Core(bot))
    print('Core Loaded!')
