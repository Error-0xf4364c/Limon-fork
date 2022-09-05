import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime
import yaml
from yaml import Loader
import random

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"
siradan = emojis["siradan"]
seyrek = emojis["seyrek"]
ender = emojis["ender"]
efsanevi = emojis["efsanevi"]
kadim = emojis["kadim"]

yaml_file2 = open("yamls/chars.yml", "rb")
heroes = yaml.load(yaml_file2, Loader = Loader) 


class eggs(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hero-egg", description="Open a hero egg by paying 200,000 Cupcoin and have one of them!")
    @app_commands.guild_only
    @app_commands.checks.cooldown(
        1, 21600, key=lambda i: (i.guild_id, i.user.id))
    async def herobox(self, interaction: discord.Interaction):
        #print(list(heroes.keys()))

        caseFee = 200000
        
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]
        economyCollection = db["economy"]
        userData = await collection.find_one({"_id" : interaction.user.id})
        userCoins = await economyCollection.find_one({"_id" : interaction.user.id})

        if userCoins['coins'] < caseFee:
            return await interaction.response.send_message(f"{emojis['cross']} You need **{caseFee - userCoins['coins']:,}** Cupcoin to open a hero egg.", ephemeral=True)

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "heroes" : []
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id" : interaction.user.id})
        

        if not "heroes" in  userData:
            fishData = { "$set" : {"heroes" : []}}
            await collection.update_one(userData ,fishData)
        
        userData = await collection.find_one({"_id" : interaction.user.id})

        

        # --------| HEROLAR
        myheroes = " ".join(heroes.keys())
        sliceHero = myheroes.split(" ")
        sliceHero.append(None)
        sliceHero.append(None)
        # --------| HEROLAR
        yourHero = random.choice(sliceHero)
        userCoins['coins'] -= caseFee
        await economyCollection.replace_one({"_id": interaction.user.id}, userCoins)


        



        if yourHero == None:
            await interaction.response.send_message(f"{emojis['3dot']} **|** The hero egg opens...")
            await asyncio.sleep(5)
            await interaction.edit_original_response(content = f"{emojis['cross']} Unfortunately, no heroes came out of the egg ;c")
            return
        
        if yourHero == "limon" and interaction.user.id != 529577110197764096:
            await interaction.response.send_message(f"{emojis['3dot']} **|** The hero egg opens...")
            await asyncio.sleep(5)
            await interaction.edit_original_response(content = f"{emojis['cross']} Unfortunately, no heroes came out of the egg ;c")
            return

        if userData['heroes'].count(yourHero) >= 1:
            await interaction.response.send_message(f"{emojis['3dot']} **|** The hero egg opens...")
            await asyncio.sleep(5)
            await interaction.edit_original_response(content = f"A **{yourHero.title()}** has appeared, but you already have this hero.")
            return

        # RARITY LOGO
        if heroes[yourHero]['rarity'] == "Ancient":
            rarityLogo = kadim
        elif heroes[yourHero]['rarity'] == "Legendary":
            rarityLogo = efsanevi
        elif heroes[yourHero]['rarity'] == "Rare":
            rarityLogo = ender
        elif heroes[yourHero]['rarity'] == "Sparse":
            rarityLogo = seyrek
        else:
            rarityLogo = siradan


        heroEmbed = discord.Embed(title= heroes[yourHero]["name"], description= heroes[yourHero]["description"], color = heroes[yourHero]['colorCode'])
        heroEmbed.set_author(name= "Congratulations. You have a new hero!", icon_url= interaction.user.avatar.url),
        heroEmbed.add_field(name = "Healt:", value =  heroes[yourHero]['hp'], inline = True),
        heroEmbed.add_field(name = "Rarity:", value =  f"{rarityLogo} {heroes[yourHero]['rarity']}", inline = True),
        heroEmbed.add_field(name= "Power:", value =  heroes[yourHero]['power'], inline = True)
        await interaction.response.send_message(f"{emojis['clock']} **|** It may take a few seconds for the hero to hatch from the egg.")
        await asyncio.sleep(4)
        await interaction.edit_original_response(content = None, embed=heroEmbed)

        userData['heroes'].append(yourHero) 
        await collection.replace_one({"_id": interaction.user.id}, userData)

        




    @herobox.error
    async def heroboxError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Heey! The other eggs are not ready! Please wait`{timeRemaining}`s and Try Again!",ephemeral=True)





async def setup(bot:commands.Bot):
    await bot.add_cog(eggs(bot))
