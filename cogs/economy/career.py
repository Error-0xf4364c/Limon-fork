import discord
from discord import Embed
from discord import app_commands
from discord.ext import commands
import datetime

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

        if await interaction.collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message(f"You have not a career. You can use `mining`, `forestry`, `hunting`, `fishing` etc. commands.", ephemeral=True)

        userCareer = await interaction.collection.find_one({"_id": interaction.user.id})


        userPoints = [ f"{' '.join(i.split('_')).title()} = {userCareer['points'][i]}" for i in userCareer["points"] ]

        viewUserPoints = "\n".join(userPoints)


        careerResponse = Embed(description= f"════════════════════════════════\n***Your Career Points:***\n {viewUserPoints}")
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
        

