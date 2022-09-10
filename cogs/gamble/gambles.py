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

    @app_commands.command(name="coinflip", description="Flip a coin and win money.")
    @app_commands.describe(miktar='Enter the Amount')
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    async def coinflip(self, interaction: discord.Interaction, miktar: app_commands.Range[int, 1, 50000]):


        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        careerCollection = db['career']

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})
        
        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "points": {"gamble_point": 0}
            }
            await careerCollection.insert_one(newData)

        userCareerData = await careerCollection.find_one({"_id": interaction.user.id})
            
        if "points" not in userCareerData:
            careerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareerData ,careerData)

        if not "gamble_point" in  userCareerData["points"]:
            gambleData = { "$set" : {"points.gamble_point" : 0}}
            await careerCollection.update_one(userCareerData ,gambleData)
        userCareerData["points"]['gamble_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if userData["coins"] < miktar:
            return await interaction.response.send_message(f"{cross} There is not enough Cupcoin in your wallet!")


        cf = [1, 0]

        moneyRecieved = random.choice(cf)



        if moneyRecieved == 1:
            r = miktar * 2
            userData['coins'] += miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content = f"{cupcoin} Congratulations, you have won **{r:,}** Cupcoin!")

        else:
            userData['coins'] -= miktar
            await collection.replace_one({"_id" : interaction.user.id}, userData)
            await interaction.response.send_message("Coinflipping...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content = f"{cupcoinBack} Unfortunately, next time ;c")


    @coinflip.error
    async def coinflipError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait `{timeRemaining}`s and Try Again!",ephemeral=True)

    # ----- GUESS NUMBER ----

    @app_commands.command(
        name="guess-number",
        description="Know the number and win 5 times the Cupcoin. (1 - 10)")
    @app_commands.describe(amount='Enter the Amount', number="Your Guess")
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))

    async def guessnumber(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 50000], number: app_commands.Range[int, 1, 10]):



        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        careerCollection = db["career"]

        

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have an account. Please use this command: **`/wallet`**")

        userData = await collection.find_one({"_id": interaction.user.id})

        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "points": {"gamble_point": 0}
            }
            await careerCollection.insert_one(newData)
        userCareerData = await careerCollection.find_one({"_id": interaction.user.id})

        if userData["coins"] < amount:
            return await interaction.response.send_message(f"{cross} There is not enough money in your wallet!")

        if "points" not in userCareerData:
            careerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareerData ,careerData)

        if not "gamble_point" in  userCareerData["points"]:
            gambleData = { "$set" : {"points.gamble_point" : 0}}
            await careerCollection.update_one(userCareerData ,gambleData)
        userCareerData["points"]['gamble_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        moneyRecieved = random.randint(1,10)

        if moneyRecieved == number:
            r = amount * 5
            userData['coins'] += r
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"{cupcoin} Congratulations. You got the number right and won **{r:,}** Cupcoin!")
        else:
            userData['coins'] -= amount
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message(f"Unfortunately, you didn't guess the number correctly. Next time ;c")

    @guessnumber.error
    async def guessnumberError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait `{timeRemaining}`s and Try Again!", ephemeral=True)


    #----- DICE -----
    @app_commands.command(
        name="roll",
        description="Roll the dice and win a cupcoin")
    @app_commands.describe(choose="Single or double?" ,amount='Enther the Amount')
    @app_commands.checks.cooldown(
        1, 10.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.choices(choose = [
        Choice(name="Double", value="cift"),
        Choice(name="Single", value="tek")
    ])
    async def roll(self, interaction: discord.Interaction, choose: str, amount: app_commands.Range[int, 1, 50000]):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        careerCollection = db["career"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have an account. Please use this command: **`/wallet`**")

        userData = await collection.find_one({"_id": interaction.user.id})

        userData['coins']

        if await careerCollection.find_one({"_id": interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "points": {"gamble_point": 0}
            }
            await careerCollection.insert_one(newData)
        userCareerData = await careerCollection.find_one({"_id": interaction.user.id})
            
        if "points" not in userCareerData:
            careerData = { "$set" : {"points" : {}}}
            await careerCollection.update_one(userCareerData ,careerData)

        if not "gamble_point" in  userCareerData["points"]:
            gambleData = { "$set" : {"points.gamble_point" : 0}}
            await careerCollection.update_one(userCareerData ,gambleData)
        userCareerData["points"]['gamble_point'] += 1
        await careerCollection.replace_one({"_id": interaction.user.id}, userCareerData)

        if userData["coins"] < amount:
            return await interaction.response.send_message(f"{cross} There are not enough Cupcoins in your wallet!")

        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        total = dice1 + dice2



        if total %2 == 0:
            if choose == "cift":
                r = amount * 2
                userData['coins'] += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Rolling the dice...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content = f"{cupcoin} Congratulations. the result of 2 dice came to {total} and you won**{r:,}** Cupcoin!")
            else:
                userData['coins'] -= amount
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Rolling the dice...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content= "Sorry you lost next time ;c")
        else:
            if choose== "tek":
                r = amount * 2
                userData['coins'] += r
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Rolling the dice...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content=f"{cupcoin} Congratulations. the result of 2 dice came to {total} and you won**{r:,}** Cupcoin!")
            else:
                userData['coins'] -= amount
                await collection.replace_one({"_id": interaction.user.id}, userData)
                await interaction.response.send_message("🎲 Rolling the dice...")
                await asyncio.sleep(4)
                await interaction.edit_original_response(content= "Sorry you lost next time ;c")
    @roll.error
    async def rollError(self, interaction: discord.Interaction,
                               error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait `{timeRemaining}`s and Try Again!",ephemeral=True)

    # ----- OPEN BOX -----
    @app_commands.command(
        name="open-box",
        description="Open a box and get rich!")
    @app_commands.describe(box = "Select the box you want to open.")
    @app_commands.choices(box=[
        Choice(name=f"Wooden Box - {woodenBox:,}", value="wooden"),
        Choice(name=f"Silver Box - {silverBox:,}" , value="silver"),
        Choice(name=f"Golden Box - {goldenBox:,}", value="golden"),
        Choice(name=f"Platinum Box - {platinBox:,}", value="platin"),
        Choice(name=f"Diamond Box - {diamondBox:,}", value="diamond"),
    ])
    @app_commands.checks.cooldown(
        1, 14400, key=lambda i: (i.guild_id, i.user.id))
    async def openbox(self, interaction: discord.Interaction, box: str):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have an account. Please use this command: **`/wallet`**")

        userData = await collection.find_one({"_id": interaction.user.id})

        

        woodenBoxBounty = random.randint(7000, 20000)
        silverBoxBounty = random.randint(17000, 30000)
        goldenBoxBounty = random.randint(35000, 60000)
        platinBoxBounty = random.randint(59000, 80000)
        diamondBoxBounty = random.randint(50000, 210000)

        if box == "wooden":
            if userData['coins'] < woodenBox:
                return await interaction.response.send_message(f"{cross} It takes **{woodenBox:,}** Cupcoin to open a wooden box! ")
            userData['coins'] -= woodenBox
            userData['coins'] += woodenBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("The box opens...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content= f" {cupcoins} **{woodenBoxBounty:,}** Cupcoin came out of the wooden box! Your new balance is **{userData['coins']:,}** ")

        elif box == "silver":
            if userData['coins'] < silverBox:
                return await interaction.response.send_message(f"{cross} It takes **{silverBox:,}** Cupcoin to open a silver box!")
            userData['coins'] -= silverBox
            userData['coins'] += silverBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("The box opens...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {cupcoins} **{silverBoxBounty:,}**  Cupcoin came out of the silver box! Your new balance is **{userData['coins']:,}** ")


        elif box == "golden":
            if userData['coins'] < goldenBox:
                return await interaction.response.send_message(f"{cross} It takes **{goldenBox:,}** Cupcoin to open a golden box!")
            userData['coins'] -= goldenBox
            userData['coins'] += goldenBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("The box opens...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(
                content=f" {cupcoins} **{goldenBoxBounty:,}** Cupcoin came out of the golden box! Your new balance is **{userData['coins']:,}** ")

        elif box == "platin":
            if userData['coins'] < platinBox:
                return await interaction.response.send_message(f"{cross} It takes **{platinBox:,}** Cupcoin to open a platinum box!")
            userData['coins'] -= platinBox
            userData['coins'] += platinBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("The box opens...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {cupcoins}**{platinBoxBounty:,}** Cupcoin came out of the platinum box! Your new balance is **{userData['coins']:,}** ")

        elif box == "diamond":
            if userData['coins'] < diamondBox:
                return await interaction.response.send_message(f"{cross} It takes **{diamondBox:,}** Cupcoin to open a diamond box!")
            userData['coins'] -= diamondBox
            userData['coins'] += diamondBoxBounty
            await collection.replace_one({"_id": interaction.user.id}, userData)
            await interaction.response.send_message("The box opens...")
            await asyncio.sleep(4)
            await interaction.edit_original_response(content=f" {cupcoins} **{diamondBoxBounty:,}** Cupcoin came out of the diamond box! Your new balance is **{userData['coins']:,}** ")

    @openbox.error
    async def openboxError(self, interaction: discord.Interaction,
                        error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait `{timeRemaining}`s and Try Again!",ephemeral=True)

# , guilds= [discord.Object(id =964617424743858176)]
async def setup(bot:commands.Bot):
    await bot.add_cog(gambles(bot))