"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

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

fish_file = open("assets/yamls/fishing.yml", "rb")
fish = yaml.load(fish_file, Loader = Loader)

hunt_file = open("assets/yamls/hunt.yml", "rb")
hunt = yaml.load(hunt_file, Loader = Loader)

mine_file = open("assets/yamls/mines.yml", "rb")
mine = yaml.load(mine_file, Loader = Loader)

wood_file = open("assets/yamls/wood.yml", "rb")
wood = yaml.load(wood_file, Loader = Loader)

char_file = open("assets/yamls/chars.yml", "rb")
chars = yaml.load(char_file, Loader = Loader)

items_file = open("assets/yamls/items.yml", "rb")
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

        if not interaction.user.id in message_author_id:
            await interaction.response.send_message("Bu envanter size ait değil! Herhangi bir işlem yapamazsınız. Lütfen **`/inventory`** komutunu kullanın.", ephemeral=True)
            return False
        return True

    
    @button(label = "Çanta", style = discord.ButtonStyle.blurple)
    async def backpack_callback(self, interaction, button):

        db = client.database["limon"]
        collection = db["inventory"]

        if collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Upss! Envanteriniz bulunmuyor! Şu komutları kullanmayı deneyiniz: `mining, forestry, hunting, fishing`", ephemeral = True)

        userData = collection.find_one({"_id": interaction.user.id})

        userFishes = ["None"]
        userMines = ["None"]
        userHunts = ["None"]
        userWood = ["None"]
        userChars = ["None"]



        if "fishes" in userData:
            userFishes = list(userData["fishes"].keys())
        if "mines" in userData:
            userMines = list(userData["mines"].keys())
        if "hunts" in userData:
            userHunts = userData["hunts"]
        if "wood" in userData:
            userWood = list(userData["wood"].keys())
        if "heroes" in userData:
            userChars = userData["heroes"]

        

        
        fishes_ = [ f"**{userFishes.count(i)}** x {all_fish[i]['name']} - **{userData['fishes'][i]}**cm 🐟" for i in all_fish_keys if i in userFishes]
        hunts_ = [ f"**{userHunts.count(i)}** x {all_hunt[i]['name']} 🦌" for i in all_hunt if i in userHunts]
        chars_ = [ f"{chars[i]['name']} **››** {chars[i]['rarity']} 🦸" for i in chars if i in userChars] 
        mines_ = [ f"**{userMines.count(i)}** x {all_mine[i]['name']} - **{userData['mines'][i]}**kg 💎" for i in all_mine_keys if i in userMines]
        wood_ = [ f"**{userWood.count(i)}** x {all_wood[i]['name']} - **{userData['wood'][i]}**m 🌲" for i in all_wood_keys if i in userWood]
        
        



        fishes_ = "\n".join(fishes_) if len(fishes_)>0 else "*Çantanızda hiç balık yok*"
        hunts_ = "\n".join(hunts_) if len(hunts_)>0 else "*Çantanızda hiç av yok*"
        chars_ = "\n".join(chars_) if len(chars_)>0 else "*Çantanızda hiç kahraman yok*"
        mines_ = "\n".join(mines_) if len(mines_)>0 else "*Çantanızda hiç maden yok*"
        wood_ = "\n".join(wood_) if len(wood_)>0 else "*Çantanızda hiç odun yok*"

        
        backpack_embed = Embed( description =  f"Bu sizin çantanız. Burada rozetleriniz ve iş yaparak(balıkçılık, avcılık vs.) kazandıklarınız görünür. \n════════════════════════════════\n***BALIKLAR:***\n{fishes_}\n════════════════════════════════\n***AVLAR:***\n{hunts_}\n════════════════════════════════\n***MADENLER:***\n{mines_}\n════════════════════════════════\n***ODUNLAR:***\n{wood_}\n════════════════════════════════\n***KAHRAMANLAR:***\n{chars_}\n════════════════════════════════", color = 0x2E3136)
        backpack_embed.set_author(name= f"{interaction.user.name} Adlı Kullanıcının Çantası", icon_url = interaction.user.avatar.url)

        await interaction.response.edit_message(embed = backpack_embed, view=self)
    
    @button(label = "Eşyalar", style = discord.ButtonStyle.blurple)
    async def items_callback(self, interaction, button):
        db = client.database["limon"]
        collection = db["inventory"]

        if collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Upss! Hiç eşyanız yok. **`store`** komutunu kullanarak yeni eşyalar satın alabilirsiniz.", ephemeral = True)

        userData = collection.find_one({"_id": interaction.user.id})

        userItems = ["None"]
        if "items" in userData:
            userItems = list(userData["items"].values())

        items_ = [ f"**▸** {all_items_dict[i]['name']}" for i in all_items if i in userItems]

        items_ = "\n".join(items_) if len(items_)>0 else "*Hiç eşyanız yok*"

        items_embed = Embed(description = f"Bu sizin eşya çantanız. Burada satın aldığınız eşyalar görünür. Eşya satın almak için **`store`** komutunu kullanın \n════════════════════════════════\n***EŞYALAR:***\n{items_}", color = 0x2E3136)
        items_embed.set_author(name= f"{interaction.user.name} Adlı Kullanıcının Eşyaları", icon_url = interaction.user.avatar.url)

        await interaction.response.edit_message(embed = items_embed, view=self)



class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Show Inventory
    @app_commands.command(name = "inventory", description = "Envanterinizi görüntüleyin")
    @app_commands.checks.cooldown( 1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def inventory(self, interaction: discord.Interaction):
        view = Buttons()

        userFishes = ["Yok"]
        userHunts = ["Yok"]
        userHeroes = ["Yok"]
        userMines = ["Yok"]

        # Embed Message
        menu_embed = Embed(description = '**Envanterinizde nelere bakmak istiyorsunuz?**\n İşlerden kazandıklarınızı(balıkçılık, avcılık vs.) görmek için "Çanta" butonuna basın\n To look at the items you have purchased, click on: "Items"', color = 0x2E3136)
        menu_embed.set_author(name= f"{interaction.user.name} Adlı Kullanıcının Envanteri", icon_url = interaction.user.avatar.url)

        if interaction.user.id in message_author_id:
            message_author_id.remove(interaction.user.id)
            #return await interaction.response.send_message("You already have a shop opened. Turn it off first", ephemeral=True)
        message_author_id.append(interaction.user.id)
        
        await interaction.response.send_message(embed = menu_embed, view=view)

    # ERROR HANDLER
    @inventory.error
    async def inventoryError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Upss! Envanter açılamadı. Lütfen `{timeRemaining}`s bekleyin.",ephemeral=True)
        else:
            if len(message_author_id) >0:
                message_author_id.clear()
            print(f"[INVENTORY]: {error}")
        

async def setup(bot:commands.Bot):
    await bot.add_cog(Inventory(bot))
