import requests
from BaseFunctions.ETF2lBase import getTeamDiv
from BaseFunctions.ETF2LSkillCheck import playerSkill

# generate a list of all players that joined and left the team based off of API output.
def transferCheck(transfers, teamID, allowedPlayerIDlist, daysToCheck):
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
                    for j in range(len(transferList[playerID]['timeJoined'])-1,0,-1):
                        transferList[playerID]['timeJoined'].remove(transferList[playerID]['timeJoined'][j])
                    transferList[playerID]['timeLeft'] = []
                elif len(transferList[playerID]['timeJoined']) == len(transferList[playerID]['timeLeft']) or len(transferList[playerID]['timeJoined']) < len(transferList[playerID]['timeLeft']):
                    transferList[playerID]['timeLeft'] = []
                    transferList[playerID]['timeJoined'] =[]
            else:
                if transferList[playerID]['timeLeft'][0] > transferList[playerID]['timeJoined'][0]:
                    resultsUrl = "http://api.etf2l.org/player/" + str(playerID) + "/results.json?per_page=100&days=" + str(daysToCheck)  # since=" + str(transferList[playerID]['timeJoined'][0][0])
                    data = requests.get(resultsUrl).json()
                    results = data['results']
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

                elif transferList[playerID]['timeLeft'][0] < transferList[playerID]['timeJoined'][0]:
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
    teamUrl = "http://api.etf2l.org/team/" + str(teamID) + "/results.json?days=" + str(daysToCheck) + "&per_page=100"
    playerUrl = "http://api.etf2l.org/player/" + str(playerID) + "/results.json?days=" + str(daysToCheck) + "&per_page=100"
    teamData = requests.get(teamUrl).json()
    playerData = requests.get(playerUrl).json()
    teamResults = teamData['results']
    playerResults = playerData['results']
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
def getPlayerSkillHS(playerID, teamDiv, fullCompList6v6,fullCompListHL, compList6v6, compListHL, previousFMC):
    resultsUrl = "http://api.etf2l.org/player/" + str(playerID) + "/results.json?per_page=100&since=0"
    data = requests.get(resultsUrl).json()
    totalPages = data['page']['total_pages']
    totalResults = []
    for i in range(1, totalPages + 1):
        APIplayerResults = "http://api.etf2l.org/player/" + str(playerID) + "/results/" + str(i) + ".json?per_page=100&since=0"
        data = requests.get(APIplayerResults).json()
        results = data['results']
        try:
            totalResults += results
        except TypeError:
            break
    try:
        NoMachtesPlayed = len(totalResults)
    except TypeError:
        NoMachtesPlayed = 1

    playerHL = dict(prem=0, div1=0, high=0, mid=0, low=0, open=0)
    player6s = dict(prem=0, div1=0, div2=0, mid=0, low=0, open=0)
    HLMatchCount = 0
    SMatchCount = 0

    for i in range(0, NoMachtesPlayed):
        try:
            match = totalResults[i]
        except TypeError:
            break

        # Get ya data
        compID = str(match['competition']['id'])
        tierName = match['division']['name']
        playOff = match['competition']['name']
        if tierName == None and "Playoffs" not in playOff:
            continue
        week = match['week']
        if teamDiv == "Fresh":
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = playerSkill(compID, fullCompList6v6,fullCompListHL, playOff,tierName, playerHL, player6s, HLMatchCount, SMatchCount, playerID, week, previousFMC)
        else:
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = playerSkill(compID, compList6v6, compListHL, playOff, tierName, playerHL, player6s, HLMatchCount, SMatchCount, playerID, week, previousFMC)

    return playerHL, player6s, HLMatchCount, SMatchCount, previousFMC

# Add player to overall team stats, look at skill comparison with team
def teamSkillHS(player6s, playerHL, team6s, teamHL, skillContribTotal6s, skillContribTotalHL, HLMatchCount, SMatchCount, playerID, teamID, activePlayerIDlist, waterfall, currentMainCompID, currentTopCompID):
    if player6s['prem'] >= 3:
        team6s['prem'] += 1
        playerScore = 6
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotal6s += skillContrib

    elif player6s['div1'] >= 3:
        team6s['div1'] += 1
        playerScore = 5
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotal6s += skillContrib

    elif player6s['div2'] >= 3:
        team6s['div2'] += 1
        playerScore = 4
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotal6s += skillContrib

    elif player6s['mid'] >= 3:
        team6s['mid'] += 1
        playerScore = 3
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotal6s += skillContrib

    elif player6s['low'] >= 3:
        team6s['low'] += 1
        playerScore = 2
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotal6s += skillContrib

    elif player6s['open'] >= 3:
        team6s['open'] += 1
        playerScore = 1
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotal6s += skillContrib

    if playerHL['prem'] >= 3:
        teamHL['prem'] += 1
        playerScore = 6
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotalHL += skillContrib

    elif playerHL['div1'] >= 3:
        teamHL['div1'] += 1
        playerScore = 5
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotalHL += skillContrib

    elif playerHL['high'] >= 3:
        teamHL['high'] += 1
        playerScore = 4
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotalHL += skillContrib

    elif playerHL['mid'] >= 3:
        teamHL['mid'] += 1
        playerScore = 3
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotalHL += skillContrib

    elif playerHL['low'] >= 3:
        teamHL['low'] += 1
        playerScore = 2
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotalHL += skillContrib

    elif playerHL['open'] >= 3:
        teamHL['open'] += 1
        playerScore = 1
        if playerID in activePlayerIDlist:
            skillContrib = getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID)
            skillContribTotalHL += skillContrib

    if 0 <= HLMatchCount < 3:
        teamHL['none'] += 1
    if 0 <= SMatchCount < 3:
        team6s['none'] += 1
    if HLMatchCount >=3 and all(value < 3 for value in playerHL.values()):
        waterfall.append(str(playerID))
    if SMatchCount >=3 and all(value < 3 for value in player6s.values()):
        waterfall.append(str(playerID))

    return team6s, teamHL, skillContribTotal6s, skillContribTotalHL, waterfall

# Calculates the total of the teams potential 6s skill contrib.
def getSkillContrib6s(teamID, playerScore, currentMainCompID, currentTopCompID):
    skillContrib = 0
    teamDivName = getTeamDiv(teamID, currentMainCompID, currentTopCompID)
    if teamDivName == "Premiership":
        return skillContrib
    elif teamDivName == "Division 1":
        if playerScore > 5:
            skillContrib += (playerScore - 5)
        return skillContrib
    elif teamDivName == "Division 2" or teamDivName == "High":
        if playerScore > 4:
            skillContrib += (playerScore - 4)
        return skillContrib
    elif teamDivName == "Mid":
        if playerScore > 3:
            skillContrib += (playerScore - 3)
        return skillContrib
    elif teamDivName == "Low":
        if playerScore > 2:
            skillContrib += (playerScore - 2)
        return skillContrib
    elif teamDivName == "Fresh"  or teamDivName == "Open":
        if playerScore > 1:
            skillContrib += (playerScore - 1)
        return skillContrib

    return 0

# Calculates the total of the teams potential HL skill contrib.
def getSkillContribHL(teamID, playerScore, currentMainCompID, currentTopCompID):
    skillContrib = 0
    teamDivName = getTeamDiv(teamID, currentMainCompID, currentTopCompID)
    if teamDivName == "Division 2":
        teamDivName = "High"
    if teamDivName == "Premiership":
        return skillContrib
    elif teamDivName == "Division 1":
        if playerScore > 5:
            skillContrib += (playerScore - 5)
        return skillContrib
    elif teamDivName == "High":
        if playerScore > 4:
            skillContrib += (playerScore - 4)
        return skillContrib
    elif teamDivName == "Mid":
        if playerScore > 3:
            skillContrib += (playerScore - 3)
        return skillContrib
    elif teamDivName == "Low"  or teamDivName == "Open":
        if playerScore > 2:
            skillContrib += (playerScore - 2)
        return skillContrib
    elif teamDivName == "Fresh":
        if playerScore > 1:
            skillContrib += (playerScore - 1)
        return skillContrib

    return 0
