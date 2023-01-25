"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import app_commands
from discord.ext import commands
import yaml
from yaml import Loader
import datetime
from fetchdata import *

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"

whiteCross = emojis['whiteCross']
cross = emojis['cross']
send = emojis['send']

class sendCoin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "send", description = "Arkadaşlarına LiCash gönder!")
    @app_commands.describe(friend='Kime LiCash göndereceksin?', amount="Ne kadar LiCash göndereceksin?")
    @app_commands.checks.cooldown(
        1, 50.0, key=lambda i: (i.guild_id, i.user.id))
    async def send(self, interaction: discord.Interaction, friend: discord.User, amount: app_commands.Range[int, 1, 50000]):

        userData, collection = create_wallet(self.bot, interaction.user.id)
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)

        

        if friend == interaction.user:
            return await interaction.response.send_message(f"{cross} Kendine para gönderemezsin!", ephemeral=True)

        if collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message(f"{whiteCross} Hesabınız bulunamadı ;c", ephemeral= True)
        elif collection.find_one({"_id": friend.id}) == None:
            return await interaction.response.send_message(f"{whiteCross} Belirttiğiniz kullanıcı bulunamadı ;c", ephemeral= True)

        userData = collection.find_one({"_id": interaction.user.id})
        targetData = collection.find_one({"_id": friend.id})

        if userData['cash'] < amount:
            return await interaction.response.send_message(f"{cross} Göndermek istediğin kadar LiCash sahip değilsin!")
        
        userCareerData["points"]['send_point'] += 1
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        userData['cash'] -= amount
        targetData['cash'] += amount
        collection.replace_one({"_id": interaction.user.id}, userData)
        collection.replace_one({"_id": friend.id}, targetData)
        await interaction.response.send_message(f"{send} **{friend.name}** arkadaşına başarıyla **{amount:,}** LiCash gönderdin.")
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
