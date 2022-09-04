import discord
from discord import app_commands, File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
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
        
async def setup(bot:commands.Bot):
    await bot.add_cog(Levelling(bot), guilds= [discord.Object(id =964617424743858176)])