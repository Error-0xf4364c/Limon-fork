import discord
from discord import app_commands, File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
import asyncio
import datetime
import yaml
from yaml import Loader

yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader)
up = emojis["up"]

levelList = ["level-5+", "level-10+", "level-15+", "level-20+", "level-25+", "level-30+", "level-35+", "level-40+", "level-45+", "level-50+"]

levelNum = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


class Levelling(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        
        if not ctx.author.bot:
            db = self.bot.mongoConnect["cupcake"]
            levellingCollection = db["levelling"]
            coinCollection = db["economy"]

            if await levellingCollection.find_one({"_id" :  ctx.author.id}) == None:
                newLevelData = {
                    "_id" : ctx.author.id,
                    "xp" : 0,
                    "level" : 1
                }
                await levellingCollection.insert_one(newLevelData)
            
            userData = await levellingCollection.find_one({"_id" :  ctx.author.id})
            

            xp = userData["xp"]
            level = userData["level"]
    
            increasedXp = xp + 25
            newLevel = int(increasedXp / 500)

            userData["xp"] = increasedXp
            await levellingCollection.replace_one({"_id" : ctx.author.id}, userData)

            for i in range(len(levelList)):
                if newLevel == levelNum[i]:
                    userWallet = await coinCollection.find_one({"_id" :  ctx.author.id})
                    levelGift = int(newLevel) * 1000
                    userWallet["coins"] += levelGift
                    await coinCollection.replace_one({"_id" : ctx.author.id}, userWallet)
                    await ctx.channel.send(content = f"{up} **| {ctx.author.name}** Just leveled up __**{newLevel}**__!!! You won **{levelGift:,}** Cupcoin!")
                    
                    userData["level"] = newLevel
                    userData["xp"] = 0
                    await levellingCollection.replace_one({"_id" : ctx.author.id}, userData)
                    return

            if newLevel > level:
                await ctx.channel.send(f"{up} **| {ctx.author.name}** Just leveled up __**{newLevel}**__!!! ")

                userData["level"] = newLevel
                userData["xp"] = 0
                await levellingCollection.replace_one({"_id" : ctx.author.id}, userData)


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
        
async def setup(bot:commands.Bot):
    await bot.add_cog(Levelling(bot), guilds= [discord.Object(id =964617424743858176)])