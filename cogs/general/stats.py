"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import Embed
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        
    
    @commands.command(hidden = True)
    @commands.is_owner()
    async def stats(self, ctx):

        
        delta = discord.utils.utcnow() - self.bot.uptime
        delta = str(delta).split(".")[0]
        print(delta)
        
        

        
        
        embed = Embed(color = 0xfff48a)
        embed.add_field(name = "Guild Count", value = f"{len(self.bot.guilds)} servers!", inline = True)
        embed.add_field(name = "Uptime", value = f"{delta}s!", inline = True)

        await ctx.send(embed = embed)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))