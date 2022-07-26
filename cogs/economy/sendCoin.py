import discord
from discord import app_commands
from discord.ext import commands
import yaml
from yaml import Loader
import datetime

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"

whiteCross = emojis['whiteCross']
cross = emojis['cross']
send = emojis['send']

class sendCoin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "send", description = "Arkadaşına Cupcoin Gönder")
    @app_commands.describe(friend='Who will you send it to?', amount="The amount of coins you will send")
    @app_commands.checks.cooldown(
        1, 50.0, key=lambda i: (i.guild_id, i.user.id))
    async def send(self, interaction: discord.Interaction, friend: discord.User, amount: app_commands.Range[int, 1, 50000]):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        invcollection = db["inventory"]

        userInvData = await invcollection.find_one({"_id": interaction.user.id})

        if not "sendpuani" in  userInvData:
            sendCData = { "$set" : {"sendpuani" : 0}}
            await invcollection.update_one(userInvData ,sendCData)
        userInvData['sendpuani'] += 1
        await invcollection.replace_one({"_id": interaction.user.id}, userInvData)

        if friend == interaction.user:
            return await interaction.response.send_message(f"{cross} Kendinize Cupcoin gönderemezsiniz!", ephemeral=True)

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return
        elif await collection.find_one({"_id": friend.id}) == None:
            return await interaction.response.send_message(f"{whiteCross} Belirttiğiniz kişi bulunamadı ;c", ephemeral= True)

        userData = await collection.find_one({"_id": interaction.user.id})
        targetData = await collection.find_one({"_id": friend.id})

        if userData['coins'] < amount:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")

        userData['coins'] -= amount
        targetData['coins'] += amount
        await collection.replace_one({"_id": interaction.user.id}, userData)
        await collection.replace_one({"_id": friend.id}, targetData)
        await interaction.response.send_message(f"{send} **{friend.name}** arkadaşınıza başarıyla **{amount:,}** Cupcoin gönderdiniz.")
    @send.error
    async def sendError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(sendCoin(bot))