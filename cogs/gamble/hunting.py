import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime

import yaml
from yaml import Loader

yaml_file = open("emojis.yml", "r")
emojis = yaml.load(yaml_file, Loader = Loader) 

yaml_file2 = open("animals.yml", "r")
animals = yaml.load(yaml_file2, Loader = Loader) 

cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"


fishes = animals["fishes"]
hunts = animals["hunts"]

import random

class hunting(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="fishing", description="Balık tut.")
    @app_commands.checks.cooldown(
        1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def fishing(self, interaction: discord.Interaction):


        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]


        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "fishes" : []
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})

        if not "fishes" in  userData:
            fishData = { "$set" : {"fishes" : []}}
            await collection.update_one(userData ,fishData)
        
        userData = await collection.find_one({"_id" : interaction.user.id})

        fishCaught = random.choice(fishes)
        await interaction.response.send_message("🎣 **|** Olta atıldı. Hadi rastgele")
        await asyncio.sleep(4)

        if fishCaught is None:
            return await interaction.edit.original_message(content = "Maalesef hiç balık tutamadınız ;c")

        
        await interaction.edit_original_message(content=f"**🐟 |** Bir **{fishCaught}** tuttunuz.")
        userData['fishes'].append(fishCaught) 
        await collection.replace_one({"_id": interaction.user.id}, userData)
        




    @fishing.error
    async def fishingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)

    @app_commands.command(name="hunt", description="Ava çık")
    @app_commands.checks.cooldown(
        1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def hunt(self, interaction: discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id": interaction.user.id,}) == None:
            newData = {
                "_id": interaction.user.id,
                "hunts" : []
            }
            await collection.insert_one(newData)

        

        userData = await collection.find_one({"_id" : interaction.user.id})

        if not "hunts" in  userData:
            fishData = { "$set" : {"hunts" : []}}
            await collection.update_one(userData ,fishData)
        
        userData = await collection.find_one({"_id" : interaction.user.id})

        huntCaught = random.choice(hunts)
        await interaction.response.send_message("🏹 **|** Av aranıyor...")
        await asyncio.sleep(5)

        if huntCaught is None:
            return await interaction.edit_original_message(content = "Hay aksi! Hiç av bulamadın ;c")
            

        
        await interaction.edit_original_message(content=f"**🦌 |** Bir **{huntCaught}** avladınız.")
        userData['hunts'].append(huntCaught) 
        await collection.replace_one({"_id": interaction.user.id}, userData)

    @hunt.error
    async def huntError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)
    

async def setup(bot:commands.Bot):
    await bot.add_cog(hunting(bot), guilds= [discord.Object(id =964617424743858176)])