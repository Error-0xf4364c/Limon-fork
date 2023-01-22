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

yaml_file2 = open("assets/yamls/hunt.yml", "rb")
hunt = yaml.load(yaml_file2, Loader = Loader) 



class Hunting(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="hunting", description="Biraz avlan bakalım")
    @app_commands.checks.cooldown(
        1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def hunting(self, interaction: discord.Interaction):

        # Connecting Database
        db = self.bot.database["limon"]
        collection = db["inventory"]
        
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)

        # Database Checks
        if collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "hunts" : [],
            }
            collection.insert_one(newData)

        userData = collection.find_one({"_id": interaction.user.id})

        # Bow check
        if "items" not in userData or "bow" not in userData["items"]:
            return await interaction.response.send_message("Avcılık yapabilmek için bir yaya ihtiyacınız var. Mağazadan bir yay satın alabilirsiniz. `/store` :)", ephemeral = True)
        # Hunt Check
        if "hunts" not in userData:
            foresterData = { "$set" : {"hunts" : []}}
            collection.update_one(userData ,foresterData)

        # User Datas
        userData = collection.find_one({"_id": interaction.user.id}) # User Data
        userBow = userData["items"]["bow"] # User Bow


        # Hunting System

        # Very Low Level Hunting
        if "woodenbow" == userBow:

            VLH = hunt["veryLowLevelHunt"] # Very Low Level Hunts
            allhunt = " ".join(VLH.keys()) # Very Low Level Hunts Keys
            splittedHunt = allhunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random Very Low Level Hunt
            if resultHunt != "none":
                huntName = VLH[resultHunt]["name"] # Result Hunt Name
                huntPrice = VLH[resultHunt]["price"] # Result HuntTotal Price   
        
        # Low Level Hunting
        elif "copperbow" == userBow:

            LH = hunt["lowLevelHunt"] # Low Level Hunts
            allhunt = " ".join(LH.keys()) #  Low Level Hunts Keys
            splittedHunt = allhunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  Low Level Hunt
            if resultHunt != "none":
                huntName = LH[resultHunt]["name"] # Result Hunt Name
                huntPrice = LH[resultHunt]["price"] # Result HuntTotal Price

        # Medium Level Hunts
        elif "silverbow" == userBow:
            M = hunt["mediumLevelHunt"] # Medium Level Hunts
            allhunt = " ".join(M.keys()) #  Medium Level Hunts Keys
            splittedHunt = allhunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  Medium Level Hunt


            huntName = M[resultHunt]["name"] # Result Hunt Name
            huntPrice = M[resultHunt]["price"] # Result HuntTotal Price

        # High Level Hunts
        elif "accuratebow" == userBow:
            H = hunt["highLevelHunt"] # High Level Hunts
            allhunt = " ".join(H.keys()) #  High Level Hunts Keys
            splittedHunt = allhunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  High Level Hunt

            huntName = H[resultHunt]["name"] # Result Hunt Name
            huntPrice = H[resultHunt]["price"] # Result HuntTotal Price

        # Very High Level Hunts
        elif "crossbow" == userBow:
            VH = hunt["veryHighLevelHunt"] # Very High Level Hunts
            allhunt = " ".join(VH.keys()) # Very High Level Hunts Keys
            splittedHunt = allhunt.split(" ") # to List Hunts keys
            resultHunt = random.choice(splittedHunt) # Random  Very High Level Hunt

            huntName = VH[resultHunt]["name"] # Result Hunt Name
            huntPrice = VH[resultHunt]["price"] # Result HuntTotal Price

        # Send user a message
        await interaction.response.send_message("🏹 **|** Bir av aranıyor...")
        await asyncio.sleep(4) 

        await interaction.edit_original_response(content = f"🦌 **|** Harika bir av! Bir **{huntName}** avladın. Anlık piyasa değeri: **{huntPrice}** Cupcoin ")

        # Update User Data
        userData["hunts"].append(resultHunt)
        userCareerData["points"]["hunter_point"] += 2
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)
        collection.replace_one({"_id": interaction.user.id}, userData)
    

    @hunting.error
    async def huntingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Yoruldun. Eve git ve `{timeRemaining}`s dinlen.",ephemeral=True)
        else:
            print(f"[HUNTING]: {error} ")

async def setup(bot:commands.Bot):
    await bot.add_cog(Hunting(bot))
