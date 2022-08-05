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

    @app_commands.command(name="fishing", description="Start fishing right now.")
    @app_commands.checks.cooldown(
        1, 100, key=lambda i: (i.guild_id, i.user.id))
    async def fishing(self, interaction: discord.Interaction):
        
        # Database Connection
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]
        careerCollection = db["career"]

        # Database Checks
        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "fishes" : {},
            }
            await collection.insert_one(newData)

        # Career Check
        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "fisherpoint": 0
            }
            await careerCollection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        userCareer = await careerCollection.find_one({"_id": interaction.user.id})

        # Axe check
        if "rod" not in userData:
            return await interaction.response.send_message("You need to buy a rod for fishing. `/store` :)", ephemeral = True)

        # Wood Check
        if "fishes" not in userData:
            foresterData = { "$set" : {"fishes" : {}}}
            await collection.update_one(userData ,foresterData)

        if "fisherpoint" not in userCareer:
            careerData = { "$set" : {"fisherpoint" : 0}}
            await careerCollection.update_one(userCareer ,careerData)

        # User Datas
        userData = await collection.find_one({"_id": interaction.user.id}) # User Data
        userCareer = await careerCollection.find_one({"_id": interaction.user.id}) # User Career Data
        userRod = userData["rod"] # User Rod

        # Fishing System

        # Very Low Level Fisher
        if "simplerod" == userRod:

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

        # Medium Level Fisher
        if "silverrod" == userRod:

            MF = fish["mediumLevelFish"] # Medium Level Fishes
            mediumLvFish = " ".join(MF.keys()) # Medium Level Fishes Keys
            splittedFish = mediumLvFish.split(" ") # to List Fishes keys
            priceByMSize = int(MF["priceByFishSizeM"]) # Price By Medium Level Fish Size
            resultFish = random.choice(splittedFish) # Random Medium Level Fish
            fishSize = random.randint(5,15) # Random fish size
            priceByFishSize = fishSize * priceByMSize # Price By Fish Size

            mFishName = MF[resultFish]["name"] # Result Fish Name
            mFishPrice = MF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

            # Send user a message
            await interaction.response.send_message("🎣 **|** The fishing line was thrown. Godspeed.")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🐟 **|** Great work fisher! You have caught a **{fishSize}**-inch long **{mFishName}** . Instantaneous market value: **{mFishPrice}** Cupcoin.")

            # Update User Data
            userData["fish"].update({resultFish : fishSize}) 
            userCareer["fisherpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # High Level Fisher
        if "luckyrod" == userRod:

            HF = fish["highLevelFish"] # High Level Fishes
            highLvFish = " ".join(HF.keys()) # High Level Fishes Keys
            splittedFish = highLvFish.split(" ") # to List Fishes keys
            priceByHSize = int(HF["priceByFishSizeH"]) # Price By High Level Fish Size
            resultFish = random.choice(splittedFish) # Random High Level Fish
            fishSize = random.randint(8,18) # Random fish size
            priceByFishSize = fishSize * priceByHSize # Price By Fish Size

            hFishName = HF[resultFish]["name"] # Result Fish Name
            hFishPrice = HF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

            # Send user a message
            await interaction.response.send_message("🎣 **|** The fishing line was thrown. Godspeed.")
            await asyncio.sleep(3)
            await interaction.edit_original_message(content = f"🐟 **|** Great work fisher! You have caught a **{fishSize}**-inch long **{hFishName}** . Instantaneous market value: **{hFishPrice}** Cupcoin.")

            # Update User Data
            userData["fish"].update({resultFish : fishSize}) 
            userCareer["fisherpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Very High Level Fisher
        if "harpoon" == userRod:

            VHF = fish["veryHighLevelFish"] # Very High Level Fishes
            veryHighLvFish = " ".join(VHF.keys()) # Very High Level Fishes Keys
            splittedFish = veryHighLvFish.split(" ") # to List Fishes keys
            priceByvHSize = int(VHF["priceByFishSizeVH"]) # Price By Very High Level Fish Size
            resultFish = random.choice(splittedFish) # Random Very High Level Fish
            fishSize = random.randint(20,55) # Random fish size
            priceByFishSize = fishSize * priceByvHSize # Price By Fish Size

            vhFishName = VHF[resultFish]["name"] # Result Fish Name
            vhFishPrice = VHF[resultFish]["price"] + priceByFishSize # Result Fish Total Price

            # Send user a message
            await interaction.response.send_message("🎣 **|** The fishing line was thrown. Godspeed.")
            await asyncio.sleep(5) 
            await interaction.edit_original_message(content = f"🐟 **|** Great work fisher! You have caught a **{fishSize}**-inch long **{vhFishName}** . Instantaneous market value: **{vhFishPrice}** Cupcoin.")

            # Update User Data
            userData["fish"].update({resultFish : fishSize}) 
            userCareer["fisherpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

    @fishing.error
    async def fishingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** You're tired. Go home and rest for `{timeRemaining}`s.",ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please inform the developer of this situation and try again later.")
            print(f"[FISHING]: {error} ")