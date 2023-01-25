"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import Embed, app_commands
from discord.ui import View, Button
from discord.ext import commands


class MessageContent(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == "<@994143430504620072>":

            #* Button
            view = View()

            supportServerButton = Button(label="Destek", style=discord.ButtonStyle.link, url="https://discord.gg/8YX57rBGTM")
            inviteButton = Button(label="Davet Et", style=discord.ButtonStyle.link, url="https://discord.com/api/oauth2/authorize?client_id=994143430504620072&permissions=139586817088&scope=bot%20applications.commands")

            view.add_item(supportServerButton)
            view.add_item(inviteButton)

            #* Embed
            aboutMe = Embed(
                description = f"👋 **Merhaba {ctx.author.name}**.\n\n __Eğik Çizgi Komutlarını__ kullanabilirsiniz. Temel Komutlar, kahramanlar, rozetler, vs. için **`/bot-help`** komutunu kullanınız.\n😉 *Hesabını aç. Belki bir hediye vardır* => </balance:1066377456015134790>",
                color = 0xf182ff
                )
            aboutMe.set_author(name = f"{self.bot.user.name} | Hadi Başla", url = "https://discord.gg/8YX57rBGTM", icon_url = self.bot.user.avatar.url)
            
            #* Send Message
            await ctx.channel.send(embed = aboutMe, view = view)
            


async def setup(bot:commands.Bot):
    await bot.add_cog(MessageContent(bot))
