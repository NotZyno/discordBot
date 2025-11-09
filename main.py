import discord
import myDiscordBot
import os
from dotenv import load_dotenv
import asyncio
from utils.colors import *
from utils import getTime



async def main():
    load_dotenv()  # Ładowanie zmiennych środowiskowych z pliku .env
    token = os.getenv("BOT_TOKEN") # Pobieranie tokena z .env
    try:
        bot = myDiscordBot.MyDiscordBot(token)
        await bot.run()
    except asyncio.exceptions.CancelledError as e:

        # Pobieranie embeda i edytowanie wartości na wyłączony
        msg = await bot.bot.get_channel(1396137986193752134).fetch_message(1426708832469647390) 
        await msg.edit(embed=discord.Embed(title="Bot został zatrzymany.", color=0xff0000))
        await bot.bot.close()

        print(f"{getTime()}{RED} Program został zatrzymany. {RESET}{e}")

asyncio.run(main())