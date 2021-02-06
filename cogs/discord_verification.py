from discord.ext import commands
import discord, asyncio, aiohttp

def disconfig_embed(ctx):
    embed = discord.Embed(
        title=f'{ctx.guild.name}',
        description='\n**VerifiedRole**\n`.disconfig verifiedrole <roleid/mention>`'
                    '\n\n**Enabled**\n`.disconfig enabled <true/false>`'
    )
    return embed


async def make_role_id(ctx, role):
    if role.isdigit():
        a = ctx.guild.get_role(role)
        if a is None:
            return False
        else:
            return True
    elif '<' in role:
        bruh = role.split('&')

        smh = bruh[1]

        bruh2 = smh.split('>')

        role2 = ctx.guild.get_role(int(bruh2[0]))
        if role2 is None:
            return False
        elif role2 is not None:
            return True
    else:
        return False


async def role_mod_check(ctx, role):
    role = ctx.guild.get_role(role)
    if any(x for i, (_, x) in enumerate(list(role.permissions)) if i in [1, 2, 3, 4, 5, 13, 27, 28]):
        return True


async def abuse_check(ctx, role):
    role1 = ctx.guild.get_role(role)
    if role1 >= ctx.author.top_role:
        return True
    else:
        return False


class DisVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='disconfig', invoke_without_command=True)
    async def _helpdis(self, ctx):
        await ctx.send(embed=disconfig_embed(ctx))

    @_helpdis.command()
    async def verifiedrole(self, ctx, role: discord.Role):
        try:
            abuse = await abuse_check(ctx, role.id)
            abuse_mod = await role_mod_check(ctx, role.id)
            if abuse is False:
                if abuse_mod is False:
                    self.bot.pool.execute(f'UPDATE verification SET roleid=$1, enabled=$2 WHERE guildid=$3;',
                                          role.id, True, ctx.guild.id)
                else:
                    return await ctx.send('You may not set a role that has moderation permissions.')
            else:
                return await ctx.send('You may not set a role that\'s higher or equal to your highest one.')
        except:
            return await ctx.send('Improper value passed!')
        await ctx.send(f'Successfully changed the config role to `{role.name}`!')

    @_helpdis.command()
    async def enabled(self, ctx, role: bool):
        a = await self.is_empty(ctx)
        try:
            if a is False:
                await self.bot.pool.execute(f'UPDATE verification SET enabled=$1 WHERE guildid=$2;', role,
                                            ctx.guild.id)
            else:
                return await ctx.send('You may not enable the module until you setup discord verification.')
        except:
            return await ctx.send('Improper value passed!')
        await ctx.send(f'Successfully changed the value to `{role}`!')

    async def is_empty(self, ctx):
        value = await self.bot.pool.fetchval(f'SELECT roleid FROM verification WHERE guildid={ctx.guild.id};')

        if value is None:
            return True
        return False

    async def is_enabled_check(self, ctx):
        value = await self.bot.pool.fetchval(f'SELECT enabled, roleid FROM verification WHERE guildid={ctx.guild.id};')
        role = ctx.guild.get_role(value["roleid"])

        if role is None:
            return False
        return value

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.guild_only()
    async def verify(self, ctx):
        if await self.is_enabled_check(ctx):
            embedlol = discord.Embed(
                title=f'Welcome to {ctx.guild.name}!',
                description='Hello, in order to gain acces to this server, __**you must**__ verify to prove that you aren\'t a bot. Please solve the simple captcha bellow, note that **captchas** are case sensitive.'
                            '\n\n**Why do I have to verify?**\n\nVerification is used to prevent malicious automated user-bot attacks against an guild.'
                            '\n\n**Your captcha:**'
            )
            embedlol.timestamp = ctx.message.created_at
            async with aiohttp.ClientSession() as cs:
                async with cs.get('http://nooonesad.pythonanywhere.com/api/') as images:
                    images1 = await images.json()
                    random_image = images1["url"]
                    images.close()

            embedlol.set_image(url=f"{random_image}")
            await ctx.send('I\'ve sent you a captcha in DMs.')
            await ctx.author.send(embed=embedlol)
            bruh = images1["captcha"]

            def check(m):
                return m.author == ctx.author and m.channel == ctx.author.dm_channel

            a = await self.bot.wait_for('message', check=check, timeout=20)
            if a.content != bruh:
                await ctx.author.send('You\'ve got **2** tries left.')

                def check2(m):
                    return m.author == ctx.author and m.channel == ctx.author.dm_channel

                a2 = await self.bot.wait_for('message', check=check2, timeout=20)
                if a2.content != bruh:
                    await ctx.author.send('You\'ve got **1** tries left.')

                    def check3(m):
                        return m.author == ctx.author and m.channel == ctx.author.dm_channel

                    a3 = await self.bot.wait_for('message', check=check3, timeout=20)

                    if a3.content != bruh:
                        await ctx.author.send('Captcha failed.')
                    else:
                        await ctx.author.send('Succesfully verified you!')
                        role = ctx.guild.get_role()
                        await ctx.author.add_roles(role)
                else:
                    await ctx.author.send('Succesfully verified you!')
                    role = ctx.guild.get_role()
                    await ctx.author.add_roles(role)
            else:
                await ctx.author.send('Succesfully verified you!')
                role = ctx.guild.get_role()
                await ctx.author.add_roles(role)

        else:
            await ctx.send('This server hasn\'t enabled discord verification or hasn\'t configured it properly!')

    @verify.error
    async def verify_error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, asyncio.exceptions.TimeoutError):
            return await ctx.author.send('You haven\'t responded in time! Please re-run the command.')


def setup(bot):
    bot.add_cog(DisVerify(bot))
