import json

import lxml.html
import requests


def getPlayerHistory(ID):
    baseUrl = "http://rgl.gg/Public/API/v1/PlayerHistory.aspx?s=" + str(ID)
    response = requests.get(baseUrl)
    tree = lxml.html.fromstring(response.content)
    playerInfo = tree.xpath('//span[@id]/text()')
    correctPart = json.loads(str(playerInfo[0]))
    try:
        data = correctPart[0]
    except IndexError:
        playerHistory = 0
        name = 0
        return playerHistory, name
    playerHistory = data['PlayerHistory']
    name = data['CurrentAlias']
    return playerHistory, name


def getDivisionPlayed(playerHistory):
    seasonsPlayed = []
    divisionsPlayed = []
    matchCount = []
    for i in range(0, len(playerHistory)):
        played = playerHistory[i]
        if "HL" in played['RegionURL'] or "MM" in played['RegionURL']:
            seasonsPlayed.append(played['SeasonName'])
            divisionsPlayed.append(played['DivisionName'])
            matchCount.append(played['Wins'] + played['Loses'])
    return seasonsPlayed, divisionsPlayed, matchCount


def higherSkillCheckRGL(seasonsPlayed, divisionsPlayed, matchCount, higherSkilledPlayerIDListRGL, playerID, id64List, id64, RGLNameList, name):
    for i in range(0, len(seasonsPlayed)):
        if "Season" in seasonsPlayed[i]:
            if divisionsPlayed[i] != "RGL-Open":
                higherSkilledPlayerIDListRGL.append(playerID)
                RGLNameList.append(name)
                id64List.append(id64)
                return higherSkilledPlayerIDListRGL, id64List, RGLNameList
            elif divisionsPlayed[i] == "RGL-Open" and matchCount[i] >= 10:
                higherSkilledPlayerIDListRGL.append(playerID)
                RGLNameList.append(name)
                id64List.append(id64)
                return higherSkilledPlayerIDListRGL, id64List, RGLNameList
        if "MM" in seasonsPlayed[i]:
            if divisionsPlayed[i] != "Open":
                higherSkilledPlayerIDListRGL.append(playerID)
                RGLNameList.append(name)
                id64List.append(id64)
                return higherSkilledPlayerIDListRGL, id64List, RGLNameList
            elif divisionsPlayed[i] == "Open" and matchCount[i] >= 10:
                higherSkilledPlayerIDListRGL.append(playerID)
                RGLNameList.append(name)
                id64List.append(id64)
                return higherSkilledPlayerIDListRGL, id64List, RGLNameList

    return higherSkilledPlayerIDListRGL, id64List, RGLNameList
