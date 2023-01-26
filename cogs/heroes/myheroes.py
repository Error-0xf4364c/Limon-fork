"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import app_commands, Interaction, Embed
from discord.app_commands import Choice
from discord.ext import commands
import yaml
from yaml import Loader
from main import MyBot
import typing
import datetime

client = MyBot()

yaml_file2 = open("assets/yamls/chars.yml", "rb")
all_heroes = yaml.load(yaml_file2, Loader = Loader) 

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"
siradan = emojis["siradan"]
seyrek = emojis["seyrek"]
ender = emojis["ender"]
efsanevi = emojis["efsanevi"]
kadim = emojis["kadim"]




class MyHeroes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    def user_heroes(user):
        db = client.database["limon"]
        collection = db["inventory"]
        
        
        
        if collection.find_one({"_id": user.id}) == None:
            new_data = {
                "_id" : user.id,
                "heroes" : [] 
            }
        
        user_data = collection.find_one({"_id": user.id})
        
        if "heroes" not in user_data:
            hero_data = { "$set" : {"heroes" : []}}
            collection.update_one(user_data, hero_data)
            
        user_data = collection.find_one({"_id": user.id})
        
        heroes = []
        """
        for i in user_data["heroes"]:
            
            print(all_heroes[i]['name'])
            
            description = f"{all_heroes[i]['name']} - {all_heroes[i]['rarity']}"
            
            heroes.append(
                Choice(name = str(all_heroes[i]["name"]), value = description)
            )
        """
        return user_data

    async def my_heroes_autocompletion(
        self,
        interaction: Interaction, 
        current: str
        ) -> typing.List[Choice[str]]:

        user_data = MyHeroes.user_heroes(interaction.user)
        
        data = [Choice(name = str(all_heroes[i]["name"]), value = i) for i in user_data["heroes"] ]
        
        return data[:24]
    
    @app_commands.command(name = "my-heroes", description = "Kahramanların hakkında bilgi edin")
    @app_commands.describe(heroes = "Hangi kahraman hakkında bilgi edinmek istersin?")
    @app_commands.checks.cooldown(1, 15, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.autocomplete(heroes=my_heroes_autocompletion)
    async def my_heroes(self, interaction: Interaction, heroes: str):
        
        user = interaction.user
        hero = all_heroes[heroes]
        
        name = hero["name"]
        description = hero["description"]
        color = hero["colorCode"]
        power = hero["power"]
        hp = hero["hp"]
        rarity = hero["rarity"]
        
        if rarity == "Ancient":
            rarityLogo = kadim
        elif rarity == "Legendary":
            rarityLogo = efsanevi
        elif rarity == "Rare":
            rarityLogo = ender
        elif rarity == "Sparse":
            rarityLogo = seyrek
        else:
            rarityLogo = siradan
        
        
        hero_embed = Embed(description = str(description), color = color)
        hero_embed.set_author(name = f"{name} hakkında bilgiler", icon_url = interaction.user.avatar.url)
        hero_embed.add_field(name = "Power / Güç", value = power, inline = True)
        hero_embed.add_field(name = "HP / Can", value = hp, inline = True)
        hero_embed.add_field(name = "Rarity / Nadirlik", value = f"{rarityLogo} {rarity}", inline = True)
        
        await interaction.response.send_message(embed = hero_embed)

    @my_heroes.error
    async def my_heroesError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",
                                                    ephemeral=True)
    
async def setup(bot:commands.Bot):
    await bot.add_cog(MyHeroes(bot))