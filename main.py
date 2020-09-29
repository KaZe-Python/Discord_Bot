import discord, os, random, asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
with open("token.txt", "r+") as file_:
    TOKEN = file_.read().strip("\n")
    file_.close()

async def chng_pr():
    await bot.wait_until_ready()
    statuses = [".help", "Al vostro servizio", "W Oasis"]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(status))
        await asyncio.sleep(5)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            raise e
bot.run(TOKEN)
