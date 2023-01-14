import discord
from discord import ui, app_commands, Embed
from discord.ext import commands
import datetime

class SuggestionModal(ui.Modal, title= "Öneri"):
    answer = ui.TextInput(
        label = "Öneriniz nedir?",
        style = discord.TextStyle.paragraph,
        placeholder= "Öneriniz hakkında detaylı açıklama yapınız?",
        required = True,
        max_length= 4000
    )

    async def on_submit(self, interaction: discord.Interaction):

        suggestionMessage = Embed(
            title = self.title,
            description = f"{self.answer}",
            timestamp= datetime.datetime.utcnow(),
            color = 0xffd32a 
        )

        suggestionMessage.set_author(
            name = interaction.user,
            icon_url = interaction.user.avatar.url
        )

        failMessage = Embed(
            description = "❌ **|** Upss, öneriniz gönderilemedi! Lütfen [destek sunucumuza](https://discord.gg/Fa26cW3Npx) gelin ve geliştiriciye bu sorunu bildirin.", 
            color = 0xff3333
        )

        suggestionsChannel = interaction.client.get_channel(1063608269404381255)
        
        try:
            await suggestionsChannel.send(embed = suggestionMessage)
            await interaction.response.send_message("✅ **|** Önerilerinizi aldık. Teşekkür ederiz :)", ephemeral = True)
        except:
            await interaction.response.send_message(embed = failMessage, ephemeral = True)


class Suggestion(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "suggestion", description = "Cupcake için bir öneride bulun")
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.user.id))
    async def suggestion(self, interaction: discord.Interaction):
        modal = SuggestionModal()

        await interaction.response.send_modal(modal)
    @suggestion.error
    async def suggestionError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s bekleyin!", ephemeral = True)
        else:
            print(f"[SUGGESTION] {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Suggestion(bot))
