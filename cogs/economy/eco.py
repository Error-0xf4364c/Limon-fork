from gc import collect
import discord
from discord import app_commands
from discord.ext import commands
import datetime
from fetchData import fetchData

import random

class economy(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ------ DAILY ------
    @app_commands.command(name = "daily", description = "Günlük Coin Al")
    @app_commands.checks.cooldown(
        10, 60.0, key=lambda i: (i.guild_id, i.user.id))
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

        await interaction.response.send_message(f"<:coins:996130484700581949> Günlük kazanç : {moneyRecieved}")

    @daily.error
    async def dailyError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)


    # ------ WALLET ------
    @app_commands.command(name = "wallet", description="Cüzdanını Aç")
    @app_commands.checks.cooldown(
        10, 60.0, key=lambda i: (i.guild_id, i.user.id))
    async def wallet(self, interaction : discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})
        await interaction.response.send_message(f"<:coinwallet64:996130487166849024> Cüzdanınızda {userData['coins']} coin var.")

    @wallet.error
    async def walletError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(economy(bot), guilds= [discord.Object(id =964617424743858176)])