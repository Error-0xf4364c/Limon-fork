
import discord
from discord import app_commands
from discord.ext import commands
import datetime

import random

cupcoins = "<:Cupcoins:997159042633961574>"
wallet = "<:wallet:997158473999581386>"
clock = "<:Cupclock:996129959758282842>" or "⏳"

class economy(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ------ DAILY ------
    @app_commands.command(name = "daily", description = "Günlük Cupcoin Al")
    @app_commands.checks.cooldown(
        1, 86400, key=lambda i: (i.guild_id, i.user.id))
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


        moneyRecieved = random.randint(400, 1100)


        #userData, collection = await fetchData(self.bot, interaction.user.id)


        userData["coins"] += moneyRecieved
        await collection.replace_one({"_id" : interaction.user.id}, userData)

        await interaction.response.send_message(f"{cupcoins} Günlük kazancınız: **{moneyRecieved}**")

    @daily.error
    async def dailyError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)


    # ------ WALLET ------
    @app_commands.command(name = "wallet", description="Cüzdanını Aç")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
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
        await interaction.response.send_message(f"{wallet} Cüzdanınızda **{userData['coins']:,}** Cupcoin var.")

    @wallet.error
    async def walletError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(economy(bot), guilds= [discord.Object(id =964617424743858176)])