import discord
from discord.ext import commands
import os, json
from discord.utils import get
from discord.abc import Messageable
from discord.utils import find


def getter(instance, iterator):
    data = get(instance, id = iterator)
    return data

def get_message(_id):
    data = Messageable.fetch_message(_id)
    return data

def finder(predicate, seq):
    data = find(predicate, seq)
    return data


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words = []
        with open(os.path.join(os.getcwd(), "banned.txt"), "r+") as file_:
            for line in file_.readlines():
                self.banned_words.append(line.strip("\n"))
            file_.close()

        try:
            with open(os.path.join(os.getcwd(), "dict.json"), "r+") as f:
                self.emoji_roles = json.load(f)
        except FileNotFoundError:
            print("[!] File not found")

    #This happens only at the bot starting process
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[!] Bot succesfully started up: {self.bot.user.name}")

    #This happens whenever a new message arrives
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot:
            print(msg.author + self.bot)
        elif not msg.content.startswith(".") or list(msg.content.split(" ")):
            for word in list(msg.content.split(" ")):
                if word in self.banned_words:
                    await msg.author.ban(reason = "Used one of the banned word :/ sorry m8")
                    print("[!] User banned for using prohibithed word")
                    await msg.channel.send("Non provare a fottermi, COMANDO IO")
                    await msg.channel.send(f"User banned: {msg.author.mention}")
                else:
                    pass
        elif msg.content.startswith("https://"):
            roles = msg.guild.roles
            player_role = discord.utils.get(roles, name="❌ WARN ❌")
            await msg.delete()
            await msg.channel.send("Non si possono inviare link, *Warn Aggiunto*")
            await msg.author.add_roles(player_role)
        else:
            await self.bot.process_commands(msg)

    #This happens whenever a new member join the server
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        roles = member.guild.roles
        player_role = discord.utils.get(roles, name="🎖️ Commer 🎖️")
        if channel is not None:
            await channel.send(f"Benvenuto {member.mention}, ti auguro una buona permanenza")
        else:
            dm = await member.create_dm()
            await dm.send(f"Benvenuto {member.mention}, ti auguro una buona permanenza")
        await member.add_roles(player_role)

    #This happens whenever there's an error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Non hai i permessi necessari per eseguire quel comando")
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Non esiste nessun comando con quel nome ... (Controlla la sintassi)")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user_id = payload.user_id
        emoji_id = payload.emoji.id
        message_id : int = payload.message_id
        channel_id : int = payload.channel_id
        guild_id : int = payload.guild_id
        for _guild in self.bot.guilds:
            if str(guild_id) in str(_guild.id):
                guild : discord.Guild = _guild
        for _channel in guild.channels:
            if str(channel_id) in str(_channel.id):
                channel : discord.ChannelType.text = _channel
        message = await channel.fetch_message(message_id)
        member = getter(message.guild.members, user_id)

        if member.display_name == self.bot.user.name:
            print("# DEBUG: Reaction by bot, ignore")
            return
        if str(emoji_id) not in str(self.emoji_roles):
            print(self.emoji_roles)
            print("[!] An error occurred while adding role")
            print(f"[DTL] Invalid Emoji ID: {emoji_id}")
            return
        else:
            role = getter(guild.roles, int(self.emoji_roles[str(emoji_id)]['role']))
            await member.add_roles(role, reason="None")



    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        user_id = payload.user_id
        emoji_id = payload.emoji.id
        message_id : int = payload.message_id
        channel_id : int = payload.channel_id
        guild_id : int = payload.guild_id
        for _guild in self.bot.guilds:
            if str(guild_id) in str(_guild.id):
                guild : discord.Guild = _guild
        for _channel in guild.channels:
            if str(channel_id) in str(_channel.id):
                channel : discord.ChannelType.text = _channel
        message = await channel.fetch_message(message_id)
        member = getter(message.guild.members, user_id)

        if member.display_name == self.bot.user.name:
            print("# DEBUG: Reaction by bot, ignore")
            return
        if str(emoji_id) not in str(self.emoji_roles):
            print(self.emoji_roles)
            print("[!] An error occurred while adding role")
            print(f"[DTL] Invalid Emoji ID: {emoji_id}")
            return
        else:
            role = getter(guild.roles, int(self.emoji_roles[str(emoji_id)]['role']))
            await member.remove_roles(role, reason="None")

def setup(bot):
    bot.add_cog(Events(bot))
