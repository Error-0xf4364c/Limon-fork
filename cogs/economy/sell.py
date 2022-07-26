import discord
from discord import Embed
from discord.ui import View
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
import yaml
from yaml import Loader
from main import MyBot

message_author_id = []

yaml_file2 = open("yamls/animals.yml", "rb")
animals = yaml.load(yaml_file2, Loader = Loader) 

priceBySize = animals["priceBySize"]
allFishes = animals['fishes']
fishesKey = " ".join(animals["fishes"].keys())
fishes = fishesKey.split(" ")

allHunts = animals["hunts"]
huntsKey = " ".join(animals["hunts"].keys())
hunts = huntsKey.split(" ")

bott = MyBot()

# Emojis
yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader) 
clock = emojis["clock"] or "⏳"
dot3 = emojis["3dot"]
check = emojis["checkMark"]

class MyButtons(View):


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not interaction.user.id in message_author_id:
            await interaction.response.send_message("Bu pazar senin değil! Bunun üzerinde işlem yapamazsın.", ephemeral=True)
            return False
        return True



    @discord.ui.button(label="Balıkları Sat!", style=discord.ButtonStyle.success, custom_id="sellfishes")
    async def sellfishes_callback(self, interaction, button):
        db = bott.mongoConnect["cupcake"]
        collection = db["inventory"]
        coincollection = db['economy']
        user_data = await collection.find_one({"_id": interaction.user.id})
        user_data_coins = await coincollection.find_one({"_id": interaction.user.id})

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Önce **`/wallet`** komutunu kullanarak bir cüzdan oluşturmalısın.", ephemeral=True)


        if not 'fishes' in user_data:
            button.label = "Balık Yok!"
            button.disabled = True
            button.style = discord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            await interaction.response.send_message("Envanterinizde hiç balık yok. Biraz balık tutun! **`/fishing`**", ephemeral=True)
            return
        elif len(user_data['fishes']) == 0:
            button.label = "Balık Yok!"
            button.disabled = True
            button.style = discord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            await interaction.response.send_message("Envanterinizde hiç balık yok. Biraz balık tutun! **`/fishing`**",ephemeral=True)
            return

        sum_fish = 0

        userFishes = list(user_data['fishes'].keys())
        for i in user_data['fishes'].values():
            sum_fish += (i * priceBySize)
        for x in fishes:
            if x in userFishes:
                sum_fish += allFishes[x]

        button.label = "Balıklar Satıldı!"
        button.style = discord.ButtonStyle.secondary
        button.disabled = True

        
        del user_data['fishes']
        user_data_coins['coins'] += sum_fish
        await coincollection.replace_one({"_id": interaction.user.id}, user_data_coins)
        await collection.replace_one({"_id": interaction.user.id}, user_data)
        await interaction.response.edit_message(view=self)
        await interaction.response.send_message(f"🐟 **|** Balıklarınızı başarıyla sattınız. Toplam geliriniz **{sum_fish}** Cupcoin")



        

    @discord.ui.button(label="Avları  Sat!", style=discord.ButtonStyle.success, custom_id="sellhunts")
    async def sellhunts_callback(self, interaction, button):
        db = bott.mongoConnect["cupcake"]
        collection = db["inventory"]
        coincollection = db['economy']
        user_data = await collection.find_one({"_id": interaction.user.id})
        user_data_coins = await coincollection.find_one({"_id": interaction.user.id})

        if await collection.find_one({"_id": interaction.user.id}) == None:
            return await interaction.response.send_message("Önce **`/wallet`** komutunu kullanarak bir cüzdan oluşturmalısın.", ephemeral=True)

        if not 'hunts' in user_data:
            button.label = "Av Yok!"
            button.disabled = True
            button.style = discord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            await interaction.response.send_message(content="Envanterinizde hiç av yok. Biraz avlanın! **`/hunt`**",ephemeral=True)
            return
        elif len(user_data['hunts']) == 0:
            button.label = "Av Yok!"
            button.disabled = True
            button.style = discord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            await interaction.response.send_message(content="Envanterinizde hiç av yok. Biraz avlanın! **`/hunt`**",ephemeral=True)
            return

        sum_hunt = 0

        userHunts = user_data['hunts']
        for x in hunts:
            if x in userHunts:
                sum_hunt += allHunts[x]

        button.label = "Avlar Satıldı!"
        button.style = discord.ButtonStyle.secondary
        button.disabled = True

        del user_data['hunts']
        user_data_coins['coins'] += sum_hunt
        await coincollection.replace_one({"_id": interaction.user.id}, user_data_coins)
        await collection.replace_one({"_id": interaction.user.id}, user_data)
        await interaction.response.edit_message(view=self)
        await interaction.response.send_message(content=f"🦌 **|** Avladığınız hayvanları başarıyla sattınız. Toplam geliriniz **{sum_hunt}** Cupcoin")


        
        

    @discord.ui.button(label="Pazarı Kapat", style=discord.ButtonStyle.danger, custom_id="closemenu")
    async def closemenu_callback(self, interaction, button):
        await interaction.response.send_message(content=f"{dot3} **|** Pazar kapatılıyor...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.edit_original_message(content=f"{check} **|** Pazar başarıyla kapatıldı.")
        await interaction.message.delete()
        message_author_id.remove(interaction.user.id)



class sell(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    

    @app_commands.command(name="sell", description="Avladığın hayvanları sat ve Cupcoin kazan")
    @app_commands.checks.cooldown(
        1, 1800, key=lambda i: (i.guild_id, i.user.id))
    async def sell(self, interaction: discord.Interaction):

        db = self.bot.mongoConnect["cupcake"]
        collection = db["inventory"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Envanteriniz bulunmuyor! Satmak için hayvan avlayın.")

        userData = await collection.find_one({"_id" : interaction.user.id})
        
        sumFish = 0
        numberFish = 0
        embed_value_fishes = "Envanterinizde balık bulunamadı."

        sumHunt = 0
        numberHunt = 0
        embed_value_hunts = "Envanterinizde av bulunamadı."

        if 'fishes' in userData and len(userData['fishes']) > 0:
            userFishes = list(userData['fishes'].keys())
            for i in userData['fishes'].values():
                sumFish += (i*priceBySize)
            for x in fishes:
                if x in userFishes:
                    sumFish += allFishes[x]
            numberFish = len(userData['fishes'])
            embed_value_fishes = f"**{numberFish}** adet balığınız var. Toplam = **{sumFish}** Cupcoin ediyor."

        if 'hunts' in userData and len(userData['hunts']) > 0:
            userHunts = userData['hunts']
            for x in hunts:
                if x in userHunts:
                    sumHunt += allHunts[x]
            numberHunt = len(userData['hunts'])
            embed_value_hunts = f"**{numberHunt}** adet avınız var. Toplam = **{sumHunt}** Cupcoin ediyor."

        if interaction.user.id in message_author_id:
            return await interaction.response.send_message("Zaten açılmış bir pazarınız var. Önce onu kapatınız", ephemeral=True)
        message_author_id.append(interaction.user.id)



        menuEmbed = Embed(description = f"Merhaba 👋 Pazara hoş geldin. Burada tuttuğun balıkları ve avladığın hayvanları satabilirsin. İşte senin envanterin:")
        menuEmbed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar.url)
        menuEmbed.add_field(name = "Fishes:", value =  embed_value_fishes)
        menuEmbed.add_field(name = "Hunts:", value =  embed_value_hunts)
        menuEmbed.set_footer(text = "Pazarını kapatmayı unutma! Bir pazarı kapatmadan yeni bir pazar açamazsın.", icon_url= "https://cdn.discordapp.com/attachments/970118423143120896/1000526619691200522/dikkat.png")


        view = MyButtons()
        await interaction.response.send_message(embed = menuEmbed, view=view)








    @sell.error
    async def sellError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        
        message_author_id.remove(interaction.user.id)
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"{clock} **|** Upss! Balık pazarı daha açılmamış. `{timeRemaining}`s sonra tekrar gel.",ephemeral=True)
        await interaction.response.send_message("Pazarda ortalık karıştı. Lütfen daha sonra tekrar deneyin! *err!*")

#, guilds= [discord.Object(id =964617424743858176)]
async def setup(bot:commands.Bot):
    await bot.add_cog(sell(bot))