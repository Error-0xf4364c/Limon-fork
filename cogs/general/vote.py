import discord
from discord import Embed
from discord import app_commands
from discord.ui import View, Button
from discord.ext import commands
import datetime
import yaml
from yaml import Loader



emojis_file = open("assets/yamls/emojis.yml", "rb")
emoji = yaml.load(emojis_file, Loader = Loader) 

topggLogo = emoji["topgg"] or "✅"

class VoteMe(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="vote", description = "Cupcake'e Top.gg'de oy ver!")
    async def vote(self, interaction: discord.Interaction):
        view = View()

        VoteButton = Button(label="Oy ver", style=discord.ButtonStyle.link, url="https://top.gg/bot/994143430504620072/vote", emoji = topggLogo)

        view.add_item(VoteButton)
    
        voteEmbed = Embed(color = 0x2E3136)
        voteEmbed.set_author(name = "Butona basarak Top.gg'ye gidebilir ve bize oy verebilirsiniz.", icon_url= interaction.user.avatar.url)
        await interaction.response.send_message(embed= voteEmbed, view=view)

    @vote.error
    async def voteError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"**Her 12 saatte bir oy verebilirsin!** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)
        else:
            await interaction.response.send_message("Bilinmedik bir hata ile karşılaştık ;c Lütfen bu durumu geliştiriciye bildiriniz.")
            print(f"[VOTE]: {error} ")


async def setup(bot: commands.Bot):
    await bot.add_cog(VoteMe(bot))
