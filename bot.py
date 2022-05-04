#!/usr/bin/env python3


from asyncio import tasks
import discord
from discord.ext import commands, tasks
from discord.utils import get
import requests
import json
import random as rd
from datetime import datetime


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

data = json.load(open('config.json'))
MAX_CARTOON = data['MAX_CARTOON']


def update_max_cartoon():
    url = f"https://xkcd.com/info.0.json"
    response = requests.get(url)
    MAX_CARTOON = response.json()['num']
    data["MAX_CARTOON"] = MAX_CARTOON
    with (open('config.json', 'w')) as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".help"))
    send_random_cartoon.start()

@bot.command(brief="get a random cartoon")
async def random(ctx):
    i = rd.randint(0, 2613)
    url = f"https://xkcd.com/{i}/info.0.json"
    response = requests.get(url)
    data = response.json()
    await ctx.send(data['img'])
    print(f"{datetime.now()} - {ctx.author} - {ctx.message.content}")

@bot.command(brief="get an image comic from number")
async def comic(ctx, number=None):
    try : 
        if  int(number) > MAX_CARTOON:
            await ctx.send("That number is too high")
        else:
            url = f"https://xkcd.com/{number}/info.0.json"
            response = requests.get(url)
            data = response.json()
            await ctx.send(data['img'])
    except:
        url = f"https://xkcd.com/info.0.json"
        response = requests.get(url)
        data = response.json()
        await ctx.send(data['img'])
    print(f"{datetime.now()} - {ctx.author} - {ctx.message.content}")

@tasks.loop(minutes=1)
async def send_random_cartoon():
    update_max_cartoon()
    data = json.load(open('config.json'))
    channel_id = int(data['CHANNEL_ID'])
    if (datetime.now().hour == data['HOUR'] and datetime.now().minute == data['MINUTE']):
        print("datetime is now")
        i = rd.randint(0, MAX_CARTOON)
        url = f"https://xkcd.com/{i}/info.0.json"
        response = requests.get(url)
        data = response.json()
        channel = bot.get_channel(channel_id)
        await channel.send(data['img'])

bot.run(data['TOKEN'])
