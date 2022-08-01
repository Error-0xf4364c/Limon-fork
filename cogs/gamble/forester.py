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

        # Database Checks
        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "wood" : {},
                "ormancipuani" : 0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})

        # Axe check
        if "balta" not in userData:
            return await interaction.response.send_message("Ormancılık yapmak için bir balta satın almalısınız. `/store` :)", ephemeral = True)

        # Wood Check
        if "wood" not in userData:
            foresterData = { "$set" : {"wood" : {}, "ormancioauni": 0}}
            await collection.update_one(userData ,foresterData)

        # User Datas
        userData = await collection.find_one({"_id": interaction.user.id}) # User Data
        userAxe = userData["balta"] # User Axe

        # Forestry System

        # Very Low Level Forestry
        if "tahtabalta" == userAxe:

            VLW = wood["veryLowLevelWood"] # Very Low Level Woods
            veryLowLvWood = " ".join(VLW.keys()) # Very Low Level Woods Keys
            splittedWood = veryLowLvWood.split(" ") # to List Woods keys
            priceByVlSize = int(VLW["priceByVlSize"]) # Price By Very Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Very Low Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByVlSize # Price By Wood Size

            vlWoodName = VLW[resultWood]["name"] # Result Wood Name
            vlWoodPrice = VLW[resultWood] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Güzel bir ağaç arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Harika iş oduncu! **{vlWoodName}** türündeki bu ağaçtan **{woodSize}** metre uzunluğunda odun elde ettiniz. Anlık piyasa değeri: {vlWoodPrice} Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userData["ormancipuani"] +=1
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Low Level Forestry
        elif "tasbalta" == userAxe:

            LW = wood["lowLevelWood"] # Low Level Woods
            lowLvWood = " ".join(LW.keys()) # Low Level Woods Keys
            splittedWood = lowLvWood.split(" ") # to List Woods keys
            priceByLSize = int(LW["priceByLSize"]) # Price By Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Low Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByLSize # Price By Wood Size

            lWoodName = LW[resultWood]["name"] # Result Wood Name
            lWoodPrice = LW[resultWood] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Güzel bir ağaç arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Harika iş oduncu! **{lWoodName}** türündeki bu ağaçtan **{woodSize}** metre uzunluğunda odun elde ettiniz. Anlık piyasa değeri: {lWoodPrice} Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userData["ormancipuani"] +=1
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Medium Level Forestry
        elif "altinbalta" == userAxe:

            M = wood["mediumLevelWood"] # Medium Level Woods
            mediumLvWood = " ".join(M.keys()) # Medium Level Woods Keys
            splittedWood = mediumLvWood.split(" ") # to List Woods keys
            priceByMSize = int(M["priceByMSize"]) # Price By Medium Level Wood Size
            resultWood = random.choice(splittedWood) # Random Medium Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByMSize # Price By Wood Size

            mWoodName = M[resultWood]["name"] # Result Wood Name
            mWoodPrice = M[resultWood] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Güzel bir ağaç arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Harika iş oduncu! **{mWoodName}** türündeki bu ağaçtan **{woodSize}** metre uzunluğunda odun elde ettiniz. Anlık piyasa değeri: {mWoodPrice} Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userData["ormancipuani"] +=1
            await collection.replace_one({"_id": interaction.user.id}, userData)
            
        # High Level Forestry
        elif "guclendirilmisbalta" == userAxe:

            H = wood["highLevelWood"] # High Level Woods
            highLvWood = " ".join(H.keys()) # High Level Woods Keys
            splittedWood = highLvWood.split(" ") # to List Woods keys
            priceByHSize = int(H["priceByHSize"]) # Price By High Level Wood Size
            resultWood = random.choice(splittedWood) # Random High Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByHSize # Price By Wood Size

            mWoodName = M[resultWood]["name"] # Result Wood Name
            mWoodPrice = M[resultWood] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Güzel bir ağaç arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Harika iş oduncu! **{mWoodName}** türündeki bu ağaçtan **{woodSize}** metre uzunluğunda odun elde ettiniz. Anlık piyasa değeri: {mWoodPrice} Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userData["ormancipuani"] +=1
            await collection.replace_one({"_id": interaction.user.id}, userData)
        
        # Very High Level Forestry
        elif "buyulubalta" == userAxe:

            VH = wood["veryHighLevelWood"] # Low Level Woods
            veryHighLvWood = " ".join(VH.keys()) # Low Level Woods Keys
            splittedWood = veryHighLvWood.split(" ") # to List Woods keys
            priceByVhSize = int(VH["priceByVhSize"]) # Price By Low Level Wood Size
            resultWood = random.choice(splittedWood) # Random Low Level Wood
            woodSize = random.randint(5,15) # Random wood size
            priceByWoodSize = woodSize * priceByVhSize # Price By Wood Size

            vHWoodName = VH[resultWood]["name"] # Result Wood Name
            vHWoodPrice = VH[resultWood] + priceByWoodSize # Result Wood Total Price

            # Send user a message
            await interaction.response.send_message("🌲 **|** Güzel bir ağaç arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🪓 **|** Harika iş oduncu! **{vHWoodName}** türündeki bu ağaçtan **{woodSize}** metre uzunluğunda odun elde ettiniz. Anlık piyasa değeri: {vHWoodPrice} Cupcoin.")

            # Update User Data
            userData["wood"].update({resultWood : woodSize}) 
            userData["ormancipuani"] +=1
            await collection.replace_one({"_id": interaction.user.id}, userData)










    # Error Handler
    @forestry.error
    async def forestryError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)
        else:
            await interaction.response.send_message("Beklenmedik bir hata oluştu. Lütfen bu durumu geliştiriciye bildiriniz ve daha sonra tekrar deneyiniz.")
            print(f"Forestry: {error}")