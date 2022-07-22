import discord
from discord import Embed
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import random
import yaml
from yaml import Loader


yaml_file2 = open("animals.yml", "r")
animals = yaml.load(yaml_file2, Loader = Loader) 

priceBySize = animals["priceBySize"]
allFishes = animals['fishes']
fishesKey = " ".join(animals["fishes"].keys())
fishes = fishesKey.split(" ")

allHunts = animals["hunts"]
huntsKey = " ".join(animals["hunts"].keys())
hunts = huntsKey.split(" ")


# Emojis
yaml_file = open("emojis.yml", "r")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"


class sell(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sell", description="Avladığın hayvanları sat ve Cupcoin kazan")
    @app_commands.checks.cooldown(
        1, 1, key=lambda i: (i.guild_id, i.user.id))
    async def sell(self, interaction: discord.Interaction):
        view = View()
        

        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Envanteriniz bulunmuyor! Satmak için hayvan avlayın.")

        userData = await collection.find_one({"_id" : interaction.user.id})

        sumFish = 0
        numberFish = 0

        sumHunt = 0
        numberHunt = 0

        if 'fishes' in userData:
            userFishes = list(userData['fishes'].keys())
            for i in userData['fishes'].values():
                sumFish += (i*priceBySize)
            for x in fishes:
                if x in userFishes:
                    sumFish += allFishes[x] 
            numberFish = len(userData['fishes'])
        
        if 'hunts' in userData:
            userHunts = userData['hunts']
            for x in hunts:
                if x in userHunts:
                    sumHunt += allHunts[x] 
            numberHunt = len(userData['hunts'])


        sellFish = Button(label="Balıkları Sat!", style=discord.ButtonStyle.success, custom_id="sellfish")
        async def sellFish_callback(interaction):
            sellFish.label = "Balıklar Satıldı"
            sellFish.style = discord.ButtonStyle.secondary
            sellFish.disabled = True
            await interaction.response.edit_message(view = view)

        sellHunt = Button(label="Avları Sat!", style=discord.ButtonStyle.success, custom_id="sellhunt")
        async def sellHunt_callback(interaction):
            sellHunt.label = "Avlar Satıldı"
            sellHunt.style = discord.ButtonStyle.secondary
            sellHunt.disabled = True
            await interaction.response.edit_message(view = view)

        menuEmbed = Embed(description = f"Merhaba 👋 Pazara hoş geldin. Burada tuttuğun balıkları ve avladığın hayvanları satabilirsin. İşte senin envanterin:")
        menuEmbed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar.url)
        menuEmbed.add_field(name = "Fishes:", value = f"**{numberFish}** adet balığınız var. Toplam = **{sumFish}** Cupcoin ediyor." )
        menuEmbed.add_field(name = "Hunts:", value = f"**{numberHunt}** adet avınız var. Toplam = **{sumHunt}** Cupcoin ediyor." )



        closeMenu = Button(label="Kapat!", style=discord.ButtonStyle.danger, custom_id="closeMenu")
        async def close_callback(interaction):
            await interaction.message.delete()

        closeMenu.callback = close_callback
        sellFish.callback = sellFish_callback
        sellHunt.callback = sellHunt_callback
        
        view.add_item(sellFish)
        view.add_item(sellHunt)
        view.add_item(closeMenu)
        
        await interaction.response.send_message(embed = menuEmbed, view=view)









    @sell.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Yorgunsun. `{timeRemaining}`s dinlen.",ephemeral=True)


async def setup(bot:commands.Bot):
    await bot.add_cog(sell(bot), guilds= [discord.Object(id =964617424743858176)])