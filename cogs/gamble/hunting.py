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

yaml_file2 = open("yamls/hunt.yml", "rb")
hunt = yaml.load(yaml_file2, Loader = Loader) 




cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"


class Hunting(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="hunting", description="Ava çık")
    @app_commands.checks.cooldown(
        1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def hunting(self, interaction: discord.Interaction):
        
        # Connecting Database
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]
        careerCollection = db["career"]

        # Database Checks
        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "hunts" : [],
                "hunterpoint" : 0
            }
            await collection.insert_one(newData)

        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "hunterpoint": 0
            }
            await careerCollection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        userCareer = await careerCollection.find_one({"_id": interaction.user.id})

        # Bow check
        if "yay" not in userData:
            return await interaction.response.send_message("Avlanmak için bir yay satın almalısınız. `/store` :)", ephemeral = True)

        # Hunt Check
        if "hunts" not in userData:
            foresterData = { "$set" : {"hunts" : [], "avpuani": 0}}
            await collection.update_one(userData ,foresterData)
        if "foresterpoint" not in userCareer:
            careerData = { "$set" : {"foresterpoint" : 0}}
            await careerCollection.update_one(userCareer ,careerData)

        userCareer = await careerCollection.find_one({"_id": interaction.user.id})

        # User Datas
        userData = await collection.find_one({"_id": interaction.user.id}) # User Data
        userBow = userData["yay"] # User Bow


        # Hunting System

        # Very Low Level Hunting
        if "tahtayay" == userBow:

            VLH = hunt["veryLowLevelHunt"] # Very Low Level Hunts
            veryLowLvHunt = " ".join(VLH.keys()) # Very Low Level Hunts Keys
            splittedHunt = veryLowLvHunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random Very Low Level Hunt

            if resultHunt == "none":
                return await interaction.response.send_message(";c **|** Maalesef hiç av bulamadınız ;c")

            vlHuntName = VLH[resultHunt]["name"] # Result Hunt Name
            vlHuntPrice = VLH[resultHunt]["price"] # Result HuntTotal Price

            # Send user a message
            await interaction.response.send_message("🏹 **|** Av arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🦌 **|** Harika bir av! **{vlHuntName}** avladın. Anlık piyasa değeri: **{vlHuntPrice}** Cupcoin")

            # Update User Data
            userData["hunts"].append(resultHunt)
            userCareer["hunterpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)
            
        
        # Low Level Hunting
        elif "bakiryay" == userBow:

            LH = hunt["lowLevelHunt"] # Low Level Hunts
            lowLvHunt = " ".join(LH.keys()) #  Low Level Hunts Keys
            splittedHunt = lowLvHunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  Low Level Hunt

            if resultHunt == "none":
                return await interaction.response.send_message(";c **|** Maalesef hiç av bulamadınız ;c")

            lHuntName = LH[resultHunt]["name"] # Result Hunt Name
            lHuntPrice = LH[resultHunt]["price"] # Result HuntTotal Price

            # Send user a message
            await interaction.response.send_message("🏹 **|** Av arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🦌 **|** Harika bir av! **{lHuntName}** avladın. Anlık piyasa değeri: **{lHuntPrice}** Cupcoin")

            # Update User Data
            userData["hunts"].append(resultHunt)
            userCareer["hunterpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Medium Level Hunts
        elif "gumusyay" == userBow:
            M = hunt["mediumLevelHunt"] # Medium Level Hunts
            mLvHunt = " ".join(M.keys()) #  Medium Level Hunts Keys
            splittedHunt = mLvHunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  Medium Level Hunt


            mHuntName = M[resultHunt]["name"] # Result Hunt Name
            mHuntPrice = M[resultHunt]["price"] # Result HuntTotal Price

            # Send user a message
            await interaction.response.send_message("🏹 **|** Av arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🦌 **|** Harika bir av! **{mHuntName}** avladın. Anlık piyasa değeri: **{mHuntPrice}** Cupcoin")

            # Update User Data
            userData["hunts"].append(resultHunt)
            userCareer["hunterpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # High Level Hunts
        elif "isabetliyay" == userBow:
            H = hunt["highLevelHunt"] # High Level Hunts
            hLvHunt = " ".join(H.keys()) #  High Level Hunts Keys
            splittedHunt = hLvHunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  High Level Hunt

            hHuntName = H[resultHunt]["name"] # Result Hunt Name
            hHuntPrice = H[resultHunt]["price"] # Result HuntTotal Price

            # Send user a message
            await interaction.response.send_message("🏹 **|** Av arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🦌 **|** Harika bir av! **{hHuntName}** avladın. Anlık piyasa değeri: **{hHuntPrice}** Cupcoin")

            # Update User Data
            userData["hunts"].append(resultHunt)
            userCareer["hunterpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)

        # Very High Level Hunts
        elif "arbalet" == userBow:
            VH = hunt["veryHighLevelHunt"] # Very High Level Hunts
            vhLvHunt = " ".join(VH.keys()) # Very High Level Hunts Keys
            splittedHunt = vhLvHunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  Very High Level Hunt

            vhHuntName = VH[resultHunt]["name"] # Result Hunt Name
            vhHuntPrice = VH[resultHunt]["price"] # Result HuntTotal Price

            # Send user a message
            await interaction.response.send_message("🏹 **|** Av arıyorsun...")
            await asyncio.sleep(4) 
            await interaction.edit_original_message(content = f"🦌 **|** Harika bir av! **{vhHuntName}** avladın. Anlık piyasa değeri: **{vhHuntPrice}** Cupcoin")

            # Update User Data
            userData["hunts"].append(resultHunt)
            userCareer["hunterpoint"] +=1
            await careerCollection.replace_one({"_id": interaction.user.id}, userCareer)
            await collection.replace_one({"_id": interaction.user.id}, userData)


    @hunting.error
    async def huntingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)
        else:
            await interaction.response.send_message("Beklenmedik bir hata oluştu. Lütfen bu durumu geliştiriciye bildiriniz ve daha sonra tekrar deneyiniz.")
            print(f"[HUNTING]: {error} ")