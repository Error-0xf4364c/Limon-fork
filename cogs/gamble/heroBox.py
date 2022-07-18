import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime
import yaml
from yaml import Loader
import random

yaml_file = open("emojis.yml", "r")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"

yaml_file2 = open("chars.yml", "r")
heroes = yaml.load(yaml_file2, Loader = Loader) 






class boxes(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hero-box", description="Kahraman kutusu aç ve onlardan birine sahip ol!")
    @app_commands.checks.cooldown(
        1, 21600, key=lambda i: (i.guild_id, i.user.id))
    async def herobox(self, interaction: discord.Interaction):
        #print(list(heroes.keys()))

        caseFee = 10
        
        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]
        economyCollection = db["economy"]
        userData = await collection.find_one({"_id" : interaction.user.id})
        userCoins = await economyCollection.find_one({"_id" : interaction.user.id})

        if userCoins['coins'] < caseFee:
            return await interaction.response.send_message(f"{emojis['cross']} Kahraman kutusu açabilmeniz için **{caseFee - userCoins['coins']:,}** Cupcoine ihtiyacınız var.", ephemeral=True)

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
        print(sliceHero)
        # --------| HEROLAR
        yourHero = random.choice(sliceHero)
        if yourHero != None:
            print(heroes[yourHero]['name'])
            print(type(heroes[yourHero]['name']))
            print(heroes[yourHero]['description'])
            print(type(heroes[yourHero]['description']))
        userCoins['coins'] -= caseFee
        await economyCollection.replace_one({"_id": interaction.user.id}, userCoins)

        if yourHero == None:
            await interaction.response.send_message(f"{emojis['3dot']} **|** Kahraman kutusu açılıyor.")
            await asyncio.sleep(5)
            return await interaction.edit_original_message(f"{emojis['cross']} Maalesef kutudan hiç kahraman çıkmadı ;c")
        
        if userData['heroes'].count(yourHero) >= 1:
            await interaction.response.send_message(f"{emojis['3dot']} **|** Kahraman kutusu açılıyor.")
            await asyncio.sleep(5)
            return await interaction.edit_original_message(f"Bir {yourHero.title()} çıktı fakat bu kahraman zaten envanterinizde mevcut.")

        heroEmbed = discord.Embed(title= heroes[yourHero]["name"], description= heroes[yourHero]["description"])
        heroEmbed.set_author(name= "Tebrikler. Yeni bir kahramanınız oldu.", icon_url= interaction.user.avatar.url),
        heroEmbed.add_field(name = "Can / Hp:", value =  heroes[yourHero]['hp'], inline = True),
        heroEmbed.add_field(name= "Güç", value =  heroes[yourHero]['power'], inline = True)
        
        #await interaction.response.send_message(f"{emojis['clock']} **|** kahramanın kutudan çıkması birkaç saniye alabilir.")
        #await asyncio.sleep(7)
        #await interaction.delete_original_message()
        await interaction.response.send_message(embed=heroEmbed)
        userData['heroes'].append(yourHero) 
        await collection.replace_one({"_id": interaction.user.id}, userData)

        




    @herobox.error
    async def heroboxError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Heey! Diğerleri daha yumurtalarından bile çıkmadılar. `{timeRemaining}`s sonra tekrar dene.",ephemeral=True)





async def setup(bot:commands.Bot):
    await bot.add_cog(boxes(bot), guilds= [discord.Object(id =964617424743858176)])