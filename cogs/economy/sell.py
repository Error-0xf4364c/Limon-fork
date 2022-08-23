import discord
from discord import app_commands, Embed
from discord.ui import View, button
from discord.ext import commands
import datetime
import yaml
from yaml import Loader
from main import MyBot

# Fishes File
fish_file = open("yamls/fishing.yml", "rb")
fish = yaml.load(fish_file, Loader = Loader)

vlf = fish["veryLowLevelFish"]
lf = fish["lowLevelFish"]
mlf = fish["mediumLevelFish"]
hf = fish["highLevelFish"]
vhf = fish["veryHighLevelFish"]
priceByFishSize = fish["priceByFishSize"]
all_fish = vlf | lf | mlf | hf | vhf
listFishes = " ".join(all_fish.keys())
splittedFish = listFishes.split(" ")

# For DB Connection
client = MyBot()

# Buttons Class
class SellButtons(View):

    # Sell Fish Button
    @button(label="Sell Fishes", style=discord.ButtonStyle.success)
    async def sell_fishes_callback(self, interaction: discord.Interaction, button):
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"] # Get Fishes
        walletCollection = db["economy"] # Get User Money

        if await walletCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You need to create a wallet to receive the proceeds of your sales. `/wallet`", ephemeral = True)

        if await inventoryCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You don't have inventory", ephemeral=True)
        
        userInvData = await inventoryCollection.find_one({ "_id" : interaction.user.id }) # Inventory Data
        userWallet = await walletCollection.find_one({ "_id" : interaction.user.id }) # User Wallet Data
        
        """If user does not have fishes collection or does not have any fish, this will work!"""
        if not 'fishes' in userInvData or len(userInvData["fishes"]) == 0:
            button.label = "No Fish!" # New Button Label
            button.disabled = True # New Button Disabled
            button.style = discord.ButtonStyle.secondary # New Button Style
            await interaction.response.edit_message(view=self) # Updated Button
            await interaction.followup.send("You don't have any fish in your inventory. catch some fish! **`/fishing`**", ephemeral=True) # Send Message
            return 


        sum_fish = 0 # Default Fish Price

        userFishes = list(userInvData['fishes'].keys())
        for i in userInvData['fishes'].values(): # Wander in fish size
            """We multiply the length of each fish by the price quoted and overwrite the current value."""
            sum_fish += (i * priceByFishSize) 
        for x in listFishes: # We are navigating the values ​​in the all_fishes dictionary collected in the list.
            if x in userFishes: # We are navigating the user fishes
                sum_fish += all_fish[x] # Adds the values ​​(prices) of all fish in the database to the default value

        button.label = "Sold Fishes!" # New Button Label
        button.style = discord.ButtonStyle.secondary # New Button Stlye
        button.disabled = True # New Button Disabled

        del userInvData['fishes']
        userWallet['coins'] += sum_fish
        await walletCollection.replace_one({"_id": interaction.user.id}, userWallet)
        await inventoryCollection.replace_one({"_id": interaction.user.id}, userInvData)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content=f"🐟 **|** You have successfully sold the fish you caught. Your total winnings are **{sum_fish}** Cupcoin.")

# Main Class
class Sell(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sell", description="Sell Hunts")
    async def sell(self, interaction: discord.Interaction):
        view = SellButtons()
        await interaction.response.send_message("Text", view=view)

    @sell.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sell(bot), guilds= [discord.Object(id =964617424743858176)])