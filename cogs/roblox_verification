from discord.ext import commands
import discord
import random
import requests
from discord.ext.commands import BucketType


class Robloxverify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_enabled(self, ctx):
        data = await self.bot.config.find(ctx.guild.id)
        if data is None:
            return False
        elif "roblox_role" in data:
            return True
        return False

    async def is_verified(self, ctx):
        data = await self.bot.roblox.find(0)

        if data is None:
            return False
        elif str(ctx.author.id) in data:
            return True

        return False

    async def get_verified_role(self, ctx):
        data = await self.bot.config.find(ctx.guild.id)
        return ctx.guild.get_role(["roblox_role"])

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.max_concurrency(1, per=BucketType.guild, wait=False)
    async def rosetup(self, ctx):
        await ctx.send('Are you sure you\'d like to start the setup?')

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.channel and 'yes' or 'no' in m.content.lower()

        ap = await self.bot.wait_for('message', check=check, timeout=300)

        if ap.content.lower() == 'yes':
            await ctx.send('Wonderful, please mention the role or type its ID that I should give once members verify.')

            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.channel

            ap2 = await self.bot.wait_for('message', check=check, timeout=300)

            if '<' in ap2.content:
                role = ap2.content

                bruh = role.split('&')

                smh = bruh[1]

                bruh2 = smh.split('>')

                role = ctx.guild.get_role(int(bruh2[0]))
                if role is None:
                    await ctx.send('Invalid role, rerun the command.')
                elif role is not None:
                    await self.bot.config.upsert({"_id": ctx.guild.id, "roblox_role": role.id})
                    await ctx.send('Succesfully setup roblox verification.')
            else:

                role = ctx.guild.get_role(ap2.content)

                if role is None:
                    await ctx.send('Invalid role, rerun the command.')
                elif role is not None:
                    await self.bot.config.upsert({"_id": ctx.guild.id, "roblox_role": role.id})
                    await ctx.send('Succesfully setup roblox verification.')

        else:
            await ctx.send('Setup stopped.')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    async def roverify(self, ctx):
        def random_str(y):
            str1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            return ''.join(random.choice(str1) for i in range(y))

        if await self.is_enabled(ctx) is True:
            if await self.is_verified(ctx) is False:
                bruhlelsmh = random_str(10)
                em = discord.Embed(
                    title='Verification',
                    description=f'Hello {ctx.author.mention} please state your roblox username so we can verify you. Say `cancel` at any time to stop this.'
                )
                await ctx.send(embed=em)

                def check(m):
                    return m.author == ctx.author

                ap = await self.bot.wait_for('message', check=check, timeout=300)
                if 'cancel' in ap.content.lower():
                    await ctx.send('Verification stopped.')
                    return
                elif ' ' in ap.content:
                    await ctx.send('Invalid username.')
                    return
                elif len(ap.content) < 3 or len(ap.content) > 20:
                    await ctx.send('Invalid username.')
                    return
                else:
                    try:
                        em = discord.Embed(
                            title='Verification',
                            description=f'Please put `{bruhlelsmh}` as your account description. Once done, say `done`.'
                        )
                        await ctx.send(embed=em)

                        def check(m):
                            return m.content in ('done', 'cancel') and m.author == ctx.author

                        apsmh = await self.bot.wait_for('message', check=check, timeout=300)

                        if 'cancel' in apsmh.content.lower():
                            return await ctx.send('Verification stopped.')
                        else:
                            you_bruhsmh = requests.get(
                                f'https://api.roblox.com/users/get-by-username?username={ap.content}')
                            breh = you_bruhsmh.json()

                            wtfsmh = breh["Id"]

                            urlsmh = requests.get(f"https://users.roblox.com/v1/users/{wtfsmh}")

                            linksmh = urlsmh.json()

                            if linksmh["description"] == f'{bruhlelsmh}':
                                em = discord.Embed(
                                    title='Verification',
                                    description=f'Succesfully verified you as `{ap.content}`!'
                                )
                                await ctx.send(embed=em)
                                await ctx.author.add_roles(await self.get_verified_role(ctx))

                            else:
                                em = discord.Embed(
                                    title='Verification',
                                    description=f'I wasn\'t able to find the description on `{ap.content}` profile.'
                                )
                                await ctx.send(embed=em)
                    except Exception as e:
                        print(e)

            elif await self.is_verified(ctx) is True:
                await ctx.send('You\'re already verified.')
        elif await self.is_enabled(ctx) is False:
            await ctx.send('This server has not enabled roblox verification.')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disverify(self, ctx):
        if self.is_verified(ctx) is True:
            await self.bot.roblox.unset({"_id": 0, str(ctx.author.id): 1})
            await ctx.send("Unverified")
        else:
            await ctx.send(
                "You're not verified, meaning that you can't be unverified because you aren't verified :neutral_face:")


def setup(bot):
    bot.add_cog(Robloxverify(bot))
