
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import yaml
from yaml import Loader
from fetchdata import create_wallet

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

wallet = emojis["limonbank"]
morelicash = emojis["morelicash"]
clock = emojis["clock"] or "⏳"


class economy(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
#i.guild_id, 
    # ------ DAILY ------
    @app_commands.command(name = "daily", description = "Günlük LiCash alın")
    @app_commands.checks.cooldown(
        1, 86400, key=lambda i: (i.user.id))
    async def daily(self, interaction: discord.Interaction):

        userData, collection = create_wallet(self.bot, interaction.user.id)
        moneyRecieved = random.randint(400, 1100)

        userData["cash"] += moneyRecieved
        collection.replace_one({"_id" : interaction.user.id}, userData)

        await interaction.response.send_message(f"{morelicash} Günlük kazancınız: **{moneyRecieved}** LiCash")

    @daily.error
    async def dailyError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",
                                                    ephemeral=True)


    # ------ WALLET ------
    @app_commands.command(name = "balance", description="Hesap bakiyenizi öğrenin")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def wallet(self, interaction : discord.Interaction):

        db = self.bot.database["limon"]
        collection = db["wallet"]

        if collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "cash" : 10000
            }
            collection.insert_one(newData)
            return await interaction.response.send_message(f"{wallet} | Bu harika! Geliştirici size tam **10,000** LiCash hediye etti!")

        userData = collection.find_one({"_id" : interaction.user.id})
        await interaction.response.send_message(f"{wallet} Cüzdanınızda **{userData['cash']:,}** LiCash bulunuyor.")

    @wallet.error
    async def walletError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(economy(bot))