import discord
from discord.ext import commands
from discord.utils import get
import json, os, asyncio

class RoleReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.save_users())
        try:
            with open(os.path.join(os.getcwd(), "dict.json"), "r+") as f:
                self.role_emoji = json.load(f)
        except FileNotFoundError:
            print("[!] File not found")



    @commands.command(pass_context = True, aliases=['r', 'reaction'])
    @commands.guild_only()
    async def _reaction(self, ctx : commands.Context,  _msg_id : int, _emoji : discord.Emoji, _role : discord.Role):
        message = await ctx.channel.fetch_message(_msg_id)
        role = _role
        emoji = _emoji
        #Check if the dictionary exist
        await ctx.send(emoji)
        isfile = os.path.isfile(".\dict.json")
        if isfile:
            with open(".\dict.json", "r+") as f:
                try:
                    self.role_emoji = json.load(f)
                except Exception as e:
                    raise(e)

        emoji_id = str(emoji.id)
        role_id = str(role.id)
        if not emoji_id in self.role_emoji:
            self.role_emoji[emoji_id] = {}
            self.role_emoji[emoji_id]['role'] = role_id
            print("# DEBUG: Creating Emoji Role Table")

        #Try to add the reaction to the specified message
        try:
            await message.add_reaction(emoji)
            print("[!] New reaction added")
            print(f"[DTL] Message ID: {msg_id}, Command Author: {ctx.author}")
        except Exception as e:
            print("Qualcosa è andato storto")
            raise e

    @_reaction.error
    async def _reaction_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print("[!] Argomento non valido")
            print(error)
            await ctx.send(error)

    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                with open(os.path.join(os.getcwd(), "dict.json"), 'r+') as f:
                    json.dump(self.role_emoji, f, indent=4)
                await asyncio.sleep(30)
            except Exception as e:
                print("[!] Of Course if the file doesn't exit HTH should I do something with it...")
                raise e
                return

def setup(bot):
    bot.add_cog(RoleReaction(bot))
