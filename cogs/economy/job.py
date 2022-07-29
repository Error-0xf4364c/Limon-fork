import discord
from discord import app_commands, Embed
from discord.ui import View, Select
from discord.ext import commands
import datetime
import yaml
from yaml import Loader
from main import MyBot
"""
# Main Class
client = MyBot()

# Get Jobs
yaml_file = open("yamls/jobs.yml", "rb")
jobs = yaml.load(yaml_file, Loader = Loader)

# Extract
allJobs = jobs['jobs']
jobsKey = " ".join(jobs["jobs"].keys())
job = jobsKey.split(" ")

# Get Emojis
yaml_file = open("yamls/emojis.yml", "rb")
emojis = yaml.load(yaml_file, Loader = Loader)
clock = emojis["clock"] or "⏳"


# Buttons Class
class JobsMenu(View):

    for i in list(job):
        print(i)

    @discord.ui.select(
        placeholder="Choose a job!",
        options = [
            discord.SelectOption(
                label = i["name"],
                value = i
            )

    ]
        )
    async def jobs_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        db = client.mongoConnect["cupcake"]
        collection = db["economy"]

        if await collection.find_one({"_id" : interaction.user.id}) == None:
            return await interaction.response.send_message("Önce `/wallet` komutunu kullanarak bir cüzdan oluşturun", ephemeral = True)

        user_data = await collection.find_one({"_id" : interaction.user.id})

        if "jobs" in user_data and select.values != "quitjob":
            return await interaction.response.send_message("Yeni bir iş almak için önce mevcut işinizi bırakmalısınız.", ephemeral = True)


        elif "jobs" not in user_data:
            job_data = {"$set": {"jobs": []}}
            await collection.update_one(user_data, job_data)

        user_data = await collection.find_one({"_id" : interaction.user.id})

        user_data["jobs"].append(select.values)
        await collection.replace_one({"_id": interaction.user.id}, user_data)




"""
class Profession(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="jobs", description="Choose a Job. Get Paid Every Day")
    @app_commands.checks.cooldown(
        1, 1800, key=lambda i: (i.guild_id, i.user.id))
    async def jobs(self, interaction: discord.Interaction):

        #view = JobsMenu()

        await interaction.response.send_message(content = "Demo")

    @jobs.error
    async def jobsError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(
                f"{clock} **|** Lütfen `{timeRemaining}`s sonra tekrar deneyiniz.",
                ephemeral=True)
        await interaction.response.send_message("Bir hata oluştu lütfen daha sonra tekrar deneyiniz.")
        print(f"[JOBS] {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Profession(bot))

