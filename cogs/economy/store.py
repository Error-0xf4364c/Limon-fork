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



# FISHING ITEMS
rods = items["fishingrod"]

# Simple Rod
simpleRod = rods["simplerod"]
simpleRodName = simpleRod["name"] # Rod Name
simpleRodPrice = simpleRod["price"] # Rod Price

# Solid Rod
solidRod = rods["solidrod"]
solidRodName = solidRod["name"] # Rod Name
solidRodPrice = solidRod["price"] # Rod Price

# Silver Rod
silverRod = rods["silverrod"]
silverRodName = silverRod["name"] # Rod Name
silverRodPrice = silverRod["price"] # Rod Price

# Lucky Rod
luckyRod = rods["luckyrod"]
luckyRodName = luckyRod["name"] # Rod Name
luckyRodPrice = luckyRod["price"] # Rod Price

# Harpoon
harpoon = rods["harpoon"]
harpoonName = harpoon["name"] # Harpoon Name
harpoonPrice = harpoon["price"] # Harpoon Price


# HUNTING ITEMS

bows = items["bow"]

# Wooden Bow
woodenBow = bows["woodenbow"]
woodenBowName = woodenBow["name"] # Wooden Bow Name
woodenBowPrice = woodenBow["price"] # Wooden Bow Price

# Copper Bow
copperBow = bows["copperbow"]
copperBowName = copperBow["name"] # Copper Bow Name
copperBowPrice = copperBow["price"] # Copper Bow Price

# Silver Bow
silverBow = bows["silverbow"]
silverBowName = silverBow["name"] # Silver Bow Name
silverBowPrice = silverBow["price"] # Silver Bow Price

# Accurate Bow
accurateBow = bows["accuratebow"]
accurateBowName = accurateBow["name"] # Accurate Bow Name
accurateBowPrice = accurateBow["price"] # Accurate Bow Price

# Crossbow
crossbow = bows["crossbow"]
crossbowName = crossbow["name"] # Crossbow Name
crossbowPrice = crossbow["price"] # Crossbow Price

# FORESTRY ITEMS
axes = items["axe"]

# Stone Axe
stoneAxe = axes["stoneaxe"]
stoneAxeName = stoneAxe["name"] # Stone Axe Name
stoneAxePrice = stoneAxe["price"] # Stone Axe Price

# Steel Axe
steelAxe = axes["steelaxe"]
steelAxeName = steelAxe["name"] # Steel Axe Name
steelAxePrice = steelAxe["price"] # Steel Axe Price

# Golden Axe
goldenAxe = axes["goldenaxe"]
goldenAxeName = goldenAxe["name"] # Golden Axe Name
goldenAxePrice = goldenAxe["price"] # Golden Axe Price

# Reinforced Axe
reinforcedAxe = axes["reinforcedaxe"]
reinforcedAxeName = reinforcedAxe["name"] # Reinforced Axe Name
reinforcedAxePrice = reinforcedAxe["price"] # Reinforced Axe Price

# Enchanted Axe
enchantedAxe = axes["enchantedaxe"]
enchantedAxeName = enchantedAxe["name"] # Enchanted Axe Name
enchantedAxePrice = enchantedAxe["price"] # Enchanted Axe Price

# SWORDS
swords = items["sword"]

# 
gladius = swords["gladius"]
gladiusName = gladius["name"]
gladiusPrice = gladius["price"] 
gladiusDcPrice = gladius["discounted_price"]

# 
chukuto = swords["chokuto"]
chukutoName = chukuto["name"]
chukutoPrice = chukuto["price"] 
chukutoDcPrice = chukuto["discounted_price"]

# 
katana = swords["katana"]
katanaName = katana["name"]
katanaPrice = katana["price"] 
katanaDcPrice = katana["discounted_price"]

# 
rapier = swords["rapier"]
rapierName = rapier["name"]
rapierPrice = rapier["price"] 
rapierDcPrice = rapier["discounted_price"]

# 
odachi = swords["odachi"]
odachiName = odachi["name"]
odachiPrice = odachi["price"] 
odachiDcPrice = odachi["discounted_price"]

# 
claymore = swords["claymore"]
claymoreName = claymore["name"]
claymorePrice = claymore["price"] 
claymoreDcPrice = claymore["discounted_price"]



# FOR DB CONNECTION
client = MyBot()



class Pickaxes(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Stone Pickaxe', value= "stonepickaxe", description=f'Price: {stonePickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Steel Pickaxe', value= "steelpickaxe", description=f'Price: {steelPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Golden Pickaxe', value= "goldenpickaxe", description=f'Price: {goldenPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Reinforced Pickaxe', value= "reinforcedpickaxe", description=f'Price: {reinforcedPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Mining Vehicle', value= "miningvehicle", description=f'Price: {miningVehiclePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Sell Pickaxe', value= "sellpickaxe", description=f'Sell to buy new pickaxe', emoji='🗑️')
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
        
        # Inventory Check
        if await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newUserData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newUserData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellpickaxe":
            if "items" not in userInventory or "pickaxe" in userInventory["items"]:
                
                userInventory["items"].pop("pickaxe")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message(content = "You have successfully sold the pickaxe")
            else:
                return await interaction.response.send_message(content = "You don't have a pickaxe")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message(content = "You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < pickaxePrice:
            needMoney = userWallet["coins"] - pickaxePrice
            return await interaction.response.send_message(content = f"You don't have enough cupcoin in your wallet! You need {needMoney:,}", ephemeral = True)

        

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

        await interaction.response.send_message(f"✨⛏️ **|** You bought a new {pickaxeName} by paying {pickaxePrice:,}. Now you will be able to extract more valuable mines with this pickaxe")

class Swords(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Gladius Sword', value= "gladius", description=f'Price: not {gladiusPrice:,}, but {gladiusDcPrice:,}', emoji='⚔️'),
            discord.SelectOption(label='Chukuto Sword', value= "chokuto", description=f'Price: not {chukutoPrice:,}, but {chukutoDcPrice:,}', emoji='⚔️'),
            discord.SelectOption(label='Katana Sword', value= "katana", description=f'Price: not {katanaPrice:,}, but {katanaDcPrice:,}', emoji='⚔️'),
            discord.SelectOption(label='Rapier Sword', value= "rapier", description=f'Price: not {rapierPrice:,}, but {rapierDcPrice:,}', emoji='⚔️'),
            discord.SelectOption(label='Odachi Sword', value= "odachi", description=f'Price: not {odachiPrice:,}, but {odachiDcPrice:,}', emoji='⚔️'),
            discord.SelectOption(label='Claymore Sword', value= "claymore", description=f'Price: not {claymorePrice:,}, but {claymoreDcPrice:,}', emoji='⚔️'),

            discord.SelectOption(label='Sell Sword', value= "sellsword", description=f'Sell to buy new sword', emoji='🗑️')

        ]
        super().__init__(placeholder='Choose a Sword', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        swordName = ""
        swordPrice = "0"
        swordId = ""
        
        if self.values[0] == "gladius":
            swordName = "Gladius Sword"
            swordPrice = gladiusDcPrice
            swordId = "gladius"
        elif self.values[0] == "chokuto":
            swordName = "Chukuto Sword"
            swordPrice = chukutoDcPrice
            swordId = "chokuto"
        elif self.values[0] == "katana":
            swordName = "Katana Sword"
            swordPrice = katanaDcPrice
            swordId = "katana"
        elif self.values[0] == "rapier":
            swordName = "Rapier Sword"
            swordPrice = rapierDcPrice
            swordId = "rapier"
        elif self.values[0] == "odachi":
            swordName = "Odachi Sword"
            swordPrice = odachiDcPrice
            swordId = "odachi"
        elif self.values[0] == "claymore":
            swordName = "Claymore Sword"
            swordPrice = claymoreDcPrice
            swordId = "claymore"

        # Database Connection
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]
        coinCollection = db["economy"]
        
        # Inventory Check
        if await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellsword":
            if "items" not in userInventory or "sword" in userInventory["items"]:
                
                userInventory["items"].pop("sword")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("You have successfully sold the sword")
            else:
                return await interaction.response.send_message("You don't have a sword")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < swordPrice:
            needMoney = userWallet["coins"] - swordPrice
            return await interaction.response.send_message(f"You don't have enough cupcoin in your wallet! You need {needMoney:,}", ephemeral = True)

        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await userInventory.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        # Pickaxe Check
        if "sword" in userInventory["items"]:
            return await interaction.response.send_message("You already have a sword", ephemeral = True)

        # Fee received
        userWallet["coins"] -= swordPrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"sword" : swordId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨⚔️ **|** You bought a new {swordName} by paying {swordPrice:,}. It's very smart to buy a sword already! It will do a lot of work in the future.")

class Rods(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Simple Rod', value= "simplerod", description=f'Price: {simpleRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Solid Rod', value= "solidrod", description=f'Price: {solidRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Silver Rod', value= "silverrod", description=f'Price: {silverRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Lucky Rod', value= "luckyrod", description=f'Price: {luckyRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Harpoon', value= "harpoon", description=f'Price: {harpoonPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Sell Rod', value= "sellrod", description=f"Sell to buy new fishing rod", emoji='🗑️')

        ]
        super().__init__(placeholder='Choose a Rod', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        rodName = ""
        rodPrice = 0
        rodId = ""
        
        if self.values[0] == "simplerod":
            rodName = "Simple Rod"
            rodPrice = simpleRodPrice
            rodId = "simplerod"
        
        elif self.values[0] == "solidrod":
            rodName = "Solid Rod"
            rodPrice = solidRodPrice
            rodId = "solidrod"
        
        elif self.values[0] == "silverrod":
            rodName = "Silver Rod"
            rodPrice = silverRodPrice
            rodId = "silverrod"
        
        elif self.values[0] == "luckyrod":
            rodName = "Lucky Rod"
            rodPrice = luckyRodPrice
            rodId = "luckyrod"
        
        elif self.values[0] == "harpoon":
            rodName = "Harpoon"
            rodPrice = harpoonPrice
            rodId = "harpoon"


        # Database Connection
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]
        coinCollection = db["economy"]
        
        # Inventory Check
        if await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellrod":
            if "items" not in userInventory or "rod" in userInventory["items"]:
                userInventory["items"].pop("rod")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("You have successfully sold the rod")
                return
            else:
                return await interaction.response.send_message("You don't have a rod")
        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < rodPrice:
            needMoney = userWallet["coins"] - rodPrice
            return await interaction.response.send_message(f"You don't have enough cupcoin in your wallet! You need {needMoney:,}", ephemeral = True)


        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await userInventory.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        # Pickaxe Check
        if "rod" in userInventory["items"]:
            return await interaction.response.send_message("You already have a rod", ephemeral = True)

        # Fee received
        userWallet["coins"] -= rodPrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"rod" : rodId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨🎣 **|** You bought a new {rodName} by paying {rodPrice:,}. Now you will be able to catch more valuable fish with this fishing rod")

class Bows(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Wooden Bow', value= "woodenbow", description=f'Price: {woodenBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Copper Bow', value= "copperbow", description=f'Price: {copperBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Silver Bow', value= "silverbow", description=f'Price: {silverBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Accurate Bow', value= "accuratebow", description=f'Price: {accurateBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Crossbow', value= "crossbow", description=f'Price: {crossbowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Sell Bow', value= "sellbow", description=f"Sell to buy new bow and arrow", emoji='🗑️')

        ]
        super().__init__(placeholder='Choose a Bow', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        bowName = ""
        bowPrice = 0
        bowId = ""
        
        if self.values[0] == "woodenbow":
            bowName = "Wooden Bow"
            bowPrice = woodenBowPrice
            bowId = "woodenbow"
        
        elif self.values[0] == "copperbow":
            bowName = "Copper Bow"
            bowPrice = copperBowPrice
            bowId = "copperbow"
        
        elif self.values[0] == "silverbow":
            bowName = "Silver Bow"
            bowPrice = silverBowPrice
            bowId = "silverbow"
        
        elif self.values[0] == "accuratebow":
            bowName = "Accurate Bow"
            bowPrice = accurateBowPrice
            bowId = "accuratebow"
        
        elif self.values[0] == "crossbow":
            bowName = "Crossbow"
            bowPrice = crossbowPrice
            bowId = "crossbow"


        # Database Connection
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]
        coinCollection = db["economy"]
        
        # Inventory Check
        if await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellbow":
            
            if "items" not in userInventory or "bow" in userInventory["items"]:
                
                userInventory["items"].pop("bow")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("You have successfully sold the bow")
                return
            else:
                return await interaction.response.send_message("You don't have a bow")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < bowPrice:
            needMoney = userWallet["coins"] - bowPrice
            return await interaction.response.send_message(f"You don't have enough cupcoin in your wallet! You need {needMoney:,}", ephemeral = True)

        
        
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await userInventory.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        # Pickaxe Check
        if "bow" in userInventory["items"]:
            return await interaction.response.send_message("You already have a bow", ephemeral = True)

        # Fee received
        userWallet["coins"] -= bowPrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        

        userInventory["items"].update({"bow" : bowId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨🏹 **|** You bought a new {bowName} by paying {bowPrice:,}. Now you will be able to hunt more valuable prey with this bow")

class Axes(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Stone Axe', value= "stoneaxe", description=f'Price: {stoneAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Steel Axe', value= "steelaxe", description=f'Price: {steelAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Golden Axe', value= "goldenaxe", description=f'Price: {goldenAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Reinforced Axe', value= "reinforcedaxe", description=f'Price: {reinforcedAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Enchanted Axe', value= "enchantedaxe", description=f'Price: {enchantedAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Sell Axe', value= "sellaxe", description=f"Sell to buy new axe", emoji='🗑️')

        ]
        super().__init__(placeholder='Choose a Axe', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        axeName = ""
        axePrice = "0"
        axeId = ""
        
        if self.values[0] == "stoneaxe":
            axeName = "Stone Axe"
            axePrice = stoneAxePrice
            axeId = "stoneaxe"
        
        elif self.values[0] == "steelaxe":
            axeName = "Steel Axe"
            axePrice = steelAxePrice
            axeId = "steelaxe"
        
        elif self.values[0] == "goldenaxe":
            axeName = "Golden Axe"
            axePrice = goldenAxePrice
            axeId = "goldenaxe"
        
        elif self.values[0] == "reinforcedaxe":
            axeName = "Reinforced Axe"
            axePrice = reinforcedAxePrice
            axeId = "reinforcedaxe"
        
        elif self.values[0] == "enchantedaxe":
            axeName = "Enchanted Axe"
            axePrice = enchantedAxePrice
            axeId = "enchantedaxe"


        # Database Connection
        db = client.mongoConnect["cupcake"]
        inventoryCollection = db["inventory"]
        coinCollection = db["economy"]
        
        # Inventory Check
        if await inventoryCollection.find_one({"_id" : interaction.user.id}) == None:
            newData = {
                "_id": interaction.user.id,
                "items" : {}
            }
            await inventoryCollection.insert_one(newData)

        # User Inventory (old)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellaxe":
            if "items" not in userInventory or "axe" in userInventory["items"]:
                
                userInventory["items"].pop("axe")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("You have successfully sold the axe")
                return
            else:
                return await interaction.response.send_message("You don't have a axe")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have a wallet! Get a wallet with using the `/wallet` command", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < axePrice:
            needMoney = userWallet["coins"] - axePrice
            return await interaction.response.send_message(f"You don't have enough cupcoin in your wallet! You need {needMoney:,}", ephemeral = True)

        
        
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await userInventory.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        # Pickaxe Check
        if "axe" in userInventory["items"]:
            return await interaction.response.send_message("You already have a axe", ephemeral = True)

        # Fee received
        userWallet["coins"] -= axePrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"axe" : axeId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨🪓 **|** You bought a new {axeName} by paying {axePrice:,}. Now you will be able to cut down larger trees with this axe")

class PickaxeView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Pickaxes())
        
class SwordView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
        self.add_item(Swords())

class RodView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Rods())

class BowView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Bows())

class AxeView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Axes())
        

    


# BASIC ITEMS CLASS
class ItemsView(View):

    # THIS BUTTON PURPOSE IS SHOW ALL PICKAXES
    @discord.ui.button(label="Pickaxes", style=discord.ButtonStyle.primary, custom_id="showpickaxes")
    async def pickaxe_callback(self, interaction, button):
        
        view = PickaxeView()

        await interaction.response.send_message(content= "Are you going to buy a new pickaxe? This is great! Prices are indicated below the pickaxes", view = view)
    
    # THIS BUTTON PURPOSE IS SHOW ALL RODS
    @discord.ui.button(label="Fishing Rods", style=discord.ButtonStyle.primary, custom_id="showrods")
    async def rods_callback(self, interaction, button):
        view = RodView()
        await interaction.response.send_message(content= "Are you going to buy a new fishing rod? This is great! Prices are indicated below the fishing rods", view = view)

    # THIS BUTTON PURPOSE IS SHOW ALL BOWS
    @discord.ui.button(label="Bows", style=discord.ButtonStyle.primary, custom_id="showbows")
    async def bows_callback(self, interaction, button):
        view = BowView()
        await interaction.response.send_message(content= "Are you going to buy a new bow? This is great! Prices are indicated below the bows", view = view)
    

    # THIS BUTTON PURPOSE IS SHOW ALL AXES
    @discord.ui.button(label="Axes", style=discord.ButtonStyle.primary, custom_id="showaxes")
    async def axes_callback(self, interaction, button):
        view = AxeView()
        await interaction.response.send_message(content= "Are you going to buy a new axe? This is great! Prices are indicated below the axes", view = view)

     # THIS BUTTON PURPOSE IS SHOW ALL SWORDS
    @discord.ui.button(label="Swords", style=discord.ButtonStyle.success, custom_id="showswords")
    async def sword_callback(self, interaction, button):
        view = SwordView()
        await interaction.response.send_message(content= "Are you going to buy a new sword? This is great! Prices are indicated below the swords", view = view)


    # THIS BUTTON PURPOSE IS CLOSE THE MENU
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="closemenu")
    async def close_callback(self, interaction, button):
        await interaction.message.delete()
        await interaction.response.send_message(content=f"The store was successfully closed.", ephemeral = True)
    

# MAIN CLASS
class Store(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "store", description = "Open store and buy items") # Commands
    @app_commands.guild_only
    @app_commands.checks.cooldown( 1, 20, key=lambda i: (i.guild_id, i.user.id)) # Cooldown
    async def store(self, interaction: discord.Interaction):
        
        view = ItemsView()

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
            print(f"[STORE]: {error} ")

async def setup(bot: commands.Bot):
    await bot.add_cog(Store(bot))