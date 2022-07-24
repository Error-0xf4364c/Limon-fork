import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands
import datetime
import yaml
from yaml import Loader

yaml_file = open("emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 

yaml_file2 = open("animals.yml", "rb")
animals = yaml.load(yaml_file2, Loader = Loader) 

yaml_file3 = open("chars.yml", "rb")
heroes = yaml.load(yaml_file3, Loader = Loader) 

yaml_file4 = open("badges.yml", "rb")
rozet = yaml.load(yaml_file4, Loader = Loader) 

clock = "<:Cupclock:996129959758282842>"

# Emojis
heropuani = rozet['heropuani']

acemibalikcipuani = rozet["acemibalikcipuani"]
amatorbalikcipuani = rozet["amatorbalikcipuani"]
ustabalikcipuani = rozet["ustabalikcipuani"]

acemiavcipuani = rozet["acemiavcipuani"]
amatoravcipuani = rozet["amatoravcipuani"]
ustaavcipuani = rozet["ustaavcipuani"]

acemikumarbazpuani = rozet['acemikumarbazpuani']
tecrubelikumarbazpuani = rozet['tecrubelikumarbazpuani']
milyonerkumarbazpuani = rozet['milyonerkumarbazpuani']

acemibalikci = "<:acemibalikci:1000403735643697262>"
amatorbalikci = "<:amatorbalikci:1000403756208377926>"
ustabalikci = "<:ustabalikci:1000403787283972208>"

acemiavci = "<:acemiavci:1000403732493783071>"
amatoravci = "<:amatoravci:1000403750684479630>"
ustaavci = "<:ustaavci:1000403782439555105>"

acemikumarbaz = "<:acemikumarbaz:1000703131254018088>"
tecrubelikumarbaz = "<:tecrbelikumarbaz:1000703148865900564>"
milyonerkumarbaz = "<:milyonerkumarbaz:1000703140519227432>"

kahramansahibi = "<:kahramanSahibi:1000403760763383909> "

# Hunts
allFishes = animals['fishes']
fishesKey = " ".join(animals["fishes"].keys())
fishes = fishesKey.split(" ")

allHunts = animals["hunts"]
huntsKey = " ".join(animals["hunts"].keys())
hunts = huntsKey.split(" ")

userBadges = []

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
            if len(userHeroes) >= heropuani:
                userBadges.append(kahramansahibi)

        if "balikcipuani" in userData:
            totalBalikciPuani = userData['balikcipuani']
            if totalBalikciPuani >= ustabalikcipuani:
                userBadges.append(ustabalikci)
            elif totalBalikciPuani >= amatorbalikcipuani:
                userBadges.append(amatorbalikci)
            elif totalBalikciPuani >= acemibalikcipuani:
                userBadges.append(acemibalikci)
        if "avpuani" in userData:
            totalAvciPuani = userData['avpuani']
            if totalAvciPuani >= ustaavcipuani:
                userBadges.append(ustaavci)
            elif totalAvciPuani >= amatoravcipuani:
                userBadges.append(amatoravci)
            elif totalAvciPuani >= acemiavcipuani:
                userBadges.append(acemiavci)
        if "kumarpuani" in userData:
            totalKumarPuani = userData['kumarpuani']
            if totalKumarPuani >= milyonerkumarbazpuani:
                userBadges.append(milyonerkumarbaz)
            elif totalKumarPuani >= tecrubelikumarbazpuani:
                userBadges.append(tecrubelikumarbaz)
            elif totalKumarPuani >= acemikumarbazpuani:
                userBadges.append(acemikumarbaz)


        fishes_ = [ f"**{userFishes.count(i)}** x {i.title()} - **{userData['fishes'][i]}**cm 🐟" for i in fishes if i in userFishes]
        hunts_ = [ f"**{userHunts.count(i)}** x {i.title()} 🦌" for i in hunts if i in userHunts]
        heroes_ = [f"{heroes[i]['rarity']} **››** {heroes[i]['name']}" for i in sliceHero if i in userHeroes]

        
        fishes_ = "\n".join(fishes_) if len(fishes_)>0 else "*Envanterinizde hiç balık yok*"
        hunts_ = "\n".join(hunts_) if len(hunts_)>0 else "*Envanterinizde hiç av yok*"
        heroes_ = "\n".join(heroes_) if len(heroes_)>0 else "*Hiç kahramanınız yok*"
        
        if len(userBadges) == 0:
            badges_ = "Henüz rozet kazanılmamış"
        else:
            badges_ = " ".join(userBadges)

        inventoryResponse = Embed(description = f"{badges_} \n\nHey! Envanterin boş mu? Hadi o zaman biraz avlan ve doldur bakalım.\n\n***Fishes:***\n{fishes_}\n\n***Hunts***\n{hunts_}\n\n***Heroes***\n{heroes_}")
        inventoryResponse.set_author(name = f"{interaction.user.name}'s Inventory", icon_url = interaction.user.avatar.url)

        await interaction.response.send_message(embed = inventoryResponse)



    @inventory.error
    async def inventoryError(self, interaction : discord.Interaction,error: app_commands.AppCommandError):
        print(error)            
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)


async def setup(bot:commands.Bot):
    await bot.add_cog(Inventory(bot))