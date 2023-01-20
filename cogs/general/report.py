import discord
from discord import ui, app_commands, Embed
from discord.ext import commands
import datetime

class ReportModal(ui.Modal, title= "Bildir"):
    answer = ui.TextInput(
        label = "Hata Nedir?",
        style = discord.TextStyle.paragraph,
        placeholder= "Hata hakkında detaylı bilgiler giriniz.",
        required = True,
        max_length= 4000
    )

    async def on_submit(self, interaction: discord.Interaction):

        reportMessage = Embed(
            title = "Hata",
            description = f"{self.answer}",
            timestamp= datetime.datetime.utcnow(),
            color = 0xfff48a 
        )

        reportMessage.set_author(
            name = interaction.user,
            icon_url = interaction.user.avatar.url
        )

        failMessage = Embed(
            description = "❌ **|** Upss, rapor gönderilemedi! Lütfen [destek sunucumuza](https://discord.gg/Fa26cW3Npx) gelin ve geliştiriciye bu sorunu bildirin.", 
            color = 0xff3333
        )

        reportsChannel = interaction.client.get_channel(1063608331836596244)
        
        try:
            await reportsChannel.send(embed = reportMessage)
            await interaction.response.send_message("✅ **|** Rapor başarıyla gönderildi. Teşekkür ederiz :)", ephemeral = True)
        except:
            await interaction.response.send_message(embed = failMessage, ephemeral = True)


class Report(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "report", description = "Hata ve Bugları bildirin")
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.user.id))
    async def report(self, interaction: discord.Interaction):
        modal = ReportModal()

        await interaction.response.send_modal(modal)
    @report.error
    async def reportError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s bekleyin!", ephemeral = True)
        else:
            print(f"[REPORT] {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))
