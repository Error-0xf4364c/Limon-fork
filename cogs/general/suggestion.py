import discord
from discord import ui, app_commands, Embed
from discord.ext import commands
import datetime

class SuggestionModal(ui.Modal, title= "Suggestion"):
    answer = ui.TextInput(
        label = "Enter Your Suggestion",
        style = discord.TextStyle.paragraph,
        placeholder= "What is your suggestion?",
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
            description = "❌ **|** Submission of suggestion failed. Please report this to the developer by coming to our [support server](https://discord.gg/M9S4Gv9Gwe).", 
            color = 0xff3333
        )

        suggestionsChannel = interaction.client.get_channel(1036720085622083705)
        
        try:
            await suggestionsChannel.send(embed = suggestionMessage)
            await interaction.response.send_message("✅ **|** You have successfully submitted your suggestion. Thank you :)", ephemeral = True)
        except:
            await interaction.response.send_message(embed = failMessage, ephemeral = True)


class Suggestion(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "suggestion", description = "Make a suggestion for Cupcake")
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.user.id))
    async def suggestion(self, interaction: discord.Interaction):
        modal = SuggestionModal()

        await interaction.response.send_modal(modal)
    @suggestion.error
    async def suggestionError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}` and Try Again!")
        else:
            print(f"[SUGGESTION] {error}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Suggestion(bot))
