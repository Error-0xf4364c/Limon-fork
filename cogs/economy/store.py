import discord
from discord import Embed
from discord.ui import View, Button, Select
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
from main import MyBot
import yaml
from yaml import Loader


# ALL ITEMS FILE
items_file = open("yamls/items.yml", "rb")
items = yaml.load(items_file, Loader = Loader) 


# MINING ITEMS 
pickaxes = items["pickaxe"]

# Stone Pickaxe
stonePickaxe = pickaxes["stonepickaxe"]
stonePickaxeName = stonePickaxe["name"] # Pickaxe Name
stonePickaxePrice = stonePickaxe["price"] # Pickaxe Price

# Steel Pickaxe
steelPickaxe = pickaxes["steelpickaxe"]
steelPickaxeName = steelPickaxe["name"] # Pickaxe Name
steelPickaxePrice = steelPickaxe["price"] # Pickaxe Price

# Gold Pickaxe
goldenPickaxe = pickaxes["goldenpickaxe"]
goldenPickaxeName = goldenPickaxe["name"] # Pickaxe Name
goldenPickaxePrice = goldenPickaxe["price"] # Pickaxe Price

# Reinforced Pickaxe
reinforcedPickaxe = pickaxes["reinforcedpickaxe"]
reinforcedPickaxeName = reinforcedPickaxe["name"] # Pickaxe Name
reinforcedPickaxePrice = reinforcedPickaxe["price"] # Pickaxe Price

# Mining Vehicle
miningVehicle = pickaxes["miningvehicle"]
miningVehicleName = miningVehicle["name"] # Pickaxe Name
miningVehiclePrice = miningVehicle["price"] # Pickaxe Price


# FOR DB CONNECTION
client = MyBot()



class Pickaxes(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Stone Pickaxe', value= "stonepickaxe", description=f'Price: {stonePickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Steel Pickaxe', value= "steelpickaxe", description=f'Price: {steelPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Golden Pickaxe', value= "goldenpickaxe", description=f'Price: {goldenPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Reinforced Pickaxe', value= "reinforcedpickaxe", description=f'Price: {reinforcedPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Mining Vehicle', value= "miningvehicle", description=f'Price: {miningVehiclePrice:,}', emoji='⛏️')
        ]
        super().__init__(placeholder='Choose a Picaxe', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        pickaxeName = ""
        pickaxePrice = "0"
        pickaxeId = ""
        
        if self.values[0] == "stonepickaxe":
            pickaxeName = "Stone Pickaxe"
            pickaxePrice = stonePickaxePrice
            pickaxeId = "stonepickaxe"
        elif self.values[0] == "steelpickaxe":
            pickaxeName = "Steel Pickaxe"
            pickaxePrice = steelPickaxePrice
            pickaxeId = "steelpickaxe"
        elif self.values[0] == "goldenpickaxe":
            pickaxeName = "Golden Pickaxe"
            pickaxePrice = goldenPickaxePrice
            pickaxeId = "goldenpickaxe"
        elif self.values[0] == "reinforcedpickaxe":
            pickaxeName = "Reinforced Pickaxe"
            pickaxePrice = reinforcedPickaxePrice
            pickaxeId = "reinforcedpickaxe"
        elif self.values[0] == "miningvehicle":
            pickaxeName = "Mining Vehicle"
            pickaxePrice = miningVehiclePrice
            pickaxeId = "mininigvehicle"

        # Database Connection
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]
        coinCollection = db["economy"]

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < pickaxePrice:
            needMoney = userWallet["coins"] - pickaxePrice
            return await interaction.response.send_message(f"You don't have enough cupcoin in your wallet! You need {needMoney:,}", ephemeral = True)

        # Inventory Check
        elif await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await userInventory.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        # Pickaxe Check
        if "pickaxe" in userInventory["items"]:
            return await interaction.response.send_message("You already have a pickaxe", ephemeral = True)

        # Fee received
        userWallet["coins"] -= pickaxePrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"pickaxe" : pickaxeId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨⛏️ **|** You bought a new {pickaxeName} by paying {pickaxePrice}. Now you will be able to extract more valuable mines with this pickaxe")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Pickaxes())

    
        
    
    


# BASIC ITEMS CLASS
class Items(View):

    # THIS BUTTON PURPOSE IS SHOW ALL PICKAXE
    @discord.ui.button(label="Pickaxe", style=discord.ButtonStyle.primary, custom_id="showpickaxes")
    async def pickaxe_callback(self, interaction, button):
        
        view = DropdownView()

        await interaction.response.send_message(content= "Kazmalar", view = view)
  

# MAIN CLASS
class Store(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "storedemo", description = "Open store and buy items") # Commands
    @app_commands.checks.cooldown( 1, 1.0, key=lambda i: (i.guild_id, i.user.id)) # Cooldown
    async def store(self, interaction: discord.Interaction):
        
        view = Items()
        


        itemsEmbed = Embed(description = f"Hello 👋 Welcome to Store. You can buy items for mining, forestry, fishing, hunting. ")
        itemsEmbed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar.url)
        itemsEmbed.add_field(name = "How can i buy item?", value = "Click on the buttons and select the level of any item", inline = False)
        itemsEmbed.add_field(name = "Am I going to pay for this?", value = "Yes, you will pay different fees according to the level of each item", inline = False)

        await interaction.response.send_message(embed = itemsEmbed, view = view) 


    @store.error
    async def storeError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}`s and Try Again!",ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please inform the developer of this situation and try again later.")
            print(f"[STORE]: {error} ")

async def setup(bot: commands.Bot):
    await bot.add_cog(Store(bot), guilds= [discord.Object(id =964617424743858176)])

"""
# Database Connection
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]
        coinCollection = db["economy"]

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < stonePickaxePrice:
            return await interaction.response.send_message("You don't have enough cupcoin in your wallet", ephemeral = True)

        # Inventory Check
        elif await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await userInventory.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        # Pickaxe Check
        if "pickaxe" in userInventory["items"]:
            button.style = discord.ButtonStyle.secondary
            button.disabled = True
            await interaction.response.edit_message(view=self)
            return await interaction.followup.send("You already have a pickaxe", ephemeral = True)

        # Fee received
        userWallet["coins"] -= stonePickaxePrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"pickaxe" : "stonepickaxe"})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        button.label = "Purchased"
        button.style = discord.ButtonStyle.secondary
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("✨⛏️ **|** You bought a new stone pickaxe. Now you will be able to extract more valuable mines with this pickaxe")
"""