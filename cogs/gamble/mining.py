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

        # Mining System

        # Very Low Level Miner
        if "stonepickaxe" == userPickaxe:

            VLM = fish["veryLowLevelMine"] # Very Low Level Mines
            veryLowLvMine = " ".join(VLM.keys()) # Very Low Level Mines Keys
            splittedMine = veryLowLvMine.split(" ") # to List Mines keys
            priceByVlSize = int(VLM["priceByVLMine"]) # Price By Very Low Level Mine Size
            resultMine = random.choice(splittedMine) # Random Very Low Level Mine
            mineSize = random.randint(5,10) # Random mine size
            priceByMineSize = mineSize * priceByVlSize # Price By Mine Size

            if resultMine == "none":
                return await interaction.response.send_message("Unfortunately, You came back empty-handed from the mine")

            vlMineName = VLM[resultMine]["name"] # Result Mine Name
            vlMinePrice = VLM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

            # Send user a message
            await interaction.response.send_message("⛏️ **|** You started digging. This process will take about 30 seconds")
            await asyncio.sleep(30) 
            await interaction.edit_original_message(content = f"💎 **|** Great Job Miner! You extracted {mineSize} kilograms of {vlMineName} from the mine. Instantaneous market value: {vlMinePrice}")

            # Update User Data
            userData["mines"].update({resultMine : mineSize}) 
            userCareer["minerpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Low Level Miner
        elif "steelpickaxe" == userPickaxe:

            LM = fish["lowLevelMine"] # Low Level Mines
            lowLvMine = " ".join(LM.keys()) # Low Level Mines Keys
            splittedMine = lowLvMine.split(" ") # to List Mines keys
            priceByLSize = int(LM["priceByLMine"]) # Price By Low Level Mine Size
            resultMine = random.choice(splittedMine) # Random Low Level Mine
            mineSize = random.randint(5,15) # Random mine size
            priceByMineSize = mineSize * priceByLSize # Price By Mine Size

            if resultMine == "none":
                return await interaction.response.send_message("Unfortunately, You came back empty-handed from the mine")

            lMineName = LM[resultMine]["name"] # Result Mine Name
            lMinePrice = LM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

            # Send user a message
            await interaction.response.send_message("⛏️ **|** You started digging. This process will take about 30 seconds")
            await asyncio.sleep(30) 
            await interaction.edit_original_message(content = f"💎 **|** Great Job Miner! You extracted {mineSize} kilograms of {lMineName} from the mine. Instantaneous market value: {lMinePrice}")

            # Update User Data
            userData["mines"].update({resultMine : mineSize}) 
            userCareer["minerpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        #Medium Level Miner
        elif "goldenpickaxe" == userPickaxe:

            MM = fish["mediumLevelMine"] #Medium Level Mines
            mediumLvMine = " ".join(MM.keys()) #Medium Level Mines Keys
            splittedMine = mediumLvMine.split(" ") # to List Mines keys
            priceByMSize = int(MM["priceByMMine"]) # Price By Medium Level Mine Size
            resultMine = random.choice(splittedMine) # Random Medium Level Mine
            mineSize = random.randint(10,20) # Random mine size
            priceByMineSize = mineSize * priceByMSize # Price By Mine Size

            mMineName = MM[resultMine]["name"] # Result Mine Name
            mMinePrice = MM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

            # Send user a message
            await interaction.response.send_message("⛏️ **|** You started digging. This process will take about 25 seconds")
            await asyncio.sleep(25) 
            await interaction.edit_original_message(content = f"💎 **|** Great Job Miner! You extracted {mineSize} kilograms of {mMineName} from the mine. Instantaneous market value: {mMinePrice}")

            # Update User Data
            userData["mines"].update({resultMine : mineSize}) 
            userCareer["minerpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # High Level Miner
        elif "reinforcedpickaxe" == userPickaxe:

            HM = fish["highLevelMine"] #High Level Mines
            highLvMine = " ".join(HM.keys()) #High Level Mines Keys
            splittedMine = highLvMine.split(" ") # to List Mines keys
            priceByHSize = int(HM["priceByHMine"]) # Price By High Level Mine Size
            resultMine = random.choice(splittedMine) # Random High Level Mine
            mineSize = random.randint(15,25) # Random mine size
            priceByMineSize = mineSize * priceByHSize # Price By Mine Size

            hMineName = HM[resultMine]["name"] # Result Mine Name
            hMinePrice = HM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

            # Send user a message
            await interaction.response.send_message("⛏️ **|** You started digging. This process will take about 20 seconds")
            await asyncio.sleep(20) 
            await interaction.edit_original_message(content = f"💎 **|** Great Job Miner! You extracted {mineSize} kilograms of {hMineName} from the mine. Instantaneous market value: {hMinePrice}")

            # Update User Data
            userData["mines"].update({resultMine : mineSize}) 
            userCareer["minerpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)
        
        # Very High Level Miner
        elif "miningvehicle" == userPickaxe:

            VHM = fish["veryHighLevelMine"] # Very High Level Mines
            veryHighLvMine = " ".join(VHM.keys()) # Very High Level Mines Keys
            splittedMine = veryHighLvMine.split(" ") # to List Mines keys
            priceByVHSize = int(VHM["priceByVHMine"]) # Price By Very High Level Mine Size
            resultMine = random.choice(splittedMine) # Random Very High Level Mine
            mineSize = random.randint(15,25) # Random mine size
            priceByMineSize = mineSize * priceByVHSize # Price By Mine Size

            vhMineName = VHM[resultMine]["name"] # Result Mine Name
            vhMinePrice = VHM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

            # Send user a message
            await interaction.response.send_message("⛏️ **|** You started digging. This process will take about 10 seconds")
            await asyncio.sleep(10) 
            await interaction.edit_original_message(content = f"💎 **|** Great Job Miner! You extracted {mineSize} kilograms of {vhMineName} from the mine. Instantaneous market value: {vhMinePrice}")

            # Update User Data
            userData["mines"].update({resultMine : mineSize}) 
            userCareer["minerpoint"] +=1
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