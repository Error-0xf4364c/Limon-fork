"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands
import datetime
import yaml
from yaml import Loader
from fetchdata import create_career_data

badges_file = open("assets/yamls/badges.yml", "rb")
rozet = yaml.load(badges_file, Loader = Loader) 

emojis_file = open("assets/yamls/emojis.yml", "rb")
emoji = yaml.load(emojis_file, Loader = Loader) 

career_emoji = emoji["career"]

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
        description= "Kariyer puanınızı görüntüleyin."
    )
    @app_commands.checks.cooldown(
        1, 600, key=lambda i: (i.guild_id, i.user.id))
    async def career(self, interaction: discord.Interaction):
        userCareer, collection = create_career_data(self.bot, interaction.user.id) 
        
        userBadges = []

        userPoints = [ f"{' '.join(i.split('_')).title()} = {userCareer['points'][i]}" for i in userCareer["points"] ]

        viewUserPoints = "\n".join(userPoints)

        """ROZETLERİNİZ"""
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
            badges_ = "*Henüz rozet kazanılmamış*"
        else:
            badges_ = " ".join(userBadges)

        careerResponse = Embed(description= f"{badges_}\n════════════════════════════════\n{career_emoji} ***Kariyer Puanlarınız:***\n {viewUserPoints}")
        careerResponse.set_author(name = f"{interaction.user.name} Adlı Kullanıcının Kariyeri", icon_url = interaction.user.avatar.url)


        await interaction.response.send_message(embed = careerResponse)

    @career.error
    async def careerError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s bekleyin.", ephemeral=True)
        else:
            await interaction.response.send_message("Beklenmedik bir hata oluştu. Lütfen geliştiriciye bildiriniz")
            print(f"[CAREER]: {error} ")


async def setup(bot:commands.Bot):
    await bot.add_cog(CareerView(bot))
        

