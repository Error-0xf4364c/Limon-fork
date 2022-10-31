import asyncio
import datetime

import discord
import yaml
from discord import Embed, app_commands
from discord.ext import commands
from discord.ui import View, button
from yaml import Loader

from main import MyBot

fighters = {}


class Start_Battle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "battle", description = "Invite battle your friend")
    @app_commands.describe(enemy = "Select Enemy")
    async def battle(self, interaction: discord.Interaction, enemy = discord.User):

        database = self.bot.mongoConnect["cupcake"]
        battle_collection = database["battle"]
        inventory_collection = database["inventory"]

        user = interaction.user

        if enemy.bot:
            return await interaction.response.send_message(content ="🤖 **| Your enemy cannot be a bot! |** ❌", ephemeral = True)

        if enemy == user:
             return await interaction.response.send_message(content ="❌ **| You can't be an enemy to yourself!**", ephemeral = True)
        

        # Database Check

        if await inventory_collection.find_one({ "_id" : user.id}) == None:
            return await interaction.response.send_message(content ="🗡️ **| You have no weapon! |** ❌", ephemeral = True)
        
        if await inventory_collection.find_one({ "_id" : enemy.id}) == None:
            return await interaction.response.send_message(content ="🗡️ **| Your enemy have no weapon! |** ❌", ephemeral = True)
        
        enemy_inventory = await inventory_collection.find_one({ "_id" : enemy.id})
        user_inventory = await inventory_collection.find_one({ "_id" : user.id})

        user_items = user_inventory["items"]
        enemy_items = enemy_inventory["items"]

        if ("sword" not in user_items) or ("sword" not in enemy_items):
            return await interaction.response.send_message(content = "🗡️ **| Your enemy have no weapon or You have no weapon! |** ❌", ephemeral = True)


        if await battle_collection.find_one({ "_id" : user.id}) == None:
            new_data = {
                "_id" : user.id,
                "in_battle" : False
            }

            await battle_collection.insert_one(new_data)


        fighters[enemy.id] = user.id

        
        
        