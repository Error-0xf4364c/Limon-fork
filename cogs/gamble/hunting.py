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

yaml_file2 = open("yamls/animals.yml", "rb")
animals = yaml.load(yaml_file2, Loader = Loader) 

cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"
"""
acemibalikci = rozet["acemibalikci"]
amatorbalikci = rozet["amatorbalikci"]
ustabalikci = rozet["ustabalikci"]
acemiavci = rozet["acemiavci"]
amatoravci = rozet["amatoravci"]
ustaavci = rozet["ustaavci"]
"""







class hunting(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="fishing", description="Balık tut.")
    @app_commands.checks.cooldown(
        1, 100, key=lambda i: (i.guild_id, i.user.id))
    async def fishing(self, interaction: discord.Interaction):
        allFishes = animals['fishes']
        fishesKey = " ".join(animals["fishes"].keys())
        fishes = fishesKey.split(" ")
        fishCaught = random.choice(fishes)

        priceBySize = animals["priceBySize"]


        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]


        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "fishes" : {},
                "balikcipuani" : 0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})

        if not "fishes" in  userData:
            fishData = { "$set" : {"fishes" : {}}}
            await collection.update_one(userData ,fishData)
        if not "balikcipuani" in userData:
            fishData1 = { "$set" : {"balikcipuani" : 0}}
            await collection.update_one(userData ,fishData1)
        
        userData = await collection.find_one({"_id" : interaction.user.id})


        fishName = fishCaught.title()
        fishSize = random.randint(3, 43)
        fishPBS = fishSize * priceBySize
        fishPrice = allFishes[fishCaught]  + fishPBS


        await interaction.response.send_message("🎣 **|** Olta atıldı. Hadi rastgele")
        await asyncio.sleep(4)

        if fishCaught == "none":
            return await interaction.edit_original_message(content = "Maalesef hiç balık tutamadınız ;c")

        
        await interaction.edit_original_message(content=f"**🐟 |** **{fishSize}**cm uzunluğunda **{fishName}** tuttunuz. Anlık piyasa değeri: **{fishPrice}** Cupcoin.")
        userData['fishes'].update({fishCaught : fishSize}) 
        userData['balikcipuani'] +=1
        await collection.replace_one({"_id": interaction.user.id}, userData)
        




    @fishing.error
    async def fishingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. `{timeRemaining}`s dinlen.",ephemeral=True)
        print(error)

    @app_commands.command(name="hunt", description="Ava çık")
    @app_commands.checks.cooldown(
        1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def hunt(self, interaction: discord.Interaction):
        allHunts = animals["hunts"]
        huntsKey = " ".join(animals["hunts"].keys())
        hunts = huntsKey.split(" ")
        huntCaught = random.choice(hunts)

        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id": interaction.user.id,}) == None:
            newData = {
                "_id": interaction.user.id,
                "hunts" : [],
                "avpuani" : 0
            }
            await collection.insert_one(newData)

        

        userData = await collection.find_one({"_id" : interaction.user.id})

        if not "hunts" in userData:
            huntData = { "$set" : {"hunts" : []}}
            await collection.update_one(userData ,huntData)
        if not "avpuani" in userData:
            huntData1 = { "$set" : {"avpuani" : 0}}
            await collection.update_one(userData ,huntData1)
        
        userData = await collection.find_one({"_id" : interaction.user.id})

        huntCaught = random.choice(hunts)
        await interaction.response.send_message("🏹 **|** Av aranıyor...")
        await asyncio.sleep(5)

        if huntCaught == "none":
            return await interaction.edit_original_message(content = "Hay aksi! Hiç av bulamadın ;c")
            
        huntName = huntCaught.title()
        huntPrice = allHunts[huntCaught]
        
        await interaction.edit_original_message(content=f"**🦌 |** Bir **{huntName}** avladınız. Anlık piyasa değeri: **{huntPrice}** Cupcoin")
        
        userData['hunts'].append(huntCaught)
        userData['avpuani'] += 1
        await collection.replace_one({"_id": interaction.user.id}, userData)

    @hunt.error
    async def huntError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)
    

async def setup(bot:commands.Bot):
    await bot.add_cog(hunting(bot))