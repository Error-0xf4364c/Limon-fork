import discord
from discord import Embed
from discord import app_commands
from discord.ui import View, Button
from discord.ext import commands
import datetime
import yaml
from yaml import Loader



emojis_file = open("yamls/emojis.yml", "rb")
emoji = yaml.load(emojis_file, Loader = Loader) 

topggLogo = emoji["topgg"] or "✅"

class VoteMe(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="vote", description = "Vote Cupcake on Top.gg")
    async def vote(self, interaction: discord.Interaction):
        view = View()

        VoteButton = Button(label="Vote", style=discord.ButtonStyle.link, url="https://top.gg/bot/994143430504620072/vote", emoji = topggLogo)

        view.add_item(VoteButton)
    
        voteEmbed = Embed(color = 0x2E3136)
        voteEmbed.set_author(name = "You can vote by pressing the button.", icon_url= interaction.user.avatar.url)
        await interaction.response.send_message(embed= voteEmbed, view=view)

    @vote.error
    async def voteError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"**You can only vote every 12 hours!** Please wait `{timeRemaining}`s and Try Again!",ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred. Please inform the developer of this situation and try again later.")
            print(f"[VOTE]: {error} ")


async def setup(bot: commands.Bot):
    await bot.add_cog(VoteMe(bot))
