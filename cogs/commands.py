import discord
from discord.ext import commands
from discord import app_commands
import datetime as date
from utils import getTime
from utils.colors import *

# Co to jest?
class CommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bearer = None

    # Reloadowanie cogów poprzez komendę !reload
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context):
       await self.bot.reload_extension('cogs.commands')
       await self.bot.reload_extension('cogs.listeners')
       # Aby nie czekać na synchronizację komend slash
       try:
           self.bot.loop.create_task(self._sync_commands())
           
       except AttributeError:
              print(f"{RED}[{self.getTime()}]{RESET} Błąd podczas synchronizacji komend slash")
              return

       print(f"{GRAY}[{self.getTime()}]{RESET} Bot został przeładowany")
       await ctx.send("Bot został przeładowany")

    # greet
    @commands.command()
    async def greet(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.mention}!')

    # bye
    @commands.command()
    async def bye(self, ctx: commands.Context):
        await ctx.send(f'Goodbye {ctx.author.mention}!')
    
    # a
    @commands.command()
    async def a(self, ctx: commands.Context, argument: str = None):
        if ctx.command.name == "a" and argument is None:
            await ctx.send("Poprawne użycie: !a detyr")
        if argument and argument.lower() == "detyr":
            await ctx.send(f'Dezodorant dla Detyra')

    # Event na ping (odpowiedź pong!)
    @app_commands.command(name="ping", description="Odpowiada Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    # Event na usuwanie wiadomości 
    @app_commands.command(name="delete", description="Usuwa wiadomości")
    async def delete(self, interaction: discord.Interaction, amount: int = 5):
        await interaction.response.defer(ephemeral=True) # Czekaj na odpowiedź, odpowiedź widzi tylko użytkownik, który wysłał

        messages = [msg async for msg in interaction.channel.history(limit=amount)]

        for msg in messages:
            await msg.delete()
        await interaction.followup.send("Usunięto 5 wiadomości!", ephemeral=True)

    def getTime(self):
        return date.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async def _sync_commands(self):
        await self.bot.wait_until_ready()
        try:
            await self.bot.tree.sync(guild=discord.Object(1186370955644260492)) # Można ustawić na dany serwer (przyśpiesza to dodawanie komend slash)
        except Exception as e:
            print(f"Error syncing commands: {e}")
    
# Potrzebne do reloadowania coga, ładowanie coga
async def setup(bot: commands.Bot):
    await bot.add_cog(CommandCog(bot))
