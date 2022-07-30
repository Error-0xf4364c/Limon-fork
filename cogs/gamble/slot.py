import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import random
import yaml
from yaml import Loader

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis['clock']

slot_left = emojis['slotleft']
slot_mid = emojis['slotmid']
slot_right = emojis['slotright']

slot7 = emojis['slotseven']
slotCherry = emojis['slotcherry']
slotCupcake = emojis['slotcupcake']
slotHeart = emojis['slotheart']
cross = emojis['cross']


class Slot(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="slot", description="Slot oyna ve paranı katla.")
    @app_commands.describe(amount='Enter the Amount')
    @app_commands.checks.cooldown(
        1, 1.0, key=lambda i: (i.guild_id, i.user.id))
    async def slot(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 50000]):
        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        invcollection = db['inventory']

        

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "coins" :0
            }
            await collection.insert_one(newData)

        if await invcollection.find_one({"_id" : interaction.user.id}) == None:
            newData1 = {
                "_id": interaction.user.id,
                "kumarpuani" :0
            }
            await invcollection.insert_one(newData1)

        userData = await collection.find_one({"_id": interaction.user.id})

        if userData["coins"] < amount:
            return await interaction.response.send_message(f"{cross} Cüzdanınızda yeterli Cupcoin bulunmuyor!")

        userInvData = await invcollection.find_one({"_id": interaction.user.id})

        if not "kumarpuani" in  userInvData:
            gambleData = { "$set" : {"kumarpuani" : 0}}
            await invcollection.update_one(userInvData ,gambleData)
        userInvData['kumarpuani'] += 1
        await invcollection.replace_one({"_id": interaction.user.id}, userInvData)

        userInvData = await invcollection.find_one({"_id": interaction.user.id})
        
        await interaction.response.send_message(f"`CUP SLOT`\n{slot_left}{slot_mid}{slot_right}\n`------->` <:Cupcoins:997159042633961574>{amount:,}\n`------->` ???")
        
        cupcakeReward = 5
        heartReward = 2
        sevenReward = 3
        cherryReward = 1

        slots = {
            0 : slot7,
            1 : slotCherry,
            2 : slotCupcake,
            3 : slotHeart
        }

        result1 = random.choice(slots)
        result2 = random.choice(slots)
        result3 = random.choice(slots)
        await asyncio.sleep(3)

        
        if (result1 == result2) and (result1 == result3):
            if result1 == slot7:
                reward = sevenReward
            elif result1 == slotCherry:
                reward = cherryReward
            elif result1 == "<:slotCupcake:1001820992928223274>":
                reward == cupcakeReward
            elif result1 == "<:slotHeart:1001820997151903785>":
                reward = heartReward
            await interaction.edit_original_message(content = f"`CUP SLOT`\n{result1}{result2}{result3}\n`------->` <:Cupcoins:997159042633961574>{amount:,}\n`------->` <:Cupcoins:997159042633961574>{amount *reward:,}")
            userData['coins'] += reward
            await collection.replace_one({"_id" : interaction.user.id}, userData)
        
        userData['coins'] -= amount
        await collection.replace_one({"_id" : interaction.user.id}, userData)
        await interaction.edit_original_message(content = f"`CUP SLOT`\n{result1}{result2}{result3}\n`------->` <:Cupcoins:997159042633961574>{amount:,}\n`------->` Lost ;c")

    @slot.error
    async def slotError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",ephemeral=True)
        print(f"SlotErr: {error}")

    

async def setup(bot:commands.Bot):
    await bot.add_cog(Slot(bot))