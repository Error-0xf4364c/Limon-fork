"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from unittest import loader
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import random
import yaml
from yaml import Loader
from fetchdata import create_career_data


yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

yaml_file2 = open("assets/yamls/fishing.yml", "rb")
fish = yaml.load(yaml_file2, Loader = Loader)


class Fishing(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
  

    @app_commands.command(name="fishing", description="Hadi biraz balık tut.")
    @app_commands.checks.cooldown(
        1, 100, key=lambda i: (i.guild_id, i.user.id))
    async def fishing(self, interaction: discord.Interaction):
        
        # Database Connection
        db = self.bot.database["limon"]
        collection = db["inventory"]

        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)

        userData = collection.find_one({"_id": interaction.user.id})

        # Axe check
        if "items" not in userData or "rod" not in userData["items"]:
            return await interaction.response.send_message("Balık tutmak için oltaya ihtiyacınız var. Mağazadan bir olta satın alabilirsiniz. `/store` :)", ephemeral = True)

        # Wood Check
        if "fishes" not in userData:
            fisherData = { "$set" : {"fishes" : {}}}
            collection.update_one(userData ,fisherData)


        # User Datas
        userData = collection.find_one({"_id": interaction.user.id}) # User Data
        userRod = userData["items"]["rod"] # User Rod

        # Fishing System

        # Very Low Level Fisher
        if "simplerod" == userRod:

            VLF = fish["veryLowLevelFish"] # Very Low Level Fishes
            allfish = " ".join(VLF.keys()) # Very Low Level Fishes Keys
            splittedFish = allfish.split(" ") # to List Fishes keys
            priceByVlSize = int(fish["priceByFishSize"]) # Price By Very Low Level Fish Size
            resultFish = random.choice(splittedFish) # Random Very Low Level Fish

            if resultFish != "none":
                fishSize = random.randint(5,15) # Random fish size
                priceByFishSize = fishSize * priceByVlSize # Price By Fish Size
                fishName = VLF[resultFish]["name"] # Result Fish Name
                fishPrice = VLF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

        # Low Level Fisher
        if "solidrod" == userRod:

            LF = fish["lowLevelFish"] # Low Level Fishes
            allfish = " ".join(LF.keys()) # Low Level Fishes Keys
            splittedFish = allfish.split(" ") # to List Fishes keys
            priceByLSize = int(fish["priceByFishSize"]) # Price By Low Level Fish Size
            resultFish = random.choice(splittedFish) # Random Low Level Fish
            if resultFish != "none":
                fishSize = random.randint(3,10) # Random fish size
                priceByFishSize = fishSize * priceByLSize # Price By Fish Size
                fishName = LF[resultFish]["name"] # Result Fish Name
                fishPrice = LF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

        # Medium Level Fisher
        if "silverrod" == userRod:

            MF = fish["mediumLevelFish"] # Medium Level Fishes
            allfish = " ".join(MF.keys()) # Medium Level Fishes Keys
            splittedFish = allfish.split(" ") # to List Fishes keys
            priceByMSize = int(fish["priceByFishSize"]) # Price By Medium Level Fish Size
            resultFish = random.choice(splittedFish) # Random Medium Level Fish
            fishSize = random.randint(5,15) # Random fish size
            priceByFishSize = fishSize * priceByMSize # Price By Fish Size

            fishName = MF[resultFish]["name"] # Result Fish Name
            fishPrice = MF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

        # High Level Fisher
        if "luckyrod" == userRod:

            HF = fish["highLevelFish"] # High Level Fishes
            allfish = " ".join(HF.keys()) # High Level Fishes Keys
            splittedFish = allfish.split(" ") # to List Fishes keys
            priceByHSize = int(fish["priceByFishSize"]) # Price By High Level Fish Size
            resultFish = random.choice(splittedFish) # Random High Level Fish
            fishSize = random.randint(8,18) # Random fish size
            priceByFishSize = fishSize * priceByHSize # Price By Fish Size

            fishName = HF[resultFish]["name"] # Result Fish Name
            fishPrice = HF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

        # Very High Level Fisher
        if "harpoon" == userRod:

            VHF = fish["veryHighLevelFish"] # Very High Level Fishes
            allfish = " ".join(VHF.keys()) # Very High Level Fishes Keys
            splittedFish = allfish.split(" ") # to List Fishes keys
            priceByvHSize = int(fish["priceByFishSize"]) # Price By Very High Level Fish Size
            resultFish = random.choice(splittedFish) # Random Very High Level Fish
            fishSize = random.randint(20,55) # Random fish size
            priceByFishSize = fishSize * priceByvHSize # Price By Fish Size

            fishName = VHF[resultFish]["name"] # Result Fish Name
            fishPrice = VHF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

        # Send user a message
        await interaction.response.send_message("🎣 **|** Olta atıldı. Rastgele")
        await asyncio.sleep(5) 

        if resultFish == "none":
            return await interaction.edit_original_response("🐟 **|** Maalesef hiç balık tutamadınız ;c")


        await interaction.edit_original_response(content = f"🐟 **|** Harika iş balıkçı! **{fishSize}**m/cm uzunluğunda bir **{fishName}** yakaladın. Anlık piyasa değeri: **{fishPrice}** Cupcoin.")

        # Update User Data
        
        if resultFish in userData["fishes"]:
            fishSize = userData["fishes"][resultFish] + fishSize
        
        userData["fishes"].update({resultFish : fishSize}) 
        userCareerData["points"]["fisher_point"] += 2
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)
        collection.replace_one({"_id": interaction.user.id}, userData)

    @fishing.error
    async def fishingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Yoruldun. Eve git ve `{timeRemaining}`s dinlen.",ephemeral=True)
        else:
            print(f"[FISHING]: {error} ")

async def setup(bot:commands.Bot):
    await bot.add_cog(Fishing(bot))
