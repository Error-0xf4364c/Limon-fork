import discord
from discord import Embed, app_commands
from discord.ext import commands
import datetime


class ShowLeaderboard(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @app_commands.command(name = "leaderboard", description = "The level shows the leader board") #
    @app_commands.guild_only
    async def leaderboard(self, interaction: discord.Interaction):
        
        db = self.bot.mongoConnect["cupcake"]
        levellingCollection = db["levelling"]


        #async for x in levellingCollection.find():
        #    print(x["_id"])
            
        
        rangeNum = 5
        l = {}
        totalXp = []

        async for userData in levellingCollection.find():
            xp = int(userData["xp"]) + int(userData["level"] * 500)
            l[xp] = f"{userData['_id']}:{userData['xp']}:{userData['level']}"
            totalXp.append(xp)

        totalXp = sorted(totalXp, reverse = True)
        index = 1

        leaderboard_message = Embed(
            title = "═════Leaderboard═════" #════════════Leaderboard════════════
        )

        for amt in totalXp:
            id_ = l[amt].split(":")[0]
            xp = l[amt].split(":")[1]
            level = l[amt].split(":")[2]

            member = await self.bot.fetch_user(id_)

            if member is not None:
                name = member.name
                leaderboard_message.add_field(
                    name = f"{index}. {name}",
                    value = f"**Level: {level} | XP: {xp}**",
                    inline = False
                )
                if index == rangeNum:
                    break
                else:
                    index += 1

        await interaction.response.send_message(embed = leaderboard_message)

    @leaderboard.error
    async def leaderboardError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            timeRemaining = str(datetime.timedelta(seconds=int(error.retry_after)))
            await interaction.response.send_message(f"Please wait `{timeRemaining}` and Try Again!")
        else:
            print(f"[LEADERBOARD] {error}")
# , guilds= [discord.Object(id =964617424743858176)]
async def setup(bot: commands.Bot):
    await bot.add_cog(ShowLeaderboard(bot))