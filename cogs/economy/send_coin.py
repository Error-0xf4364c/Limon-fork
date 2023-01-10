import discord
from discord import app_commands
from discord.ext import commands
import yaml
from yaml import Loader
import datetime
from fetchData import *

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"

whiteCross = emojis['whiteCross']
cross = emojis['cross']
send = emojis['send']

class sendCoin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "send", description = "Arkadaşlarına Cupcoin gönder!")
    @app_commands.describe(friend='Kime Cupcoin göndereceksin?', amount="Ne kadar Cupcoin göndereceksin?")
    @app_commands.checks.cooldown(
        1, 50.0, key=lambda i: (i.guild_id, i.user.id))
    async def send(self, interaction: discord.Interaction, friend: discord.User, amount: app_commands.Range[int, 1, 50000]):

        userData, collection = await economyData(self.bot, interaction.user.id)
        userCareerData, careerCollection = await careerData(self.bot, interaction.user.id)

        

        if friend == interaction.user:
            return await interaction.response.send_message(f"{cross} Kendine para gönderemezsin!", ephemeral=True)

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return
        elif await collection.find_one({"_id": friend.id}) == None:
            return await interaction.response.send_message(f"{whiteCross} Belirttiğiniz kullanıcı bulunamadı ;c", ephemeral= True)

        userData = await collection.find_one({"_id": interaction.user.id})
        targetData = await collection.find_one({"_id": friend.id})

        if userData['coins'] < amount:
            return await interaction.response.send_message(f"{cross} Göndermek istediğin kadar Cupcoine sahip değilsin!")
        
        userCareerData["points"]['send_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        userData['coins'] -= amount
        targetData['coins'] += amount
        await collection.replace_one({"_id": interaction.user.id}, userData)
        await collection.replace_one({"_id": friend.id}, targetData)
        await interaction.response.send_message(f"{send} **{friend.name}** arkadaşına başarıyla **{amount:,}** Cupcoin gönderdin.")
    @send.error
    async def sendError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s bekleyin!",
                                                    ephemeral=True)
        else:
            print(error)

async def setup(bot:commands.Bot):
    await bot.add_cog(sendCoin(bot))
