#!/usr/bin/env python3


from asyncio import tasks
import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import json
from datetime import datetime

import tools as tools
from tools import addServer, setTime, addCartoon, checkChannel, checkTime, isInToSend, getServerFollowers
from xkcd import getRandomCartoon
from xkcd import update_max_cartoon

MAX_CARTOON = 0


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)
slash = SlashCommand(bot, sync_commands=True)

data = json.load(open('config.json'))


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="."))
    sendCartoon.start()


@slash.slash(name="setChannel", description="set the channel to send the cartoons to")
async def setChannel(ctx: SlashContext, channel: discord.TextChannel, hour: int, minute: int):
    if (ctx.author.id != ctx.guild.owner.id):
        await ctx.send("You are not the owner of this server. Ask the owner to use this command.")
        return
    if addServer(ctx.guild.id) == 0:
        print(f"Create Server: {ctx.guild.id}, {ctx.guild.name}")
    tools.setChannel(ctx.guild.id, channel.id)
    tools.setTime(ctx.guild.id, hour, minute)
    await ctx.send("Channel set to <#" + str(channel.id) + "> successfully.")
    

@slash.slash(name="addCartoon", description="add a new cartoon to the list", options=[create_option(
    name="cartoon",
    description="The name of the cartoon available",
    required=True,
    option_type=3,
    choices=[
        create_choice(name="xkcd", value="xkcd"),
        create_choice(name="Vdm", value="vdm"),
    ]
)])
async def addCartoon(ctx: SlashContext, cartoon: str):
    if (ctx.author.id != ctx.guild.owner.id):
        await ctx.send("You are not the owner of this server. Ask the owner to use this command.")
        return
    if addServer(ctx.guild.id) == 0:
        print(f"Create Server: {ctx.guild.id}, {ctx.guild.name}")
    if checkChannel(ctx.guild.id) == False:
        await ctx.send("Please set a channel to send the news first")
        return
    if (tools.isInServer(ctx.guild.id, cartoon) == False):
        tools.addCartoon(ctx.guild.id, cartoon)
        await ctx.send("Cartoon added successfully.")
    else:
        await ctx.send("Cartoon already in it")


@slash.slash(name="listCartoon", description="List all the cartoons")
async def listFollow(ctx: SlashContext):
    follow = getServerFollowers(ctx.guild.id)
    if len(follow) == 0:
        await ctx.send("No cartoon are being followed")
        return
    embed = discord.Embed(title="Cartoons being followed", color=0x384dc2)
    
    for i in range(len(follow)):
        embed.add_field(name=str(i+1), value=follow[i], inline=False)
    await ctx.send(embed=embed)

@tasks.loop(minutes=1)
async def sendCartoon():
    data = json.load(open('data.json'))
    for server in data:
        srv = server[list(server.keys())[0]]
        if (datetime.now().hour == srv["HOUR"] and datetime.now().minute == srv["MINUTE"]):
            embeds = tools.getEmbedsCartoon(srv["cartoonIds"])
            for embed in embeds:
                await bot.get_channel(srv['ChannelToSend']).send(embed=embed)


bot.run(data['TOKEN'])
