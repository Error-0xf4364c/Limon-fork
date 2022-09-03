import asyncio
import aiohttp
import discord
import os
from discord import Embed
from discord.ext import commands
import motor.motor_asyncio
from dotenv import load_dotenv
import datetime, time

load_dotenv()
token = os.getenv("discordkey")
prefix = os.getenv("prefix")
app_id = os.getenv("application_id")
guild_id = os.getenv("owner_guild_id")
mongoConnection = os.getenv("mongoConnection")


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
        #self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # guild = discord.Object(id = guild_id)
        await bot.tree.sync(guild = discord.Object(id = guild_id))

    """async def close(self):
        await super().close()
        await self.session.close()"""

    async def on_ready(self):
        await bot.change_presence(activity=discord.Streaming(name="Economy and Fun | Slash Commands", url="https://www.twitch.tv/iamabduley"))
        print("Bot aktif")

    # ADD GUILD
    async def on_guild_join(self, guild):
        log_channel = bot.get_channel(1001859600708022332)
        join_embed = Embed(color = 0x65ff50)
        join_embed.set_author(name = f"I join the {guild.name} server. It has {guild.member_count} members", icon_url = guild.icon or "https://cdn.discordapp.com/attachments/1009437091295395840/1009437593773015120/discordlogo.png")
        await log_channel.send(embed = join_embed)

    # REMOVE GUILD
    async def on_guild_remove(self, guild):
        log_channel = bot.get_channel(1001859600708022332)
        join_embed = Embed(color = 0xff3030)
        join_embed.set_author(name = f"I left the {guild.name} server. It has {guild.member_count} members", icon_url = guild.icon or "https://cdn.discordapp.com/attachments/1009437091295395840/1009437593773015120/discordlogo.png")
        await log_channel.send(embed = join_embed)

bot = MyBot()

async def main():
    async with bot:
        
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())