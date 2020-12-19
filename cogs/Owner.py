from discord.ext import commands
import discord
import ast
from config import OWNERS
from tools.autocogs import AutoCogsReload
import datetime
from dateutil.relativedelta import relativedelta
import random
import sqlite3
def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNERS

    return commands.check(predicate)

conn = sqlite3.connect("main.db")

cur = conn.cursor()
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notice_channels = []

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if str(type(e)) == "<class 'discord.ext.commands.errors.CheckFailure'>":
            pass

    @commands.command(name="프리미엄적용")
    @is_owner()
    async def insert_premium(self, ctx, member: str, year: str, month: str, day: str):
        a = random.randint(111111111, 999999999)
        b = random.randint(1111111, 9999999)
        c = random.randint(11111111111, 99999999999)
        seriel = f'{a}-{b}-{c}'


        ending = datetime.datetime.now() + relativedelta(years=int(year),months=int(month),days=int(day))
        ending = ending.strftime('%Y-%m-%d %H:%M:%S')

        cur.execute(f"INSERT INTO premium VALUES (?, ?, ?)", (member, seriel, ending))
        conn.commit()
        await ctx.send('✅')

    @commands.command(name="프리미엄삭제")
    @is_owner()
    async def deleted_premium(self, ctx, member: str):
        cur.execute("DELETE FROM premium WHERE user=" + str(member))
        conn.commit()
        await ctx.send('✅')

    @commands.command(name="프리미엄상태")
    @is_owner()
    async def show_user_premium(self, ctx, member: str):
        cur.execute(f"SELECT * FROM premium WHERE user= {member}")
        P_M = cur.fetchone()
        if P_M == None:
            await ctx.send('지정한상대의 프리미엄기간이 종료되었거나 가입하지않아 정보가 존재하지않아요!')
        else:
            await ctx.send(f'`{member}`의 프리미엄 상태\n시리얼코드: {P_M[1]}\n만료일: {P_M[2]}')

    @commands.command(name="reload", aliases=["리로드", "r"])
    @is_owner()
    async def 리로드(self, ctx, c=None):
        if c == None:
            try:
                AutoCogsReload(self.bot)
                await ctx.send(f"모든 모듈을 리로드했어요.")
            except Exception as a:
                await ctx.send(f"리로드에 실패했어요. [{a}]")
        else:
            try:
                self.bot.reload_extension(c)
                await ctx.send(f"{c} 모듈을 리로드했어요.")
            except Exception as a:
                await ctx.send(f"{c} 모듈 리로드에 실패했어요. [{a}]")

    @commands.command(name="eval")
    @is_owner()
    async def eval_fn(self, ctx, *, cmd):
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                "bot": self.bot,
                "discord": discord,
                "commands": commands,
                "ctx": ctx,
                "__import__": __import__,
                "load": self.bot.load_extension,
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = await eval(f"{fn_name}()", env)
            await ctx.send(result)
        except Exception as a:
            await ctx.send(a)




def setup(bot):
    bot.add_cog(Owner(bot))