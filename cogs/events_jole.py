from discord.ext import commands

def sqlify(path):
    return open(path, 'r').read()

class Event_jole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(sqlify('./sql_files/_main/_guild_join.sql'), guild.id, '.')

                await connection.execute(sqlify('./sql_files/modules/dis_ver_join.sql'), False, None, None, guild.id)
                await connection.execute(sqlify('./sql_files/modules/roblox_ver_join.sql'), False, None, None, guild.id)
                await connection.execute(sqlify('./sql_files/modules/ticket_sys_join.sql'), False, guild.id, None, None, None, None)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(sqlify('./sql_files/_main/_guild_leave.sql'), guild.id)

                await connection.execute(sqlify('./sql_files/modules/dis_ver_leave.sql'), guild.id)
                await connection.execute(sqlify('./sql_files/modules/roblox_ver_leave.sql'), guild.id)
                await connection.execute(sqlify('./sql_files/modules/ticket_sys_leave.sql'), guild.id)

def setup(bot):
    bot.add_cog(Event_jole(bot))
