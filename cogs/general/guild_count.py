import discord
from discord import app_commands
from discord.ext import commands
import datetime

class BasicCommands(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="guild_count", description="Shows the number of servers where the Cupcake is located")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def guild_count(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"I am currently on **{len(self.bot.guilds)}** servers!", ephemeral = True)
    @guild_count.error
    async def guild_countError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}`s and Try Again.",ephemeral=True)
        print(f"GUILD_COUNT: {error}")

    @app_commands.command(name="ping", description="Shows Cupcake's latency")
    @app_commands.checks.cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong! {round(self.bot.latency * 1000)}ms", ephemeral = True)
    @ping.error
    async def pingError(self, interaction: discord.Interaction,
                         error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}`s and Try Again.",ephemeral=True)
        print(f"PING: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCommands(bot), guilds= [discord.Object(id =964617424743858176)])