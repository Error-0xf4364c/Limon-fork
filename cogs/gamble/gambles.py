import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime
import yaml
from yaml import Loader

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

cupcoin = emojis["cupcoin"]
cross = emojis["cross"]
cupcoinBack = emojis["cupcoinBack"]
cupcoins = emojis["cupcoins"]
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

    @app_commands.command(name="coinflip", description="Yazı-Tura atarak Cupcoin kazan.")
    @app_commands.describe(miktar='Enter the Amount')
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def coinflip(self, interaction: discord.Interaction, miktar: app_commands.Range[int, 1, 50000]):


        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        invcollection = db['inventory']

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        userInvData = await invcollection.find_one({"_id": interaction.user.id})
            

        if not "kumarpuani" in  userInvData:
            gambleData = { "$set" : {"kumarpuani" : 0}}
            await invcollection.update_one(userInvData ,gambleData)
        userInvData['kumarpuani'] += 1
        await invcollection.replace_one({"_id": interaction.user.id}, userInvData)

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")


        cf = [1, 0]

        moneyRecieved = random.choice(cf)

        if moneyRecieved == 1:
            r = miktar * 2
            userData['coins'] += miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content = f"{cupcoin} Tebrikler, **{r:,}** Cupcoin kazandınız!")

        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content = f"{cupcoinBack} Maalesef bir dahaki sefere ;c")


    @coinflip.error
    async def coinflipError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",ephemeral=True)

    # ----- GUESS NUMBER ----

    @app_commands.command(
        name="guess-number",
        description="Sayıyı bil ve 5 katı coin kazan. (1 - 10)")
    @app_commands.describe(miktar='Enter the Amount', number="Your Guess")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))

    async def guessnumber(self, interaction: discord.Interaction, miktar: app_commands.Range[int, 1, 50000], number: app_commands.Range[int, 1, 10]):



        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        invcollection = db['inventory']

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Henüz bir hesabınız yok.")

        userData = await collection.find_one({"_id": interaction.user.id})
        userInvData = await invcollection.find_one({"_id": interaction.user.id})

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")

        if not "kumarpuani" in  userInvData:
            gambleData = { "$set" : {"kumarpuani" : 0}}
            await invcollection.update_one(userInvData ,gambleData)
        userInvData['kumarpuani'] += 1
        await invcollection.replace_one({"_id": interaction.user.id}, userInvData)

        moneyRecieved = random.randint(1,10)

        if moneyRecieved == number:
            r = miktar * 5
            userData['coins'] += r
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"{cupcoin} Tebrikler, sayıyı doğru bildiniz ve tam **{r:,}** Cupcoin kazandınız!")
        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"Maalesef sayıyı doğru tahmin edemediniz. Bir dahaki sefere ;c")

    @guessnumber.error
    async def guessnumberError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.", ephemeral=True)


    #----- DICE -----
    @app_commands.command(
        name="roll",
        description="Zar at ve Cupcoin kazan")
    @app_commands.describe(seç="Tek mi, Çift mi?" ,miktar='Enther the Amount')
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(seç = [
        Choice(name="Çift", value="cift"),
        Choice(name="Tek", value="tek")
    ])
    async def roll(self, interaction: discord.Interaction, seç: str, miktar: app_commands.Range[int, 1, 50000]):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        invcollection = db['inventory']

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Henüz bir hesabınız yok.")

        userData = await collection.find_one({"_id": interaction.user.id})
        userInvData = await invcollection.find_one({"_id": interaction.user.id})
        userData['coins']


        if not "kumarpuani" in  userInvData:
            gambleData = { "$set" : {"kumarpuani" : 0}}
            await invcollection.update_one(userInvData ,gambleData)
        userInvData['kumarpuani'] += 1
        await invcollection.replace_one({"_id": interaction.user.id}, userInvData)

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        total = dice1 + dice2



        if total %2 == 0:
            if seç == "cift":
                r = miktar * 2
                userData['coins'] += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content = f"{cupcoin} Tebrikler, iki zar sonucu {total} geldi ve tam **{r:,}** Cupcoin kazandınız!")
            else:
                userData['coins'] -= miktar
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content= "Maalesef kaybettiniz. Bir dahaki sefere ;c")
        else:
            if seç == "tek":
                r = miktar * 2
                userData['coins'] += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content=f"{cupcoin} Tebrikler, iki zar sonucu {total} geldi ve tam **{r:,}** Cupcoin kazandınız!")
            else:
                userData['coins'] -= miktar
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content= "Maalesef kaybettiniz. Bir dahaki sefere ;c")
    @roll.error
    async def rollError(self, interaction: discord.Interaction,
                               error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",ephemeral=True)

    # ----- OPEN BOX -----
    @app_commands.command(
        name="open-box",
        description="Kutu aç ve Zengin Ol!")
    @app_commands.describe(box = "Açmak istediğiniz kutuyu seçiniz.")
    @app_commands.choices(box=[
        Choice(name=f"Tahta Kutu - {woodenBox:,}", value="wooden"),
        Choice(name=f"Gümüş Kutu - {silverBox:,}" , value="silver"),
        Choice(name=f"Altın Kutu - {goldenBox:,}", value="golden"),
        Choice(name=f"Platin Kutu - {platinBox:,}", value="platin"),
        Choice(name=f"Elmas Kutu - {diamondBox:,}", value="diamond"),
    ])
    @app_commands.checks.cooldown(
        1, 14400, key=lambda i: (i.guild_id, i.user.id))
    async def openbox(self, interaction: discord.Interaction, box: str):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Henüz bir hesabınız yok.")

        userData = await collection.find_one({"_id": interaction.user.id})

        

        woodenBoxBounty = random.randint(7000, 20000)
        silverBoxBounty = random.randint(17000, 30000)
        goldenBoxBounty = random.randint(35000, 60000)
        platinBoxBounty = random.randint(59000, 80000)
        diamondBoxBounty = random.randint(50000, 210000)

        if box == "wooden":
            if userData['coins'] < woodenBox:
                return await interaction.response.send_message(f"{cross} Tahta kutu açmak için **{woodenBox:,}** Cupcoin gerekiyor! ")
            userData['coins'] -= woodenBox
            userData['coins'] += woodenBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kutu açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content= f" {cupcoins} Tahta kutudan tam **{woodenBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz: **{userData['coins']:,}** Cupcoin")

        elif box == "silver":
            if userData['coins'] < silverBox:
                return await interaction.response.send_message(f"{cross} Gümüş kutu açmak için **{silverBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= silverBox
            userData['coins'] += silverBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kutu açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content=f" {cupcoins} Gümüş kutudan tam **{silverBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz: **{userData['coins']:,}** Cupcoin")


        elif box == "golden":
            if userData['coins'] < goldenBox:
                return await interaction.response.send_message(f"{cross} Altın kutu açmak için **{goldenBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= goldenBox
            userData['coins'] += goldenBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kutu açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(
                content=f" {cupcoins} Altın kutudan tam **{goldenBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz: **{userData['coins']:,}** Cupcoin")

        elif box == "platin":
            if userData['coins'] < platinBox:
                return await interaction.response.send_message(f"{cross} Platin kutu açmak için **{platinBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= platinBox
            userData['coins'] += platinBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kutu açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content=f" {cupcoins} Platin kutudan tam **{platinBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz: **{userData['coins']:,}** Cupcoin")

        elif box == "diamond":
            if userData['coins'] < diamondBox:
                return await interaction.response.send_message(f"{cross} Elmas kutu açmak için **{diamondBox:,}** Cupcoin gerekiyor!")
            userData['coins'] -= diamondBox
            userData['coins'] += diamondBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("Kutu açılıyor...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content=f" {cupcoins} Elmas kutudan tam **{diamondBoxBounty:,}** Cupcoin çıktı! Yeni bakiyeniz: **{userData['coins']:,}** Cupcoin")

    @openbox.error
    async def openboxError(self, interaction: discord.Interaction,
                        error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",ephemeral=True)

# , guilds= [discord.Object(id =964617424743858176)]
async def setup(bot:commands.Bot):
    await bot.add_cog(gambles(bot))