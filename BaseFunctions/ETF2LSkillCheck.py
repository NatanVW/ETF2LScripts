import requests


# Get skill level per player
def getPlayerSkill(playerID, compList6v6, compListHL):
    resultsUrl = "http://api.etf2l.org/player/" + str(playerID) + "/results.json?per_page=100&since=0"
    totalPages = requests.get(resultsUrl).json()['page']['total_pages']
    totalResults = []
    previousFMC = 0
    for i in range(1, totalPages + 1):
        APIplayerResults = "http://api.etf2l.org/player/" + str(playerID) + "/results/" + str(i) + ".json?per_page=100&since=0"
        results = requests.get(APIplayerResults).json()['results']
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
        playOff = match['competition']['name']
        tierName = match['division']['name']
        if tierName == None and "Playoffs" not in playOff:
            continue

        week = match['week']
        playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = playerSkill(compID, compList6v6, compListHL, playOff, tierName, playerHL, player6s, HLMatchCount, SMatchCount, playerID,
                                                                                 week, previousFMC)

    return playerHL, player6s, HLMatchCount, SMatchCount, previousFMC


# Support function for getPlayerSkill, will do the calculations
def playerSkill(compID, compList6v6, compListHL, playOff, tierName, playerHL, player6s, HLMatchCount, SMatchCount, playerID, week, previousFMC):
    # Check match history to see what skill group the player belongs to
    if compID in compListHL:
        HLMatchCount = HLMatchCount + 1
        if "Playoffs" in playOff:
            if "High" in playOff[22:] or "Division 1" in playOff in playOff:
                playerHL['prem'] += 1
            if "Division 2" in playOff:
                playerHL['div1'] += 1
            if "Mid" in playOff or "Division 3" in playOff or "Division 4" in playOff:
                playerHL['high'] += 1
            if "Low" in playOff or "Division 5" in playOff:
                playerHL['mid'] += 1
            if "Open" in playOff or "Division 6" in playOff:
                playerHL['mid'] += 1
        elif week > 7 or (int(compID) > 470 and week > 5):
            if tierName == "Premiership" or "Division 1" in tierName:
                playerHL['prem'] += 1
            elif "Division 2" in tierName:
                playerHL['div1'] += 1
        else:
            if tierName == "Premiership":
                playerHL['prem'] += 1
            elif "Division 1" in tierName:
                playerHL['div1'] += 1
            elif tierName == "High" or "Division 2" in tierName or tierName == "High/Mid":
                playerHL['high'] += 1
            elif tierName == "Mid" or "Division 3" in tierName or "Division 4" in tierName:
                playerHL['mid'] += 1
            elif tierName == "Low" or "Division 5" in tierName:
                playerHL['low'] += 1
            elif tierName == "Open" or "Division 6" in tierName:
                playerHL['open'] += 1

    elif compID in compList6v6:
        SMatchCount = SMatchCount + 1
        if "Playoffs" in playOff:
            if "High" in playOff or "Division 1" in playOff in playOff:
                player6s['prem'] += 1
            if "Division 2" in playOff:
                player6s['div1'] += 1
            if "Mid" in playOff or "Division 3" in playOff or "Division 4" in playOff:
                player6s['div2'] += 1
            if "Low" in playOff or "Division 5" in playOff:
                player6s['mid'] += 1
            if "Open" in playOff or "Division 6" in playOff:
                player6s['low'] += 1
        elif week > 7:
            if tierName == "Premiership" or "Division 1" in tierName:
                player6s['prem'] += 1
            elif "Division 2" in tierName:
                player6s['div1'] += 1
        else:
            if tierName == "Premiership":
                player6s['prem'] += 1
            elif "Division 1" in tierName:
                player6s['div1'] += 1
            elif tierName == "High" or "Division 2" in tierName:
                player6s['div2'] += 1
            elif tierName == "Mid" or "Division 3" in tierName or "Division 4" in tierName:
                player6s['mid'] += 1
            elif tierName == "Low" or "Division 5" in tierName:
                player6s['low'] += 1
            elif tierName == "Open" or "Division 6" in tierName:
                player6s['open'] += 1

    if int(compID) == 490:
        if week > 2:
            previousFMC = 1

    return playerHL, player6s, HLMatchCount, SMatchCount, previousFMC


# Add player to overall team stats, look at skill comparison with team
def teamSkill(player6s, playerHL, team6s, teamHL, HLMatchCount, SMatchCount):
    if player6s['prem'] >= 3:
        team6s['prem'] += 1

    elif player6s['div1'] >= 3:
        team6s['div1'] += 1

    elif player6s['div2'] >= 3:
        team6s['div2'] += 1

    elif player6s['mid'] >= 3:
        team6s['mid'] += 1

    elif player6s['low'] >= 3:
        team6s['low'] += 1

    elif player6s['open'] >= 3:
        team6s['open'] += 1

    if playerHL['prem'] >= 3:
        teamHL['prem'] += 1

    elif playerHL['div1'] >= 3:
        teamHL['div1'] += 1

    elif playerHL['high'] >= 3:
        teamHL['high'] += 1

    elif playerHL['mid'] >= 3:
        teamHL['mid'] += 1

    elif playerHL['low'] >= 3:
        teamHL['low'] += 1

    elif playerHL['open'] >= 3:
        teamHL['open'] += 1

    if 0 <= HLMatchCount < 3:
        teamHL['none'] += 1
    if 0 <= SMatchCount < 3:
        team6s['none'] += 1

    return team6s, teamHL


# Check if player has to high of a skill level to play in the cup
def higherSkillCheckETF2LFMC(player6s, playerHL, HLMatchCount, SMatchCount, playerID, higherSkilledPlayerIDList, previousFMC):
    if player6s['prem'] > 0 or player6s['div1'] > 0 or player6s['div2'] > 0 or player6s['mid'] > 0 or player6s['low'] > 0 or player6s['open'] > 10:
        higherSkilledPlayerIDList.append(playerID)
        return higherSkilledPlayerIDList

    if playerHL['prem'] > 0 or playerHL['div1'] > 0 or playerHL['high'] > 0 or playerHL['mid'] > 0 or playerHL['low'] > 0 or playerHL['open'] > 10:
        higherSkilledPlayerIDList.append(playerID)
        return higherSkilledPlayerIDList

    if previousFMC == 1:
        higherSkilledPlayerIDList.append(playerID)
        return higherSkilledPlayerIDList

    if HLMatchCount + SMatchCount > 10:
        higherSkilledPlayerIDList.append(playerID)
        return higherSkilledPlayerIDList

    return higherSkilledPlayerIDList
