import discord
from discord import Embed
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import datetime
import yaml
from yaml import Loader


yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"

class help(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="bot-help",
        description="Bot hakkında bilgi edin!")
    @app_commands.describe(topic = "Choose a topic")
    @app_commands.choices(topic=[
        Choice(name=f"Basic Commands", value="basiccommandshelp"),
        Choice(name=f"Gamble", value="gamblecommands"),
        Choice(name=f"Hunting", value="huntingcommands"),
        Choice(name=f"Badges", value="badgescommands"),
        Choice(name=f"Heroes", value="heroescommands")

    ])
    @app_commands.checks.cooldown(
        1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def bothelp(self, interaction: discord.Interaction, topic: str):

        if topic == "basiccommandshelp":
            commandsEmbed = Embed(description = """
            ```Basic commands of Cupcake```\n
            **/wallet** **››** You view your wallet.
            **/daily** **››** You can earn your daily cupcoin.
            **/inventory** **››** You view your inventory.
            **/send** **››** You can send cupcoin to your friends.
            **/user-info** **››** You view any user's information.""" )
            commandsEmbed.set_author(name = "About the commands", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=commandsEmbed)

        elif topic == "gamblecommands":
            gamblesEmbed = Embed(description = """
            ```Gambles with Cupcake```\n
            **/coinflip** **››** You can play coin flip.
            **/roll** **››** Guess the sum of 2 dice in odd or even.
            **/guess-number** **››** Guess the number and win exactly 5 times Cupcoin.
            **/open-box** **››** Open one of the 5 different safes and get rich.""" )
            gamblesEmbed.set_author(name = "About the gambles", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=gamblesEmbed)
        elif topic == "huntingcommands":
            huntingEmbed = Embed(description = """
            ```Hunting with Cupcake```\n
            **/hunt** **››** Hunt animals.
            **/fishing** **››** Fishing.
            **/inventory** **››** View your fishes and hunts.
            **/sell** **››** You can sell your fishes and hunts""")
            huntingEmbed.set_author(name = "About the hunting", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=huntingEmbed)
        elif topic == "badgescommands":
            badgesEmbed = Embed(description = """
            ```What are badges?```\n
            In a certain area (hunting, gambling, etc.) too much is given to interested users. 
            It consists of 3 levels.Beginner, amateur and master. Except for hero owners and wonderful people badges
            \n
            ```How will I get a badge?```\n
            You can get a gambler's badge by gambling. 
            You can get a hunter badge by hunting animals. 
            You can get a fisherman's badge by fishing. 
            3 as a hero owner, you can get a hero owner badge. 
            You can get a great person badge by sending Cupcoin to your friends.
            """)
            badgesEmbed.set_author(name = "About the badges", icon_url = interaction.user.avatar.url)
            badgesEmbed.set_image(url="https://cdn.discordapp.com/attachments/899751701077164043/1001246682215878666/unknown.png")
            await interaction.response.send_message(embed=badgesEmbed)
        elif topic == "heroescommands":
            heroesEmbed = Embed(description = """
            ```Heroesof with Cupcake```\n
            **/hero-egg** **››** Open hero eggs and have one of them.
            **/inventory** **››** You can view your heroes here for now.
            \n```Why should I get a hero?```\n
            Actually, you can think of it as a pre-registration. 
            When you have a hero, you read his short story. 
            You will learn the HP and Power values. You will learn about the degree of rarity. 
            In the future, there will always be a command for your heroes, where you can get information.
             You will be able to make heroes fight. You'll be able to trade them and sell them. 
             You can't have the same hero 2 times. You can buy eggs, but inside some eggs may be empty
            """)
            heroesEmbed.set_author(name = "About the heroes", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=heroesEmbed)

    @bothelp.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):

        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Upss! Balık pazarı daha açılmamış. `{timeRemaining}`s sonra tekrar gel.",ephemeral=True)



async def setup(bot:commands.Bot):
    await bot.add_cog(help(bot))

