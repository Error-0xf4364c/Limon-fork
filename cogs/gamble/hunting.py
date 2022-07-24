import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import random
import yaml
from yaml import Loader

yaml_file = open("emojis.yml", "r")
emojis = yaml.load(yaml_file, Loader = Loader) 

yaml_file2 = open("animals.yml", "r")
animals = yaml.load(yaml_file2, Loader = Loader) 

cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"
acemibalikci = emojis["acemibalikci"]
amatorbalikci = emojis["amatorbalikci"]
ustabalikci = emojis["ustabalikci"]
acemiavci = emojis["acemiavci"]
amatoravci = emojis["amatoravci"]
ustaavci = emojis["ustaavci"]


allFishes = animals['fishes']
fishesKey = " ".join(animals["fishes"].keys())
fishes = fishesKey.split(" ")
fishCaught = random.choice(fishes)

priceBySize = animals["priceBySize"]

allHunts = animals["hunts"]
huntsKey = " ".join(animals["hunts"].keys())
hunts = huntsKey.split(" ")
huntCaught = random.choice(hunts)



class hunting(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="fishing", description="Balık tut.")
    @app_commands.checks.cooldown(
        1, 100, key=lambda i: (i.guild_id, i.user.id))
    async def fishing(self, interaction: discord.Interaction):


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
            fishData = { "$set" : {"fishes" : {}, "balikcipuani" : 0}}
            await collection.update_one(userData ,fishData)
        
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
        await collection.replace_one({"_id": interaction.user.id}, userData)
        




    @fishing.error
    async def fishingError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. `{timeRemaining}`s dinlen.",ephemeral=True)

    @app_commands.command(name="hunt", description="Ava çık")
    @app_commands.checks.cooldown(
        1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def hunt(self, interaction: discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id": interaction.user.id,}) == None:
            newData = {
                "_id": interaction.user.id,
                "hunts" : []
            }
            await collection.insert_one(newData)

        

        userData = await collection.find_one({"_id" : interaction.user.id})

        if not "hunts" in  userData:
            fishData = { "$set" : {"hunts" : []}}
            await collection.update_one(userData ,fishData)
        
        userData = await collection.find_one({"_id" : interaction.user.id})

        huntCaught = random.choice(hunts)
        await interaction.response.send_message("🏹 **|** Av aranıyor...")
        await asyncio.sleep(5)

        if huntCaught == "none":
            return await interaction.edit_original_message(content = "Hay aksi! Hiç av bulamadın ;c")
            
        huntName = huntCaught.title()
        huntPrice = allHunts[huntCaught]
        
        await interaction.edit_original_message(content=f"**🦌 |** Bir **{huntName}** avladınız. Anlık piyasa değeri: {huntPrice} Cupcoin")
        
        userData['hunts'].append(huntCaught)
        await collection.replace_one({"_id": interaction.user.id}, userData)

    @hunt.error
    async def huntError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)
    

async def setup(bot:commands.Bot):
    await bot.add_cog(hunting(bot), guilds= [discord.Object(id =964617424743858176)])