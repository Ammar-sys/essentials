import asyncpg
import asyncio
from discord.ext import commands
import discord
import sys, traceback

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(
    command_prefix='.',
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    print('Essentials has successfully booted up! | v 2.0.0 | Credit to Vixen and Ammar')

initial_extensions = [
    'discord_verification',
    'ticketsys',
    'events_jole',
    'erh',
    'eval',
    'fun',
    'roblox_verification'
]

if __name__ == "__main__":
    for cog in initial_extensions:
        try:
            bot.load_extension(f"cogs.{cog}")
            print(f"Successfully loaded {cog}!")
        except Exception as e:
            print(
                f"Failed to load {cog}, error:\n",
                file=sys.stderr
            )
            traceback.print_exc()

loop = asyncio.get_event_loop()
bot.pool = loop.run_until_complete(asyncpg.create_pool(
                            host="localhost",
                            port='5433',
                            database="timedsys",
                            user="postgres",
                            password="Bruhbruh123",
                                    ))

def set_token():
    token = open('./essentials_token.txt', 'r').read()
    return token

bot.run(
    # bot.token,
    set_token(),
    reconnect=True
)
