import asyncio
import aiohttp
import discord
import os
from discord import Embed
from discord.ext import commands
import motor.motor_asyncio
from dotenv import load_dotenv

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
        await bot.tree.sync()

    """async def close(self):
        await super().close()
        await self.session.close()"""

    async def on_ready(self):
        await bot.change_presence(activity=discord.Streaming(name="Public Beta", url="https://www.twitch.tv/iamabduley"))
        print("Bot aktif")
        
    async def on_guild_join(self, guild):
        embed = Embed(title = "Sunucuya Eklendi!", color = 0x66F00)
        embed.set_author(name = guild.name , icon_url = guild.icon)
        embed.add_field( name = "ID", value = guild.id, inline = False)
        embed.add_field( name = "Üye Sayısı", value = guild.member_count, inline = False)
        #embed.add_field( name = "Oluşturulma tarihi", value = guild.created_at, inline = False)
        embed.add_field( name = "Sahip", value = f"{guild.owner} {guild.owner.id}", inline = False)
        await bot.get_channel(1001859600708022332).send(embed= embed)

    async def on_guild_remove(self, guild):
        embed = Embed(title = "Sunucudan Ayrıldı!", color = 0xFF2400)
        embed.set_author(name = guild.name , icon_url = guild.icon)
        embed.add_field( name = "ID", value = guild.id, inline = False)
        embed.add_field( name = "Üye Sayısı", value = guild.member_count, inline = False)
        #embed.add_field( name = "Oluşturulma tarihi", value = guild.created_at, inline = False)
        embed.add_field( name = "Sahip", value = f"{guild.owner} {guild.owner.id}", inline = False)
        await bot.get_channel(1001859600708022332).send(embed= embed)
        

bot = MyBot()

async def main():
    async with bot:
        
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())