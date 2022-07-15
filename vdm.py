#!/usr/bin/env python3

import requests

import discord
import xml.dom.minidom

def getRandomVDM():
    url = "https://www.viedemerde.fr/rss/random"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.text
        dom = xml.dom.minidom.parseString(data)
        item = dom.getElementsByTagName("item")[0]
        nf = item.getElementsByTagName("title")[0].firstChild.data.split("|")[0].strip()
        if nf[0] == '[':
            title = item.getElementsByTagName("title")[0].firstChild.data.split("|")[1].strip()
        else:
            title = item.getElementsByTagName("title")[0].firstChild.data.strip()
        description = item.getElementsByTagName("description")[0].firstChild.data.strip().split("\n")[0]
        return title, description, nf == "[Épicée]"
    else:
        print("Error")
        return None

def getEmbedVdm():
    title, description, isEpic = getRandomVDM()
    if title != None:
        while isEpic:
            title, description, isEpic = getRandomVDM()
        if len(title) < len(description):
            embed = discord.Embed(title=title, description=description, color=0x085FD5)
        else:
            embed = discord.Embed(title=description, description=title, color=0x085FD5)
        return (embed)