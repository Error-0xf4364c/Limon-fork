from gc import collect
import discord
from discord import app_commands
from discord.ext import commands
from fetchData import fetchData
import datetime

import random


class gambles(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Yazı-Tura atarak para kazan.")
    @app_commands.checks.cooldown(
        10, 60.0, key=lambda i: (i.guild_id, i.user.id))
    async def coinflip(self, interaction: discord.Interaction, miktar: int):


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
            return await interaction.response.send_message("<:cx:991397749486522499> Cüzdanınızda yeterli coin bulunmuyor!")


        cf = [1, 0]

        moneyRecieved = random.choice(cf)

        if moneyRecieved == 1:
            r = miktar * 2
            userData['coins'] += r
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await interaction.edit_original_message(f"<:ccoin:996130482519552000> Tebrikler, **{r}** coin kazandınız!")
        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await interaction.edit_original_message(content = f"<:ccoin:996130482519552000> Maalesef bir dahaki sefere ;c")

    @coinflip.error
    async def coinflipError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)

    @app_commands.command(
        name="guessnumber",
        description="Sayıyı bil ve 5 katı coin kazan."
    )
    @app_commands.checks.cooldown(
        10, 60.0, key=lambda i: (i.guild_id, i.user.id))
    async def guessnumber(self, interaction: discord.Interaction, miktar: int, number: int):


        if number >= 10 or number <= 1:
            return await interaction.response.send_message("Lütfen yalnızca `1` ve `10` arası sayılar giriniz.", ephemeral=True)

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins": 0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})

        if userData["coins"] < miktar:
            return await interaction.response.send_message("<:cx:991397749486522499> Cüzdanınızda yeterli coin bulunmuyor!")



        moneyRecieved = random.randint(1,10)

        if moneyRecieved == number:
            r = miktar * 5
            userData['coins'] += r
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"<:ccoin:996130482519552000> Tebrikler, sayıyı doğru bildiniz ve tam **{r}** coin kazandınız!")
        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"<:ccoin:996130482519552000> Maalesef sayıyı doğru tahmin edemediniz. Bir dahaki sefere ;c")

    @guessnumber.error
    async def guessnumberError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)



async def setup(bot:commands.Bot):
    await bot.add_cog(gambles(bot), guilds= [discord.Object(id =964617424743858176)])