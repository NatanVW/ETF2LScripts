import requests

from BaseFunctions.ETF2LSkillCheck import playerSkill
from BaseFunctions.ETF2lBase import getTeamDiv


# generate a list of all players that joined and left the team based off of API output.
def transferCheck(transfers, teamID, allowedPlayerIDlist, daysToCheck, provisionalsRelease):
    transferList = {}
    playerIDList = []
    playerIDListJoined = []
    for transfer in transfers:
        playerID = transfer['who']['id']
        if str(playerID) in allowedPlayerIDlist:
            continue
        else:
            if playerIDList.count(playerID) == 0:
                playerIDList.append(playerID)
            time = str(transfer['time']).split()
            try:
                if transferList[playerID]:
                    if transfer['type'] == 'left':
                        transferList[playerID]['timeLeft'].append(time)
                    elif transfer['type'] == "joined":
                        transferList[playerID]['timeJoined'].append(time)
            except KeyError:
                transferList[playerID] = {}
                transferList[playerID]['timeLeft'] = []
                transferList[playerID]['timeJoined'] = []
                if transfer['type'] == 'left':
                    transferList[playerID]['timeLeft'].append(time)
                elif transfer['type'] == "joined":
                    transferList[playerID]['timeJoined'].append(time)

    for playerID in playerIDList:
        if transferList[playerID]['timeJoined'] != [] and transferList[playerID]['timeLeft'] != []:
            if len(transferList[playerID]['timeJoined']) > 1 and len(transferList[playerID]['timeLeft']) > 1:
                if len(transferList[playerID]['timeJoined']) > len(transferList[playerID]['timeLeft']):
                    for j in range(len(transferList[playerID]['timeJoined']) - 1, 0, -1):
                        transferList[playerID]['timeJoined'].remove(transferList[playerID]['timeJoined'][j])
                    transferList[playerID]['timeLeft'] = []
                elif len(transferList[playerID]['timeJoined']) == len(transferList[playerID]['timeLeft']) or len(transferList[playerID]['timeJoined']) < len(
                        transferList[playerID]['timeLeft']):
                    transferList[playerID]['timeLeft'] = []
                    transferList[playerID]['timeJoined'] = []
            else:
                if transferList[playerID]['timeLeft'][0] > transferList[playerID]['timeJoined'][0]:
                    resultsUrl = "https://api.etf2l.org/player/" + str(playerID) + "/results.json?per_page=100&days=" + str(
                        daysToCheck)
                    results = requests.get(resultsUrl).json()['results']
                    try:
                        len(results)
                    except TypeError:
                        continue
                    for i in range(0, len(results)):
                        match = results[i]
                        matchTime = match['time']
                        if (matchTime < int(transferList[playerID]['timeLeft'][0][0])) and (match['clan1']['id'] == teamID or match['clan2']['id'] == teamID):
                            if playerIDListJoined.count(playerID) == 0:
                                playerIDListJoined.append(playerID)

                elif transferList[playerID]['timeLeft'][0] < transferList[playerID]['timeJoined'][0] and int(transferList[playerID]['timeLeft'][0][0]) < int(provisionalsRelease):
                    transferList[playerID]['timeLeft'] = []
        if transferList[playerID]['timeJoined'] == []:
            continue
        elif transferList[playerID]['timeLeft'] == []:
            if playerIDListJoined.count(playerID) == 0:
                playerIDListJoined.append(playerID)
    totalJoins = len(playerIDListJoined)

    return playerIDListJoined, totalJoins


# See how many of the late joined players played in the matches.
def activeLineup(teamID, playerID, daysToCheck):
    teamUrl = "https://api.etf2l.org/team/" + str(teamID) + "/results.json?days=" + str(daysToCheck) + "&per_page=100"
    playerUrl = "https://api.etf2l.org/player/" + str(playerID) + "/results.json?days=" + str(daysToCheck) + "&per_page=100"
    teamResults = requests.get(teamUrl).json()['results']
    playerResults = requests.get(playerUrl).json()['results']
    activeLineup = 0
    try:
        len(teamResults)
        len(playerResults)
    except TypeError:
        return activeLineup
    for teamMatch in teamResults:
        for playerMatch in playerResults:
            if (teamMatch['id'] == playerMatch['id'] and teamMatch['competition']['id'] == playerMatch['competition']['id']):
                activeLineup = activeLineup + 1
    return activeLineup


# Get skill level per player
def getPlayerSkillHS(playerID, teamDiv, fullCompList6v6, fullCompListHL, compList6v6, compListHL, previousFMC):
    resultsUrl = "https://api.etf2l.org/player/" + str(playerID) + "/results.json?per_page=100&since=0"
    totalPages = requests.get(resultsUrl).json()['page']['total_pages']
    totalResults = []
    for i in range(1, totalPages + 1):
        APIplayerResults = "https://api.etf2l.org/player/" + str(playerID) + "/results/" + str(i) + ".json?per_page=100&since=0"
        results = requests.get(APIplayerResults).json()['results']
        try:
            totalResults += results
        except TypeError:
            break
    try:
        NoMachtesPlayed = len(totalResults)
    except TypeError:
        NoMachtesPlayed = 1

    playerHL = dict(prem=0, div1=0, high=0, div2=0, div3=0, mid=0, div4=0, low=0, div5=0, div6=0, open=0)
    player6s = dict(prem=0, div1=0, high=0, div2=0, div3=0, mid=0, div4=0, low=0, div5=0, div6=0, open=0)
    HLMatchCount = 0
    SMatchCount = 0
    tier = 0

    for i in range(0, NoMachtesPlayed):
        try:
            match = totalResults[i]
        except TypeError:
            break

        # Get ya data
        compID = str(match['competition']['id'])
        tierName = match['division']['name']
        tier = match['division']['skill_contrib']
        if tier == None:
            tier = 0
        playOff = match['competition']['name']
        if tierName == None and "Playoffs" not in playOff:
            continue
        week = match['week']
        if teamDiv == "Fresh":
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = playerSkill(compID, fullCompList6v6, fullCompListHL, playOff, tierName, tier, playerHL, player6s, HLMatchCount,
                                                                                     SMatchCount, playerID, week, previousFMC)
        else:
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = playerSkill(compID, compList6v6, compListHL, playOff, tierName, tier, playerHL, player6s, HLMatchCount, SMatchCount,
                                                                                     playerID, week, previousFMC)

    return playerHL, player6s, HLMatchCount, SMatchCount, previousFMC


# Add player to overall team stats, look at skill comparison with team
def teamSkillHS(player6s, playerHL, team6s, teamHL, skillContribTotal6s, skillContribTotalHL, HLMatchCount, SMatchCount, playerID, teamID, activePlayerIDlist, waterfall, currentMainCompID,
                currentTopCompID):
    tier ={
        "prem":28,
        "div1":24,
        "high":22,
        "div2":20,
        "div3":16,
        "mid":15,
        "div4":12,
        "low":9,
        "div5":8,
        "div6":4,
        "open":4,
        "none":0,
    }
    for key in player6s:
        if player6s[key] >= 3:
            team6s[key] += 1
            if playerID in activePlayerIDlist:
                skillContrib = getSkillContrib(teamID, tier[key], currentMainCompID, currentTopCompID)
                skillContribTotal6s += skillContrib
            break

    for key in playerHL:
        if playerHL[key] >= 3:
            teamHL[key] += 1
            if playerID in activePlayerIDlist:
                skillContrib = getSkillContrib(teamID, tier[key], currentMainCompID, currentTopCompID)
                skillContribTotalHL += skillContrib
            break

    if 0 <= HLMatchCount < 3:
        teamHL['none'] += 1
    if 0 <= SMatchCount < 3:
        team6s['none'] += 1
    if HLMatchCount >= 3 and all(value < 3 for value in playerHL.values()):
        waterfall.append(str(playerID))
    if SMatchCount >= 3 and all(value < 3 for value in player6s.values()):
        waterfall.append(str(playerID))

    return team6s, teamHL, skillContribTotal6s, skillContribTotalHL, waterfall


# Calculates the total of the teams potential 6s skill contrib.
def getSkillContrib(teamID, playerDiv, currentMainCompID, currentTopCompID):
    skillContrib = 0
    teamDiv = getTeamDiv(teamID, currentMainCompID, currentTopCompID)
    if playerDiv > teamDiv:
        skillContrib = playerDiv - teamDiv
        return skillContrib
    else:
        return skillContrib
