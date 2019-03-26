import requests
import lxml.html
import json

def getPlayerHistory(ID):
    baseUrl= "http://rgl.gg/Public/API/v1/PlayerHistory.aspx?s=" + str(ID)
    response = requests.get(baseUrl)
    tree= lxml.html.fromstring(response.content)
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
    for i in range (0,len(playerHistory)):
        played = playerHistory[i]
        if "HL" in played['RegionURL'] or "MM" in played['RegionURL']:
            seasonsPlayed.append(played['SeasonName'])
            divisionsPlayed.append(played['DivisionName'])
            matchCount.append(played['Wins'] + played['Loses'])
    return seasonsPlayed, divisionsPlayed, matchCount

def higherSkillCheckRGL(seasonsPlayed,divisionsPlayed, matchCount, higherSkilledPlayerIDListRGL, playerID):
    for i in range(0,len(seasonsPlayed)):
        if "Season" in seasonsPlayed[i]:
            if divisionsPlayed[i] != "RGL-Open":
                higherSkilledPlayerIDListRGL.append(playerID)
                return higherSkilledPlayerIDListRGL
            elif divisionsPlayed[i] == "RGL-Open" and matchCount[i] >=10:
                higherSkilledPlayerIDListRGL.append(playerID)
                return higherSkilledPlayerIDListRGL
        if "MM" in seasonsPlayed[i]:
            if divisionsPlayed[i] != "Open":
                higherSkilledPlayerIDListRGL.append(playerID)
                return higherSkilledPlayerIDListRGL
            elif divisionsPlayed[i] == "Open" and matchCount[i] >=10:
                higherSkilledPlayerIDListRGL.append(playerID)
                return higherSkilledPlayerIDListRGL
    return higherSkilledPlayerIDListRGL