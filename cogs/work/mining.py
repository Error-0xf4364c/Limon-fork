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

yaml_file2 = open("assets/yamls/mines.yml", "rb")
mine = yaml.load(yaml_file2, Loader = Loader)


class Mining(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mining", description="Hadi kaz ve değerli madenler çıkar.")
    @app_commands.checks.cooldown(
        1, 1200, key=lambda i: (i.guild_id, i.user.id))
    async def mining(self, interaction: discord.Interaction):
        
        # Database Connection
        db = self.bot.database["limon"]
        collection = db["inventory"]
        
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)

        # Database Checks
        if collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "mines" : {},
            }
            collection.insert_one(newData)


        userData = collection.find_one({"_id": interaction.user.id})

        # Axe check
        if "items" not in userData or "pickaxe" not in userData["items"]:
            return await interaction.response.send_message("Madencilik yapabilmek için bir kazmaya ihtiyacınız var. Mağazadan bir kazma satın alabilirsiniz. `/store` :)", ephemeral = True)

        # Wood Check
        if "mines" not in userData:
            foresterData = { "$set" : {"mines" : {}}}
            collection.update_one(userData ,foresterData)

        # User Datas
        userData = collection.find_one({"_id": interaction.user.id}) # User Data
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
        await interaction.response.send_message(f"⛏️ **|** Kazmaya başladınız. Bu işlem yaklaşık {sleepTime} saniye sürecek.")
        await asyncio.sleep(sleepTime) 

        await interaction.edit_original_response(content = f"💎 **|** Harika iş madenci! Madenden tam **{mineSize}** kilogram **{mineName}** madeni çıkardın. Anlık piyasa değeri: {minePrice}")

        if resultMine in userData["mines"]:
            mineSize = userData["mines"][resultMine] + mineSize
        
        # Update User Data
        userData["mines"].update({resultMine : mineSize}) 
        userCareerData["points"]["miner_point"] += 2
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)
        collection.replace_one({"_id": interaction.user.id}, userData)




    @mining.error
    async def miningError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Yoruldun. Eve git ve `{timeRemaining}`s dinlen.",ephemeral=True)
        else:
            print(f"[MINING]: {error} ")

async def setup(bot:commands.Bot):
    await bot.add_cog(Mining(bot))
