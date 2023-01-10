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
items_file = open("assets/yamls/items.yml", "rb")
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
            discord.SelectOption(label='Maden Aracı', value= "miningvehicle", description=f'Ücret: {miningVehiclePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Güçlendirilmiş Kazma', value= "reinforcedpickaxe", description=f'Ücret: {reinforcedPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Altın Kazma', value= "goldenpickaxe", description=f'Ücret: {goldenPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Çelik Kazma', value= "steelpickaxe", description=f'Ücret: {steelPickaxePrice:,}', emoji='⛏️'),
            discord.SelectOption(label='Taş Kazma', value= "stonepickaxe", description=f'Ücret: {stonePickaxePrice:,}', emoji='⛏️'),
            
            
            discord.SelectOption(label='Kazmayı Sat', value= "sellpickaxe", description=f'Kazmanı sat ve yenisini satın al', emoji='🗑️')
        ]
        super().__init__(placeholder='Bir Kazma Seç', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        pickaxeName = ""
        pickaxePrice = 0
        pickaxeId = ""
        
        if self.values[0] == "stonepickaxe":
            pickaxeName = "Taş Kazma"
            pickaxePrice = stonePickaxePrice
            pickaxeId = "stonepickaxe"
        elif self.values[0] == "steelpickaxe":
            pickaxeName = "Çelik Kazma"
            pickaxePrice = steelPickaxePrice
            pickaxeId = "steelpickaxe"
        elif self.values[0] == "goldenpickaxe":
            pickaxeName = "Altın Kazma"
            pickaxePrice = goldenPickaxePrice
            pickaxeId = "goldenpickaxe"
        elif self.values[0] == "reinforcedpickaxe":
            pickaxeName = "Güçlendirilmiş Kazma"
            pickaxePrice = reinforcedPickaxePrice
            pickaxeId = "reinforcedpickaxe"
        elif self.values[0] == "miningvehicle":
            pickaxeName = "Maden Aracı"
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

        # Items Check
        if "items" not in userInventory:

            itemsData = { "$set" : {"items" : {}}}

            await inventoryCollection.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellpickaxe":
            if "pickaxe" in userInventory["items"]:
                
                userInventory["items"].pop("pickaxe")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message(content = "Kazmanı başarıyla sattın")
            else:
                return await interaction.response.send_message(content = "Bir kazmaya sahip değilsin!")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message(content = "Cüzdanın yok! `/wallet` komutunu kullan ve bir cüzdan oluştur", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < pickaxePrice:
            needMoney = pickaxePrice - userWallet["coins"]
            return await interaction.response.send_message(content = f"Cüzdanınızda yeteri kadar Cupcoin bulunmuyor! {needMoney:,} Cupcoin'e ihtiyacınız var.", ephemeral = True)



        # Pickaxe Check
        if "pickaxe" in userInventory["items"]:
            return await interaction.response.send_message("Zaten bir kazmanız var", ephemeral = True)

        # Fee received
        userWallet["coins"] -= pickaxePrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)

        # Add Item
        userInventory["items"].update({"pickaxe" : pickaxeId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨⛏️ **|** {pickaxePrice:,} Cupcoin ödeyerek yeni bir {pickaxeName} satın aldınız. Artık daha değerli madenler çıkarabileceksiniz.")

class Swords(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Claymore Kılıcı', value= "claymore", description=f' {claymorePrice:,} yerine sadece {claymoreDcPrice:,} Cupcoin', emoji='⚔️'),
            discord.SelectOption(label='Odachi Kılıcı', value= "odachi", description=f'{odachiPrice:,} yerine sadece {odachiDcPrice:,} Cupcoin', emoji='⚔️'),
            discord.SelectOption(label='Rapier Kılıcı', value= "rapier", description=f'{rapierPrice:,} yerine sadece {rapierDcPrice:,} Cupcoin', emoji='⚔️'),
            discord.SelectOption(label='Katana Kılıcı', value= "katana", description=f'{katanaPrice:,} yerine sadece {katanaDcPrice:,} Cupcoin', emoji='⚔️'),
            discord.SelectOption(label='Chukuto Kılıcı', value= "chokuto", description=f'{chukutoPrice:,} yerine sadece {chukutoDcPrice:,} Cupcoin', emoji='⚔️'),
            discord.SelectOption(label='Gladius Kılıcı', value= "gladius", description=f'{gladiusPrice:,} yerine sadece {gladiusDcPrice:,} Cupcoin', emoji='⚔️'),      

            discord.SelectOption(label='Kılıcını Sat', value= "sellsword", description=f'Kılıcını sat ve yenisini al', emoji='🗑️')

        ]
        super().__init__(placeholder='Bir Kılıç Seç', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        swordName = ""
        swordPrice = 0
        swordId = ""
        
        if self.values[0] == "gladius":
            swordName = "Gladius Kılıcı"
            swordPrice = gladiusDcPrice
            swordId = "gladius"
        elif self.values[0] == "chokuto":
            swordName = "Chukuto Kılıcı"
            swordPrice = chukutoDcPrice
            swordId = "chokuto"
        elif self.values[0] == "katana":
            swordName = "Katana Kılıcı"
            swordPrice = katanaDcPrice
            swordId = "katana"
        elif self.values[0] == "rapier":
            swordName = "Rapier Kılıcı"
            swordPrice = rapierDcPrice
            swordId = "rapier"
        elif self.values[0] == "odachi":
            swordName = "Odachi Kılıcı"
            swordPrice = odachiDcPrice
            swordId = "odachi"
        elif self.values[0] == "claymore":
            swordName = "Claymore Kılıcı"
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
            
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await inventoryCollection.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        

        if self.values[0] == "sellsword":
            if "sword" in userInventory["items"]:
                
                userInventory["items"].pop("sword")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("Kılıcını başarıyla sattın")
            else:
                return await interaction.response.send_message("Bir kılıca sahip değilsin")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Cüzdanın yok! `/wallet` komutunu kullan ve bir cüzdan oluştur", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < swordPrice:
            needMoney = swordPrice - userWallet["coins"]
            return await interaction.response.send_message(f"Cüzdanınızda yeteri kadar Cupcoin bulunmuyır! {needMoney:,} Cupcoin'e ihtiyacınız var", ephemeral = True)


        # Pickaxe Check
        if "sword" in userInventory["items"]:
            return await interaction.response.send_message("Zaten bir kılıca sahipsiniz", ephemeral = True)

        # Fee received
        userWallet["coins"] -= swordPrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"sword" : swordId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨⚔️ **|** {swordPrice:,} Cupcoin ödeyerek yeni bir {swordName} satın aldınız. Bir kılıç almak çok akıllıca! Gelecekte çok iş yapacak.")

class Rods(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Zıpkın', value= "harpoon", description=f'Ücret: {harpoonPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Şanslı Olta', value= "luckyrod", description=f'Ücret: {luckyRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Gümüş Olta', value= "silverrod", description=f'Ücret: {silverRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Sağlam Olta', value= "solidrod", description=f'Ücret: {solidRodPrice:,}', emoji='🎣'),
            discord.SelectOption(label='Basit Olta', value= "simplerod", description=f'Ücret: {simpleRodPrice:,}', emoji='🎣'),
            
            discord.SelectOption(label='Oltayı Sat', value= "sellrod", description=f"Oltanı sat ve yenisini al", emoji='🗑️')

        ]
        super().__init__(placeholder='Bir Olta Seç', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        rodName = ""
        rodPrice = 0
        rodId = ""
        
        if self.values[0] == "simplerod":
            rodName = "Basit Olta"
            rodPrice = simpleRodPrice
            rodId = "simplerod"
        
        elif self.values[0] == "solidrod":
            rodName = "Sağlam Olta"
            rodPrice = solidRodPrice
            rodId = "solidrod"
        
        elif self.values[0] == "silverrod":
            rodName = "Gümüş Olta"
            rodPrice = silverRodPrice
            rodId = "silverrod"
        
        elif self.values[0] == "luckyrod":
            rodName = "Şanslı Olta"
            rodPrice = luckyRodPrice
            rodId = "luckyrod"
        
        elif self.values[0] == "harpoon":
            rodName = "Zıpkın"
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
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await inventoryCollection.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellrod":
            if "rod" in userInventory["items"]:
                userInventory["items"].pop("rod")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("Oltanızı başarıyla sattınız")
                return
            else:
                return await interaction.response.send_message("Zaten bir oltaya sahip değilsiniz")
        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Cüzdanın yok! `/wallet` komutunu kullan ve bir cüzdan oluştur", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < rodPrice:
            needMoney = rodPrice - userWallet["coins"] 
            return await interaction.response.send_message(f"Cüzdanınızda yeteri kadar Cupcoin bulunmuyor! {needMoney:,} Cupcoin'e ihtiyacınız var", ephemeral = True)


        # Pickaxe Check
        if "rod" in userInventory["items"]:
            return await interaction.response.send_message("Zaten bir oltaya sahipsiniz", ephemeral = True)

        # Fee received
        userWallet["coins"] -= rodPrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"rod" : rodId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨🎣 **|** {rodPrice:,} ödeyerek yeni bir {rodName} satın aldınız . Bu olta ile daha değerli balıklar tutabileceksiniz.")

class Bows(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Arbalet', value= "crossbow", description=f'Ücret: {crossbowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='İsabetli Yay', value= "accuratebow", description=f'Ücret: {accurateBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Gümüş Yay', value= "silverbow", description=f'Ücret: {silverBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Bakır Yay', value= "copperbow", description=f'Ücret: {copperBowPrice:,}', emoji='🏹'),
            discord.SelectOption(label='Tahta Yay', value= "woodenbow", description=f'Ücret: {woodenBowPrice:,}', emoji='🏹'),
            
            discord.SelectOption(label='Yayı Sat', value= "sellbow", description=f"Yayını sat ve yenisini al", emoji='🗑️')

        ]
        super().__init__(placeholder='Bir Yay Seç', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        bowName = ""
        bowPrice = 0
        bowId = ""
        
        if self.values[0] == "woodenbow":
            bowName = "Tahta Yay"
            bowPrice = woodenBowPrice
            bowId = "woodenbow"
        
        elif self.values[0] == "copperbow":
            bowName = "Bakır Yay"
            bowPrice = copperBowPrice
            bowId = "copperbow"
        
        elif self.values[0] == "silverbow":
            bowName = "Gümüş Yay"
            bowPrice = silverBowPrice
            bowId = "silverbow"
        
        elif self.values[0] == "accuratebow":
            bowName = "İsabetli Yay"
            bowPrice = accurateBowPrice
            bowId = "accuratebow"
        
        elif self.values[0] == "crossbow":
            bowName = "Arbalet"
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
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await inventoryCollection.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellbow":
            
            if "bow" in userInventory["items"]:
                
                userInventory["items"].pop("bow")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("Yayınızı başarıyla sattınız")
                return
            else:
                return await interaction.response.send_message("Zaten bir yaya sahip değilsiniz")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Cüzdanın yok! `/wallet` komutunu kullan ve bir cüzdan oluştur", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < bowPrice:
            needMoney = bowPrice - userWallet["coins"]
            return await interaction.response.send_message(f"Cüzdanında yeterli Cupcoin bulunmuyor! {needMoney:,} Cupcoin'e ihtiyacın var", ephemeral = True)


        # Pickaxe Check
        if "bow" in userInventory["items"]:
            return await interaction.response.send_message("Zaten bir yaya sahipsiniz", ephemeral = True)

        # Fee received
        userWallet["coins"] -= bowPrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        

        userInventory["items"].update({"bow" : bowId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨🏹 **|** {bowPrice:,} ödeyerek yeni bir {bowName} satın aldınız. Artık daha değerli avlar avlayabileceksiniz.")

class Axes(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Büyülü Balta', value= "enchantedaxe", description=f'Price: {enchantedAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Güçlendirilmiş Balta', value= "reinforcedaxe", description=f'Price: {reinforcedAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Altın Balta', value= "goldenaxe", description=f'Price: {goldenAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Çelik Balta', value= "steelaxe", description=f'Price: {steelAxePrice:,}', emoji='🪓'),
            discord.SelectOption(label='Taş Balta', value= "stoneaxe", description=f'Price: {stoneAxePrice:,}', emoji='🪓'),
            
            
            
            
            
            discord.SelectOption(label='Baltanı Sata', value= "sellaxe", description=f"Baltanı sat ve yenisini al", emoji='🗑️')

        ]
        super().__init__(placeholder='Bir Balta Seç', options=options)

    async def callback(self, interaction: discord.Interaction):
        
        axeName = ""
        axePrice = 0
        axeId = ""
        
        if self.values[0] == "stoneaxe":
            axeName = "Taş Balta"
            axePrice = stoneAxePrice
            axeId = "stoneaxe"
        
        elif self.values[0] == "steelaxe":
            axeName = "Çelik Balta"
            axePrice = steelAxePrice
            axeId = "steelaxe"
        
        elif self.values[0] == "goldenaxe":
            axeName = "Altın Balta"
            axePrice = goldenAxePrice
            axeId = "goldenaxe"
        
        elif self.values[0] == "reinforcedaxe":
            axeName = "Güçlendirilmiş Balta"
            axePrice = reinforcedAxePrice
            axeId = "reinforcedaxe"
        
        elif self.values[0] == "enchantedaxe":
            axeName = "Büyülü Balta"
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
        
        # Items Check
        if "items" not in userInventory:
            itemsData = { "$set" : {"items" : {}}}
            await inventoryCollection.update_one(userInventory, itemsData)

        # User Inventory (new)
        userInventory = await inventoryCollection.find_one({"_id": interaction.user.id})

        if self.values[0] == "sellaxe":
            if "axe" in userInventory["items"]:
                
                userInventory["items"].pop("axe")
                await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)
                await interaction.response.send_message("Baltanı başarıyla sattın")
                return
            else:
                return await interaction.response.send_message("Zaten bir baltaya sahip değilsin")

        # Wallet Check
        if await coinCollection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Cüzdanın yok! `/wallet` komutunu kullan ve bir cüzdan oluştur", ephemeral = True)

        # User Wallet
        userWallet = await coinCollection.find_one({"_id" : interaction.user.id})

        # Cupcoin (money) Check
        if userWallet["coins"] < axePrice:
            needMoney = axePrice - userWallet["coins"]
            return await interaction.response.send_message(f"Cüzdanında yeteri kadar Cupcoin bulunamadı! {needMoney:,} Cupcoin'e ihtiyacınız var", ephemeral = True)


        # Pickaxe Check
        if "axe" in userInventory["items"]:
            return await interaction.response.send_message("Zaten bir baltaya sahipsiniz", ephemeral = True)

        # Fee received
        userWallet["coins"] -= axePrice
        await coinCollection.replace_one({"_id" : interaction.user.id}, userWallet)
        
        # Add Item
        userInventory["items"].update({"axe" : axeId})
        await inventoryCollection.replace_one({"_id" : interaction.user.id}, userInventory)

        await interaction.response.send_message(f"✨🪓 **|** {axePrice:,} ödeyerek yeni bir {axeName} satın aldınız. Artık daha büyük ve değerli ağaçları kesebileceksiniz.")

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
    @discord.ui.button(label="Kazmalar", style=discord.ButtonStyle.primary, custom_id="showpickaxes")
    async def pickaxe_callback(self, interaction, button):
        
        view = PickaxeView()

        await interaction.response.send_message(content= "Yeni bir kazma mı alacaksın? Bu harika! Aşağıdaki menüden kazmaları görüntüleyebilirsin.", view = view)
    
    # THIS BUTTON PURPOSE IS SHOW ALL RODS
    @discord.ui.button(label="Oltalar", style=discord.ButtonStyle.primary, custom_id="showrods")
    async def rods_callback(self, interaction, button):
        view = RodView()
        await interaction.response.send_message(content= "Yeni bir olta mı alacaksın? Bu harika! Aşağıdaki menüden oltaları görüntüleyebilirsin.", view = view)

    # THIS BUTTON PURPOSE IS SHOW ALL BOWS
    @discord.ui.button(label="Yaylar", style=discord.ButtonStyle.primary, custom_id="showbows")
    async def bows_callback(self, interaction, button):
        view = BowView()
        await interaction.response.send_message(content= "Yeni bir yay mı alacaksın? Bu harika! Aşağıdaki menüden yayları görüntüleyebilirsin.", view = view)
    

    # THIS BUTTON PURPOSE IS SHOW ALL AXES
    @discord.ui.button(label="Baltalar", style=discord.ButtonStyle.primary, custom_id="showaxes")
    async def axes_callback(self, interaction, button):
        view = AxeView()
        await interaction.response.send_message(content= "Yeni bir balta mı alacaksın? Bu harika! Aşağıdaki menüden baltaları görüntüleyebilirsin.", view = view)

     # THIS BUTTON PURPOSE IS SHOW ALL SWORDS
    @discord.ui.button(label="Kılıçlar", style=discord.ButtonStyle.success, custom_id="showswords")
    async def sword_callback(self, interaction, button):
        view = SwordView()
        await interaction.response.send_message(content= "Yeni bir kılıç mı alacaksın? Bu harika! Aşağıdaki menüden kılıçları görüntüleyebilirsin.", view = view)


    # THIS BUTTON PURPOSE IS CLOSE THE MENU
    @discord.ui.button(label="Kapat", style=discord.ButtonStyle.danger, custom_id="closemenu")
    async def close_callback(self, interaction, button):
        await interaction.message.delete()
        await interaction.response.send_message(content=f"Mağaza başarıyla kapatıldı.", ephemeral = True)
    

# MAIN CLASS
class Store(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "store", description = "Mağazayı aç ve eşya satın al!") # Commands
    @app_commands.guild_only
    @app_commands.checks.cooldown( 1, 20, key=lambda i: (i.guild_id, i.user.id)) # Cooldown
    async def store(self, interaction: discord.Interaction):
        
        view = ItemsView()

        itemsEmbed = Embed(description = f"Merhaba 👋 Mağazaya hoş geldin. Balıkçılık, avcılık, madencilik ve ormancılık için buradan ekipman satın alabilirsin. ")
        itemsEmbed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar.url)
        itemsEmbed.add_field(name = "Nasıl Eşya Satın Alacağım?", value = "Butonlara tıklayın ve seviyelere göre eşya satın alınız", inline = False)
        itemsEmbed.add_field(name = "Bunun için ödeme yapacak mıyım?", value = "Evet, eşyalara ve onların seviyelerine göre farklı ücretlendirmeler bulunuyor (Cupcoin ile)", inline = False)

        await interaction.response.send_message(embed = itemsEmbed, view = view) 

    @store.error
    async def storeError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)
        else:
            print(f"[STORE]: {error} ")

async def setup(bot: commands.Bot):
    await bot.add_cog(Store(bot))