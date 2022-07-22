import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands
import datetime
import yaml
from yaml import Loader

yaml_file = open("emojis.yml", "r")
emojis = yaml.load(yaml_file, Loader = Loader) 

yaml_file2 = open("animals.yml", "r")
animals = yaml.load(yaml_file2, Loader = Loader) 

yaml_file2 = open("chars.yml", "r")
heroes = yaml.load(yaml_file2, Loader = Loader) 

clock = emojis["clock"]  or "⏳"

# Emojis


# Hunts
allFishes = animals['fishes']
fishesKey = " ".join(animals["fishes"].keys())
fishes = fishesKey.split(" ")
print(fishes)
print(fishesKey)
print(allFishes)

allHunts = animals["hunts"]
huntsKey = " ".join(animals["hunts"].keys())
hunts = huntsKey.split(" ")



myheroes = " ".join(heroes.keys())
sliceHero = myheroes.split(" ")

class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # Show Inventory
    @app_commands.command(
        name = "inventory",
        description = "Envanterini görüntüle"
    )
    @app_commands.checks.cooldown(
        1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def inventory(self, interaction: discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Upss! Envanterin yok. Biraz avlanmaya ne dersin? **|** 🦌", ephemeral = True)
        
        userData = await collection.find_one({"_id" : interaction.user.id})

        userFishes = ["Yok"]
        userHunts = ["Yok"]
        userHeroes = ["Yok"]

        if "hunts" in userData:
            userHunts = userData['hunts']
        if "fishes" in userData:
            userFishes = list(userData['fishes'].keys())
            
        if "heroes" in userData:
            userHeroes = userData['heroes']




        fishes_ = [ f"**{userFishes.count(i)}** x {i.title()} - **{userData['fishes'][i]}**cm 🐟" for i in fishes if i in userFishes]
        hunts_ = [ f"**{userHunts.count(i)}** x {i.title()} 🦌" for i in hunts if i in userHunts]
        heroes_ = [f"{heroes[i]['rarity']} **››** {heroes[i]['name']}" for i in sliceHero if i in userHeroes]


        
        fishes_ = "\n".join(fishes_) if len(fishes_)>0 else "*Envanterinizde hiç balık yok*"
        hunts_ = "\n".join(hunts_) if len(hunts_)>0 else "*Envanterinizde hiç av yok*"
        heroes_ = "\n".join(heroes_) if len(heroes_)>0 else "*Hiç kahramanınız yok*"

        inventoryResponse = Embed(description = f"Hey! Envanterin boş mu? Hadi o zaman biraz avlan ve doldur bakalım.\n\n***Fishes:***\n{fishes_}\n\n***Hunts***\n{hunts_}\n\n***Heroes***\n{heroes_}")
        inventoryResponse.set_author(name = f"{interaction.user.name}'s Inventory", icon_url = interaction.user.avatar.url)

        await interaction.response.send_message(embed = inventoryResponse)

    @inventory.error
    async def inventoryError(self, interaction : discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Inventory(bot), guilds= [discord.Object(id =964617424743858176)])