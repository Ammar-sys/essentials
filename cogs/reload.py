from discord.ext import commands
import discord
import asyncio

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", aliases=["relaod"], hidden=True)
    async def _reload(self, ctx, *, cogs_to_reload: str=""):
        cogs_to_reload = cogs_to_reload.lower()
        cogs_to_reload = ["cogs." + cog for cog in cogs_to_reload.split()]
        if len(cogs_to_reload) == 0:
            cogs_to_reload = dict(self.bot.extensions)
        embed = discord.Embed()
        embed.set_author(
            name=f"| {ctx.author.name} | {chr(127850)}",
            icon_url=ctx.author.avatar_url
        )
        success = "https://essentials-bot.netlify.app/imgs/success.png"
        fail = "https://essentials-bot.netlify.app/imgs/fail.png"

        for cog in cogs_to_reload:
            if cog not in self.bot.extensions:
                embed.set_thumbnail(
                    url=fail
                )
                embed.add_field(
                    name = cog,
                    value = "That cog doesn't exist!"
                )
                print(f"{cog}: That cog doesn't exist!")
                continue
            else:
                try:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                except Exception as e:
                    embed.set_thumbnail(
                        url=fail
                    )
                    embed.add_field(
                        name = cog,
                        value = f"Error trying to reload the cog: {str(e)}"
                    )
                    print(f"{cog}: Error trying to reload the cog: {str(e)}")
                    continue
                embed.set_thumbnail(
                    url=success
                )
                embed.add_field(
                    name = cog,
                    value = "Reloaded properly."
                )
                print(f"{cog}: Reloaded properly.")
        await ctx.send(
            embed=embed#,
            # delete_after = 5
        )
        await asyncio.sleep(.5)
        await ctx.message.delete()

    @commands.command(name="unload", aliases=["disable"])
    async def unload(self, ctx, *, cog: str):
        self.bot.unload_extension(f"cogs.{cog}")
        await ctx.send(f"Disabled {cog}")

    @commands.command(name="load", aliases=["enable"])
    async def load(self, ctx, *, cog: str):
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"Enabled {cog}")

def setup(bot):
    bot.add_cog(Reload(bot))
