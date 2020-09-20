import asyncio
import json
import requests
import calendar
import time
from datetime import date, timedelta

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("api_key.txt", "r") as f:
            lines = f.readlines()
            self.key = lines[0].strip()
        self.valid_roles = ["Officer", "Head Officer", "External"]


    @commands.command()
    async def daily(self, ctx, past=1):
        await ctx.send("Update daily gexp!")

        cond1 = ctx.message.author.id == 166305040774987776
        author_roles = [y.name.lower() for y in ctx.message.author.roles]
        cond2 = any(role.lower() in author_roles for role in self.valid_roles)
        if not (cond1 or cond2):
            return

        exps = []
        while True:
            try:
                data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
                    .format(self.key, "Salvation")).json()

                members = data["guild"]["members"]

                t = date.today() - timedelta(days=past)
                year = t.year
                month = t.month if t.month>=10 else "0{}".format(t.month)
                day = t.day if t.day>=10 else "0{}".format(t.day)
                yesterday = "{}-{}-{}".format(year, month, day)

                exps = []

                for m in members:
                    print(m["uuid"])
                    print(m["expHistory"])
                    exps.append([m["uuid"], m["expHistory"][yesterday]])

                break
            except KeyError:
                time.sleep(10)


        exps.sort(key=lambda x: x[1], reverse=True)

        desc = ""
        for i in range(20):
            player_data = requests.get("https://api.hypixel.net/player?key={}&uuid={}"
                    .format(self.key, exps[i][0])).json()
            name = player_data["player"]["displayname"]
            line = "{}. {} - {}\n".format(i+1, name, exps[i][1])
            desc += line

        desc = desc.replace("_", "\_")

        date_str = "{} {} {}".format(t.day, calendar.month_name[t.month], t.year)

        embed = Embed(
                    title="Top Guild Experience: {}".format(date_str),
                    description=desc,
                    color=Color.dark_green()
                )

        channel = self.bot.get_channel(702384629847556137)
        await channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Daily(bot))
