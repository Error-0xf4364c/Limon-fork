import discord
from discord import File, app_commands
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
import asyncio
import datetime


class MyRank(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name = "rank", description = "Show your rank")
    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.user.id))
    async def rank(self, interaction: discord.Interaction):
        
        db = self.bot.mongoConnect["cupcake"]
        levellingCollection = db["levelling"]
        user = interaction.user

        if await levellingCollection.find_one({"_id" :  interaction.user.id}) == None:
            newLevelData = {
                    "_id" : interaction.user.id,
                    "xp" : 0,
                    "level" : 1
            }
            await levellingCollection.insert_one(newLevelData)

        userData = await levellingCollection.find_one({"_id" :  interaction.user.id})
        
        xp = userData["xp"]
        level = userData["level"]

        nextLevelUp = (level + 1) * 500
        xpNeed = nextLevelUp
        xpHave = userData["xp"]

        percentage = int(((xpHave * 500)/xpNeed))

        background = Editor("pictures/levelCardBackgroundFinal.png")
        profile = await load_image_async(user.avatar.url)

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppinsSmall = Font.poppins(size=30)


        ima =  Editor("pictures/levelBlack.png")
        background.blend(image = ima, alpha =1, on_top = False)

        background.paste(profile.image, (30,30))
        background.rectangle((30, 220), width = 650, height=40, fill = "#ffffff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height = 40,
            percentage=percentage,
            fill = "#0054ff",
            radius = 20,
        )
        background.text((200,40), user.name, font = poppins, color = "#ffffff")

        background.rectangle((200, 100), width = 350, height =2, fill="#ffffff")
        background.text(
            (200,130),
            f"Level: {level} "
            + f"XP : {xp} / {(level+1)*500}",
            font = poppinsSmall,
            color = "#ffffff"
        )
        
        card = File(fp=background.image_bytes, filename="pictures/levelCard.png")

        await interaction.response.defer()
        await asyncio.sleep(4)
        await interaction.followup.send(file =card)

    @rank.error
    async def rankError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}` and Try Again!")
        else:
            print(f"[RANK] {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(MyRank(bot))