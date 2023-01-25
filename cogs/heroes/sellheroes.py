"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import discord
from discord import Embed, app_commands, Interaction
from discord.ext import commands


class SellHeroes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    @app_commands.command(name = "sell-heroes", description = "desc")
    async def sell_heroes(self, interaction: Interaction):
        pass
    
    
    
async def setup(bot:commands.Bot):
    await bot.add_cog(SellHeroes(bot))