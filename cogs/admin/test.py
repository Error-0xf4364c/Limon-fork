from code import interact
import discord
from discord import app_commands
from discord.ext import commands
from interactions import Choice

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(
        name = "cupcake",
        description = "Selam ver!")

    async def cupcake(self, interaction: discord.Interaction,
    name: str) -> None:
        await interaction.response.send_message(f"Merhaba {name}")
    







async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        test(bot),
        guilds = [discord.Object(id = 964617424743858176)]
    )