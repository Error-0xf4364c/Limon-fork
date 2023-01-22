import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import asyncio
import yaml
from yaml import Loader
from fetchdata import create_career_data

# Yaml file open
yaml_file = open("assets/yamls/wood.yml", "rb")
wood = yaml.load(yaml_file, Loader = Loader) 

class Forester(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name = "forestry",
        description = "Biraz ağaç kes bakalım")
    @app_commands.checks.cooldown(
        1, 8400, key = lambda i: (i.guild_id, i.user.id))
    async def forestry(self, interaction: discord.Interaction):
        
        # Database Connection
        db = self.bot.database["limon"]
        collection = db["inventory"]
        
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)

        # Database Checks
        if collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "wood" : {},
            }
            collection.insert_one(newData)


        userData = collection.find_one({"_id": interaction.user.id})

        # Axe check
        if "items" not in userData or "axe" not in userData["items"]:
            return await interaction.response.send_message("Odunculuk yapmak için baltaya ihtiyacın var. Mağazadan bir balta satın alabilirsin. `/store` :)", ephemeral = True)

        # Wood Check
        if "wood" not in userData:
            foresterData = { "$set" : {"wood" : {}}}
            collection.update_one(userData ,foresterData)

        # User Datas
        userData = collection.find_one({"_id": interaction.user.id}) # User Data
        userAxe = userData["items"]["axe"] # User Axe

        # Forestry System

        # Very Low Level Forestry
        if "stoneaxe" == userAxe:

            VLW = wood["veryLowLevelWood"] # Very Low Level Woods
            veryLowLvWood = " ".join(VLW.keys()) # Very Low Level Woods Keys
            splittedWood = veryLowLvWood.split(" ") # to List Woods keys
            priceByVlSize = int(wood["priceByWoodSize"]) # Price By Very Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Very Low Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByVlSize # Price By Wood Size

            woodName = VLW[resultWood]["name"] # Result Wood Name
            woodPrice = VLW[resultWood]["price"] + priceByWoodSize # Result Wood Total Price


        # Low Level Forestry
        elif "steelaxe" == userAxe:

            LW = wood["lowLevelWood"] # Low Level Woods
            lowLvWood = " ".join(LW.keys()) # Low Level Woods Keys
            splittedWood = lowLvWood.split(" ") # to List Woods keys
            priceByLSize = int(wood["priceByWoodSize"]) # Price By Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Low Level Wood
            woodSize = random.randint(8,18) # Random wood size
            priceByWoodSize = woodSize * priceByLSize # Price By Wood Size

            woodName = LW[resultWood]["name"] # Result Wood Name
            woodPrice = LW[resultWood]["price"] + priceByWoodSize # Result Wood Total Price


        # Medium Level Forestry
        elif "goldenaxe" == userAxe:

            M = wood["mediumLevelWood"] # Medium Level Woods
            mediumLvWood = " ".join(M.keys()) # Medium Level Woods Keys
            splittedWood = mediumLvWood.split(" ") # to List Woods keys
            priceByMSize = int(wood["priceByWoodSize"]) # Price By Medium Level Wood Size
            resultWood = random.choice(splittedWood) # Random Medium Level Wood
            woodSize = random.randint(9,19) # Random wood size
            priceByWoodSize = woodSize * priceByMSize # Price By Wood Size

            woodName = M[resultWood]["name"] # Result Wood Name
            woodPrice = M[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

            
        # High Level Forestry
        elif "reinforcedaxe" == userAxe:

            H = wood["highLevelWood"] # High Level Woods
            highLvWood = " ".join(H.keys()) # High Level Woods Keys
            splittedWood = highLvWood.split(" ") # to List Woods keys
            priceByHSize = int(wood["priceByWoodSize"]) # Price By High Level Wood Size
            resultWood = random.choice(splittedWood) # Random High Level Wood
            woodSize = random.randint(13,23) # Random wood size
            priceByWoodSize = woodSize * priceByHSize # Price By Wood Size

            woodName = H[resultWood]["name"] # Result Wood Name
            woodPrice = H[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

        
        # Very High Level Forestry
        elif "enchantedaxe" == userAxe:

            VH = wood["veryHighLevelWood"] # Low Level Woods
            veryHighLvWood = " ".join(VH.keys()) # Low Level Woods Keys
            splittedWood = veryHighLvWood.split(" ") # to List Woods keys
            priceByVhSize = int(wood["priceByWoodSize"]) # Price By Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Low Level Wood
            woodSize = random.randint(17,30) # Random wood size
            priceByWoodSize = woodSize * priceByVhSize # Price By Wood Size

            woodName = VH[resultWood]["name"] # Result Wood Name
            woodPrice = VH[resultWood]["price"] + priceByWoodSize # Result Wood Total Price

        # Send user a message
        await interaction.response.send_message("🌲 **|** Güzel bir ağaç aranıyor...")
        await asyncio.sleep(4) 
        await interaction.edit_original_response(content = f"🪓 **|** Harika iş oduncu! Tam **{woodSize}** metre **{woodName}** ağacı kestin. Anlık piyasa değeri: **{woodPrice}** Cupcoin.")

        if resultWood in userData["wood"]:
            woodSize = userData["wood"][resultWood] + woodSize
        
        # Update User Data
        userData["wood"].update({resultWood : woodSize}) 
        userCareerData["points"]["forester_point"] +=1
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)
        collection.replace_one({"_id": interaction.user.id}, userData)

    # Error Handler
    @forestry.error
    async def forestryError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Yoruldun. Eve git ve `{timeRemaining}`s dinlen",ephemeral=True)
        else:
            print(f"[Forestry]: {error}")

async def setup(bot:commands.Bot):
    await bot.add_cog(Forester(bot))