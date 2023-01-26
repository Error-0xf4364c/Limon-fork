"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import Embed, app_commands, Interaction, SelectOption, ui
from discord.ext import commands
import yaml
from yaml import Loader
from fetchdata import create_wallet
from main import MyBot
import datetime

client = MyBot()

yaml_file2 = open("assets/yamls/chars.yml", "rb")
all_heroes = yaml.load(yaml_file2, Loader = Loader) 

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

cross = emojis["cross"]
clock = emojis["clock"] or "⏳"
done = emojis["done"]

siradan = emojis["siradan"]
seyrek = emojis["seyrek"]
ender = emojis["ender"]
efsanevi = emojis["efsanevi"]
kadim = emojis["kadim"]


def list_of_heroes(bot, _id):


    user_id = _id
    
    db = bot.database["limon"]
    collection = db["inventory"]
    
    user_data = collection.find_one({"_id": user_id})

    global options
    options = []
    
    for i in user_data["heroes"]:
        
        name = all_heroes[i]["name"]
        rarity = all_heroes[i]["rarity"]
        price = all_heroes[i]["price"]
        
        if rarity == "Ancient":
            rarityLogo = kadim
            rarity = "Kadim"
        elif rarity == "Legendary":
            rarityLogo = efsanevi
            rarity = "Efsanevi"
        elif rarity == "Rare":
            rarityLogo = ender
            rarity = "Ender"
        elif rarity == "Sparse":
            rarityLogo = seyrek
            rarity = "Seyrek"
        else:
            rarityLogo = siradan
            rarity = "Sıradan"
            
        options.append(SelectOption(label=str(name), value=i, description=f"{rarity} - {price:,} LiCash", emoji = rarityLogo or "🥇"))


    

class HeroesMenu(ui.Select):
    def __init__(self):
        
        super().__init__(placeholder='Kahramanlarım', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        
        
        
        if interaction.user.id != user_id:
            return await interaction.response.send_message(content = f"{cross} **|** Size ait olmayan menüde bir işlem yapamazsınız!", ephemeral = True)
        
        db = client.database["limon"]
        collection = db["inventory"]
        
        
        user_data = collection.find_one({"_id" : interaction.user.id})
        
        user_heroes = user_data["heroes"]
        
        selected_hero = self.values[0]
        
        if selected_hero not in user_heroes:
            return await interaction.response.send_message(content = f"{cross} **|** Muhtemelen bu kahramanı az önce sattınız!", ephemeral = True)
        
        price = all_heroes[selected_hero]["price"]
        name = all_heroes[selected_hero]["name"]
        rarity = all_heroes[selected_hero]["rarity"]

        user_heroes.remove(selected_hero)
        collection.replace_one({"_id" : interaction.user.id}, user_data)

        user_wallet, wallet= create_wallet(client, interaction.user.id)

        user_wallet["cash"] += price
        wallet.replace_one({"_id" : interaction.user.id}, user_wallet)
        
        if rarity == "Ancient":
            rarity = "Kadim"
        elif rarity == "Legendary":
            rarity = "Efsanevi"
        elif rarity == "Rare":
            rarity = "Ender"
        elif rarity == "Sparse":
            rarity = "Seyrek"
        else:
            rarity = "Sıradan"

        await interaction.response.send_message(
            content = f"{done} **{rarity}** nadirlik derecesine sahip olan kahramanınız **{name}**, **{price:,}** LiCash karşılığında tüccara satıldı. - {interaction.user.mention}"
            )
        
        
class ShowHeroes(ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(HeroesMenu())

class SellHeroes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    @app_commands.command(name = "hero-trader", description = "Kahraman tüccarında kahramanlarını sat!")
    async def sell_heroes(self, interaction: Interaction):
        
        db = self.bot.database["limon"]
        collection = db["inventory"]

        count_heroes = 0
        
        global user_id
        user_id = interaction.user.id
        
        if collection.find_one({"_id": interaction.user.id}) == None:
            count_heroes = 0 
        
        user_data = collection.find_one({"_id": interaction.user.id})
        
        if "heroes" not in user_data:
            count_heroes = 0 
        
        elif len(user_data["heroes"]) == 0:
            count_heroes = 0 
        else:
            list_of_heroes(self.bot, interaction.user.id)
            count_heroes = len(options)
        
        embed_message = Embed(
            title = "Kahraman Tüccarına Hoş Geldin",
            description = f"""

                **Kahraman Tüccarına Nedir?**
                Kahramanlarınızı normal tüccarlara satamazsınız. Sadece Kahraman Tüccarına satabilirsiniz.
                `Güç`, `Can` ve `Nadirlik` derecesine göre kahramanlarınıza fiyat biçilir. Satmak ne kadar akıllıca bir hareket bilinmez ama
                eğer kahramanlarınızı satmak isterseniz burada satabilirsiniz. 
                
                **Kahraman Fiyatlarını Nasıl Öğrenebilirim**
                Aşağıdaki seçenek menüsünde kahramanlar isimlerinin altındaki açıklama bölümünde nadirlik derecesinin yanında kahraman fiyatları yazıyor.
                
                Toplam **{count_heroes}** kahramanınız var
            """,
            color = 0xfff48a)
        embed_message.set_author(name = f"Merhaba {interaction.user.name}", icon_url = interaction.user.avatar.url)

        if count_heroes == 0:
            return await interaction.response.send_message(embed = embed_message)

        
        view = ShowHeroes()
        await interaction.response.send_message(embed = embed_message, view= view)
        
    @sell_heroes.error
    async def sell_heroesxError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Upss! Kahraman tüccarı burada değill! Lütfen`{timeRemaining}`s sonra geliniz!",ephemeral=True)
    
    
async def setup(bot:commands.Bot):
    await bot.add_cog(SellHeroes(bot))
