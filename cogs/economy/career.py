import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands
import datetime
import yaml
from yaml import Loader

badges_file = open("yamls/badges.yml", "rb")
rozet = yaml.load(badges_file, Loader = Loader) 

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

greatpersonpuani = rozet["greatpersonpuani"]

acemibalikci = rozet['acemibalikci']
amatorbalikci = rozet['amatorbalikci']
ustabalikci = rozet['ustabalikci']

acemiavci = rozet['acemiavci']
amatoravci = rozet['amatoravci']
ustaavci = rozet['ustaavci']

acemikumarbaz = rozet['acemikumarbaz']
tecrubelikumarbaz = rozet['tecrubelikumarbaz']
milyonerkumarbaz = rozet['milyonerkumarbaz']
goodperson = rozet['greatperson']
kahramansahibi = rozet['kahramansahibi']


class CareerView(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
        name = "career",
        description= "View your career"
    )
    @app_commands.checks.cooldown(
        1, 600, key=lambda i: (i.guild_id, i.user.id))
    async def career(self, interaction: discord.Interaction):
        db = self.bot.mongoConnect["cupcake"]
        collection = db["career"]

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message(f"You have not a career. You can use `mining`, `forestry`, `hunting`, `fishing` etc. commands.", ephemeral=True)

        userCareer = await collection.find_one({"_id": interaction.user.id})
        userBadges = []

        userPoints = [ f"{' '.join(i.split('_')).title()} = {userCareer['points'][i]}" for i in userCareer["points"] ]

        viewUserPoints = "\n".join(userPoints)

        """BADGES"""
        if "fisher_point" in userCareer:
            totalBalikciPuani = userCareer['fisher_point']
            if totalBalikciPuani >= ustabalikcipuani:
                userBadges.append(ustabalikci)
            elif totalBalikciPuani >= amatorbalikcipuani:
                userBadges.append(amatorbalikci)
            elif totalBalikciPuani >= acemibalikcipuani:
                userBadges.append(acemibalikci)
        if "hunter_point" in userCareer:
            totalAvciPuani = userCareer['hunter_point']
            if totalAvciPuani >= ustaavcipuani:
                userBadges.append(ustaavci)
            elif totalAvciPuani >= amatoravcipuani:
                userBadges.append(amatoravci)
            elif totalAvciPuani >= acemiavcipuani:
                userBadges.append(acemiavci)
        if "gamble_point" in userCareer:
            totalKumarPuani = userCareer['gamble_point']
            if totalKumarPuani >= milyonerkumarbazpuani:
                userBadges.append(milyonerkumarbaz)
            elif totalKumarPuani >= tecrubelikumarbazpuani:
                userBadges.append(tecrubelikumarbaz)
            elif totalKumarPuani >= acemikumarbazpuani:
                userBadges.append(acemikumarbaz)
        if "send_point" in userCareer:
            totalSendPuani = userCareer['send_point']
            if totalSendPuani >= greatpersonpuani:
                userBadges.append(goodperson)

        if len(userBadges) == 0:
            badges_ = "No badge has been earned yet"
        else:
            badges_ = " ".join(userBadges)

        careerResponse = Embed(description= f"{badges_}\n════════════════════════════════\n***Your Career Points:***\n {viewUserPoints}")
        careerResponse.set_author(name = f"{interaction.user.name}'s Career", icon_url = interaction.user.avatar.url)


        await interaction.response.send_message(embed = careerResponse)

    @career.error
    async def careerError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}`s and Try Again",ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please inform the developer of this situation and try again later.")
            print(f"[CAREER]: {error} ")


async def setup(bot:commands.Bot):
    await bot.add_cog(CareerView(bot))
        

