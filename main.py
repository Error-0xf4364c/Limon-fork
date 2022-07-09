import asyncio
import aiohttp
import discord
import os
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


        await bot.tree.sync(guild = discord.Object(id = guild_id))

    """async def close(self):
        await super().close()
        await self.session.close()"""

    async def on_ready(self):
        print("Bot aktif")
        

bot = MyBot()

async def main():
    async with bot:
        
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())