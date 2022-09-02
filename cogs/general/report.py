import discord
from discord import ui, app_commands, Embed
from discord.ext import commands
import datetime

class ReportModal(ui.Modal, title= "Report"):
    answer = ui.TextInput(
        label = "Enter Your Report",
        style = discord.TextStyle.paragraph,
        placeholder= "Explain in detail the error you received or the bug you encountered.. ",
        required = True,
        max_length= 4000
    )

    async def on_submit(self, interaction: discord.Interaction):

        reportMessage = Embed(
            title = self.title,
            description = f"{self.answer}",
            timestamp= datetime.datetime.utcnow(),
            color = 0xff3333 
        )

        reportMessage.set_author(
            name = interaction.user,
            icon_url = interaction.user.avatar.url
        )

        failMessage = Embed(
            description = "❌ **|** Submission of report failed. Please report this to the developer by coming to our [support server](https://discord.gg/M9S4Gv9Gwe).", 
            color = 0xff3333
        )

        reportsChannel = interaction.client.get_channel(1015377937261940736)
        
        try:
            await reportsChannel.send(embed = reportMessage)
            await interaction.response.send_message("✅ **|** You have successfully reported. Thank you :)", ephemeral = True)
        except:
            await interaction.response.send_message(embed = failMessage, ephemeral = True)


class Report(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "report", description = "Report Bugs/Errors")
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.user.id))
    async def report(self, interaction: discord.Interaction):
        modal = ReportModal()

        await interaction.response.send_modal(modal)
    @report.error
    async def reportError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}` and Try Again!")
        else:
            print(f"[REPORT] {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))