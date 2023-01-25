"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime
import yaml
from yaml import Loader
import random
from fetchdata import create_wallet

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"
siradan = emojis["siradan"]
seyrek = emojis["seyrek"]
ender = emojis["ender"]
efsanevi = emojis["efsanevi"]
kadim = emojis["kadim"]

yaml_file2 = open("assets/yamls/chars.yml", "rb")
heroes = yaml.load(yaml_file2, Loader = Loader) 


class eggs(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hero-egg", description="200,000 LiCash vererek bir kahraman yumurtası aç!")
    @app_commands.guild_only
    @app_commands.checks.cooldown(
        1, 21600, key=lambda i: (i.guild_id, i.user.id))
    async def herobox(self, interaction: discord.Interaction):

        caseFee = 200000
        
        db = self.bot.mongoConnect["limon"]
        collection = db["inventory"]
        userData = collection.find_one({"_id" : interaction.user.id})

        userCoins, economyCollection = create_wallet(self.bot, interaction.user.id)

        if userCoins['cash'] < caseFee:
            return await interaction.response.send_message(f"{emojis['cross']} Kahraman yumurtası açabilmek için **{caseFee - userCoins['cash']:,}** LiCash'e ihtiyacınız var.", ephemeral=True)

        if collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "heroes" : []
            }
            collection.insert_one(newData)

        userData = collection.find_one({"_id" : interaction.user.id})
        

        if not "heroes" in  userData:
            fishData = { "$set" : {"heroes" : []}}
            collection.update_one(userData ,fishData)
        
        userData = collection.find_one({"_id" : interaction.user.id})

        

        # --------| HEROLAR
        myheroes = " ".join(heroes.keys())
        sliceHero = myheroes.split(" ")
        #sliceHero.append(None)
        #sliceHero.append(None)
        # --------| HEROLAR
        yourHero = random.choice(sliceHero)
        userCoins['coins'] -= caseFee
        economyCollection.replace_one({"_id": interaction.user.id}, userCoins)


        



        if yourHero == None:
            await interaction.response.send_message(f"{emojis['3dot']} **|** Kahraman yumurtası açılıyor...")
            await asyncio.sleep(5)
            await interaction.edit_original_response(content = f"{emojis['cross']} Oh, bu çok üzücü! Yumurtadan hiç kahraman çıkmadı ;c")
            return
        
        if yourHero == "limon" and interaction.user.id != 529577110197764096:
            await interaction.response.send_message(f"{emojis['3dot']} **|** Kahraman yumurtası açılıyor...")
            await asyncio.sleep(5)
            await interaction.edit_original_response(content = f"{emojis['cross']} Oh, bu çok üzücü! Yumurtadan hiç kahraman çıkmadı ;c")
            return

        if userData['heroes'].count(yourHero) >= 1:
            await interaction.response.send_message(f"{emojis['3dot']} **|** Kahraman yumurtası açılıyor...")
            await asyncio.sleep(5)
            await interaction.edit_original_response(content = f"Yumurtadan bir **{yourHero.title()}** çıktı fakat siz zaten bu kahramana sahipsiniz.")
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
        heroEmbed.set_author(name= "Tebrikler! Yeni bir kahramanınız oldu.", icon_url= interaction.user.avatar.url),
        heroEmbed.add_field(name = "Can:", value =  heroes[yourHero]['hp'], inline = True),
        heroEmbed.add_field(name = "Nadirlik:", value =  f"{rarityLogo} {heroes[yourHero]['rarity']}", inline = True),
        heroEmbed.add_field(name= "Güç:", value =  heroes[yourHero]['power'], inline = True)
        await interaction.response.send_message(f"{emojis['clock']} **|** Kahramanın yumurtadan çıkması birkaç saniyenizi alabilir.")
        await asyncio.sleep(4)
        await interaction.edit_original_response(content = None, embed=heroEmbed)

        userData['heroes'].append(yourHero) 
        collection.replace_one({"_id": interaction.user.id}, userData)

        




    @herobox.error
    async def heroboxError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f" Heey! Diğer yumurtalar hazır değil! Lütfen`{timeRemaining}`s bekleyin!",ephemeral=True)





async def setup(bot:commands.Bot):
    await bot.add_cog(eggs(bot))
