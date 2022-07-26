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

yaml_file1 = open("yamls/mines.yml", "rb")
mines = yaml.load(yaml_file1, Loader = Loader) 

clock = emojis['clock'] or "⏳"


class Mining(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "mining", description = "Madencilik yap ve değerli madenler kazan.")
    @app_commands.checks.cooldown(
        1, 8400, key=lambda i: (i.guild_id, i.user.id))
    async def mining(self, interaction: discord.Interaction):

        # Random Mine
        allMines = mines['mines']
        minesKey = " ".join(mines["mines"].keys())
        miness = minesKey.split(" ")
        resultMine = random.choice(miness)
        kilograms = random.randint(2, 20)
        priceByKg = mines['priceByKg']

        # Connect Mongo
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "mines" : {},
                "miningpuani" : 0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})
        
        # Control
        if not "mines" in userData:
            mineData = { "$set" : {"mines" : {}, "miningpuani": 0}}
            await collection.update_one(userData ,mineData)

        mineName = resultMine.title()
        minePBS = kilograms * priceByKg
        minePrice = allMines[resultMine]  + minePBS

        await interaction.response.send_message("⛏️ **|** Kazmaya başladın. Tahmini olarak 30 saniye sürecek.")
        await asyncio.sleep(30)

        if resultMine == "none":
            return await interaction.edit_original_message(content = "Maalesef hiç değerli bir maden bulamadık ;c")

        await interaction.edit_original_message(content = f"💎 **|** Madenden **{kilograms}**kg ağırlığında {mineName} madeni çıktı. Anlık piyasa değeri **{minePrice}** Cupcoin")
        userData['mines'].update({resultMine : kilograms}) 
        userData['miningpuani'] +=1
        await collection.replace_one({"_id": interaction.user.id}, userData)


    @mining.error
    async def miningError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. Eve git ve`{timeRemaining}`s dinlen.",ephemeral=True)
        print(f"Mining: {error}")


async def setup(bot:commands.Bot):
    await bot.add_cog(Mining(bot))