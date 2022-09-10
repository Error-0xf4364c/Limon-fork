import discord
from discord import Embed
from discord.ui import View, Button
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import datetime
import yaml
from yaml import Loader


yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"
settings = emojis["settings"] or "🔧"

        

class Help(commands.Cog, commands.Bot):
    

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="bot-help",
        description="Don't you know what's what?")
    @app_commands.describe(topic = "Choose a topic")
    @app_commands.choices(topic=[
        Choice(name="Basic Commands", value="basiccommandshelp"),
        Choice(name="Gamble", value="gamblecommands"),
        Choice(name="Hunting", value="huntingcommands"),
        Choice(name="Badges", value="badgescommands"),
        Choice(name="Heroes", value="heroescommands"),
        Choice(name="Ranking", value="rankingsystem")

    ])
    @app_commands.checks.cooldown(
        1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def bothelp(self, interaction: discord.Interaction, topic: str):
        SupportServerButton = Button(label="Support Server", style=discord.ButtonStyle.link, url="https://discord.gg/M9S4Gv9Gwe", emoji=settings)
        view = View()
        view.add_item(SupportServerButton)

        if topic == "basiccommandshelp":
            commandsEmbed = Embed(description = """
            ```Basic commands of Cupcake```\n
            **/wallet** **››** You view your wallet.
            **/daily** **››** You can earn your daily cupcoin.
            **/inventory** **››** You view your inventory.
            **/send** **››** You can send cupcoin to your friends.
            **/user-info** **››** You view any user's information.
            **/suggestion **››** Make a suggestion for Cupcake.
            **/report** **››** Report Bugs/Errors
            **/vote** **››** Vote Cupcake on Top.gg
            """ )
            commandsEmbed.set_author(name = "About the commands", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=commandsEmbed, view=view)

        elif topic == "gamblecommands":
            gamblesEmbed = Embed(description = """
            ```Gambles with Cupcake```\n
            **/coinflip** **››** You can play coin flip.
            **/roll** **››** Guess the sum of 2 dice in odd or even.
            **/guess-number** **››** Guess the number and win exactly 5 times Cupcoin.
            **/open-box** **››** Open one of the 5 different safes and get rich.""" )
            gamblesEmbed.set_author(name = "About the gambles", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=gamblesEmbed, view=view)
        elif topic == "huntingcommands":
            huntingEmbed = Embed(description = """
            ```Hunting with Cupcake```\n
            **/hunt** **››** Hunt animals.
            **/fishing** **››** Fishing.
            **/forestry** **››** Cut down the tree
            **/mining** **››** Digging and earn valuable mines
            **/store** **››** Buy items and start working!
            **/inventory** **››** View your fishes and hunts.
            **/sell** **››** You can sell your fishes and hunts""")
            huntingEmbed.set_author(name = "About the hunting", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=huntingEmbed, view=view)
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
            await interaction.response.send_message(embed=badgesEmbed, view=view)
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
            await interaction.response.send_message(embed=heroesEmbed, view=view)

        elif topic == "rankingsystem":
            rankingEmbed = Embed(description = """
            ```How to raise my level```
            You can talk with your friends on chat channels to raise your level.
            ```How can i learn my level```
            **/rank** **››** Shows your level card
            **/leaderboard** **››** Shows the top 5 in the ranking
            """)
            rankingEmbed.set_author(name = "About the ranking system", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=rankingEmbed, view=view)
    @bothelp.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):

        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Please wait`{timeRemaining}`s try again!",ephemeral=True)



async def setup(bot:commands.Bot):
    await bot.add_cog(Help(bot))

