import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import asyncio
import yaml
from yaml import Loader

# Yaml file open
yaml_file = open("yamls/wood.yml", "rb")
wood = yaml.load(yaml_file, Loader = Loader) 

class Forester(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name = "forestry",
        description = "Cut down the tree")
    @app_commands.checks.cooldown(
        1, 8400, key = lambda i: (i.guild_id, i.user.id))
    async def forestry(self, interaction: discord.Interaction):
        
        # Database Connection
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]
        careerCollection = db["career"]

        # Database Checks
        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "wood" : {},
            }
            await collection.insert_one(newData)

        # Career Check
        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "foresterpoint": 0
            }
            await careerCollection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        userCareer = await careerCollection.find_one({"_id": interaction.user.id})

        # Axe check
        if "axe" not in userData:
            return await interaction.response.send_message("To do forestry, you need to buy an axe. `/store` :)", ephemeral = True)

        # Wood Check
        if "wood" not in userData:
            foresterData = { "$set" : {"wood" : {}}}
            await collection.update_one(userData ,foresterData)

        if "points" not in userCareer:
            careerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareer ,careerData)

        if "forester_point" not in userCareer["points"]:
            careerData = { "$set" : {"forester_point" : 0}}
            await careerCollection.update_one(userCareer["points"] ,careerData)

        # User Datas
        userData = await collection.find_one({"_id": interaction.user.id}) # User Data
        userCareer = await careerCollection.find_one({"_id": interaction.user.id}) # User Career Data
        userAxe = userData["axe"] # User Axe

        # Forestry System

        # Very Low Level Forestry
        if "stoneaxe" == userAxe:

            VLW = wood["veryLowLevelWood"] # Very Low Level Woods
            veryLowLvWood = " ".join(VLW.keys()) # Very Low Level Woods Keys
            splittedWood = veryLowLvWood.split(" ") # to List Woods keys
            priceByVlSize = int(VLW["priceByVlSize"]) # Price By Very Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Very Low Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByVlSize # Price By Wood Size

            vlWoodName = VLW[resultWood]["name"] # Result Wood Name
            vlWoodPrice = VLW[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Searching for a beautiful tree...")
            await asyncio.sleep(6) 
            await interaction.edit_original_message(content = f"🪓 **|** Great work lumberjack!  You got **{woodSize}** meters of wood from **{vlWoodName}**. Instantaneous market value: **{vlWoodPrice}** Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userCareer["points"]["forester_point"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Low Level Forestry
        elif "steelaxe" == userAxe:

            LW = wood["lowLevelWood"] # Low Level Woods
            lowLvWood = " ".join(LW.keys()) # Low Level Woods Keys
            splittedWood = lowLvWood.split(" ") # to List Woods keys
            priceByLSize = int(LW["priceByLSize"]) # Price By Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Low Level Wood
            woodSize = random.randint(8,18) # Random wood size
            priceByWoodSize = woodSize * priceByLSize # Price By Wood Size

            lWoodName = LW[resultWood]["name"] # Result Wood Name
            lWoodPrice = LW[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Searching for a beautiful tree...")
            await asyncio.sleep(5) 
            await interaction.edit_original_message(content = f"🪓 **|** Great work lumberjack!  You got **{woodSize}** meters of wood from **{lWoodName}**. Instantaneous market value: **{lWoodPrice}** Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userCareer["points"]["forester_point"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Medium Level Forestry
        elif "goldenaxe" == userAxe:

            M = wood["mediumLevelWood"] # Medium Level Woods
            mediumLvWood = " ".join(M.keys()) # Medium Level Woods Keys
            splittedWood = mediumLvWood.split(" ") # to List Woods keys
            priceByMSize = int(M["priceByMSize"]) # Price By Medium Level Wood Size
            resultWood = random.choice(splittedWood) # Random Medium Level Wood
            woodSize = random.randint(9,19) # Random wood size
            priceByWoodSize = woodSize * priceByMSize # Price By Wood Size

            mWoodName = M[resultWood]["name"] # Result Wood Name
            mWoodPrice = M[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Searching for a beautiful tree...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Great work lumberjack!  You got **{woodSize}** meters of wood from **{mWoodName}**. Instantaneous market value: **{mWoodPrice}** Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userCareer["points"]["forester_point"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)
            
        # High Level Forestry
        elif "reinforcedaxe" == userAxe:

            H = wood["highLevelWood"] # High Level Woods
            highLvWood = " ".join(H.keys()) # High Level Woods Keys
            splittedWood = highLvWood.split(" ") # to List Woods keys
            priceByHSize = int(H["priceByHSize"]) # Price By High Level Wood Size
            resultWood = random.choice(splittedWood) # Random High Level Wood
            woodSize = random.randint(13,23) # Random wood size
            priceByWoodSize = woodSize * priceByHSize # Price By Wood Size

            hWoodName = H[resultWood]["name"] # Result Wood Name
            hWoodPrice = H[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Searching for a beautiful tree...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Great work lumberjack!  You got **{woodSize}** meters of wood from **{hWoodName}**. Instantaneous market value: **{hWoodPrice}** Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userCareer["points"]["forester_point"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)
        
        # Very High Level Forestry
        elif "enchantedaxe" == userAxe:

            VH = wood["veryHighLevelWood"] # Low Level Woods
            veryHighLvWood = " ".join(VH.keys()) # Low Level Woods Keys
            splittedWood = veryHighLvWood.split(" ") # to List Woods keys
            priceByVhSize = int(VH["priceByVhSize"]) # Price By Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Low Level Wood
            woodSize = random.randint(17,30) # Random wood size
            priceByWoodSize = woodSize * priceByVhSize # Price By Wood Size

            vHWoodName = VH[resultWood]["name"] # Result Wood Name
            vHWoodPrice = VH[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Searching for a beautiful tree...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Great work lumberjack!  You got **{woodSize}** meters of wood from **{vHWoodName}**. Instantaneous market value: **{vHWoodPrice}** Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userCareer["points"]["forester_point"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

    # Error Handler
    @forestry.error
    async def forestryError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"You're tired. Go home and rest for `{timeRemaining}`s",ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please inform the developer of this situation and try again later.")
            print(f"Forestry: {error}")

async def setup(bot:commands.Bot):
    await bot.add_cog(Forester(bot))