import discord
from discord import ui, app_commands, Embed
from discord.ext import commands
from main import MyBot
import datetime
import asyncio
import random

client = MyBot()


def convert(time):
    pos = [ "s", "m", "h", "d" ]
    
    time_dict = {
        "s" : 1,
        "m" : 60,
        "h" : 3600,
        "d" : 3600 * 24
    }
    
    unit = time[-1]
    
    if unit not in pos:
        return -1
    
    try:
        val = int(time[:-1])
    except:
        return -2
    
    return val * time_dict[unit]


class GiveawayButton(ui.View):
    
    @ui.button(label = "Join", style = discord.ButtonStyle.blurple, emoji = "🎉")
    async def join_callback(self, interaction, button):
        db = client.mongoConnect["cupcake"]
        collection = db["giveaway"]
        
        data = await collection.find_one({"_id" : interaction.guild.id})
        
        participants = data["participants"]
        
        if interaction.user.id in participants:
            return await interaction.response.send_message(content = "You have already joined the giveaway.", ephemeral = True)
        
        participants.append(interaction.user.id)
        
        await collection.replace_one({"_id" : interaction.guild.id}, data)
        
        await interaction.response.send_message(content = "You have  joined the giveaway.", ephemeral = True)
        
        
        



class GiveawayModal(ui.Modal, title= "Giveaway"):
    
    g_title = ui.TextInput(
        label = "Title",
        style = discord.TextStyle.short,
        placeholder = "Giveaway Title",
        required = True,
        max_length= 100
    )
    description = ui.TextInput(
        label = "Description",
        style = discord.TextStyle.paragraph,
        placeholder = "Giveaway Description",
        required = False,
        max_length= 4000
    )
    g_time = ui.TextInput(
        label = "End Time",
        style = discord.TextStyle.short,
        placeholder = "The Giveaway End Time (s/m/h/d) Ex. : 10h",
        required = True,
        max_length = 50
    )
    price = ui.TextInput(
        label = "Price",
        style = discord.TextStyle.short,
        placeholder = "The Giveaway Price",
        required = True,
        max_length = 100
    )
    winner_count = ui.TextInput(
        label = "Winner Count",
        style = discord.TextStyle.short,
        placeholder = "The Giveaway Winner Count",
        required = True,
        max_length = 2
    )

    async def on_submit(self, interaction: discord.Interaction):
        
        w_c = str(self.winner_count)
        gtime = str(self.g_time)
        
        if not w_c.isnumeric():
            return await interaction.response.send_message(content = "Winner Count is must be a integer!", ephemeral = True)

        

        
        waiting_time = ""
        
        if gtime[-1] == "s":
            waiting_time = "second"
        elif gtime[-1] == "m":
            waiting_time = "minute"
        elif gtime[-1] == "h":
            waiting_time = "hour"
        elif gtime[-1] == "d":
            waiting_time = "day"
            
        buttons = GiveawayButton()

        time = convert(str(self.g_time))


        giveaway_message = Embed(
            title = self.g_title,
            description = self.description,
            color = 0x2E3136
        )
        giveaway_message.add_field(name = "Number of Winner", value = self.winner_count, inline = True)
        giveaway_message.add_field(name = "Price", value = self.price, inline = True)
        giveaway_message.set_footer(text = f"By {interaction.user} - End: {gtime} {waiting_time}", icon_url = interaction.client.user.avatar.url)

        await interaction.response.send_message(embed = giveaway_message, view = buttons)
        
        
        
        
        
            
        await asyncio.sleep(time)
        
        db = client.mongoConnect["cupcake"]
        collection = db["giveaway"]
        
        data = await collection.find_one({"_id" : interaction.guild.id})
        participants = data["participants"]
        
        if participants == []:
            await interaction.edit_original_response(content = f"❌ **| The Giveaway has been canceled due to**\n**Insufficient Participation**\nor\n⏳ **| Invalid End Time**")
            try:
                interaction.user.send(content = f"Your giveaway on server {interaction.guild.name} has been canceled due to insufficient participation \n`Giveaway Title = {self.g_title}`")
            except:
                return

        winners = []
        winner_count = 0

        
        while winner_count < int(str(self.winner_count)):

            winner = random.choice(participants)
            
            if winner in winners:
                continue
            
            winners.append(winner)
            winner_count += 1

        
        if len(winners) == 1:
           winners = f"<@{winner}>"
        else:
            winners = " - ".join([f"<@{w}>" for w in winners])
        
        giveaway_end_message = Embed(
            title = f"(Ended !!!) { self.g_title}",
            url = "https://discord.com/api/oauth2/authorize?client_id=994143430504620072&permissions=139586817088&scope=bot%20applications.commands",
            description = self.description,
            color = 0x2E3136
        )
        giveaway_end_message.add_field(name = "Winners", value = winners, inline = True)
        giveaway_end_message.add_field(name = "Price", value = self.price, inline = True)
        giveaway_end_message.set_footer(text = f"By {interaction.user} - Ended",icon_url = interaction.client.user.avatar.url)

        await interaction.edit_original_response(content = f"Winners of The Giveaway: {winners}", embed = giveaway_end_message, view = None)
        await collection.delete_one({"_id" : interaction.guild.id})

class Giveaway(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "giveaway", description = "Giveaway")
    async def giveaway(self, interaction: discord.Interaction):
        
        db = self.bot.mongoConnect["cupcake"]
        collection = db["giveaway"]
        
        if await collection.find_one({"_id" : interaction.guild.id}) == None:
            new_data = {
                "_id" : interaction.guild.id,
                "participants" : []
                
            }
            await collection.insert_one(new_data)
        
        
        modal = GiveawayModal()
    
        await interaction.response.send_modal(modal)
        
    @giveaway.error
    async def giveawayError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"[GIVEAWAY] {error} ")
async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))
