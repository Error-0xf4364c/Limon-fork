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
    
    @ui.button(label = "Katıl", style = discord.ButtonStyle.blurple, emoji = "🎉")
    async def join_callback(self, interaction, button):
        db = client.database["limon"]
        collection = db["giveaway"]
        
        data = collection.find_one({"_id" : interaction.guild.id})
        
        participants = data["participants"]
        
        if interaction.user.id in participants:
            return await interaction.response.send_message(content = "Çekilişe zaten katılmışsınız.", ephemeral = True)
        
        participants.append(interaction.user.id)
        
        collection.replace_one({"_id" : interaction.guild.id}, data)
        
        await interaction.response.send_message(content = "Çekilişe başarıyla katıldınız.", ephemeral = True)
        
        
        



class GiveawayModal(ui.Modal, title= "Çekiliş"):
    
    g_title = ui.TextInput(
        label = "Başlık",
        style = discord.TextStyle.short,
        placeholder = "Çekiliş Başlığı",
        required = True,
        max_length= 100
    )
    description = ui.TextInput(
        label = "Açıklama",
        style = discord.TextStyle.paragraph,
        placeholder = "Çekiliş hakkında bilgi verin",
        required = False,
        max_length= 4000
    )
    g_time = ui.TextInput(
        label = "Bitiş tarihi",
        style = discord.TextStyle.short,
        placeholder = "Çekilişin bitiş zamanını ayarlayın. (s/m/h/d) Ör. : 10h",
        required = True,
        max_length = 50
    )
    price = ui.TextInput(
        label = "Ödül",
        style = discord.TextStyle.short,
        placeholder = "Çekilişte vereceğiniz ödül",
        required = True,
        max_length = 100
    )
    winner_count = ui.TextInput(
        label = "Kazanan Sayısı",
        style = discord.TextStyle.short,
        placeholder = "Çekilişi kazanacak kişi sayısı",
        required = True,
        max_length = 2
    )

    async def on_submit(self, interaction: discord.Interaction):
        
        w_c = str(self.winner_count)
        gtime = str(self.g_time)
        
        if not w_c.isnumeric():
            return await interaction.response.send_message(content = "Kazanan sayısı tamsayı olmalıdır!", ephemeral = True)

        

        
        waiting_time = ""
        
        if gtime[-1] == "s":
            waiting_time = "saniye"
        elif gtime[-1] == "m":
            waiting_time = "dakika"
        elif gtime[-1] == "h":
            waiting_time = "saat"
        elif gtime[-1] == "d":
            waiting_time = "gün"
            
        buttons = GiveawayButton()

        time = convert(str(self.g_time))


        giveaway_message = Embed(
            title = self.g_title,
            description = self.description,
            color = 0x2E3136
        )
        giveaway_message.add_field(name = "Kazanan Sayısı", value = self.winner_count, inline = True)
        giveaway_message.add_field(name = "Ödül", value = self.price, inline = True)
        giveaway_message.set_footer(text = f"{interaction.user} tarafından - Bitiş: {gtime} {waiting_time}", icon_url = interaction.client.user.avatar.url)

        await interaction.response.send_message(embed = giveaway_message, view = buttons)
        
            
        await asyncio.sleep(time)
        
        db = client.database["limon"]
        collection = db["giveaway"]
        
        data = collection.find_one({"_id" : interaction.guild.id})
        participants = data["participants"]
        
        if participants == []:
            await interaction.edit_original_response(content = f"❌ **| Çekiliş iptal edildi. Sebebi şu olabilir:**\n`Yetersiz katılımcı`\nveya\n⏳ `| Geçersiz bitiş tarihi`")
            collection.delete_one({"_id" : interaction.guild.id})
            try:
                user_send_embed = Embed(description = f"**{interaction.guild.name}** adlı sunucudaki **{self.g_title}** başlıklı çekişiniz yetersiz katılımcı sebebiyle iptal edildi.", color = 0xfa4b4b)

                await interaction.user.send(embed = user_send_embed)
            except:
                return

        winners = []
        winner_count = 0

        
        while winner_count < int(str(self.winner_count)):

            winner = random.choice(participants)
            winner_count += 1
            
            if winner in winners:
                continue
            
            winners.append(winner)
            
        
        if len(winners) == 1:
           winners = f"<@{winner}>"
        else:
            winners = " - ".join([f"<@{w}>" for w in winners])
        
        giveaway_end_message = Embed(
            title = f"(Bitti !!!) { self.g_title}",
            url = "https://discord.com/api/oauth2/authorize?client_id=994143430504620072&permissions=139586817088&scope=bot%20applications.commands",
            description = self.description,
            color = 0x2E3136
        )
        giveaway_end_message.add_field(name = "Kazananlar", value = winners, inline = True)
        giveaway_end_message.add_field(name = "Ödül", value = self.price, inline = True)
        giveaway_end_message.set_footer(text = f"{interaction.user} tarafından - Bitti",icon_url = interaction.client.user.avatar.url)

        await interaction.edit_original_response(content = f"Çekilişi Kazananlar: {winners}", embed = giveaway_end_message, view = None)
        collection.delete_one({"_id" : interaction.guild.id})

class Giveaway(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "giveaway", description = "Hemen bir çekiliş yapın")
    async def giveaway(self, interaction: discord.Interaction):
        
        db = self.bot.database["limon"]
        collection = db["giveaway"]
        
        if collection.find_one({"_id" : interaction.guild.id}) == None:
            new_data = {
                "_id" : interaction.guild.id,
                "participants" : []
                
            }
            collection.insert_one(new_data)
        
        
        modal = GiveawayModal()
    
        await interaction.response.send_modal(modal)
        
    @giveaway.error
    async def giveawayError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"[GIVEAWAY] {error} ")
async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))
