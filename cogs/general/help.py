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
support_url = "https://discord.gg/8YX57rBGTM"

        

class Help(commands.Cog, commands.Bot):
    

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="bot-help",
        description="Ne nedir?")
    @app_commands.describe(topic = "Choose a topic")
    @app_commands.choices(topic=[
        Choice(name="Temel Komutlar", value="basiccommandshelp"),
        Choice(name="Kumar", value="gamblecommands"),
        Choice(name="İşler", value="huntingcommands"),
        Choice(name="Rozetler", value="badgescommands"),
        Choice(name="Kahramanlar", value="heroescommands"),

    ])
    @app_commands.checks.cooldown(
        1, 10, key=lambda i: (i.guild_id, i.user.id))
    async def bothelp(self, interaction: discord.Interaction, topic: str):
        SupportServerButton = Button(label="Support Server", style=discord.ButtonStyle.link, url=support_url, emoji=settings)
        view = View()
        view.add_item(SupportServerButton)

        if topic == "basiccommandshelp":
            commandsEmbed = Embed(description = """
            ```Cupcake'in Temel Komutlar```\n
            **/wallet** **››** Cüzdanınızı açın.
            **/daily** **››** Günlük Cupcoin kazanın.
            **/inventory** **››** Envanterinizi Görüntüleyin.
            **/send** **››** Arkadaşlarınıza Cupcoin gönderin.
            **/user-info** **››** Kullanıcılar hakkında bilgi edinin.
            **/suggestion **››** Cupcake için bir öneride bulunun.
            **/report** **››** Hataları bildirin.
            **/vote** **››** Cupcake'e Top.gg üzerinden oy verin.
            """ )
            commandsEmbed.set_author(name = "Komutlar hakkında", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=commandsEmbed, view=view)

        elif topic == "gamblecommands":
            gamblesEmbed = Embed(description = """
            ```Kumar```\n
            **/coinflip** **››** Yazı tura atın. Yazı gelirse siz, tura gelirse kasa kazanır.
            **/roll** **››** 2 zarın toplam sonucunun tek mi, çift mi olduğunu tahmin edin.
            **/guess-number** **››** 1 ile 10 arasındaki rakamı tahmin edin ve paranızı 5'e katlayın.
            **/open-box** **››** 5 farklı kasadan bütçenize uygun olanı açın ve zengin olun.""" )
            gamblesEmbed.set_author(name = "Kumar hakkında", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=gamblesEmbed, view=view)
        elif topic == "huntingcommands":
            huntingEmbed = Embed(description = """
            ```İşler```\n
            **/hunting** **››** Hayvan avlayın ve onları satarak Cupcoin kazanın.
            **/fishing** **››** Balık tutun ve onları satarak Cupcoin kazanın.
            **/forestry** **››** Odun kesin ve onları satarak Cupcoin kazanın.
            **/mining** **››** Madene girin ve değerli madenler çıkarın
            **/store** **››** İşe başlamak için ekipman satın alın!
            **/inventory** **››** İşlerden kazandıklarını ve ekipmanlarınızı görüntüleyin.
            **/sell** **››** İşlerden kazandıklarınızı satın.""")
            huntingEmbed.set_author(name = "İşler hakkında", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=huntingEmbed, view=view)
        elif topic == "badgescommands":
            badgesEmbed = Embed(description = """
            ```Rozetler nedir?```\n
            Bir iş yaptığınızda, kumar oynadığınızda, arkadaşınıza Cupcoin gönderdiğinizde sahip olabileceğiniz,
            toplam 3 farklı seviyesi (acemi, amatör ve usta) bulunan ve envanterinizde görünen sizin bir konuda ne kadar iyi olduğunuzu gösteren bir çeşit madalya 
            \n
            ```Peki nasıl rozet alabilirim??```\n
            Kumar oynayarak **Kumarbaz** rozeti kazanabilirsiniz. 
            Avcılık yaparak **Avcı** rozeti kazanabilirsiniz. 
            Balıkçılık yaparak **Balıkçı** rozeti kazanabilirsiniz. 
            En az 3 kahraman sahip olarak **Kahraman Sahibi** rozeti kazanabilirsiniz. 
            Arkadaşlarınıza Cupcoin göndererek **İyi İnsan** rozeti kazanabilirsiniz.
            """)
            badgesEmbed.set_author(name = "Rozetler hakkında", icon_url = interaction.user.avatar.url)
            badgesEmbed.set_image(url="https://cdn.discordapp.com/attachments/899751701077164043/1001246682215878666/unknown.png")
            await interaction.response.send_message(embed=badgesEmbed, view=view)
        elif topic == "heroescommands":
            heroesEmbed = Embed(description = """
            ```Kahramanlar```\n
            **/hero-egg** **››** Bir yumurta açın ve kahraman sahibi olun. Bazı yumurtalar boş olabilir
            **/inventory** **››** Kahramanlarınızı envanterinizde görüntüleyebilirsiniz.
            \n```Neden bir kahraman sahibi olmalıyım?```\n 
            Yumurtadan bir kahraman çıkardığınız zaman onun hikayesini okuyabilirsiniz. 
            Can, nadirlik ve güç değerlerini öğrenebilirsiniz.
            Yakında onları savaştırabilecek ve başkasıyla kahraman takası yapabileceksiniz. 
            Aynı kahramana 2 kez sahip olamazsınız. Bir yumurta satın alın ve kahraman sahibi olun
            """)
            heroesEmbed.set_author(name = "Kahramanlar hakkında", icon_url = interaction.user.avatar.url)
            await interaction.response.send_message(embed=heroesEmbed, view=view)

    @bothelp.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):

        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Lütfen `{timeRemaining}`s bekleyin!",ephemeral=True)



async def setup(bot:commands.Bot):
    await bot.add_cog(Help(bot))

