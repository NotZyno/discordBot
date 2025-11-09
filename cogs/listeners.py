import discord
from discord.ext import commands
from discord import app_commands
import datetime as date
from utils import fetchAPI, fetchToken
import requests
import os
from utils import getTime
from utils.colors import *

# Co to jest?
class ListenerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bearer = None
        self.token = os.getenv("API")

    # Reakcja na wiadomość
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f"{getTime()}{RESET} Użytkownik: {message.author} wysłał wiadomość: " f"{message.content.replace(f'<@{message.mentions[0].id}>', '@'+message.mentions[0].name) if message.mentions else {getTime()} + message.content}") # Pierdzielenie
        if message.author == self.bot.user:
            return
        if message.author.id == 529349846218309652:
            await message.channel.send("Potrzebujesz antyperspirantu!")
            return
        if message.content.startswith('!reload'):
            return
        if message.channel.name != "bot-ai":
            await message.channel.send("Wiadomości mogą być wysyłane tylko w kanale #bot-ai")
            return
        if not message.content.startswith('!!'):
            return
        

        # Pobieranie tokenu, jeżeli API wymaga
        
        # if self.bearer is None: # Pobierz token tylko raz
        #     self.bearer = await fetchToken(password="AAAA", username="AAAA")
        #     self.bearer = self.bearer.json()
        #     self.bearer = self.bearer.get("token")
        #     print(f"******{self.getTime()} Token: {self.bearer} ******")

        res: requests.Response = await fetchAPI(message.content, token=self.token) # Odpowiedź z API
        print(f"[{GRAY}{getTime()}{RESET}{GREEN}res.status_code: {res.status_code}{RESET}") # Status code

        if(res.status_code == 200): # Jeżeli Status code 200
            await message.channel.send(f"{res.json()['candidates'][0]['content']['parts'][0]['text']}") # Pierdzielenie
            print(f"{GRAY}{getTime()}{RESET} Odpowiedź API: {res.json()['candidates'][0]['content']['parts'][0]['text']}") # Pierdzielenie
        else:
            print(f"{GRAY}{getTime()}{RESET} Błąd przy pobieraniu API, status: {res.status_code}*") # Jeszcze więcej pierdzielenia
            await message.channel.send(f"*Błąd przy pobieraniu API, status: {res.status_code}*") # Pierdzielenie ++

    # Event na zmianę stanu głosowego tzn. dołączenie/opuszczenie kanału
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel == after.channel:
            print(f"{getTime()} Użytkownik {member} wyciszył się" if member.voice.self_mute else f"{getTime()} Użytkownik {member} odciszył się") # wyciszenie/odciszenie
        elif before.channel is not None and after.channel is not None:
            print(f"{getTime()} Użytkownik: {member} zmienił stan głosowy z {before.channel} na {after.channel}")
        elif before.channel is None and after.channel is not None:
            print(f"{getTime()} Użytkownik: {member} dołączył do kanału {after.channel}")
        elif before.channel is not None and after.channel is None:
            print(f"{getTime()} Użytkownik: {member} opuścił kanał {before.channel}")
        return
    
    def getTime(self):
        return date.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
# Potrzebne do reloadowania coga, ładowanie coga
async def setup(bot: commands.Bot):
    await bot.add_cog(ListenerCog(bot))
