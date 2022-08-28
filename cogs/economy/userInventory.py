import discord
from discord import Embed
from discord.ui import View, button
from discord import app_commands
from discord.ext import commands
import datetime
import yaml
from yaml import Loader
from main import MyBot

client = MyBot()

fish_file = open("yamls/fishing.yml", "rb")
fish = yaml.load(fish_file, Loader = Loader)

hunt_file = open("yamls/hunt.yml", "rb")
hunt = yaml.load(hunt_file, Loader = Loader)

mine_file = open("yamls/mines.yml", "rb")
mine = yaml.load(mine_file, Loader = Loader)

wood_file = open("yamls/wood.yml", "rb")
wood = yaml.load(wood_file, Loader = Loader)

items_file = open("yamls/items.yml", "rb")
item = yaml.load(items_file, Loader = Loader)

vlf = fish["veryLowLevelFish"]
lf = fish["lowLevelFish"]
mlf = fish["mediumLevelFish"]
hf = fish["highLevelFish"]
vhf = fish["veryHighLevelFish"]
all_fish = vlf | lf | mlf | hf | vhf
all_fish_keys = list(all_fish.keys())

vlh = hunt["veryLowLevelHunt"]
lh = hunt["lowLevelHunt"]
mlh = hunt["mediumLevelHunt"]
hh = hunt["highLevelHunt"]
vhh = hunt["veryHighLevelHunt"]
all_hunt = vlh | lh | mlh | hh | vhh
all_hunt_keys = list(all_hunt.keys())

vlm = mine["veryLowLevelMine"]
lm = mine["lowLevelMine"]
mlm = mine["mediumLevelMine"]
hm = mine["highLevelMine"]
vhm = mine["veryHighLevelMine"]
all_mine = vlm | lm | mlm | hm | vhm
all_mine_keys = list(all_mine.keys())

vlw = wood["veryLowLevelWood"]
lw = wood["lowLevelWood"]
mlw = wood["mediumLevelWood"]
hw = wood["highLevelWood"]
vhw = wood["veryHighLevelWood"]
all_wood = vlw | lw | mlw | hw | vhw
all_wood_keys = list(all_wood.keys())

items_pickaxes = item["pickaxe"]
pickaxeKey = " ".join(items_pickaxes.keys())
pickaxe_item = pickaxeKey.split(" ")

items_fishingrods = item["fishingrod"]
rodKey = " ".join(items_fishingrods.keys())
rod_item = rodKey.split(" ")

items_bow = item["bow"]
bowKey = " ".join(items_bow.keys())
bow_item = bowKey.split(" ")

items_axe = item["axe"]
axeKey = " ".join(items_axe.keys())
axe_item = axeKey.split(" ")

all_items = pickaxe_item + rod_item + bow_item + axe_item
all_items_dict = items_axe | items_bow | items_fishingrods | items_pickaxes

message_author_id = []

class Buttons(View):
    
    # Interaction User Check
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print(message_author_id)
        if not interaction.user.id in message_author_id:
            await interaction.response.send_message("This shop doesn't belong to you. You can't trade in someone else's store. Please use the /sell command.", ephemeral=True)
            return False
        return True

    
    @button(label = "Backpack", style = discord.ButtonStyle.blurple)
    async def backpack_callback(self, interaction, button):

        db = client.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Upss! You don't have an inventory! Please use this commands: `mining, forestry, hunting, fishing`", ephemeral = True)

        userData = await collection.find_one({"_id": interaction.user.id})

        userFishes = ["None"]
        userMines = ["None"]
        userHunts = ["None"]
        userWood = ["None"]

        if "fishes" in userData:
            userFishes = list(userData["fishes"].keys())
        if "mines" in userData:
            userMines = list(userData["mines"].keys())
        if "hunts" in userData:
            userHunts = userData["hunts"]
        if "wood" in userData:
            userWood = list(userData["wood"].keys())

        
        fishes_ = [ f"**{userFishes.count(i)}** x {all_fish[i]['name']} - **{userData['fishes'][i]}**cm 🐟" for i in all_fish_keys if i in userFishes]
        hunts_ = [ f"**{userHunts.count(i)}** x {all_hunt[i]['name']} 🦌" for i in all_hunt if i in userHunts]
        mines_ = [ f"**{userMines.count(i)}** x {all_mine[i]['name']} - **{userData['mines'][i]}**kg 💎" for i in all_mine_keys if i in userMines]
        wood_ = [ f"**{userWood.count(i)}** x {all_wood[i]['name']} - **{userData['wood'][i]}**m 🌲" for i in all_wood_keys if i in userWood]
        
        



        fishes_ = "\n".join(fishes_) if len(fishes_)>0 else "*No fish in your inventory*"
        hunts_ = "\n".join(hunts_) if len(hunts_)>0 else "*No hunt in your inventory*"
        mines_ = "\n".join(mines_) if len(mines_)>0 else "*No mine in your inventory*"
        wood_ = "\n".join(wood_) if len(wood_)>0 else "*No wood in your inventory*"

        
        backpack_embed = Embed( description =  f"This is the section in your inventory that shows what you have achieved as a result of the work you have done. \n════════════════════════════════\n***FISHES:***\n{fishes_}\n════════════════════════════════\n***HUNTS:***\n{hunts_}\n════════════════════════════════\n***MINES:***\n{mines_}\n════════════════════════════════\n***WOOD:***\n{wood_}", color = 0x2E3136)
        backpack_embed.set_author(name= f"{interaction.user.name}'s Backpack", icon_url = interaction.user.avatar.url)

        await interaction.response.edit_message(embed = backpack_embed, view=self)
    
    @button(label = "Items", style = discord.ButtonStyle.blurple)
    async def items_callback(self, interaction, button):
        db = client.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Upss! You don't have items! Please buy an item. You can use this command: `store`", ephemeral = True)

        userData = await collection.find_one({"_id": interaction.user.id})

        userItems = ["None"]
        if "items" in userData:
            userItems = list(userData["items"].values())

        items_ = [ f"**▸** {all_items_dict[i]['name']}" for i in all_items if i in userItems]

        items_ = "\n".join(items_) if len(items_)>0 else "*No item in your inventory*"

        items_embed = Embed(description = f"This is the section with the items in your inventory. To buy more items, use `store` \n════════════════════════════════\n***ITEMS:***\n{items_}", color = 0x2E3136)
        items_embed.set_author(name= f"{interaction.user.name}'s Items", icon_url = interaction.user.avatar.url)

        await interaction.response.edit_message(embed = items_embed, view=self)



class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Show Inventory
    @app_commands.command(name = "inventory", description = "View your inventory")
    @app_commands.checks.cooldown( 1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def inventory(self, interaction: discord.Interaction):
        view = Buttons()

        userData = await collection.find_one({"_id" : interaction.user.id})

        userFishes = ["Yok"]
        userHunts = ["Yok"]
        userHeroes = ["Yok"]
        userMines = ["Yok"]

        # Embed Message
        menu_embed = Embed(description = '**What do you want to look at in your inventory?**\n To see what you have achieved as a result of your work, click on "Backpack"\n To look at the items you have purchased, click on: "Items"', color = 0x2E3136)
        menu_embed.set_author(name= f"{interaction.user.name}'s Inventory", icon_url = interaction.user.avatar.url)

        
        await interaction.response.send_message(embed = menu_embed, view=view)

    # ERROR HANDLER
    @inventory.error
    async def inventoryError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Upss! The inventory hasn't opened yet. Please try again after {timeRemaining}s.",ephemeral=True)
        else:
            if len(message_author_id) >0:
                message_author_id.clear()
            print(f"[INVENTORY]: {error}")
        

async def setup(bot:commands.Bot):
    await bot.add_cog(Inventory(bot))
