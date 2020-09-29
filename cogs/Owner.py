import discord
from discord.ext import commands

class ServerOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"L'estensione {cog}, è stata ricaricata")
        except Exception as e:
            print(f"{cog} non può essere ricaricata")
            await ctx.send(f"Un errore ha bloccato la ricarica di {cog}")
            raise e

    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        try:
            await self.bot.logout()
        except:
            print("EnvironmentError")
            self.bot.clear()

            
def setup(bot):
    bot.add_cog(ServerOwner(bot))
