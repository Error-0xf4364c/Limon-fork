"""
 * Cupcake Bot for Discord
 * Copyright (C) 2022 Abdurrahman Coşar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import asyncio
import discord
import os
from discord import Embed
from discord.ext import commands
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN")
prefix = os.getenv("PREFIX")
app_id = os.getenv("APP_ID")
guild_id = os.getenv("OG_ID")
mongoConnection = str(os.getenv("MONGO_CONNECTION"))
log_channel = os.getenv("LOG_CHANNEL")
mongoConnectionUrl = 'mongodb+srv://'+mongoConnection+'@cluster0.acpju.mongodb.net/test'

class MyBot(commands.Bot):

    
    def __init__(self):
        super().__init__(
            command_prefix = prefix,
            intents = discord.Intents.all(),
            application_id = app_id)
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(mongoConnection)

        self.initial_extensions = []

    async def setup_hook(self):
        folders = os.listdir("./cogs")

        for folder in folders:
          if folder != "__pycache__":
            files = os.listdir(f"./cogs/{folder}")

            for file in files:
              if file != "__pycache__":
                self.initial_extensions.append(f"cogs.{folder}.{file[:-3]}")

        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # guild = discord.Object(id = guild_id)
        await bot.tree.sync()
    
    async def on_ready(self):
        
        await bot.change_presence(activity=discord.Streaming(name="Ekonomi ve Eğlence | Slash Commands", url="https://www.twitch.tv/iamabduley"))
        print(f"{self.user} is connected to Discord")




    #ADD GUILD
    async def on_guild_join(self, guild):
        log_channel = self.get_channel(log_channel)
        join_embed = Embed(color = 0x65ff50)
        join_embed.set_author(name = f"I join the {guild.name} server. It has {guild.member_count} members", icon_url = guild.icon or "https://cdn.discordapp.com/attachments/1009437091295395840/1009437593773015120/discordlogo.png")
        await log_channel.send(embed = join_embed)

    #REMOVE GUILD
    async def on_guild_remove(self, guild):
        log_channel = self.get_channel(log_channel)
        join_embed = Embed(color = 0xff3030)
        join_embed.set_author(name = f"I left the {guild.name} server. It has {guild.member_count - 1} members", icon_url = guild.icon or "https://cdn.discordapp.com/attachments/1009437091295395840/1009437593773015120/discordlogo.png")
        await log_channel.send(embed = join_embed)


bot = MyBot()

async def main():
    async with bot:
        
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
