#!/usr/bin/env python3


from asyncio import tasks
import discord
from discord.ext import commands, tasks
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
        json.dump(data, f)


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)

@bot.command(brief="get a random cartoon")
async def random(ctx):
    i = rd.randint(0, 2613)
    url = f"https://xkcd.com/{i}/info.0.json"
    response = requests.get(url)
    data = response.json()
    await ctx.send(data['img'])

@bot.command(brief="get an image comic from number")
async def comic(ctx, number):
    try : 
        if  int(number) > MAX_CARTOON:
            await ctx.send("That number is too high")
        else:
            url = f"https://xkcd.com/{number}/info.0.json"
            response = requests.get(url)
            data = response.json()
            await ctx.send(data['img'])
    except:
        await ctx.send("please enter a number")

@tasks.loop(minutes=1)
async def send_random_cartoon():
    update_max_cartoon()
    if (datetime.now().hour == data['HOUR'] and datetime.now().minute == data['MINUTE']):
        i = rd.randint(0, MAX_CARTOON)
        url = f"https://xkcd.com/{i}/info.0.json"
        response = requests.get(url)
        data = response.json()
        await bot.get_channel(data['CHANNEL_ID']).send(data['img'])

bot.run(data['TOKEN'])
