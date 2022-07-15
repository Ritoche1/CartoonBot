#!/usr/bin/env python3


import requests
import random as rd
from datetime import datetime
import discord
import json


def update_max_cartoon():
    data = json.load(open('config.json'))
    url = f"https://xkcd.com/info.0.json"
    response = requests.get(url)
    MAX_CARTOON = response.json()['num']
    data["MAX_CARTOON"] = MAX_CARTOON
    with (open('config.json', 'w')) as f:
        json.dump(data, f, indent=4)

def getRandomCartoon():
    update_max_cartoon()
    data = json.load(open('config.json'))
    i = rd.randint(0, data['MAX_CARTOON'])
    url = f"https://xkcd.com/{i}/info.0.json"
    response = requests.get(url)
    data = response.json()
    return (data['img'])

def getEmbedXkcd():
    url = getRandomCartoon()
    embed = discord.Embed(title="XKCD", color=0x085FD5)
    embed.set_image(url=url)
    return (embed)


# @bot.command(brief="get a random cartoon")
# async def random(ctx):
#     i = rd.randint(0, 2613)
#     url = f"https://xkcd.com/{i}/info.0.json"
#     response = requests.get(url)
#     data = response.json()
#     await ctx.send(data['img'])
#     print(f"{datetime.now()} - {ctx.author} - {ctx.message.content}")

# @bot.command(brief="get an image comic from number")
# async def comic(ctx, number=None):
#     try : 
#         if  int(number) > MAX_CARTOON:
#             await ctx.send("That number is too high")
#         else:
#             url = f"https://xkcd.com/{number}/info.0.json"
#             response = requests.get(url)
#             data = response.json()
#             await ctx.send(data['img'])
#     except:
#         url = f"https://xkcd.com/info.0.json"
#         response = requests.get(url)
#         data = response.json()
#         await ctx.send(data['img'])
#     print(f"{datetime.now()} - {ctx.author} - {ctx.message.content}")
