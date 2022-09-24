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

            supportServerButton = Button(label="Support Server", style=discord.ButtonStyle.link, url="https://discord.gg/M9S4Gv9Gwe")
            inviteButton = Button(label="Invite Me", style=discord.ButtonStyle.link, url="https://discord.com/api/oauth2/authorize?client_id=994143430504620072&permissions=139586817088&scope=bot%20applications.commands")

            view.add_item(supportServerButton)
            view.add_item(inviteButton)

            #* Embed
            aboutMe = Embed(
                description = f"👋 **Hi {ctx.author.name}**.\n\n You can use __Slash Commands__. Basic commands, heroes, badges, etc. to get information about it, you can use the **`/bot-help`** command.\n😉 *Open your wallet, maybe there's a gift* => **`/wallet`**",
                color = 0xf182ff
                )
            aboutMe.set_author(name = f"{self.bot.user.name} | Get started", url = "https://discord.gg/M9S4Gv9Gwe", icon_url = self.bot.user.avatar.url)
            
            #* Send Message
            await ctx.channel.send(embed = aboutMe, view = view)
            


async def setup(bot:commands.Bot):
    await bot.add_cog(MessageContent(bot))
