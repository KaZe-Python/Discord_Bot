import discord
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def cgs(self):
        pass

def setup(bot):
    bot.add_cog(Ticket(bot))
