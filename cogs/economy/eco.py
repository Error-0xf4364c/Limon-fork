from gc import collect
import discord
from discord import app_commands
from discord.ext import commands
from fetchData import fetchData

import random

class economy(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "daily", description = "Günlük Coin Al")
    async def daily(self, interaction: discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]


        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})


        moneyRecieved = random.randint(0, 100)


        #userData, collection = await fetchData(self.bot, interaction.user.id)


        userData["coins"] += moneyRecieved
        await collection.replace_one({"_id" : interaction.user.id}, userData)

        await interaction.response.send_message(f"Günlük kazanç : {moneyRecieved}")

    @app_commands.command(name = "wallet", description="Cüzdanını Aç")
    async def wallet(self, interaction : discord.Interaction):

        userData, collection = await fetchData(self.bot, interaction.user.id)
        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})
        await interaction.response.send_message(f"Cüzdanınızda {userData['coins']} coin var.")



async def setup(bot:commands.Bot):
    await bot.add_cog(economy(bot), guilds= [discord.Object(id =964617424743858176)])