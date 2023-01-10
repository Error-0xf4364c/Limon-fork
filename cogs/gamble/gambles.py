import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime
import yaml
from yaml import Loader

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
clock = emojis["clock"] or "⏳"
from fetchData import *


woodenBox = 10000 # on bin
silverBox = 20000 # yirmi bin
goldenBox = 50000 # elli bin
platinBox = 70000 # yetmiş bin
diamondBox = 100000 # yüz bin

import random

class gambles(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Yazı tura at ve paranı katla")
    @app_commands.describe(miktar='Miktar giriniz')
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def coinflip(self, interaction: discord.Interaction, miktar: app_commands.Range[int, 1, 50000]):

        userData, collection = await economyData(self.bot, interaction.user.id)
        userCareerData, careerCollection = await careerData(self.bot, interaction.user.id)
        
        userCareerData["points"]['gamble_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Yetersiz Cupcoin!")


        cf = [1, 0]

        moneyRecieved = random.choice(cf)



        if moneyRecieved == 1:
            r = miktar * 2
            userData['coins'] += miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content = f"{cupcoin} Tebrikler, **{r:,}** Cupcoin kazandınız!")

        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content = f"{cupcoinBack} Maalesef, bir dahaki sefere ;c")


    @coinflip.error
    async def coinflipError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)

    # ----- GUESS NUMBER ----

    @app_commands.command(
        name="guess-number",
        description="(1 - 10) arası rakamı bil ve paranı katla")
    @app_commands.describe(amount='Miktar Giriniz', number="Tahmininiz")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))

    async def guessnumber(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 50000], number: app_commands.Range[int, 1, 10]):


        userData, collection = await economyData(self.bot, interaction.user.id)
        userCareerData, careerCollection = await careerData(self.bot, interaction.user.id)

        
        userCareerData["points"]['gamble_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        moneyRecieved = random.randint(1,10)

        if moneyRecieved == number:
            r = amount * 5
            userData['coins'] += r
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"{cupcoin} Tebrikler. Rakamı doğru tahmin ettiniz ve **{r:,}** Cupcoin kazandınız!")
        else:
            userData['coins'] -= amount
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"Maalesef, doğru tahminde bulunamadınız. Bir dahaki sefere ;c")

    @guessnumber.error
    async def guessnumberError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!", ephemeral=True)


    #----- DICE -----
    @app_commands.command(
        name="roll",
        description="Zar at ve paranı katla")
    @app_commands.describe(choose="Tek mi, Çift mi?" ,amount='Miktar giriniz')
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(choose = [
        Choice(name="Çift", value="cift"),
        Choice(name="Tek", value="tek")
    ])
    async def roll(self, interaction: discord.Interaction, choose: str, amount: app_commands.Range[int, 1, 50000]):

        userData, collection = await economyData(self.bot, interaction.user.id)
        userCareerData, careerCollection = await careerData(self.bot, interaction.user.id)
        
        userCareerData["points"]['gamble_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if userData["coins"] < amount:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        total = dice1 + dice2



        if total %2 == 0:
            if choose == "cift":
                r = amount * 2
                userData['coins'] += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content = f"{cupcoin} Tebrikler. 2 zar sonucu {total} geldi ve toplam**{r:,}** Cupcoin kazandınız!")
            else:
                userData['coins'] -= amount
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content= "Maalesef, bir dahaki sefere ;c")
        else:
            if choose== "tek":
                r = amount * 2
                userData['coins'] += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content=f"{cupcoin} Tebrikler. 2 zar sonucu {total} geldi ve toplam**{r:,}** Cupcoin kazandınız!")
            else:
                userData['coins'] -= amount
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content= "Maalesef, bir dahaki sefere ;c")
    @roll.error
    async def rollError(self, interaction: discord.Interaction,
                               error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)

    # ----- OPEN BOX -----
    @app_commands.command(
        name="open-box",
        description="Kasa aç ve zengin ol!")
    @app_commands.describe(box = "Select the box you want to open.")
    @app_commands.choices(box=[
        Choice(name=f"Tahta Kasa - {woodenBox:,}", value="wooden"),
        Choice(name=f"Gümüş Kasa - {silverBox:,}" , value="silver"),
        Choice(name=f"Altın Kasa - {goldenBox:,}", value="golden"),
        Choice(name=f"Platin Kasa - {platinBox:,}", value="platin"),
        Choice(name=f"Elmas Kasa - {diamondBox:,}", value="diamond"),
    ])
    @app_commands.checks.cooldown(
        1, 14400, key=lambda i: (i.guild_id, i.user.id))
    async def openbox(self, interaction: discord.Interaction, box: str):

        userData, collection = await economyData(self.bot, interaction.user.id)

        

        woodenBoxBounty = random.randint(7000, 20000)
        silverBoxBounty = random.randint(17000, 30000)
        goldenBoxBounty = random.randint(35000, 60000)
        platinBoxBounty = random.randint(59000, 80000)
        diamondBoxBounty = random.randint(50000, 210000)

        if box == "wooden":
            if userData['coins'] < woodenBox:
                return await interaction.response.send_message(f"{cross} Tahta kasa açabilmek için **{woodenBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= woodenBox
            userData['coins'] += woodenBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content= f" {cupcoins} Tahta kasadan tam **{woodenBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz **{userData['coins']:,}** Cupcoin")

        elif box == "silver":
            if userData['coins'] < silverBox:
                return await interaction.response.send_message(f"{cross} Gümüş kasa açabilmek için **{silverBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= silverBox
            userData['coins'] += silverBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {cupcoins} Gümüş kasadan tam**{silverBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz **{userData['coins']:,}** Cupcoin")


        elif box == "golden":
            if userData['coins'] < goldenBox:
                return await interaction.response.send_message(f"{cross} Altın kasa açabilmek için **{goldenBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= goldenBox
            userData['coins'] += goldenBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(
                content=f" {cupcoins} Altın kasadan tam **{goldenBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz **{userData['coins']:,}** Cupcoin")

        elif box == "platin":
            if userData['coins'] < platinBox:
                return await interaction.response.send_message(f"{cross} Platin kasa açabilmek için **{platinBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= platinBox
            userData['coins'] += platinBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {cupcoins} Platin kasadan tam**{platinBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz **{userData['coins']:,}** Cupcoin")

        elif box == "diamond":
            if userData['coins'] < diamondBox:
                return await interaction.response.send_message(f"{cross} Elmas kasa açabilmek için **{diamondBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= diamondBox
            userData['coins'] += diamondBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {cupcoins} Elmas kasadan tam**{diamondBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz **{userData['coins']:,}** Cupcoin")

    @openbox.error
    async def openboxError(self, interaction: discord.Interaction,
                        error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)

# , guilds= [discord.Object(id =964617424743858176)]
async def setup(bot:commands.Bot):
    await bot.add_cog(gambles(bot))