"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import random
import yaml
from yaml import Loader
from fetchdata import *

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis['clock']

slot_left = emojis['slotleft']
slot_mid = emojis['slotmid']
slot_right = emojis['slotright']

slot7 = emojis['slotseven']
slotCherry = emojis['slotcherry']
slotCupcake = emojis['slotcupcake']
slotHeart = emojis['slotheart']
cross = emojis['cross']


class Slot(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="slot", description="Slot oyna ve paranı katla!")
    @app_commands.describe(amount='Miktar giriniz')
    @app_commands.checks.cooldown(
        1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def slot(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 50000]):
    
        await interaction.response.send_message(content = "Slot makinesi arızalı! Lütfen daha sonra tekrar deneyiniz.", ephemeral = True)
        """
        userData, collection = await economyData(self.bot, interaction.user.id)
        userCareerData, careerCollection = await careerData(self.bot, interaction.user.id)
        

        if userData["coins"] < amount:
            return await interaction.response.send_message(f"{cross} **|** Bakiyeniz yetersiz!")


        if "points" not in userCareerData:
            newCareerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareerData ,newCareerData)

        if not "gamble_point" in  userCareerData["points"]:
            gambleData = { "$set" : {"points.gamble_point" : 0}}
            await careerCollection.update_one(userCareerData ,gambleData)

        userCareerData["points"]['gamble_point'] += 1

        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        
        await interaction.response.send_message(f"`CUP SLOT`\n{slot_left}{slot_mid}{slot_right}\n`------->` <:Cupcoins:997159042633961574>{amount:,}\n`------->` ???")
        
        cupcakeReward = 5
        heartReward = 2
        sevenReward = 3
        cherryReward = 1

        slots = {
            0 : slot7,
            1 : slotCherry,
            2 : slotCupcake,
            3 : slotHeart
        }

        result1 = random.choice(slots)
        result2 = random.choice(slots)
        result3 = random.choice(slots)
        await asyncio.sleep(3)

        reward = 2
        if (result1 == result2) and (result1 == result3):
            if result1 == slot7:
                reward = sevenReward
            elif result1 == slotCherry:
                reward = cherryReward
            elif result1 == "<:slotCupcake:1001820992928223274>":
                reward == cupcakeReward
            elif result1 == "<:slotHeart:1001820997151903785>":
                reward = heartReward
            await interaction.edit_original_response(content = f"`CUP SLOT`\n{result1}{result2}{result3}\n`------->` <:Cupcoins:997159042633961574>{amount:,}\n`------->` <:Cupcoins:997159042633961574>{amount *reward:,}")
            userData['coins'] += reward
            await collection.replace_one({"_id" : interaction.user.id}, userData)
        
        userData['coins'] -= amount
        await collection.replace_one({"_id" : interaction.user.id}, userData)
        await interaction.edit_original_response(content = f"`CUP SLOT`\n{result1}{result2}{result3}\n`------->` <:Cupcoins:997159042633961574>{amount:,}\n`------->` Kaybettin ;c")
        """
    @slot.error
    async def slotError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)
        else:
            print(f"SlotErr: {error}")

    

async def setup(bot:commands.Bot):
    await bot.add_cog(Slot(bot))