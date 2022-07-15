#!/usr/bin/env python3


import json

from vdm import getEmbedVdm
from xkcd import getEmbedXkcd

def addServer(serverId):
    data = json.load(open("data.json"))
    dicToadd = {"ChannelToSend" : 0, "cartoonIds" : [], "HOUR" : -1, "MINUTE" : -1}
    for server in data:
        if str(serverId) in server:
            return -1
    data.append({str(serverId) : dicToadd})
    json.dump(data, open("data.json", "w"), indent=4)
    return 0

def setChannel(serverId, channelId):
    data = json.load(open("data.json"))
    for server in data:
        if str(serverId) in server:
            server[str(serverId)]["ChannelToSend"] = channelId
            json.dump(data, open("data.json", "w"), indent=4)
            return

def setTime(serverId, hour: int, minute: int):
    data = json.load(open("data.json"))
    for server in data:
        if str(serverId) in server:
            server[str(serverId)]["HOUR"] = int(hour)
            server[str(serverId)]["MINUTE"] = int(minute)
            json.dump(data, open("data.json", "w"), indent=4)
            return

def addCartoon(serverId, cartoonId):
    data = json.load(open("data.json"))
    if (isInToSend(cartoonId) == False):
        addToSend(cartoonId)
    for server in data:
        if str(serverId) in server:
            server[str(serverId)]["cartoonIds"].append(cartoonId)
            json.dump(data, open("data.json", "w"), indent=4)
            return

def checkChannel(serverId):
    data = json.load(open("data.json"))
    for server in data:
        if str(serverId) in server:
            if server[str(serverId)]["ChannelToSend"] == 0:
                return False
            return True
    return False

def checkTime(serverId):
    data = json.load(open("data.json"))
    for server in data:
        if str(serverId) in server:
            if (server[str(serverId)]['HOUR'] == -1):
                return False
    return True

def getServerFollowers(serverId):
    data = json.load(open("data.json"))
    for server in data:
        if str(serverId) in server:
            return server[str(serverId)]["cartoonIds"]
    return []

def getChannelToSend(cartoonId):
    data = json.load(open("data.json"))
    res = []
    for server in data:
        for cartoon in server:
            if cartoonId in server[cartoon]["cartoonIds"]:
                res.append(server[cartoon]["ChannelToSend"])
    return res

def isInToSend(cartoonId):
    data = json.load(open("toSend.json"))
    for cartoon in data:
        if str(cartoonId) == cartoon["id"]:
            return True
    return False

def isInServer(serverId, cartoonId):
    data = json.load(open("data.json"))
    for server in data:
        if str(serverId) in server:
            if cartoonId in server[str(serverId)]["cartoonIds"]:
                return True
    return False

def addToSend(cartoonId):
    data = json.load(open("toSend.json"))
    dicToAdd = {"id":str(cartoonId), "lastSent" : ""}
    for cartoon in data:
        if str(cartoonId) in cartoon:
            return
    data.append(dicToAdd)
    json.dump(data, open("toSend.json", "w"), indent=4)


def getEmbedsCartoon(cartoonIds):
    resEmbed = []
    for cartoon in cartoonIds:
        if cartoon == "vdm":
            resEmbed.append(getEmbedVdm())
        elif cartoon == "xkcd":
            resEmbed.append(getEmbedXkcd())
    return resEmbed