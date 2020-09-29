import discord
from discord.ext import commands
import asyncio

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #A fun relatively useless command, to see some info about a user
    @commands.command(pass_context=True)
    @commands.guild_only()
    async def info(self, ctx, member: discord.Member):
        #Making a list with all guild roles
        roles = [role for role in member.roles]

        #Creating the embed
        eb = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)

        #Setting up all embed features
        eb.set_author(name=f"Info Utente = {member}")
        eb.set_thumbnail(url=member.avatar_url)
        eb.set_footer(text=f"Richiesto da: {ctx.author}", icon_url=ctx.author.avatar_url)

        #Creating all embed fields
        eb.add_field(name="ID: ", value = member.id)
        eb.add_field(name="Nome nel server: ", value = member.display_name)
        eb.add_field(name="Data di creazione account: ", value = member.created_at.strftime("%a, %#D %B %Y, %I:%M %p UTC"))
        eb.add_field(name="Accesso al server: ", value = member.joined_at.strftime("%a, %#D %B %Y, %I:%M %p UTC"))
        eb.add_field(name=f"Ruoli ({len(roles)})", value = " ".join([role.mention for role in roles]))
        eb.add_field(name="Ruolo più alto: ", value=member.top_role.mention)
        eb.add_field(name="E un bot?", value=member.bot)

        #Sending the last created embed to the chat
        asyncio.sleep(.5)
        await ctx.send(embed=eb)

    #Command for clearing the chat messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx, amount: int=10):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"Tutti i messaggi sono stati eliminati con successo. Numero messaggi eliminati: {amount}")
        await ctx.send(ctx.message.author)

    #Handling the possible errors created by clear command
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            print(error)
        if isinstance(error, commands.BadArgument):
            await ctx.send("Il valore inserito non è valido")

    #This command is used for, as the name applies, banning a user
    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, user: discord.Member, *, reason="Nessun motivo"):
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} è stato bannato da {ctx.author.mention}. Motivo: [{reason}]")

    #This command is used for, as the name applies, kicking a user out of the server. (The difference between ban and kick is that after a ban the user cannot join back even with an invite)
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, user: discord.Member, *, reason="Nessun motivo"):
        await user.kick(reason=reason)
        await ctx.send(f"{user.mention} è stato kickato da {ctx.author.mention}. Motivo: [{reason}]")


def setup(bot):
    bot.add_cog(Mod(bot))
