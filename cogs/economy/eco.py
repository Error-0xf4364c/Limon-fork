
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import yaml
from yaml import Loader

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

wallet = emojis["wallet"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"


class economy(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
#i.guild_id, 
    # ------ DAILY ------
    @app_commands.command(name = "daily", description = "Get a daily Cupcoin")
    @app_commands.checks.cooldown(
        1, 86400, key=lambda i: (i.user.id))
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

        await interaction.response.send_message(f"{cupcoins} Your daily earnings: **{moneyRecieved}** Cupcoin")

    @daily.error
    async def dailyError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait `{timeRemaining}`s and Try Again!",
                                                    ephemeral=True)


    # ------ WALLET ------
    @app_commands.command(name = "wallet", description="Open your wallet")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def wallet(self, interaction : discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" : 10000
            }
            await collection.insert_one(newData)
            return await interaction.response.send_message(f"{wallet} | That is so awesome! The developer gave you a gift of **10,000** Cupcoin")

        userData = await collection.find_one({"_id" : interaction.user.id})
        await interaction.response.send_message(f"{wallet} You have **{userData['coins']:,}** Cupcoin in your wallet.")

    @wallet.error
    async def walletError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait `{timeRemaining}`s and Try Again!",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(economy(bot))