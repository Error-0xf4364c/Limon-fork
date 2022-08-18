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

VLF = fish["veryLowLevelFish"]
LF = fish["lowLevelFish"]
MLF = fish["mediumLevelFish"]
HF = fish["highLevelFish"]
VHF = fish["veryHighLevelFish"]
all_fish = VLF | LF | MLF | HF | VHF

VLH = hunt["veryLowLevelHunt"]
LH = hunt["lowLevelHunt"]
MLH = hunt["mediumLevelHunt"]
HH = hunt["highLevelHunt"]
VHH = hunt["veryHighLevelHunt"]
all_hunt = VLH | LH | MLH | HH | VHH

VLM = mine["veryLowLevelMine"]
LM = mine["lowLevelMine"]
MLM = mine["mediumLevelMine"]
HM = mine["highLevelMine"]
VHM = mine["veryHighLevelMine"]
all_mine = VLM | LM | MLM | HM | VHM

VLW = wood["veryLowLevelWood"]
LW = wood["lowLevelWood"]
MLW = wood["mediumLevelWood"]
HW = wood["highLevelWood"]
VHW = wood["veryHighLevelWood"]
all_wood = VLW | LW | MLW | HW | VHW






class Buttons(View):

    
    @button(label = "Backpack", style = discord.ButtonStyle.blurple)
    async def backpack_callback(self, interaction, button):

        db = client.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("You don't have an inventory! Please use this commands: `mining, forestry, hunting, fishing`", ephemeral = True)

        userData = await collection.find_one({"_id": interaction.user.id})

        userFishes = ["None"]
        userMines = ["None"]
        userHunts = ["None"]
        userWood = ["None"]

        if "fishes" in userData:
            userFishes = list(userData["fish"].keys())
        if "mines" in userData:
            userMines = list(userData["mines"].keys())
        if "hunts" in userData:
            userHunts = userData["hunts"]
        if "wood" in userData:
            userWood = list(userData["wood"].keys())
        
        fishes_ = [ f"**{userFishes.count(i)}** x {i.title()} - **{userData['fishes'][i]}**cm 🐟" for i in all_fish if i in userFishes]
        hunts_ = [ f"**{userHunts.count(i)}** x {i.title()} 🦌" for i in all_hunt if i in userHunts]
        mines_ = [ f"**{userMines.count(i)}** x {i.title()} - **{userData['mines'][i]}**kg 💎" for i in all_mine if i in userMines]
        wood_ = [ f"**{userWood.count(i)}** x {i.title()} - **{userData['wood'][i]}**m 🌲" for i in all_wood if i in userWood]
        
        fishes_ = "\n".join(fishes_) if len(fishes_)>0 else "*No fish in your inventory*"
        hunts_ = "\n".join(hunts_) if len(hunts_)>0 else "*No hunt in your inventory*"
        mines_ = "\n".join(mines_) if len(mines_)>0 else "*No mine in your inventory*"
        wood_ = "\n".join(wood_) if len(wood_)>0 else "*No wood in your inventory*"
        
        print(fishes_)
        
        backpack_embed = Embed( description =  f"Your Hunts \n\n════════════════════════════════\n***FISHES:*** {fishes_}")
        backpack_embed.set_author(name= interaction.user.name, icon_url = interaction.user.avatar.url)

        await interaction.response.edit_message(embed = backpack_embed, view=self)




class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Show Inventory
    @app_commands.command(name = "inventory", description = "View your inventory")
    @app_commands.checks.cooldown( 1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def inventory(self, interaction: discord.Interaction):
        view = Buttons()

        await interaction.response.send_message("Click a button", view=view)

        

async def setup(bot:commands.Bot):
    await bot.add_cog(Inventory(bot), guilds= [discord.Object(id =964617424743858176)])