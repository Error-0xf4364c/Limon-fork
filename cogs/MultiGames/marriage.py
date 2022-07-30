import discord
from discord import Embed
from discord import app_commands
from discord import Button
from discord.ext import commands
from discord.ui import View
import datetime
from main import MyBot

client = MyBot()

message_author_id = []
message_author_id2 = []

ring = 500000

# MARRIED BUTTON
class MarriageButton(View):

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.id in message_author_id2:
            await interaction.response.send_message("You can't take any action..", ephemeral=True)
            return False
        return True


    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="accept")
    async def accept_callback(self, interaction, button):
        db = client.mongoConnect["cupcake"]
        collection = db["career"]
        invCollection = db["inventory"]
        coinCollection = db["economy"]

        # PROPOSED
        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "marriage": True,
                "wife": message_author_id
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})

        # Create New Data
        if "marriage" not in userData:
            marriageData = { "$set" : {"marriage": True, "wife": message_author_id}}
            await collection.update_one(userData ,marriageData)

        # New Data
        userData = await collection.find_one({"_id": interaction.user.id})
        userCoinData = await coinCollection.find_one({"_id": interaction.user.id})
        userCoinData["coins"] += 1000000
        await coinCollection.replace_one({"_id": interaction.user.id}, userCoinData)

        # BIDDER
        if await collection.find_one({"_id" : message_author_id}) == None:
            newData = {
                "_id": message_author_id,
                "marriage": True,
                "wife": interaction.user.id
            }
            await collection.insert_one(newData)

        userDataBidder = await collection.find_one({"_id": message_author_id})

        # Create New Data
        if "marriage" not in userDataBidder:
            marriageData = { "$set" : {"marriage": True, "wife": interaction.user.id}}
            await collection.update_one(userDataBidder ,marriageData)

        # New Data
        userDataBidder = await collection.find_one({"_id": message_author_id})
        userCoinDataBidder = await coinCollection.find_one({"_id": message_author_id})
        userInvData = await collection.find_one({"_id": message_author_id})


        await invCollection.delete_one({"_id": message_author_id}, userInvData["weddingring"])

        userCoinDataBidder["coins"] += 1000000
        await coinCollection.replace_one({"_id": message_author_id}, userCoinDataBidder)

        button.disabled = True
        button.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"🎉 **|** Congratulations! You married <@{message_author_id}>. We are giving you **2,000,000** Cupcoins as a small wedding gift.")
        message_author_id.clear()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.success, custom_id="decline")
    async def decline_callback(self, interaction, button):
        button.disabled = True
        button.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("You turned down the marriage proposal.")





# BUY WEDDING RING
class RingButtons(View):

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.id in message_author_id:
            await interaction.response.send_message("You can't take any action..", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Buy Wedding Ring", style=discord.ButtonStyle.success, custom_id="buyring")
    async def buyring_callback(self, interaction, button):
        db = client.mongoConnect["cupcake"]
        collection = db["career"]
        invCollection = db["inventory"]
        coinCollection = db["economy"]

        userData = await collection.find_one({"_id": interaction.user.id})
        userCoinData = await coinCollection.find_one({"_id": interaction.user.id})
        userInvData = await invCollection.find_one({"_id": interaction.user.id})


        if userCoinData["coins"] < ring:
            return await interaction.response.send_message("You don't have enough balance", ephemeral = True)

        # DB Check
        if "weddingring" not in userInvData:
            ringData = { "$set" : {"weddingring": True}}
            await collection.update_one(userInvData ,ringData)
        
        else:
            return await interaction.response.send_message("You already have a wedding ring", ephemeral = True)

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "marriage": False,
                "wife": None
            }
            await collection.insert_one(newData)

        userData = await collection.find_one({"_id": interaction.user.id})

        # Create New Data
        if "marriage" not in userData:
            marriageData = { "$set" : {"marriage": False, "wife": None}}
            await collection.update_one(userData ,marriageData)

        # New Data
        userData = await collection.find_one({"_id": interaction.user.id})

        userCoinData["coins"] -= ring
        await coinCollection.replace_one({"_id": interaction.user.id}, userCoinData)

        view2 = MarriageButton()

        button.disabled = True
        button.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"You have received a wedding ring worth {ring:,} Cupcoins with your credit card", view=view2)


# MAIN MESSAGE
class Marriage(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @app_commands.commands(
        name = "Marriage",
        description = "Hey sevdiğin biriyle ilişkini ilerletmek mi istiyorsun?"
    )
    @app_commands.checks.cooldown( 1, 10, key = lambda i: (i.guild.id, i.user.id))
    async def marriage(self, interaction: discord.Interaction, wife: discord.User):
        
        view = RingButtons()

        # Check user
        if wife.bot == True:
            return await interaction.response.send_message("🤖 **|** You can't marry a bot", ephemeral=True)


        # Connect DB
        db = self.bot.mongoConnect["cupcake"]
        collection = db["career"]
        coinCollection = db["economy"]

        userData = await collection.find_one({"_id": interaction.user.id})

        # Are you sure?
        sure = Embed(
            title = "Are you Sure?",
            description = f"To marry someone, you must first buy a wedding ring. To buy a wedding ring, you need to pay **{ring:,}** Cupcoins. After receiving the wedding ring, you can propose marriage. If your offer is rejected, you keep the wedding ring.\n If you are sure that you want to get married, you can buy a wedding ring by clicking on the bot below."
        )
        sure.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1003068837413007410/1003068931050848386/weddingring.png")

        await interaction.response.send_message(embed = sure, view = view)
        message_author_id.append(interaction.user.id)
        message_author_id2.append(wife.id)
        
async def setup(bot:commands.Bot):
    await bot.add_cog(Marriage(bot))  