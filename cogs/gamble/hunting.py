import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime

cupcoin = "<:Cupcoin:997158251944738938>"
cross = "<:cx:991397749486522499>"
cupcoinBack = "<:CupcoinBack:997241145438503023>"
cupcoins = "<:Cupcoins:997159042633961574>"
clock = "<:Cupclock:996129959758282842>" or "⏳"

fishes = ["Somon", "Kılıç Balığı", None,"Fangri Mercan", "Sazan", "İstavrit", None, "Kalkan", "Levrek", "Lüfer", "Palamut", "Orkinos", None, "Sardalya"]
hunts = ["Ceylan", "Geyik", "Yaban Keçisi", None,"Tavşan", "Keklik", "Serçe", "Bıldırcın", "Yaban Domuzu", None,"Tilki", "Tilki", "Sansar"]

import random

class hunting(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="fishing", description="Balık tut.")
    @app_commands.checks.cooldown(
        1, 21600, key=lambda i: (i.guild_id, i.user.id))
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

        if fishCaught == None:
            return await interaction.response.send_message("Maalesef hiç balık tutamadınız ;c")

        
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
        1, 21600, key=lambda i: (i.guild_id, i.user.id))
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

        if huntCaught == None:
            return await interaction.response.send_message("Hay aksi! Hiç av bulamadık ;c")

        
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