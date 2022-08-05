from unittest import loader
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import random
import yaml
from yaml import Loader

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

yaml_file2 = open("yaml/fishing.yml", "rb")
fish = yaml.load(yaml_file2, Loader = Loader)


cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"

class Fishing(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mining", description="Let's start digging and earn valuable mines")
    @app_commands.checks.cooldown(
        1, 1200, key=lambda i: (i.guild_id, i.user.id))
    async def mining(self, interaction: discord.Interaction):
        
        # Database Connection
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]
        careerCollection = db["career"]

        # Database Checks
        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "mines" : {},
            }
            await collection.insert_one(newData)

        # Career Check
        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "minerpoint": 0
            }
            await careerCollection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        userCareer = await careerCollection.find_one({"_id": interaction.user.id})

        # Axe check
        if "pickaxe" not in userData:
            return await interaction.response.send_message("You need to buy a pickaxe for mining. `/store` :)", ephemeral = True)

        # Wood Check
        if "mines" not in userData:
            foresterData = { "$set" : {"mines" : {}}}
            await collection.update_one(userData ,foresterData)

        if "minerpoint" not in userCareer:
            careerData = { "$set" : {"minerpoint" : 0}}
            await careerCollection.update_one(userCareer ,careerData)

        # User Datas
        userData = await collection.find_one({"_id": interaction.user.id}) # User Data
        userCareer = await careerCollection.find_one({"_id": interaction.user.id}) # User Career Data
        userPickaxe = userData["pickaxe"] # User Pickaxe

        # Fishing System

        # Very Low Level Fisher
        if "stoneaxe" == userPickaxe:

            VLF = fish["veryLowLevelFish"] # Very Low Level Fishes
            veryLowLvFish = " ".join(VLF.keys()) # Very Low Level Fishes Keys
            splittedFish = veryLowLvFish.split(" ") # to List Fishes keys
            priceByVlSize = int(VLF["priceByFishSizeVL"]) # Price By Very Low Level Fish Size
            resultFish = random.choice(splittedFish) # Random Very Low Level Fish
            fishSize = random.randint(5,15) # Random fish size
            priceByFishSize = fishSize * priceByVlSize # Price By Fish Size

            if resultFish == "none":
                return await interaction.response.send_message("Unfortunately, You couldn't fish")

            vlFishName = VLF[resultFish]["name"] # Result Fish Name
            vlFishPrice = VLF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

            # Send user a message
            await interaction.response.send_message("🎣 **|** The fishing line was thrown. Godspeed.")
            await asyncio.sleep(6) 
            await interaction.edit_original_message(content = f"🐟 **|** Great work fisher! You have caught a **{fishSize}**-inch long **{vlFishName}** . Instantaneous market value: **{vlFishPrice}** Cupcoin.")

            # Update User Data
            userData["fish"].update({resultFish : fishSize}) 
            userCareer["fisherpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)
        
        # Low Level Fisher
        if "solidrod" == userRod:

            LF = fish["lowLevelFish"] # Low Level Fishes
            lowLvFish = " ".join(LF.keys()) # Low Level Fishes Keys
            splittedFish = lowLvFish.split(" ") # to List Fishes keys
            priceByLSize = int(LF["priceByFishSizeL"]) # Price By Low Level Fish Size
            resultFish = random.choice(splittedFish) # Random Low Level Fish
            fishSize = random.randint(3,10) # Random fish size
            priceByFishSize = fishSize * priceByLSize # Price By Fish Size

            if resultFish == "none":
                return await interaction.response.send_message("Unfortunately, You couldn't fish")

            lFishName = LF[resultFish]["name"] # Result Fish Name
            lFishPrice = LF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

            # Send user a message
            # Send user a message
            await interaction.response.send_message("🎣 **|** The fishing line was thrown. Godspeed.")
            await asyncio.sleep(5) 
            await interaction.edit_original_message(content = f"🐟 **|** Great work fisher! You have caught a **{fishSize}**-inch long **{lFishName}** . Instantaneous market value: **{lFishPrice}** Cupcoin.")

            # Update User Data
            userData["fish"].update({resultFish : fishSize}) 
            userCareer["fisherpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)



    @mining.error
    async def miningError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** You're tired. Go home and rest for `{timeRemaining}`s.",ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please inform the developer of this situation and try again later.")
            print(f"[MINING]: {error} ")