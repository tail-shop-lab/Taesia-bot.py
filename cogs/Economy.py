import asyncio
import datetime
import json
import sqlite3

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound, BucketType, cooldown, CommandOnCooldown
from discord import Webhook, RequestsWebhookAdapter
from discord.utils import get
import youtube_dl
import logging
import random
from cogs.core import Core
from pytz import timezone
from tools.checker import Checker,Embed
money = sqlite3.connect("animal.db")

money_cur = money.cursor()

premium = sqlite3.connect("premium.db")

premium_cur = premium.cursor()

EmbedColor = 0x4d004d

level = sqlite3.connect("level.db")

level_cur = level.cursor()
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def cog_after_invoke(self, ctx):
        ser = str(ctx.author.id)
        premium_cur.execute(f"SELECT * FROM premium WHERE user= {ser}")
        P_M = premium_cur.fetchone()
        ad = random.randint(1, 5)
        if P_M == None:
            if ad <= 2:
                await ctx.send('(광고)프리미엄서비스가 출시되었습니다! 자세한사항은 `가위#1111`로 DM주세요!')
            else:
                pass
        else:
            pass

    @commands.command()
    async def 랭킹(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        level_cur.execute(f"SELECT user, exp, lv from level WHERE guild_id = {ctx.guild.id} ORDER BY exp + 0 DESC LIMIT 5")
        result = level_cur.fetchall()
        embed = discord.Embed(title="채팅랭크 TOP5", colour=discord.Colour(0x6790a7))
        for i, x in enumerate(result, 1):
            embed.add_field(name=f"#{i}", value=f"<@{str(x[0])}> Level- `{str(x[2])}` Exp- `{str(x[1])}`",
                            inline=False)
        embed.set_footer(text='채팅랭크는 서버별로 각각 다르게 다옵니다!')
        await ctx.send(embed=embed)
        print(result)

    @commands.command()
    async def 전체랭킹(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        level_cur.execute(f"SELECT name, exp, lv from level ORDER BY exp + 1 DESC LIMIT 10")
        result = level_cur.fetchall()
        embed = discord.Embed(title="채팅랭크 TOP10", colour=discord.Colour(0x6790a7))
        for i, x in enumerate(result, 1):
            embed.add_field(name=f"#{i}", value=f"{str(x[0])} Level- `{str(x[2])}` Exp- `{str(x[1])}`",
                            inline=False)
        await ctx.send(embed=embed)
        print(result)




    @commands.command()
    async def 직업(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
            return await ctx.send(embed=em.no_())
        joblist = discord.Embed(title="직업리스트", description="1. 배관공\n2. 은행원\n3. 낚시꾼\n4. 경비원\n5. 유튜버\n\n직업을 가지고있지않으신분들은 'ㅌ취직 (직업이름)'으로 직업을 얻으세요.", color=EmbedColor)
        await ctx.send(embed=joblist)

    @commands.command()
    async def 취직(self, ctx, jobname):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT job FROM economy WHERE user= {ser}")
        J_D = money_cur.fetchone()
        print(J_D)
        if jobname == "배관공":
            job = '배관공'
            money_cur.execute(f"UPDATE economy SET job = ? WHERE user = ?",(job, ser))
            money.commit()
            await ctx.send("배관공으로 취직하셨습니다!")
        elif jobname == "은행원":
            job = '은행원'
            money_cur.execute(f"UPDATE economy SET job = ? WHERE user = ?", (job, ser))
            money.commit()
            await ctx.send("은행원으로 취직하셨습니다!")
        elif jobname == "낚시꾼":
            job = '낚시꾼'
            money_cur.execute(f"UPDATE economy SET job = ? WHERE user = ?", (job, ser))
            money.commit()
            await ctx.send("낚시꾼으로 취직하셨습니다!")
        elif jobname == "경비원":
            job = '경비원'
            money_cur.execute(f"UPDATE economy SET job = ? WHERE user = ?", (job, ser))
            money.commit()
            await ctx.send("경비원으로 취직하셨습니다!")
        elif jobname == "유튜버":
            job = '유튜버'
            money_cur.execute(f"UPDATE economy SET job = ? WHERE user = ?", (job, ser))
            money.commit()
            await ctx.send("유튜버로 취직하셨습니다!")
        else:
            await ctx.send("이런..입력하신건 직업리스트에 없는거에요 다시 시도해주세요!")

    @commands.command(pass_context=True)
    async def 지갑(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        E_C = money_cur.fetchone()
        balance = discord.Embed(title=f"{ctx.message.author}님의 지갑",description=f"**가진돈 : `{E_C[1]}`**\n**직업 : `{E_C[3]}`**", color=EmbedColor)
        await ctx.send(embed=balance)

    @commands.command(pass_context=True)
    async def 통장(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        E_C = money_cur.fetchone()
        balance = discord.Embed(title=f"{ctx.message.author}님의 통장",
                                description=f"**계좌번호 : {ctx.message.author.id}**\n**가진돈 : `{E_C[2]}`**\n**직업 : `{E_C[3]}`**",
                                color=EmbedColor)
        await ctx.send(embed=balance)

    @commands.command(pass_context=True)
    async def 가방(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM backpack WHERE user= {ser}")
        pack = money_cur.fetchone()
        backpack = discord.Embed(title=f'{ctx.author.display_name}님의 가방!',colour=discord.Colour.dark_green())
        backpack.add_field(name='강아지사료',value=f'수량: {pack[1]}',inline=False)
        backpack.add_field(name='고양이사료', value=f'수량: {pack[2]}',inline=False)
        backpack.add_field(name='앵무새사료', value=f'수량: {pack[3]}',inline=False)
        backpack.add_field(name='여우사료', value=f'수량: {pack[4]}',inline=False)
        await ctx.send(embed=backpack)


    @commands.command(pass_context=True)
    async def 탈퇴(self, ctx):
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        E_C = money_cur.fetchone()
        DL = await ctx.send(f'진짜로 전체서비스(경제서비스및 봇라이센스)에서 탈퇴하시겠어요? 탈퇴하시면 아래의 모든 정보가 삭제되며 일부 기능을 제외한 나머지 기능은 사용하실수없습니다!!\n경제)가진돈- {E_C[1]}, 계좌- {E_C[2]}, 직업- {E_C[3]}\n라이센스) 사용자ID\n애완동물소유정보')
        reaction_list = ['✅', '❎']
        for r in reaction_list:
            await DL.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == DL.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                money_cur.execute(f"DELETE FROM economy WHERE user= {ser}")
                money_cur.execute(f"DELETE FROM license WHERE user= {ser}")
                money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                money_cur.execute(f"DELETE FROM animalsell WHERE seller= {ser}")
                money.commit()
                return await ctx.send("✅탈퇴처리되었습니다.\n다시 가입하실려면 'ㅌ가입'을 명령해주세요.")
            elif str(reaction) == "❎":
                return await ctx.send("❌탈퇴작업을 거부하셨습니다.")
        except TimeoutError:
            return await ctx.send("시간초과로 탈퇴작업이 취소되었습니다.")




    @commands.command(pass_context=True)
    async def 로또구매(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        M = await ctx.send('복권 구매하실?')
        reaction_list = ['✅', '❎']
        for r in reaction_list:
            await M.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == M.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                await ctx.send('OK 로또 발급중임')
                Text = ""
                number = [1, 2, 3]  # 배열크기 선언해줌
                count = 0
                for i in range(0, 3):
                    num = random.randrange(1, 10)
                    number[i] = num
                    if count >= 1:
                        for i2 in range(0, i):
                            if number[i] == number[i2]:  # 만약 현재랜덤값이 이전숫자들과 값이 같다면
                                numberText = number[i]
                                print("작동 이전값 : " + str(numberText))
                                number[i] = random.randrange(1, 10)
                                numberText = number[i]
                                print("작동 현재값 : " + str(numberText))
                                if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
                                    numberText = number[i]
                                    print("작동 이전값 : " + str(numberText))
                                    number[i] = random.randrange(1, 10)
                                    numberText = number[i]
                                    print("작동 현재값 : " + str(numberText))
                                    if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
                                        numberText = number[i]
                                        print("작동 이전값 : " + str(numberText))
                                        number[i] = random.randrange(1, 10)
                                        numberText = number[i]
                                        print("작동 현재값 : " + str(numberText))
                    count = count + 1
                    Text = Text + "  " + str(number[i])
                print(Text)
                embed = discord.Embed(title="복권 숫자!", description=Text.strip(), colour=discord.Color.red())
                await ctx.send(embed=embed)
                money_cur.execute(f"DELETE FROM rotto WHERE user= {ser}")
                money.commit()
                await asyncio.sleep(0.3)
                money_cur.execute("INSERT INTO rotto VALUES (?, ?)", (ser, Text.strip()))
                money.commit()
                await ctx.send('OK 데이터에 저장함')
            else:
                await ctx.send('NO')
        except TimeoutError:
            await ctx.send('NO')

    @commands.command(pass_context=True)
    async def 당첨확인(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM rotto WHERE user= {ser}")
        E_C = money_cur.fetchone()
        await ctx.send(E_C[1])
        money_cur.execute(f"SELECT * FROM rottocheck WHERE user= 300535826088067072")
        R_C = money_cur.fetchone()
        if E_C[1] == R_C[1]:
            await ctx.send('당첨')
        else:
            await ctx.send('미당첨')

    @commands.command(pass_context=True)
    async def 복추(self, ctx):
        ser = str(ctx.author.id)
        Text = ""
        number = [1, 2, 3]  # 배열크기 선언해줌
        count = 0
        for i in range(0, 3):
            num = random.randrange(1, 10)
            number[i] = num
            if count >= 1:
                for i2 in range(0, i):
                    if number[i] == number[i2]:  # 만약 현재랜덤값이 이전숫자들과 값이 같다면
                        numberText = number[i]
                        print("작동 이전값 : " + str(numberText))
                        number[i] = random.randrange(1, 10)
                        numberText = number[i]
                        print("작동 현재값 : " + str(numberText))
                        if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
                            numberText = number[i]
                            print("작동 이전값 : " + str(numberText))
                            number[i] = random.randrange(1, 10)
                            numberText = number[i]
                            print("작동 현재값 : " + str(numberText))
                            if number[i] == number[i2]:  # 만약 다시 생성한 랜덤값이 이전숫자들과 또 같다면
                                numberText = number[i]
                                print("작동 이전값 : " + str(numberText))
                                number[i] = random.randrange(1, 10)
                                numberText = number[i]
                                print("작동 현재값 : " + str(numberText))
            count = count + 1
            Text = Text + "  " + str(number[i])
        print(Text)
        embed = discord.Embed(title="복권 숫자!", description=Text.strip(), colour=discord.Color.red())
        await ctx.send(embed=embed)
        money_cur.execute(f"DELETE FROM rottocheck WHERE user= {ser}")
        money.commit()
        await asyncio.sleep(0.3)
        money_cur.execute("INSERT INTO rottocheck VALUES (?, ?)", (ser, Text.strip()))
        money.commit()
        await ctx.send('OK')

    @commands.command(pass_context=True)
    async def 랜덤입양(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        global msg, msg1, msg3
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        P_T = money_cur.fetchone()
        if P_T is not None:
            return await ctx.send('펫은 한마리만 가질수있습니다!')
        animal = ['강아지', '고양이', '앵무새', '여우']
        ANI = random.choice(animal)
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        Y = now.strftime('%Y')
        M = now.strftime('%m')
        D = now.strftime('%d')
        birth = f'{Y}년 {M}월 {D}일'
        first = '낯섦'
        print(ANI, birth)
        await ctx.send(f'랜덤으로 뽑힌 종류: {ANI}')
        await ctx.send('이름을 지정해주세요')
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("> 애완동물 분양이 취소되었습니다.", delete_after=30)
        MG = await ctx.send(f'이름을 {msg.content}로 하시겠습니까? 동의하시면 ✅모양의 반응을, 다시 하실려면 ❎모양의 반응을 클릭해주세요. 또는 작업을 취소하실려면 🚫모양의 반응을 클릭해주세요.')
        reaction_list = ['✅', '❎', '🚫']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                money_cur.execute("INSERT INTO animal VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (ser, ANI, msg.content, birth, 0, first, 1))
                money.commit()
                await ctx.send(f'펫이름을 {msg.content}로 하여 정상분양되었습니다.')
            elif str(reaction) == "❎":
                await ctx.send('이름을 다시 지정해주세요')
                try:
                    msg1 = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                except asyncio.TimeoutError:
                    await ctx.send("> 애완동물 분양이 취소되었습니다.", delete_after=30)
                money_cur.execute("INSERT INTO animal VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (ser, ANI, msg1.content, birth, 0, first, 1))
                money.commit()
                await ctx.send(f'펫이름을 {msg1.content}로 하여 정상분양되었습니다.')
            elif str(reaction) == "🚫":
                await ctx.send('입양작업을 취소하셨습니다.')
        except asyncio.TimeoutError:
            await ctx.send("> 애완동물 분양이 취소되었습니다.", delete_after=30)


    @commands.command(pass_context=True)
    async def 유저입양(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        global msg, msg1, msg3
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        P_T = money_cur.fetchone()
        if P_T is not None:
            return await ctx.send('펫은 한마리만 가질수있습니다!')
        money_cur.execute(f"SELECT * FROM animalsell")
        sell = money_cur.fetchone()
        if sell is not None:
            money_cur.execute(f"SELECT * FROM animalsell")
            sel = money_cur.fetchall()
            MG = await ctx.send('분양게시글에 게시된 글이 있습니다! 여기서 입양하시겠습니까?')
            reaction_list = ['✅', '❎']
            for r in reaction_list:
                await MG.add_reaction(r)

            def check(reaction, user):
                return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                if str(reaction) == "✅":
                    num = 0
                    for show in sel:
                        num += 1
                        await ctx.send(f'{str(num)}.게시글 작성자- {show[0]}, 펫종류- {show[1]}, 펫이름- {show[2]}, 펫생일- {show[3]}')
                    await ctx.send('어떤분의 펫을 입양하실건가요? 채팅으로 게시자의 이름을 적어주세요(ex: 홍길동)')
                    try:
                        msg3 = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                    except asyncio.TimeoutError:
                        await ctx.send("> 애완동물 분양이 취소되었습니다.", delete_after=30)
                    MG2 = await ctx.send(f'{msg3.content}님이 올린 펫을 입양하시겠습니까? 동의하시면 ✅모양의 반응을, 다시 하실려면 ❎모양의 반응을 클릭해주세요.')
                    reaction_list = ['✅', '❎']
                    for r in reaction_list:
                        await MG2.add_reaction(r)

                    def check(reaction, user):
                        return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG2.id

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                        if str(reaction) == "✅":
                            await ctx.send('거래중입니다.')
                            try:
                                money_cur.execute(f"SELECT * FROM animalsell WHERE seller= '{msg3.content}'")
                                sell2 = money_cur.fetchone()
                                first = '낯섦'
                                money_cur.execute("INSERT INTO animal VALUES (?, ?, ?, ?, ?, ?, ?)",
                                            (ser, sell2[1], sell2[2], sell2[3], 0, first, 1))
                                await self.bot.get_channel(int(sell2[5])).send(
                                    f'<@{sell2[6]}>님이 분양중이신 펫({sell2[2]})이 {ctx.author}님에게 분양되었어요!')
                                money_cur.execute(f"DELETE FROM animalsell WHERE seller= '{msg3.content}'")
                                money.commit()
                                await ctx.send('거래완료!')
                            except:
                                await ctx.send(
                                    '거래중 에러가 발생했습니다! \n게시자의 닉네임을 **__정확히__**입력했는지 확인하여 다시 시도하시고 \n그래도 오류가 발생한다면 `가위#1111`로 연락부탁드리겠습니다.')
                        elif str(reaction) == "❎":
                            await ctx.send('거래를 거부하였습니다.')
                    except asyncio.TimeoutError:
                        await ctx.send('거래가 취소되었습니다.')
                elif str(reaction) == "❎":
                    await ctx.send('입양작업을 거부하였습니다.')
            except asyncio.TimeoutError:
                await ctx.send('거래가 취소되었습니다.')
        else:
            await ctx.send('이런 아무도 분양글을 게시하지않았어요.')

            #print(sold)
            #await ctx.send(f'분양글 게시자- {sold[0]},펫종류- {sold[1]}, 펫이름- {sold[2]},펫생일-{sold[3]}')

    @commands.command(pass_context=True)
    async def 자판기(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        global value
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM automachine")
        sel = money_cur.fetchall()
        num = 0
        sold = discord.Embed(title='자판기',colour=discord.Colour.dark_green())
        for show in sel:
            num += 1
            if show[1] == 0:
                value = '매진'
            else:
                value = show[1]
            sold.add_field(name=f'{str(num)}.{show[0]} 가격:{show[2]}',value=f'수량: {value}',inline=False)
        sold.set_footer(text='테스트 자판기')
        MG = await ctx.send(embed=sold)
        reaction_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=check)
            if str(reaction) == "1️⃣":
                money_cur.execute(f"SELECT * FROM automachine")
                val = money_cur.fetchone()
                if val[1] == 0:
                    await ctx.send('매진된 상품입니다. 다시 요청해주세요.')
                    for r in reaction_list:
                        await MG.remove_reaction(r, self.bot.user)
                    return
                for r in reaction_list:
                    await MG.remove_reaction(r, self.bot.user)
                money_cur.execute(f"UPDATE automachine SET 수량 = 수량 - 5 WHERE 물건 = '사료(강아지용)'")
                money_cur.execute(f"SELECT * FROM backpack")
                money_cur.fetchone()
                money_cur.execute(f"UPDATE backpack SET dog = dog + 5 WHERE user = {ser}")
                money.commit()
                await ctx.send('ok')
                await asyncio.sleep(30)
                await MG.clear_reactions()
            elif str(reaction) == "2️⃣":
                money_cur.execute(f"SELECT * FROM automachine")
                val = money_cur.fetchone()
                if val[1] == 0:
                    await ctx.send('매진된 상품입니다. 다시 요청해주세요.')
                    for r in reaction_list:
                        await MG.remove_reaction(r, self.bot.user)
                    return
                for r in reaction_list:
                    await MG.remove_reaction(r,self.bot.user)
                money_cur.execute(f"UPDATE automachine SET 수량 = 수량 - 5 WHERE 물건 = '사료(고양이용)'")
                money_cur.execute(f"SELECT * FROM backpack")
                money_cur.fetchone()
                money_cur.execute(f"UPDATE backpack SET cat = cat + 5 WHERE user = {ser}")
                money.commit()
                await ctx.send('ok')
                await asyncio.sleep(30)
                await MG.clear_reactions()
            elif str(reaction) == "3️⃣":
                money_cur.execute(f"SELECT * FROM automachine")
                val = money_cur.fetchone()
                if val[1] == 0:
                    await ctx.send('매진된 상품입니다. 다시 요청해주세요.')
                    for r in reaction_list:
                        await MG.remove_reaction(r, self.bot.user)
                    return
                for r in reaction_list:
                    await MG.remove_reaction(r, self.bot.user)
                money_cur.execute(f"UPDATE automachine SET 수량 = 수량 - 5 WHERE 물건 = '사료(앵무새용)'")
                money_cur.execute(f"SELECT * FROM backpack")
                money_cur.fetchone()
                money_cur.execute(f"UPDATE backpack SET bird = bird + 5 WHERE user = {ser}")
                money.commit()
                await ctx.send('ok')
                await asyncio.sleep(30)
                await MG.clear_reactions()
            elif str(reaction) == "4️⃣":
                money_cur.execute(f"SELECT * FROM automachine")
                val = money_cur.fetchone()
                if val[1] == 0:
                    await ctx.send('매진된 상품입니다. 다시 요청해주세요.')
                    for r in reaction_list:
                        await MG.remove_reaction(r, self.bot.user)
                    return
                for r in reaction_list:
                    await MG.remove_reaction(r, self.bot.user)
                money_cur.execute(f"UPDATE automachine SET 수량 = 수량 - 5 WHERE 물건 = '사료(여우용)'")
                money_cur.execute(f"SELECT * FROM backpack")
                money_cur.fetchone()
                money_cur.execute(f"UPDATE backpack SET fox = fox + 5 WHERE user = {ser}")
                money.commit()
                await asyncio.sleep(30)
                await MG.clear_reactions()
        except asyncio.TimeoutError:
            await ctx.send('시간오버')
        '''try:
            msg3 = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("> 애완동물 분양이 취소되었습니다.", delete_after=30)'''

    @commands.command(name='프리미엄')
    async def show_premium_statue(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        premium_cur.execute(f"SELECT * FROM premium WHERE user= {ser}")
        P_M = premium_cur.fetchone()
        if P_M == None:
            await ctx.send(f'{ctx.author.mention}님! 가입하신 프리미엄기간이 종료되었거나 가입하지않아 정보가 존재하지않아요! 가입문의는 `가위#1111`로 문의주세요.')
        else:
            await ctx.send(f'{ctx.author.mention}님의 프리미엄 상태\n시리얼코드: {P_M[1]}\n만료일: {P_M[2]}')

    @commands.command(pass_context=True)
    async def 파양(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        P_T = money_cur.fetchone()
        if P_T == None:
            return await ctx.send('애완동물이 없어요 분양받고 다시 요청하세요')
        MG = await ctx.send(f'이름: {P_T[2]}\n정말로 이 펫을 파양(소유권 포기)하시겠습니까?파양할시 소유정보에서 삭제됩니다!')
        reaction_list = ['✅', '❎']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                money.commit()
                await ctx.send('성공적으로 파양하였습니다.')
            elif str(reaction) == "❎":
                await ctx.send('파양작업을 취소하셨습니다.')
        except asyncio.TimeoutError:
            await ctx.send("시간초과로 파양작업을 취소하였습니다.")

    @commands.command(pass_context=True)
    async def 펫이름변경(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        global msg, msg2
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        P_T = money_cur.fetchone()
        await ctx.send(f'{P_T[2]}를 무슨 이름으로 변경하시겠습니까? 채팅으로 적어주세요.')
        try:
            msg = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send('시간초과로 취소되었습니다.')
        MG = await ctx.send(f'이름을 {msg.content}로 하시겠습니까? 반응을 클릭해주세요.\n✅:동의 \n❎:다시설정\n🚫: 취소')
        reaction_list = ['✅', '❎', '🚫']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                money_cur.execute(f"UPDATE animal SET petname = '{msg.content}' WHERE user = {ser}")
                money.commit()
                await ctx.send(f'성공적으로 {msg.content}으로 변경되었습니다!')
            elif str(reaction) == "❎":
                await ctx.send('다시 적어주세요.')
                try:
                    msg2 = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                except asyncio.TimeoutError:
                    await ctx.send('시간초과로 취소되었습니다.')
                money_cur.execute(f"UPDATE animal SET petname = '{msg2.content}' WHERE user = {ser}")
                money.commit()
                await ctx.send(f'성공적으로 {msg2.content}으로 변경되었습니다!')
            else:
                await ctx.send('취소하셨습니다.')
        except asyncio.TimeoutError:
            await ctx.send('시간초과로 취소되었습니다.')




    @commands.command(pass_context=True)
    async def 펫분양(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        global msg
        ser = str(ctx.author.id)
        seller = str(ctx.author.name)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        P_T = money_cur.fetchone()
        if P_T == None:
            return await ctx.send('애완동물이 없어요 분양받고 다시 요청하세요')
        money_cur.execute(f"SELECT * FROM animalsell WHERE seller= {ser}")
        sold = money_cur.fetchone()
        if sold is not None:
            return await ctx.send('이미 분양중인 펫이 있습니다! 분양거래가 완료된후 다시 올릴수있습니다.')
        MG = await ctx.send(f'이름: {P_T[2]}\n정말로 이 펫을 분양하시겠습니까? 분양글 올릴시 소유정보에서 삭제되고 분양데이터로 이전됩니다!')
        reaction_list = ['✅', '❎']
        for r in reaction_list:
            await MG.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == MG.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "✅":
                m_G = await ctx.send('분양게시글에 추가적으로 글을 쓰시겠습니까?')
                reaction_list = ['✅', '❎']
                for r in reaction_list:
                    await m_G.add_reaction(r)

                def check(reaction, user):
                    return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == m_G.id

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                    if str(reaction) == "✅":
                        await ctx.send('분양게시글에 추가적으로 쓰실내용을 적어주세요.')
                        try:
                            msg = await self.bot.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                        except asyncio.TimeoutError:
                            await ctx.send("> 분양 게시글에 아무 내용을 쓰지않아 자동으로 기본으로 설정되었습니다.", delete_after=30)
                            msg = '게시글 내용없음(미작성)'
                            pass
                        try:
                            channel = discord.utils.get(ctx.guild.channels, name='펫-분양' or '펫분양')
                            own = ctx.author.id
                            await channel.send(f'{ctx.author.mention}님이 분양글을 올렸습니다!\n펫정보:\n펫종류- {P_T[1]}\n펫이름- {P_T[2]}\n생일- {P_T[3]}\n게시글 작성자의 추가글- {msg.content}')
                            money_cur.execute("INSERT INTO animalsell VALUES (?, ?, ?, ?, ?, ?, ?)", (seller, P_T[1], P_T[2], P_T[3], msg.content, channel.id, own))
                            money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                            money.commit()
                        except AttributeError:
                            await ctx.send(f'{ctx.author.mention}님이 분양글을 올렸습니다!\n펫정보:\n펫종류- {P_T[1]}\n펫이름- {P_T[2]}\n생일- {P_T[3]}\n게시글 작성자의 추가글- {msg.content}')
                            ch = ctx.channel.id
                            own = ctx.author.id
                            money_cur.execute("INSERT INTO animalsell VALUES (?, ?, ?, ?, ?, ?, ?)", (seller, P_T[1], P_T[2], P_T[3], msg.content, ch, own))
                            money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                            money.commit()
                    elif str(reaction) == "❎":
                        try:
                            channel = discord.utils.get(ctx.guild.channels, name='펫-분양' or '펫분양')
                            own = ctx.author.id
                            mG = '게시글 내용없음(미작성)'
                            await channel.send(f'{ctx.author.mention}님이 분양글을 올렸습니다!\n펫정보:\n펫종류- {P_T[1]}\n펫이름- {P_T[2]}\n생일- {P_T[3]}\n게시글 작성자의 추가글- 게시글 내용없음(미작성)')
                            money_cur.execute("INSERT INTO animalsell VALUES (?, ?, ?, ?, ?, ?, ?)", (seller, P_T[1], P_T[2], P_T[3], mG, channel.id, own))
                            money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                            money.commit()
                        except AttributeError:
                            own = ctx.author.id
                            ch = ctx.channel.id
                            mG = '게시글 내용없음(미작성)'
                            await ctx.send(
                                f'{ctx.author.mention}님이 분양글을 올렸습니다!\n펫정보:\n펫종류- {P_T[1]}\n펫이름- {P_T[2]}\n생일- {P_T[3]}\n게시글 작성자의 추가글- 게시글 내용없음(미작성)')
                            money_cur.execute("INSERT INTO animalsell VALUES (?, ?, ?, ?, ?, ?, ?)", (seller, P_T[1], P_T[2], P_T[3], mG, ch, own))
                            money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                            money.commit()
                except asyncio.TimeoutError:
                    await ctx.send('1분동안 미반응하여 기본으로 설정되어 글을 올렸습니다.')
                    try:
                        channel = discord.utils.get(ctx.guild.channels, name='펫-분양' or '펫분양')
                        own = ctx.author.id
                        await channel.send(
                            f'{ctx.author.mention}님이 분양글을 올렸습니다!\n펫정보:\n펫종류- {P_T[1]}\n펫이름- {P_T[2]}\n생일- {P_T[3]}\n게시글 작성자의 추가글- 게시글 내용없음(미작성)')
                        money_cur.execute("INSERT INTO animalsell VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (seller, P_T[1], P_T[2], P_T[3], msg.content, channel.id, own))
                        money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                        money.commit()
                    except AttributeError:
                        own = ctx.author.id
                        ch = ctx.channel.id
                        await ctx.send(
                            f'{ctx.author.mention}님이 분양글을 올렸습니다!\n펫정보:\n펫종류- {P_T[1]}\n펫이름- {P_T[2]}\n생일- {P_T[3]}\n게시글 작성자의 추가글- 게시글 내용없음(미작성)')
                        money_cur.execute("INSERT INTO animalsell VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (seller, P_T[1], P_T[2], P_T[3], msg.content, ch, own))
                        money_cur.execute(f"DELETE FROM animal WHERE user= {ser}")
                        money.commit()
            elif str(reaction) == "❎":
                await ctx.send('분양을 취소하셨습니다.')
        except asyncio.TimeoutError:
            await ctx.send('분양이 취소되었습니다.')



    @commands.command(pass_context=True)
    async def 펫상태(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        P_T = money_cur.fetchone()
        if P_T == None:
            return await ctx.send('애완동물이 없어요 분양받고 다시 요청하세요')
        await ctx.send(f'종류: {P_T[1]}\n이름: {P_T[2]}\n생일: {P_T[3]}\n상태: {P_T[5]}\n호감도: {P_T[4]}')



    @commands.command(pass_context=True)
    async def 길들이기(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
        am = money_cur.fetchone()
        if am == None:
            return await ctx.send('애완동물이 없어요 분양받고 다시 요청하세요')
        UMM = '의심중'
        HMM = '익숙해짐'
        OH = '따르기시작함'
        GOOD = '따름'
        FAMILY = '가족'
        ran = ['좋아', '좋아', '좋아', '싫어']
        FOOD1 = ['싫어!','안먹어!','맛없어!']
        FOOD2 = ['맛있당','또 줘봐라!','주인 뭘좀 아는군']
        TOUCH1 = ['만지지마!','기분나빠!','그냥 좀 내버려둬!']
        TOUCH2 = ['더 만져줘~','기분 좋아~', '주인손은 내꺼!']
        exp = [25, 45, 65, 85, 110]
        randomchoice = random.choice(ran)
        ser = str(ctx.author.id)
        premium_cur.execute(f"SELECT * FROM premium WHERE user= {ser}")
        P_M = premium_cur.fetchone()
        print(randomchoice)
        M = await ctx.send(f'[{am[2]}] 주인아~')
        reaction_list = ['🍽', '👐']
        for r in reaction_list:
            await M.add_reaction(r)

        def check(reaction, user):
            return user == ctx.author and str(reaction) in reaction_list and reaction.message.id == M.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction) == "🍽":
                for r in reaction_list:
                    await M.remove_reaction(r, self.bot.user)
                money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                L_V = money_cur.fetchone()
                print(L_V[1])
                if L_V[1] == '강아지':
                    money_cur.execute(f"SELECT * FROM backpack WHERE user= {ser}")
                    F_D = money_cur.fetchone()
                    if F_D[1] == 0:
                        return await ctx.send('어머 사료가 다 떨어졌네요! `ㅌ자판기`로 사료를 구매하세요!')
                    else:
                        money_cur.execute(f"UPDATE backpack SET dog = dog - 1 WHERE user = {ser}")
                        if randomchoice == '좋아':
                            if P_M == None:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                money_cur.execute(f"UPDATE animal SET exp = exp + 1 WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +1')
                            else:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                a = random.randint(2, 5)
                                money_cur.execute(f"UPDATE animal SET exp = exp + {a} WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +' + str(a))
                        elif randomchoice == '싫어':
                            FOODCHOICE2 = random.choice(FOOD1)
                            print(FOODCHOICE2)
                            await ctx.send(FOODCHOICE2 + '\n호감도를 얻지못했어요..')
                        print(L_V[4])
                        if L_V[4] >= exp[L_V[6] - 1]:
                            money_cur.execute(f"UPDATE animal SET lv = lv + 1 WHERE user = {ser}")
                            money.commit()
                            money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                            L_V2 = money_cur.fetchone()
                            if L_V2[6] == 2:
                                await ctx.send(f'상태가 {L_V[5]}에서 {UMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (UMM, ser))
                                money.commit()
                            elif L_V2[6] == 3:
                                await ctx.send(f'상태가 {L_V[5]}에서 {HMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (HMM, ser))
                                money.commit()
                            elif L_V2[6] == 4:
                                await ctx.send(f'상태가 {L_V[5]}에서 {OH}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (OH, ser))
                                money.commit()
                            elif L_V2[6] == 5:
                                await ctx.send(f'상태가 {L_V[5]}에서 {GOOD}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (GOOD, ser))
                                money.commit()
                            elif L_V2[6] == 6:
                                await ctx.send(f'상태가 {L_V[5]}에서 {FAMILY}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (FAMILY, ser))
                                money.commit()
                        money.commit()
                elif L_V[1] == '고양이':
                    money_cur.execute(f"SELECT * FROM backpack WHERE user= {ser}")
                    F_D = money_cur.fetchone()
                    if F_D[2] == 0:
                        return await ctx.send('어머 사료가 다 떨어졌네요! `ㅌ자판기`로 사료를 구매하세요!')
                    else:
                        money_cur.execute(f"UPDATE backpack SET cat = cat - 1 WHERE user = {ser}")
                        if randomchoice == '좋아':
                            if P_M == None:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                money_cur.execute(f"UPDATE animal SET exp = exp + 1 WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +1')
                            else:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                a = random.randint(2, 5)
                                money_cur.execute(f"UPDATE animal SET exp = exp + {a} WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +' + str(a))
                        elif randomchoice == '싫어':
                            FOODCHOICE2 = random.choice(FOOD1)
                            print(FOODCHOICE2)
                            await ctx.send(FOODCHOICE2 + '\n호감도를 얻지못했어요..')
                        print(L_V[4])
                        if L_V[4] >= exp[L_V[6] - 1]:
                            money_cur.execute(f"UPDATE animal SET lv = lv + 1 WHERE user = {ser}")
                            money.commit()
                            money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                            L_V2 = money_cur.fetchone()
                            if L_V2[6] == 2:
                                await ctx.send(f'상태가 {L_V[5]}에서 {UMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (UMM, ser))
                                money.commit()
                            elif L_V2[6] == 3:
                                await ctx.send(f'상태가 {L_V[5]}에서 {HMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (HMM, ser))
                                money.commit()
                            elif L_V2[6] == 4:
                                await ctx.send(f'상태가 {L_V[5]}에서 {OH}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (OH, ser))
                                money.commit()
                            elif L_V2[6] == 5:
                                await ctx.send(f'상태가 {L_V[5]}에서 {GOOD}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (GOOD, ser))
                                money.commit()
                            elif L_V2[6] == 6:
                                await ctx.send(f'상태가 {L_V[5]}에서 {FAMILY}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (FAMILY, ser))
                                money.commit()
                        money.commit()
                elif L_V[1] == '앵무새':
                    money_cur.execute(f"SELECT * FROM backpack WHERE user= {ser}")
                    F_D = money_cur.fetchone()
                    if F_D[3] == 0:
                        return await ctx.send('어머 사료가 다 떨어졌네요! `ㅌ자판기`로 사료를 구매하세요!')
                    else:
                        money_cur.execute(f"UPDATE backpack SET bird = bird - 1 WHERE user = {ser}")
                        if randomchoice == '좋아':
                            if P_M == None:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                money_cur.execute(f"UPDATE animal SET exp = exp + 1 WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +1')
                            else:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                a = random.randint(2, 5)
                                money_cur.execute(f"UPDATE animal SET exp = exp + {a} WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +' + str(a))
                        elif randomchoice == '싫어':
                            FOODCHOICE2 = random.choice(FOOD1)
                            print(FOODCHOICE2)
                            await ctx.send(FOODCHOICE2 + '\n호감도를 얻지못했어요..')
                        print(L_V[4])
                        if L_V[4] >= exp[L_V[6] - 1]:
                            money_cur.execute(f"UPDATE animal SET lv = lv + 1 WHERE user = {ser}")
                            money.commit()
                            money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                            L_V2 = money_cur.fetchone()
                            if L_V2[6] == 2:
                                await ctx.send(f'상태가 {L_V[5]}에서 {UMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (UMM, ser))
                                money.commit()
                            elif L_V2[6] == 3:
                                await ctx.send(f'상태가 {L_V[5]}에서 {HMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (HMM, ser))
                                money.commit()
                            elif L_V2[6] == 4:
                                await ctx.send(f'상태가 {L_V[5]}에서 {OH}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (OH, ser))
                                money.commit()
                            elif L_V2[6] == 5:
                                await ctx.send(f'상태가 {L_V[5]}에서 {GOOD}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (GOOD, ser))
                                money.commit()
                            elif L_V2[6] == 6:
                                await ctx.send(f'상태가 {L_V[5]}에서 {FAMILY}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (FAMILY, ser))
                                money.commit()
                        money.commit()
                elif L_V[1] == '여우':
                    money_cur.execute(f"SELECT * FROM backpack WHERE user= {ser}")
                    F_D = money_cur.fetchone()
                    if F_D[4] == 0:
                        return await ctx.send('어머 사료가 다 떨어졌네요! `ㅌ자판기`로 사료를 구매하세요!')
                    else:
                        money_cur.execute(f"UPDATE backpack SET fox = fox - 1 WHERE user = {ser}")
                        if randomchoice == '좋아':
                            if P_M == None:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                money_cur.execute(f"UPDATE animal SET exp = exp + 1 WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +1')
                            else:
                                FOODCHOICE1 = random.choice(FOOD2)
                                print(FOODCHOICE1)
                                a = random.randint(2, 5)
                                money_cur.execute(f"UPDATE animal SET exp = exp + {a} WHERE user = {ser}")
                                await ctx.send(FOODCHOICE1 + '\n호감도가 올랐습니다! +' + str(a))
                        elif randomchoice == '싫어':
                            FOODCHOICE2 = random.choice(FOOD1)
                            print(FOODCHOICE2)
                            await ctx.send(FOODCHOICE2 + '\n호감도를 얻지못했어요..')
                        print(L_V[4])
                        if L_V[4] >= exp[L_V[6] - 1]:
                            money_cur.execute(f"UPDATE animal SET lv = lv + 1 WHERE user = {ser}")
                            money.commit()
                            money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                            L_V2 = money_cur.fetchone()
                            if L_V2[6] == 2:
                                await ctx.send(f'상태가 {L_V[5]}에서 {UMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (UMM, ser))
                                money.commit()
                            elif L_V2[6] == 3:
                                await ctx.send(f'상태가 {L_V[5]}에서 {HMM}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (HMM, ser))
                                money.commit()
                            elif L_V2[6] == 4:
                                await ctx.send(f'상태가 {L_V[5]}에서 {OH}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (OH, ser))
                                money.commit()
                            elif L_V2[6] == 5:
                                await ctx.send(f'상태가 {L_V[5]}에서 {GOOD}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (GOOD, ser))
                                money.commit()
                            elif L_V2[6] == 6:
                                await ctx.send(f'상태가 {L_V[5]}에서 {FAMILY}으로 변경되었습니다~!')
                                money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (FAMILY, ser))
                                money.commit()
                        money.commit()
            elif str(reaction) == "👐":
                money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                L_V = money_cur.fetchone()
                if randomchoice == '좋아':
                    if P_M == None:
                        TOUCHCHOICE = random.choice(TOUCH2)
                        money_cur.execute(f"UPDATE animal SET exp = exp + 1 WHERE user = {ser}")
                        await ctx.send('호감도가 올랐습니다! +1')
                    else:
                        TOUCHCHOICE = random.choice(TOUCH2)
                        a = random.randint(2, 5)
                        money_cur.execute(f"UPDATE animal SET exp = exp + {a} WHERE user = {ser}")
                        await ctx.send('호감도가 올랐습니다! +' + str(a))
                else:
                    TOUCHCHOICE = random.choice(TOUCH1)
                    await ctx.send('호감도를 얻지못했어요..')
                await ctx.send(TOUCHCHOICE)
                print(L_V[4])
                if L_V[4] >= exp[L_V[6] - 1]:
                    money_cur.execute(f"UPDATE animal SET lv = lv + 1 WHERE user = {ser}")
                    money_cur.execute(f"SELECT * FROM animal WHERE user= {ser}")
                    L_V2 = money_cur.fetchone()
                    if L_V2[6] == 2:
                        await ctx.send(f'상태가 {am[5]}에서 {UMM}으로 변경되었습니다~!')
                        money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (UMM, ser))
                    elif L_V2[6] == 3:
                        await ctx.send(f'상태가 {am[5]}에서 {HMM}으로 변경되었습니다~!')
                        money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (HMM, ser))
                    elif L_V2[6] == 4:
                        await ctx.send(f'상태가 {am[5]}에서 {OH}으로 변경되었습니다~!')
                        money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (OH, ser))
                    elif L_V2[6] == 5:
                        await ctx.send(f'상태가 {am[5]}에서 {GOOD}으로 변경되었습니다~!')
                        money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (GOOD, ser))
                    elif L_V2[6] == 6:
                        await ctx.send(f'상태가 {am[5]}에서 {FAMILY}으로 변경되었습니다~!')
                        money_cur.execute(f"UPDATE animal SET statue = ? WHERE user = ?", (FAMILY, ser))
                money.commit()
        except asyncio.TimeoutError:
            await ctx.send('왜 부른거지..다시 잘레..')








    @commands.command(pass_context=True)
    async def 입금(self,ctx, amount: int):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        I_S = money_cur.fetchone()
        print(ser)
        if amount < 0:
            return await ctx.send('No')
        elif I_S[1] < money:
            return await ctx.send('No')
        money_cur.execute(f"UPDATE economy SET amounts = amounts - {amount} WHERE user = {ser}")
        money_cur.execute(f"UPDATE economy SET bank = bank + {amount} WHERE user = {ser}")
        money.commit
        await ctx.send('ok')

    @commands.command(pass_context=True)
    async def 출금(self, ctx, amount: int):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        I_S = money_cur.fetchone()
        print(ser)
        if amount < 0:
            return await ctx.send('No')
        elif I_S[2] < amount:
            return await ctx.send('No')
        money_cur.execute(f"UPDATE economy SET bank = bank - {amount} WHERE user = {ser}")
        money_cur.execute(f"UPDATE economy SET amounts = amounts + {amount} WHERE user = {ser}")
        money.commit()
        await ctx.send('ok')

    @commands.command(pass_context=True)
    async def 도박(self, ctx, amount: int):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        I_S = money_cur.fetchone()
        print(ser)
        if amount > I_S[1]:
            await ctx.send(f"{ctx.message.author.mention}님! 도박에 배팅하실려는 금액이 지갑에 가지고계신돈보다 커서 배팅할수가없어요!")
            return
        wl = random.randint(1, 9)
        randomNum = random.randint(2, 10)
        print(randomNum)
        if wl == 1:
            amount *= randomNum
            money_cur.execute(f"UPDATE economy SET bank = bank + {amount} WHERE user = {ser}")
            print(amount)
            money.commit()
            await ctx.send(f"{ctx.message.author.mention}님! 도박에 **__성공__**하여 {randomNum}배만큼 돈을 얻었습니다.\n얻은돈 : {amount}")
            await ctx.send("고액인만큼 안전하게 바로 통장으로 입금해드렸습니다!")
            account = discord.Embed(title=f"{ctx.message.author}님의 통장",
                                    description=f"**계좌번호 : {ctx.message.author.id}**\n**예금 : {str(int(I_S[2]) + amount)} \n입금된 금액 : {amount}**",
                                    color=EmbedColor)
            await ctx.send(embed=account)

        else:
            amount *= randomNum
            if I_S[2] < amount:
                money_cur.execute(f"UPDATE economy SET bank = 0 WHERE user = {ser}")
                money_cur.execute(f"UPDATE economy SET amounts = 0 WHERE user = {ser}")
                money.commit()
                account = discord.Embed(title=f"{ctx.message.author}님의 재산",
                                        description=f"**계좌번호 : {ctx.message.author.id}**\n**지갑 : 0 \n통장 : 0**",
                                        color=EmbedColor)
                await ctx.send(f"{ctx.message.author.mention} 도박에 **__실패__**하여 전재산을 탕진했습니다.")
                return await ctx.send(embed=account)
            money_cur.execute(f"UPDATE economy SET bank = amounts - {amount} WHERE user = {ser}")
            await ctx.send(f"{ctx.message.author.mention} 도박에 **__실패__**하여 돈을 잃었습니다.")
            money.commit()
            account = discord.Embed(title=f"{ctx.message.author}님의 지갑",
                                    description=f"**계좌번호 : {ctx.message.author.id}**\n**가진돈 : {str(int(I_S[1]) + amount)} \n잃은 돈 : {amount}**",
                                    color=EmbedColor)
            await ctx.send(embed=account)





    @commands.command(name="나무")
    @cooldown(3, 120, BucketType.user)
    async def namu(self,ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        I_S = money_cur.fetchone()
        print(ser)
        randomNum = random.randint(2, 5)
        embed = discord.Embed(title="나무를 캡니다.", colour=discord.Colour.dark_green())
        msg = await ctx.send(embed=embed)
        embed = discord.Embed(title=f"나무를 캐는중...", colour=discord.Colour.dark_green())
        await msg.edit(embed=embed)
        await asyncio.sleep(randomNum)
        embed = discord.Embed(title="나무가 쓰러집니다", colour=discord.Colour.dark_green())
        await msg.edit(embed=embed)
        randomNum = random.randint(100, 150)
        print(randomNum)
        money_cur.execute(f"UPDATE economy SET amounts = amounts + {randomNum} WHERE user = {ser}")
        embed = discord.Embed(title=f"{ctx.message.author.display_name}님의 지갑",
                              colour=discord.Colour.dark_green())
        embed.add_field(name="자금", value="가진돈:" + str(int(I_S[1]) + randomNum) + "원" f"\n얻은수익: +{randomNum}")
        embed.add_field(name="직업", value=I_S[3], inline=False)
        embed.set_footer(text="아나타...부자이신가요?")
        await ctx.send(embed=embed)
        money.commit()

    @commands.command(name="치트")
    @commands.has_permissions(administrator=True)
    async def cheat(self, ctx, amount: int):
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        money_cur.fetchone()
        print(ser)
        money_cur.execute(f"UPDATE economy SET amounts = amounts + {amount} WHERE user = {ser}")
        money_cur.execute(f"UPDATE economy SET bank = bank + {amount} WHERE user = {ser}")
        await ctx.send(f"관리자의 권력으로 {amount}만큼 돈을 넣었습니다!")
        money.commit()













    @commands.command(pass_context=True)
    async def 가입(self, ctx):
        em = Embed(ctx=ctx)
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}") #economy라는 테이블에서 ser이라는 값을 가진 란을 선택함
        E_C = money_cur.fetchone() #cur.fetchone이면 한줄만 읽고 cur.fetchall 이면 모든걸 읽음
        print(ser)
        if E_C == None:
            amounts = 0
            bank = 0
            job = '무직'
            money_cur.execute("INSERT INTO economy VALUES (?, ?, ?, ?)", (ser, amounts, bank, job)) #값을 넣음
            money_cur.execute("INSERT INTO backpack VALUES (?, ?, ?, ?, ?)", (ser, 0, 0, 0, 0))
            money.commit()
            await ctx.send(embed=em.ok_())
            print(f"[+] Registered {ctx.message.author} - {ctx.message.author.id}")
        else:
            print("[+] The register command was executed but the user was already registed.")
            await ctx.send("이미 가입되어있습니다!")

    @commands.command(pass_context=True)
    async def 지원금(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT amounts FROM economy WHERE user= {ser}")
        money_cur.fetchone()
        print(ser)
        amount = 5
        money_cur.execute(f"UPDATE economy SET amounts = amounts + {amount} WHERE user = {ser}") #economy라는 테이블에서 ser값을 가진 란에 amounts라는 인덱스를 수정함
        money.commit()
        await ctx.send("지원금 지급완료")

    @commands.command(pass_context=True)
    async def 송금(self, ctx, amount: int, other: discord.Member):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        other_id = str(other.id)
        money_cur.execute(f"SELECT amounts FROM economy")
        money_cur.fetchall()
        money_cur.execute(f"UPDATE economy SET amounts = amounts - {amount} WHERE user = {ser}")
        money_cur.execute(f"UPDATE economy SET amounts = amounts + {amount} WHERE user = {other_id}")
        money_cur.execute(f"SELECT amounts FROM economy WHERE user= {other_id}")
        O_T = money_cur.fetchone()
        if O_T == None:
            return await ctx.send("지정하신 상대방은 경제서비스에 가입되어있지않아요!")
        if other_id == ser:
            return await ctx.send("자기자신에게 송금할수없습니다!")
        money.commit()
        await ctx.send("송금 완료")

    @commands.command(pass_context=True)
    @cooldown(1, 10, BucketType.user)
    async def 일하기(self, ctx):
        ch = Checker(ctx=ctx)
        em = Embed(ctx=ctx)
        if await ch.licence() == 400:
            return await ctx.send(embed=em.no_())
        elif await ch.licence() == 200:
            pass
        ser = str(ctx.author.id)
        money_cur.execute(f"SELECT * FROM economy WHERE user= {ser}")
        J_D = money_cur.fetchone()
        print(J_D[4])
        if J_D[4] == "배관공":
            randomCoins = random.randint(50, 100)
            money_cur.execute(f"UPDATE economy SET amounts = amounts + {randomCoins} WHERE user = {ser}")
            await ctx.send("화장실을 수리하여 " + str(randomCoins) + " 만큼의 돈을 벌었습니다!")
            money.commit()
        elif J_D[4] == "은행원":
            randomCoins = random.randint(50, 100)
            money_cur.execute(f"UPDATE economy SET amounts = amounts + {randomCoins} WHERE user = {ser}")
            await ctx.send("은행에서 일을하여 " + str(randomCoins) + " 만큼의 돈을 벌었습니다!")
            money.commit()
        elif J_D[4] == "낚시꾼":
            randomCoins = random.randint(50, 100)
            money_cur.execute(f"UPDATE economy SET amounts = amounts + {randomCoins} WHERE user = {ser}")
            await ctx.send("낚시를 하여 잡은 물고기를 판매하여 " + str(randomCoins) + " 만큼의 돈을 벌었습니다!")
            money.commit()
        elif J_D[4] == "경비원":
            randomCoins = random.randint(50, 100)
            money_cur.execute(f"UPDATE economy SET amounts = amounts + {randomCoins} WHERE user = {ser}")
            await ctx.send("밤동안 경비를 하여 " + str(randomCoins) + " 만큼의 돈을 벌었습니다!")
            money.commit()
        elif J_D[4] == "유튜버":
            randomCoins = random.randint(50, 100)
            money_cur.execute(f"UPDATE economy SET amounts = amounts + {randomCoins} WHERE user = {ser}")
            await ctx.send("유튭각을 잡은 컨텐츠를 유튜브에 업로드하여 " + str(randomCoins) + " 만큼의 돈을 벌었습니다!")
            money.commit()
        elif J_D[4] == '무직':
            await ctx.send("직업을 가지고있지않네요! 'ㅌ직업'으로 직업을 보신후 'ㅌ취직'으로 직업을 선택하세요!")

def setup(bot):
    bot.add_cog(Economy(bot))