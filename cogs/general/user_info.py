import discord
from discord import app_commands
from discord.ext import commands
import datetime
import random
import asyncio

from io import BytesIO
from PIL import Image, ImageChops, ImageDraw, ImageFont

from cogs.ranking.level import Levelling


back1 = Image.open(r"pictures/anime1_background.png").convert("RGBA")
back2 = Image.open(r"pictures/anime2_background.png").convert("RGBA")
back3 = Image.open(r"pictures/anime3_background.png").convert("RGBA")
back4 = Image.open(r"pictures/gaming1_background.png").convert("RGBA")
back5 = Image.open(r"pictures/gaming3_background.png").convert("RGBA")

backgroundList = [back1, back2, back3, back4, back5]

class general(commands.Cog, commands.Bot):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def circle(pfp,size = (215, 215)):
            pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
            
            bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
            mask = Image.new("L", bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill = 255)
            mask = mask.resize(pfp.size, Image.ANTIALIAS)
            mask = ImageChops.darker(mask, pfp.split()[-1])
            pfp.putalpha(mask)
            return pfp

    @app_commands.command(name = "user-info", description = "You view user information")
    @app_commands.describe(user='Select a User')
    @app_commands.guild_only
    @app_commands.checks.cooldown(
        1, 1.0, key=lambda i: (i.guild_id, i.user.id))
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member):
        
        member =  user

        if member.bot == True:
            return await interaction.response.send_message("Bir bot hakkında bilgi edinemezsiniz.", ephemeral = True)

        db = self.bot.mongoConnect["cupcake"]
        collection = db["economy"]
        heroesCollection = db["inventory"]
        levellingCollection = db["levelling"]
        
        userCoins = 0
        userHeroes = 0
        userData = []
        userLevel = 1

        
        if await collection.find_one({"_id": member.id}) != None:
            userData = await collection.find_one({"_id": member.id})
        
        if await levellingCollection.find_one ({"_id": member.id}) != None:
            userLevelData = await levellingCollection.find_one ({"_id": member.id})
            userLevel = userLevelData["level"]
        

        
        
        if "coins" in userData:
            userCoins = userData['coins']

        



        
        name, nick, Id, status = str(member), member.display_name, str(member.id), str(interaction.guild.get_member(member.id).status).upper()

        created_at = member.created_at.strftime("%a %b\n%B %Y")
        joined_at = member.joined_at.strftime("%a %b\n%B %Y")
        money, level = f"{userCoins:,}", str(userLevel)

        base = Image.open(r"pictures/baseEdited.png").convert("RGBA")

        newBackground = random.choice(backgroundList)

        background = newBackground

        pfp = member.avatar.replace(size = 256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")
        name = f"{name[:16]}.." if len(name)>16 else name
        nick = f"AKA - {nick[:16]}.." if len(nick)>16 else f"AKA - {nick}"


        def circle(pfp,size = (215,215)):
            pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
            bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask) 
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(pfp.size, Image.ANTIALIAS)
            mask = ImageChops.darker(mask, pfp.split()[-1])
            pfp.putalpha(mask)
            return pfp


        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, size=(215, 215))
        font = ImageFont.truetype("fonts/Nunito-Regular.ttf", 38)
        akaFont = ImageFont.truetype("fonts/Nunito-Regular.ttf", 30)
        subfont = ImageFont.truetype("fonts/Nunito-Regular.ttf", 25)

        draw.text((280,240), name,font = font)
        draw.text((270, 315), nick,font = akaFont)
        draw.text((65, 490), Id,font = subfont)
        draw.text((405, 490), status,font = subfont)
        draw.text((65, 635), money,font = subfont)
        draw.text((405, 635), level,font = subfont)
        draw.text((65, 770), created_at,font = subfont)
        draw.text((405, 770), joined_at,font = subfont)
        base.paste(pfp, (56,158),pfp)

        background.paste(base, (0,0),base)
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            await interaction.response.defer()
            await asyncio.sleep(4)
            await interaction.followup.send(content= None, file = discord.File(a, "profile.png"))


    @userinfo.error
    async def userinfoError(self, interaction : discord.Interaction,error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds = int(error.retry_after)))
            await interaction.response.send_message(f"Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                                                    ephemeral=True)
        else:
            print(error)


async def setup(bot:commands.Bot):
    await bot.add_cog(general(bot))

