from discord.ext import commands
import asyncio
from timeit import default_timer as timer
import lorem
import time
import discord
import random

def calc(arg):
    if arg > 50:
        return 'above average'
    elif arg < 50:
        return 'bellow average'
    elif arg == 50:
        return 'average'

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def cookie(self, ctx):
        a = await ctx.send('First one to eat the cookie wins!')
        await asyncio.sleep(3)
        await a.edit(content='3')
        await asyncio.sleep(1)
        await a.edit(content='2')
        await asyncio.sleep(1)
        await a.edit(content='1')
        await asyncio.sleep(1.0 + float(f'0.{random.randint(0, 10)}'))
        await a.add_reaction('🍪')
        start = timer()

        def check(*args):
            return args[1].id != 731197041006346281 and args[0].message.id == a.id

        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        if str(reaction) == '🍪':
            end = timer()
            if user.name == ctx.guild.me.name:
                return await ctx.send('Something went wrong! Someone could be trying to cheat...')
            await a.edit(content=f'{user.name} won in `{round(end - start, 5)}s`!')

    # credit to Stella for the idea and the copy paste check :D
    @commands.command()
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def typeracer(self, ctx):
        msg = await ctx.send('Starting soonly... be ready')
        await asyncio.sleep(1)
        correct = lorem.sentence()
        display = ''.join(map("\u200b{}".format, correct))
        content = discord.Embed(title='Typeracer',
        description=f"Type this please: ***\n{display}***"
                                )
        await msg.edit(embed=content)

        def m_2(m_s):
            return m_s.id != 727910779696971868 and m_s.content in [correct, display] and m_s.channel == ctx.channel

        try:
            while True:
                start = time.perf_counter()
                m = await self.bot.wait_for("message", check=m_2, timeout=30)
                if m.content == correct:

                    end = time.perf_counter()
                    time_elp = end-start
                    else_ = len(correct)/5
                    time_elp2 = time_elp/60

                    avg_func = round(else_/time_elp2) - 40
                    avg_v2 = avg_func/round(else_/time_elp2)
                    avg_v3 = avg_v2 * 100

                    await msg.edit(embed=discord.Embed(
                                description=f'Good job {m.author.mention}, you have a typing speed of `{round(else_/time_elp2)} wpm` it took you '
                                f'`{round(time_elp)}s` '
                                f'and the lenght of the sentence was `{len(correct)}` characters. Your typing speed is '
                                f'`{round(abs(avg_v3))}%` *{calc(round(else_/time_elp2))}*.'))
                    break
                else:
                    await ctx.send('Don\'t copy paste it.')
                    continue
        except asyncio.TimeoutError:
            await ctx.send('Times up! No one got the sentence right, please start a new game.')


def setup(bot):
    bot.add_cog(Fun(bot))
