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

    @app_commands.command(name = "send", description = "Send Cupcoin to your friends!")
    @app_commands.describe(friend='Who will you send it to?', amount="The amount of coins you will send")
    @app_commands.checks.cooldown(
        1, 50.0, key=lambda i: (i.guild_id, i.user.id))
    async def send(self, interaction: discord.Interaction, friend: discord.User, amount: app_commands.Range[int, 1, 50000]):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        careerCollection = db["career"]
        
        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "points": {"send_point": 0}
            }
            await careerCollection.insert_one(newData)

        userCareerData = await careerCollection.find_one({"_id": interaction.user.id})

        if "points" not in userCareerData:
            careerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareerData ,careerData)

        if not "send_point" in  userCareerData["points"]:
            sendCData = { "$set" : {"points.send_point" : 0}}
            await careerCollection.update_one(userCareerData ,sendCData)
            
        userCareerData = await careerCollection.find_one({"_id": interaction.user.id})
        userCareerData["points"]['send_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if friend == interaction.user:
            return await interaction.response.send_message(f"{cross} You don't send money to yourself!", ephemeral=True)

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return
        elif await collection.find_one({"_id": friend.id}) == None:
            return await interaction.response.send_message(f"{whiteCross} The person you specified was not found ;c", ephemeral= True)

        userData = await collection.find_one({"_id": interaction.user.id})
        targetData = await collection.find_one({"_id": friend.id})

        if userData['coins'] < amount:
            return await interaction.response.send_message(f"{cross} There is not enough Cupcoin in your wallet!")

        userData['coins'] -= amount
        targetData['coins'] += amount
        await collection.replace_one({"_id": interaction.user.id}, userData)
        await collection.replace_one({"_id": friend.id}, targetData)
        await interaction.response.send_message(f"{send} You successfully sent **{amount:,}** Cupcoin to your friend  **{friend.name}**.")
    @send.error
    async def sendError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}`s and Try Again!",
                                                    ephemeral=True)
        else:
            print(error)

async def setup(bot:commands.Bot):
    await bot.add_cog(sendCoin(bot))
