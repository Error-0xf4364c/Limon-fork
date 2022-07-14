import discord
from discord import app_commands
from discord.ext import commands
import datetime


class sendCoin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "send", description = "Arkadaşına Coin Gönder")
    @app_commands.describe(friend='Who will you send it to?', amount="The amount of coins you will send")
    @app_commands.checks.cooldown(
        10, 60.0, key=lambda i: (i.guild_id, i.user.id))
    async def send(self, interaction: discord.Interaction, friend: discord.User, amount: app_commands.Range[int, 1, 50000]):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if friend == interaction.user:
            return await interaction.response.send_message("<:cx:991397749486522499> Kendinize coin gönderemezsiniz!", ephemeral=True)

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return
        elif await collection.find_one({"_id": friend.id}) == None:
            return await interaction.response.send_message("<:whiteCross:996130010471600228> Belirttiğiniz kişi bulunamadı ;c", ephemeral= True)

        userData = await collection.find_one({"_id": interaction.user.id})
        targetData = await collection.find_one({"_id": friend.id})

        if userData['coins'] < amount:
            return await interaction.response.send_message("<:cx:991397749486522499> Cüzdanınızda yeterli coin bulunmuyor!")

        userData['coins'] -= amount
        targetData['coins'] += amount
        await collection.replace_one({"_id": interaction.user.id}, userData)
        await collection.replace_one({"_id": friend.id}, targetData)
        await interaction.response.send_message(f"<:sendcoin:996130502698336257> **{friend.name}** arkadaşınıza başarıyla **{amount}** Cupcoin gönderdiniz.")
    @send.error
    async def sendError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(sendCoin(bot), guilds= [discord.Object(id =964617424743858176)])