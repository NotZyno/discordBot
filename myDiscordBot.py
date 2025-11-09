import discord
from discord.ext import commands
import datetime as date
from cogs import CommandCog
from cogs import ListenerCog
from utils import colors, getTime
GRAY = "\033[90m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"


# Główna klasa bota
class MyDiscordBot:
    def __init__(self, token):
        self.token = token

        # Uprawnienia bota?
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.messages = True

        # Inicjalizacja bota
        self.bot = commands.Bot(command_prefix='!', intents=intents)

        # Dodanie coga (Nw co to jest) potrzebne do komend
        async def hook():
            # Należy dodać cogi
            # await self.bot.add_cog(CommandCog(self.bot))
            # await self.bot.add_cog(ListenerCog(self.bot))

            # Ładowanie cogów poprzez rozszerzenia tzn cogi są ładowane przez funkcję setup w klasach modułu cogs
            await self.bot.load_extension('cogs.commands')
            await self.bot.load_extension('cogs.listeners')

            # Synchronizacja komend slash
            try:
                self.bot.loop.create_task(self.sync_commands())
            except AttributeError as e:
                print(f"Error syncing commands: {e}")
        self.bot.setup_hook = hook
            
        # Łączenie bota
        @self.bot.event
        async def on_ready():
            print(f'[{self.getTime()}] LOGGED IN AS {GREEN}{self.bot.user}{RESET}')
            try:
                # Wiadomość o włączeniu bota
                await self.bot.wait_until_ready()
                channel = self.bot.get_channel(1396137986193752134)  # Zamień na ID swojego kanału
                message_id = 1426708832469647390  # Zamień na ID swojej wiadomości
                msg = await channel.fetch_message(message_id)
                await msg.edit(embed=discord.Embed(title="Bot jest włączony", color=0x00ff00))
            except Exception as e:
                print(f"Error updating message: {e}")

        # Obsługa błędów komend
        @self.bot.event
        async def on_command_error(ctx: commands.Context, error: commands.CommandError):
            print(f"Użytkownik {ctx.message.author} wywołał {ctx.command}: {error}")
            if ctx.message.content.startswith('!!'):
                return
            if isinstance(error, commands.CommandNotFound):
                if ctx.message.content.startswith('!'):
                    await ctx.send(f"Nie ma komendy {ctx.message.content}")
                return
    # Uruchomienie bota
    async def run(self):
        await self.bot.start(self.token)

    async def sync_commands(self):
        await self.bot.wait_until_ready()
        try:
            await self.bot.tree.sync(guild=discord.Object(1186370955644260492)) # Można ustawić na dany serwer (przyśpiesza to dodawanie komend slash)
        except Exception as e:
            print(f"Error syncing commands: {e}")

     # Getter Time
    def getTime(self):
        return date.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

