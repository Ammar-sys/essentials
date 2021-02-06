from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def setprefix(self, ctx, *, prefix=None):
        if len(prefix) >= 8:
            return await ctx.send('Prefix must not be longer than 8 characters.')

        if prefix is None:
            return await ctx.send('The prefix must not be empty.')

        if ' ' in prefix:
            return await ctx.send('Prefix must not have a space in it.')

        prf = await self.bot.pool.fetch('SELECT prefix FROM guilds WHERE guildid = $1;', ctx.guild.id)

        if prefix == prf[0]["prefix"]:
            return await ctx.send('That\'s already the prefix!')

        await ctx.send(f'Successfully changed the prefix to `{prefix}`!')
        await self.bot.pool.execute('UPDATE guilds SET prefix = $1 WHERE guildid = $2;', prefix, ctx.guild.id)

def setup(bot):
    bot.add_cog(Fun(bot))
