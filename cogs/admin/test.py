import discord
from discord import app_commands
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(
        name = "cupcake",
        description = "Selam ver!")

    async def cupcake(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"Merhaba {interaction.user.name}")
    







async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        test(bot),
        guilds = [discord.Object(id = 964617424743858176)]
    )
