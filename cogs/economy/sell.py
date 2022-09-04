import discord
from discord import app_commands, Embed
from discord.ui import View, button
from discord.ext import commands
import datetime
import asyncio
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
all_fish = vlf | lf | mlf | hf | vhf # We combine all the fish in one dictionary
fishesKey = " ".join(all_fish.keys()) # We get all the dictionary keys
listFishes = fishesKey.split(" ") # We collect all the dictionary keys in the list

# Hunts File
hunt_file = open("yamls/hunt.yml", "rb")
hunt = yaml.load(hunt_file, Loader = Loader)

vlh = hunt["veryLowLevelHunt"]
lh = hunt["lowLevelHunt"]
mlh = hunt["mediumLevelHunt"]
hh = hunt["highLevelHunt"]
vhh = hunt["veryHighLevelHunt"]
all_hunt = vlh | lh | mlh | hh | vhh # We combine all the hunt in one dictionary
huntsKey = " ".join(all_hunt.keys()) # We get all the dictionary keys
listHunts = huntsKey.split(" ") # We collect all the dictionary keys in the list

# Mines File
mine_file = open("yamls/mines.yml", "rb")
mine = yaml.load(mine_file, Loader = Loader)

vlm = mine["veryLowLevelMine"]
lm = mine["lowLevelMine"]
mlm = mine["mediumLevelMine"]
hm = mine["highLevelMine"]
vhm = mine["veryHighLevelMine"]
priceByMineKg = mine["priceByMineKg"] 
all_mine = vlm | lm | mlm | hm | vhm # We combine all the mine in one dictionary
minesKey = " ".join(all_mine.keys()) # We get all the dictionary keys
listMines = minesKey.split(" ") # We collect all the dictionary keys in the list

# Wood File
wood_file = open("yamls/wood.yml", "rb")
wood = yaml.load(wood_file, Loader = Loader)

vlw = wood["veryLowLevelWood"]
lw = wood["lowLevelWood"]
mlw = wood["mediumLevelWood"]
hw = wood["highLevelWood"]
vhw = wood["veryHighLevelWood"]
priceByWoodSize = wood["priceByWoodSize"] 
all_wood = vlw | lw | mlw | hw | vhw # We combine all the wood in one dictionary
woodKey = " ".join(all_wood.keys()) # We get all the dictionary keys
listWood = woodKey.split(" ") # We collect all the dictionary keys in the list


message_author_id = []

# For DB Connection
client = MyBot()

# Buttons Class
class SellButtons(View):
    
    # Interaction User Check
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        if not interaction.user.id in message_author_id:
            await interaction.response.send_message("This shop doesn't belong to you. You can't trade in someone else's store. Please use the /sell command.", ephemeral=True)
            return False
        return True
    
    # Sell Fish Button
    @button(label="Sell Fishes", style=discord.ButtonStyle.success, emoji = "🐟")
    async def sell_fishes_callback(self, interaction: discord.Interaction, button):
        
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"] # Get User Inventory Data
        walletCollection = db["economy"] # Get User Money

        # Making wallet inquiry
        if await walletCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You need to create a wallet to receive the proceeds of your sales. `/wallet`", ephemeral = True)
        
        # Making inventory inquiry
        if await inventoryCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You don't have inventory", ephemeral=True)
        
        # User Data
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
            print(i)
            """We multiply the length of each fish by the price quoted and overwrite the current value."""
            sum_fish += (i * priceByFishSize) 
        for x in listFishes: # We are navigating the values ​​in the all_fishes dictionary collected in the list.
            if x in userFishes: # We are navigating the user fishes
                sum_fish += int(all_fish[x]["price"]) # Adds the values ​​(prices) of all fish in the database to the default value

        button.label = "Sold Fishes!" # New Button Label
        button.style = discord.ButtonStyle.secondary # New Button Stlye
        button.disabled = True # New Button Disabled

        del userInvData['fishes']
        userWallet['coins'] += sum_fish
        await walletCollection.replace_one({"_id": interaction.user.id}, userWallet)
        await inventoryCollection.replace_one({"_id": interaction.user.id}, userInvData)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content=f"🐟 **| {interaction.user.name} **You have successfully sold the fish you caught. Your total winnings are **{sum_fish}** Cupcoin.")
        
    # Sell Hunt Button
    @button(label="Sell Hunts", style=discord.ButtonStyle.success, emoji = "🦌")
    async def sell_hunts_callback(self, interaction: discord.Interaction, button):
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"] # Get User Inventory Data
        walletCollection = db["economy"] # Get User Money

        # Making wallet inquiry
        if await walletCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You need to create a wallet to receive the proceeds of your sales. `/wallet`", ephemeral = True)
        
        # Making inventory inquiry
        if await inventoryCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You don't have inventory", ephemeral=True)
        
        # User Data
        userInvData = await inventoryCollection.find_one({ "_id" : interaction.user.id }) # Inventory Data
        userWallet = await walletCollection.find_one({ "_id" : interaction.user.id }) # User Wallet Data

        """If user does not have hunts collection or does not have any hunt, this will work!"""
        if not 'hunts' in userInvData or len(userInvData["hunts"]) == 0:
            button.label = "No Hunt!" # New Button Label
            button.disabled = True # New Button Disabled
            button.style = discord.ButtonStyle.secondary # New Button Style
            await interaction.response.edit_message(view=self) # Updated Button
            await interaction.followup.send("You don't have any hunt in your inventory. Hunt a little! **`/hunting`**", ephemeral=True) # Send Message
            return 


        sum_hunt = 0 # Default Hunt Price
        userHunts = userInvData['hunts']
        for x in listHunts:
            if x in userHunts:
                sum_hunt += int(all_hunt[x]["price"])
        

        button.label = "Sold Hunts!" # New Button Label
        button.style = discord.ButtonStyle.secondary # New Button Stlye
        button.disabled = True # New Button Disabled

        del userInvData['hunts']
        userWallet['coins'] += sum_hunt
        await walletCollection.replace_one({"_id": interaction.user.id}, userWallet)
        await inventoryCollection.replace_one({"_id": interaction.user.id}, userInvData)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content=f"🦌 **| {interaction.user.name}** You have successfully sold the prey you have hunted. Your total winnings are **{sum_hunt}** Cupcoin.")
    
    # Sell Mine Button
    @button(label="Sell Mines", style=discord.ButtonStyle.success, emoji = "💎")
    async def sell_mines_callback(self, interaction: discord.Interaction, button):
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"] # Get User Inventory Data
        walletCollection = db["economy"] # Get User Money

        # Making wallet inquiry
        if await walletCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You need to create a wallet to receive the proceeds of your sales. `/wallet`", ephemeral = True)
        
        # Making inventory inquiry
        if await inventoryCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You don't have inventory", ephemeral=True)
        
        # User Data
        userInvData = await inventoryCollection.find_one({ "_id" : interaction.user.id }) # Inventory Data
        userWallet = await walletCollection.find_one({ "_id" : interaction.user.id }) # User Wallet Data

        """If user does not have mines collection or does not have any hunt, this will work!"""
        if not 'mines' in userInvData or len(userInvData["mines"]) == 0:
            button.label = "No Mine!" # New Button Label
            button.disabled = True # New Button Disabled
            button.style = discord.ButtonStyle.secondary # New Button Style
            await interaction.response.edit_message(view=self) # Updated Button
            await interaction.followup.send("You don't have any mine in your inventory. Let's start digging! **`/mining`**", ephemeral=True) # Send Message
            return 


        sum_mine = 0 # Default Mine Price
        userMines = list(userInvData['mines'].keys())
        for i in userInvData['mines'].values(): # Wander in mine kg
            """We multiply the length of each mine by the price quoted and overwrite the current value."""
            sum_mine += (i * priceByMineKg) 
        for x in listMines: # We are navigating the values ​​in the all_mine dictionary collected in the list.
            if x in userMines: # We are navigating the user mines
                sum_mine += int(all_mine[x]["price"]) # Adds the values ​​(prices) of all mines in the database to the default value
        
        

        button.label = "Sold Mines!" # New Button Label
        button.style = discord.ButtonStyle.secondary # New Button Stlye
        button.disabled = True # New Button Disabled

        del userInvData['mines']
        userWallet['coins'] += sum_mine
        await walletCollection.replace_one({"_id": interaction.user.id}, userWallet)
        await inventoryCollection.replace_one({"_id": interaction.user.id}, userInvData)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content=f"💎 **| {interaction.user.name}** You have successfully sold your mines. Your total winnings are **{sum_mine}** Cupcoin.")

    # Sell Wood Button
    @button(label="Sell Wood", style=discord.ButtonStyle.success, emoji = "🌲")
    async def sell_wood_callback(self, interaction: discord.Interaction, button):
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"] # Get User Inventory Data
        walletCollection = db["economy"] # Get User Money

        # Making wallet inquiry
        if await walletCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You need to create a wallet to receive the proceeds of your sales. `/wallet`", ephemeral = True)
        
        # Making inventory inquiry
        if await inventoryCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You don't have inventory", ephemeral=True)
        
        # User Data
        userInvData = await inventoryCollection.find_one({ "_id" : interaction.user.id }) # Inventory Data
        userWallet = await walletCollection.find_one({ "_id" : interaction.user.id }) # User Wallet Data

        """If user does not have wood collection or does not have any hunt, this will work!"""
        if not 'wood' in userInvData or len(userInvData["wood"]) == 0:
            button.label = "No Wood!" # New Button Label
            button.disabled = True # New Button Disabled
            button.style = discord.ButtonStyle.secondary # New Button Style
            await interaction.response.edit_message(view=self) # Updated Button
            await interaction.followup.send("You don't have any wood in your inventory. Grab your axe and dive into the forest! **`/forestry`**", ephemeral=True) # Send Message
            return 


        sum_wood = 0 # Default Wood Price
        userWood = list(userInvData['wood'].keys())
        for i in userInvData['wood'].values(): # Wander in wood size
            """We multiply the length of each wood by the price quoted and overwrite the current value."""
            sum_wood += (i * priceByWoodSize) 
        for x in listWood: # We are navigating the values ​​in the all wood dictionary collected in the list.
            if x in userWood: # We are navigating the user wood
                sum_wood += int(all_wood[x]["price"]) # Adds the values ​​(prices) of all wood in the database to the default value
        
        

        button.label = "Sold Wood!" # New Button Label
        button.style = discord.ButtonStyle.secondary # New Button Stlye
        button.disabled = True # New Button Disabled

        del userInvData['wood']
        userWallet['coins'] += sum_wood
        await walletCollection.replace_one({"_id": interaction.user.id}, userWallet)
        await inventoryCollection.replace_one({"_id": interaction.user.id}, userInvData)
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content=f"🌲 **| {interaction.user.name}** You have successfully sold your wood. Your total winnings are **{sum_wood}** Cupcoin.")

    # Close Button
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def closemenu_callback(self, interaction, button):
        await interaction.response.send_message(content=f"Closing...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.edit_original_response(content=f"✅ **|** Shop is succesfully closed.")
        await interaction.message.delete()
        message_author_id.remove(interaction.user.id)

# Main Class
class Sell(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Sell Comands
    @app_commands.command(name="sell", description="Sell Hunts")
    @app_commands.guild_only
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
    async def sell(self, interaction: discord.Interaction):

        # Database Connection:
        db = self.bot.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]

        view = SellButtons() # Buttons

        # Making inventory inquiry
        if await inventoryCollection.find_one({ "_id" : interaction.user.id }) == None:
            return await interaction.response.send_message("You don't have inventory", ephemeral=True)
        
        userData = await inventoryCollection.find_one({ "_id" : interaction.user.id })
        message_author_id.append(interaction.user.id) # We add the id of the message owner to the list

        sum_fish = 0
        number_fish = 0
        embed_value_fishes = "No fish found in your inventory."

        sum_hunt = 0
        number_hunt = 0
        embed_value_hunts = "No hunt found in your inventory."

        sum_mine = 0
        number_mine = 0
        embed_value_mines = "No mine found in your inventory."

        sum_wood = 0
        number_wood = 0
        embed_value_wood = "No wood found in your inventory"

        

        if 'fishes' in userData and len(userData['fishes']) > 0:
            userFishes = list(userData['fishes'].keys())
            for i in userData['fishes'].values():

                sum_fish += (i*priceByFishSize)
            for x in listFishes:
                if x in userFishes:

                    sum_fish += int(all_fish[x]["price"])
            number_fish = len(userData['fishes'])
            embed_value_fishes = f"You have **{number_fish}** fish. Total = **{sum_fish}** Cupcoin."

        if "mines" in userData and len(userData['mines']) > 0:
            userMines = list(userData['mines'].keys())
            for i in userData['mines'].values():
                sum_mine += (i*priceByMineKg)
            for x in listMines:
                if x in userMines:
                    sum_mine += all_mine[x]["price"]
            number_mine = len(userData['mines'])
            embed_value_mines = f"You have **{number_mine}** mine. Total = **{sum_mine}** Cupcoin."

        if 'hunts' in userData and len(userData['hunts']) > 0:
            userHunts = userData['hunts']
            for x in listHunts:
                if x in userHunts:
                    sum_hunt += all_hunt[x]["price"]
            number_hunt = len(userData['hunts'])
            embed_value_hunts = f"You have **{number_hunt}** hunt. Total = **{sum_hunt}** Cupcoin."

        if "wood" in userData and len(userData['wood']) > 0:
            userWood = list(userData['wood'].keys())
            for i in userData['wood'].values():
                sum_wood += (i*priceByWoodSize)
            for x in listWood:
                if x in userWood:
                    sum_wood += all_wood[x]["price"]
            number_wood = len(userData['wood'])
            embed_value_wood = f"You have **{number_wood}** wood. Total = **{sum_wood}** Cupcoin."

        
        if interaction.user.id in message_author_id:
            message_author_id.remove(interaction.user.id)
            #return await interaction.response.send_message("You already have a shop opened. Turn it off first", ephemeral=True)
        message_author_id.append(interaction.user.id)

        menuEmbed = Embed(description = f"Hello, welcome to the store. Here you can sell mines, hunts, fishes and wood. Here is your inventory:")
        menuEmbed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar.url)
        menuEmbed.add_field(name = "Fishes:", value =  embed_value_fishes, inline = True)
        menuEmbed.add_field(name = "Hunts:", value =  embed_value_hunts, inline = True)
        menuEmbed.add_field(name = "Mines:", value =  embed_value_mines, inline = True)
        menuEmbed.add_field(name = "Wood:", value =  embed_value_wood, inline = True)
        menuEmbed.set_footer(text = "Don't forget to close the shop. You can't open a new store without closing it!", icon_url= "https://cdn.discordapp.com/attachments/970118423143120896/1000526619691200522/dikkat.png")

        await interaction.response.send_message(embed = menuEmbed, view=view)


    # ERROR HANDLER
    @sell.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Upss! The shop hasn't opened yet. Please try again after {timeRemaining}s.",ephemeral=True)
        else:
            if len(message_author_id) >0:
                message_author_id.clear()
            print(f"[SELL]: {error}")


# Register Command
async def setup(bot: commands.Bot):
    await bot.add_cog(Sell(bot))