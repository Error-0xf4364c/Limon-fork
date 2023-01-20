import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime
import yaml
from yaml import Loader
from fetchdata import *

yaml_file = open("assets/yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

licash = emojis["licash"]
cross = emojis["cross"]
coinback = emojis["coinback"]
coinfront = emojis["coinfront"]

morelicash = emojis["morelicash"]
clock = emojis["clock"] or "⏳"



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

        userData, collection = create_wallet(self.bot, interaction.user.id)
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)
        
        userCareerData["points"]['gamble_point'] += 1
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if userData["cash"] < miktar:
            return await interaction.response.send_message(f"{cross} Yetersiz LiCash!")


        cf = [1, 0]

        moneyRecieved = random.choice(cf)



        if moneyRecieved == 1:
            r = miktar * 2
            userData['cash'] += miktar
            collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Yazı Tura atılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content = f"{coinfront} Tebrikler, **{r:,}** LiCash kazandınız!")

        else:
            userData['cash'] -= miktar
            collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Yazı Tura atılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content = f"{coinback} Maalesef, bir dahaki sefere ;c")


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


        userData, collection = create_wallet(self.bot, interaction.user.id)
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)

        
        userCareerData["points"]['gamble_point'] += 1
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        moneyRecieved = random.randint(1,10)

        if moneyRecieved == number:
            r = amount * 5
            userData['cash'] += r
            collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"{licash} Tebrikler. Rakamı doğru tahmin ettiniz ve **{r:,}** LiCash kazandınız!")
        else:
            userData['cash'] -= amount
            collection.replace_one({"_id": interaction.user.id}, userData)
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

        userData, collection = create_wallet(self.bot, interaction.user.id)
        userCareerData, careerCollection = create_career_data(self.bot, interaction.user.id)
        
        userCareerData["points"]['gamble_point'] += 1
        careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if userData["cash"] < amount:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli LiCash bulunmuyor!")

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        total = dice1 + dice2



        if total %2 == 0:
            if choose == "cift":
                r = amount * 2
                userData['cash'] += r
                collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content = f"{licash} Tebrikler. 2 zar sonucu {total} geldi ve toplam**{r:,}** LiCash kazandınız!")
            else:
                userData['cash'] -= amount
                collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content= "Maalesef, bir dahaki sefere ;c")
        else:
            if choose== "tek":
                r = amount * 2
                userData['cash'] += r
                collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content=f"{licash} Tebrikler. 2 zar sonucu {total} geldi ve toplam**{r:,}** LiCash kazandınız!")
            else:
                userData['cash'] -= amount
                collection.replace_one({"_id": interaction.user.id}, userData)
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

        userData, collection = create_wallet(self.bot, interaction.user.id)

        

        woodenBoxBounty = random.randint(7000, 20000)
        silverBoxBounty = random.randint(17000, 30000)
        goldenBoxBounty = random.randint(35000, 60000)
        platinBoxBounty = random.randint(59000, 80000)
        diamondBoxBounty = random.randint(50000, 210000)

        if box == "wooden":
            if userData['cash'] < woodenBox:
                return await interaction.response.send_message(f"{cross} Tahta kasa açabilmek için **{woodenBox:,}** LiCash gerekiyor!")
            userData['cash'] -= woodenBox
            userData['cash'] += woodenBoxBounty
            collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content= f" {morelicash} Tahta kasadan tam **{woodenBoxBounty:,}** LiCash çıktı! Yeni bakiyeniz **{userData['cash']:,}** LiCash")

        elif box == "silver":
            if userData['cash'] < silverBox:
                return await interaction.response.send_message(f"{cross} Gümüş kasa açabilmek için **{silverBox:,}** LiCash gerekiyor!")
            userData['cash'] -= silverBox
            userData['cash'] += silverBoxBounty
            collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {morelicash} Gümüş kasadan tam**{silverBoxBounty:,}** LiCash çıktı! Yeni bakiyeniz **{userData['cash']:,}** LiCash")


        elif box == "golden":
            if userData['cash'] < goldenBox:
                return await interaction.response.send_message(f"{cross} Altın kasa açabilmek için **{goldenBox:,}** LiCash gerekiyor!")
            userData['cash'] -= goldenBox
            userData['cash'] += goldenBoxBounty
            collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(
                content=f" {licash} Altın kasadan tam **{goldenBoxBounty:,}** LiCash çıktı! Yeni bakiyeniz **{userData['cash']:,}** LiCash")

        elif box == "platin":
            if userData['cash'] < platinBox:
                return await interaction.response.send_message(f"{cross} Platin kasa açabilmek için **{platinBox:,}** LiCash gerekiyor!")
            userData['cash'] -= platinBox
            userData['cash'] += platinBoxBounty
            collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {morelicash} Platin kasadan tam**{platinBoxBounty:,}** LiCash çıktı! Yeni bakiyeniz **{userData['cash']:,}** LiCash")

        elif box == "diamond":
            if userData['cash'] < diamondBox:
                return await interaction.response.send_message(f"{cross} Elmas kasa açabilmek için **{diamondBox:,}** LiCash gerekiyor!")
            userData['cash'] -= diamondBox
            userData['cash'] += diamondBoxBounty
            collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kasa açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {morelicash} Elmas kasadan tam**{diamondBoxBounty:,}** LiCash çıktı! Yeni bakiyeniz **{userData['cash']:,}** LiCash")

    @openbox.error
    async def openboxError(self, interaction: discord.Interaction,
                        error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)

# , guilds= [discord.Object(id =964617424743858176)]
async def setup(bot:commands.Bot):
    await bot.add_cog(gambles(bot))