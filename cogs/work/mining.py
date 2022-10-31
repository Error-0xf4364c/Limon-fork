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

yaml_file2 = open("yamls/mines.yml", "rb")
mine = yaml.load(yaml_file2, Loader = Loader)


cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"

class Mining(commands.Cog, commands.Bot):
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
                "points": {"miner_point": 0}
            }
            await careerCollection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        userCareer = await careerCollection.find_one({"_id": interaction.user.id})


        # Axe check
        if "items" not in userData or "pickaxe" not in userData["items"]:
            return await interaction.response.send_message("You need to buy a pickaxe for mining. `/store` :)", ephemeral = True)

        # Wood Check
        if "mines" not in userData:
            foresterData = { "$set" : {"mines" : {}}}
            await collection.update_one(userData ,foresterData)

        if "points" not in userCareer:
            careerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareer ,careerData)

        if "miner_point" not in userCareer["points"]:
            careerData = { "$set" : {"points.miner_point" : 0}}
            await careerCollection.update_one(userCareer ,careerData)

        # User Datas
        userData = await collection.find_one({"_id": interaction.user.id}) # User Data
        userCareer = await careerCollection.find_one({"_id": interaction.user.id}) # User Career Data
        userPickaxe = userData["items"]["pickaxe"] # User Pickaxe

        # Mining System
        sleepTime = 30
        # Very Low Level Miner
        if "stonepickaxe" == userPickaxe:

            VLM = mine["veryLowLevelMine"] # Very Low Level Mines
            veryLowLvMine = " ".join(VLM.keys()) # Very Low Level Mines Keys
            splittedMine = veryLowLvMine.split(" ") # to List Mines keys
            priceByVlSize = int(mine["priceByMineKg"]) # Price By Very Low Level Mine Size
            resultMine = random.choice(splittedMine) # Random Very Low Level Mine
            sleepTime = 30

            if resultMine != "none":
                mineSize = random.randint(5,10) # Random mine size
                priceByMineSize = mineSize * priceByVlSize # Price By Mine Size
                mineName = VLM[resultMine]["name"] # Result Mine Name
                minePrice = VLM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

        # Low Level Miner
        elif "steelpickaxe" == userPickaxe:

            LM = mine["lowLevelMine"] # Low Level Mines
            lowLvMine = " ".join(LM.keys()) # Low Level Mines Keys
            splittedMine = lowLvMine.split(" ") # to List Mines keys
            priceByLSize = int(mine["priceByMineKg"]) # Price By Low Level Mine Size
            resultMine = random.choice(splittedMine) # Random Low Level Mine
            sleepTime = 30

            if resultMine != "none":
                mineSize = random.randint(5,15) # Random mine size
                priceByMineSize = mineSize * priceByLSize # Price By Mine Size
                mineName = LM[resultMine]["name"] # Result Mine Name
                minePrice = LM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

        #Medium Level Miner
        elif "goldenpickaxe" == userPickaxe:

            MM = mine["mediumLevelMine"] #Medium Level Mines
            mediumLvMine = " ".join(MM.keys()) #Medium Level Mines Keys
            splittedMine = mediumLvMine.split(" ") # to List Mines keys
            priceByMSize = int(mine["priceByMineKg"]) # Price By Medium Level Mine Size
            resultMine = random.choice(splittedMine) # Random Medium Level Mine
            mineSize = random.randint(10,20) # Random mine size
            priceByMineSize = mineSize * priceByMSize # Price By Mine Size

            sleepTime = 25
            mineName = MM[resultMine]["name"] # Result Mine Name
            minePrice = MM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

        # High Level Miner
        elif "reinforcedpickaxe" == userPickaxe:

            HM = mine["highLevelMine"] #High Level Mines
            highLvMine = " ".join(HM.keys()) #High Level Mines Keys
            splittedMine = highLvMine.split(" ") # to List Mines keys
            priceByHSize = int(mine["priceByMineKg"]) # Price By High Level Mine Size
            resultMine = random.choice(splittedMine) # Random High Level Mine
            mineSize = random.randint(15,25) # Random mine size
            priceByMineSize = mineSize * priceByHSize # Price By Mine Size

            sleepTime = 20
            mineName = HM[resultMine]["name"] # Result Mine Name
            minePrice = HM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

        # Very High Level Miner
        elif "miningvehicle" == userPickaxe:

            VHM = mine["veryHighLevelMine"] # Very High Level Mines
            veryHighLvMine = " ".join(VHM.keys()) # Very High Level Mines Keys
            splittedMine = veryHighLvMine.split(" ") # to List Mines keys
            priceByVHSize = int(mine["priceByMineKg"]) # Price By Very High Level Mine Size
            resultMine = random.choice(splittedMine) # Random Very High Level Mine
            mineSize = random.randint(15,25) # Random mine size
            priceByMineSize = mineSize * priceByVHSize # Price By Mine Size

            sleepTime = 10
            mineName = VHM[resultMine]["name"] # Result Mine Name
            minePrice = VHM[resultMine]["price"] + priceByMineSize # Result Mine Total Price

        # Send user a message
        await interaction.response.send_message(f"⛏️ **|** You started digging. This process will take about {sleepTime} seconds")
        await asyncio.sleep(sleepTime) 

        if resultMine == "none":
            return await interaction.edit_original_response("Unfortunately, You came back empty-handed from the mine ;c")
        await interaction.edit_original_response(content = f"💎 **|** Great Job Miner! You extracted **{mineSize}** kilograms of **{mineName}** from the mine. Instantaneous market value: {minePrice}")

        # Update User Data
        userData["mines"].update({resultMine : mineSize}) 
        userCareer["points"]["miner_point"] +=1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
        await collection.replace_one({"_id": interaction.user.id}, userData)




    @mining.error
    async def miningError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** You're tired. Go home and rest for `{timeRemaining}`s.",ephemeral=True)
        else:
            print(f"[MINING]: {error} ")

async def setup(bot:commands.Bot):
    await bot.add_cog(Mining(bot))
