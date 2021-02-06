import asyncpg
import asyncio
from discord.ext import commands
import discord
import sys, traceback
import json

async def get_prefix(bot_par, message):
    if not message.guild:
        return commands.when_mentioned_or(".")(bot_par, message)

    data = await bot.pool.fetch('SELECT prefix FROM guilds WHERE guildid=$1;', message.guild.id)

    return data[0]["prefix"]

def read_json():
    with open(fr"config.json", "r") as f:
        data = json.load(f)
    return data


config = read_json()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=intents
)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Essentials has successfully booted up! | v.2 | Credit to Vixen and Ammar')


initial_extensions = [
    'discord_verification',
    'ticketsys',
    'events_jole',
    'erh',
    'eval',
    'fun',
    'help',
    'config',
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
    host=config["database_info"]["host"],
    port=config["database_info"]["port"],
    database=config["database_info"]["database"],
    user=config["database_info"]["user"],
    password=config["database_info"]["password"],
))

bot.token = config["token"]
bot.run(
    bot.token,
    reconnect=True
)
