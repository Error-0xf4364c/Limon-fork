import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import asyncio
import datetime

cupcoin = "<:Cupcoin:997158251944738938>"
cross = "<:cx:991397749486522499>"
cupcoinBack = "<:CupcoinBack:997241145438503023>"

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

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")


        cf = [1, 0]

        moneyRecieved = random.choice(cf)

        if moneyRecieved == 1:
            r = miktar * 2
            userData['coins'] += r
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_message(content = f"{cupcoin} Tebrikler, **{r}** Cupcoin kazandınız!")

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
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",ephemeral=True)

    # ----- GUESS NUMBER ----

    @app_commands.command(
        name="guess-number",
        description="Sayıyı bil ve 5 katı coin kazan.")
    @app_commands.describe(miktar='Enter the Amount', number="Your Guess")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))

    async def guessnumber(self, interaction: discord.Interaction, miktar: app_commands.Range[int, 1, 50000], number: app_commands.Range[int, 1, 10]):



        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Henüz bir hesabınız yok.")

        userData = await collection.find_one({"_id": interaction.user.id})

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")



        moneyRecieved = random.randint(1,10)

        if moneyRecieved == number:
            r = miktar * 5
            userData['coins'] += r
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"{cupcoin} Tebrikler, sayıyı doğru bildiniz ve tam **{r}** Cupcoin kazandınız!")
        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"Maalesef sayıyı doğru tahmin edemediniz. Bir dahaki sefere ;c")

    @guessnumber.error
    async def guessnumberError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.", ephemeral=True)


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

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Henüz bir hesabınız yok.")

        userData = await collection.find_one({"_id": interaction.user.id})
        balance = userData['coins']

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        total = dice1 + dice2


        if total %2 == 0:
            if seç == "cift":
                r = miktar * 2
                balance += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content = f"{cupcoin} Tebrikler, iki zar sonucu {total} geldi ve tam **{r}** Cupcoin kazandınız!")
            else:
                balance -= miktar
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content= "Maalesef kaybettiniz. Bir dahaki sefere ;c")
        else:
            if seç == "tek":
                r = miktar * 2
                balance += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content=f"{cupcoin} Tebrikler, iki zar sonucu {total} geldi ve tam **{r}** Cupcoin kazandınız!")
            else:
                balance -= miktar
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Zarlar atılıyor...")
                await asyncio.sleep(4)
                await interaction.edit_original_message(content= "Maalesef kaybettiniz. Bir dahaki sefere ;c")
    @roll.error
    async def rollError(self, interaction: discord.Interaction,
                               error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",ephemeral=True)




async def setup(bot:commands.Bot):
    await bot.add_cog(gambles(bot), guilds= [discord.Object(id =964617424743858176)])