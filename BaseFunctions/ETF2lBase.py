from datetime import datetime

import requests
from bs4 import BeautifulSoup


# Get a list of all teams from given compID.
def getTeamIDs(currentMainCompID, currentTopCompID = None):
    firstPageUrl = "https://api.etf2l.org/competition/" + str(currentMainCompID) + "/teams.json?per_page=100"
    totalPages = requests.get(firstPageUrl).json()['page']['total_pages']
    mainIDList = []
    for i in range(1, totalPages + 1):
        pageUrl = "https://api.etf2l.org/competition/" + str(currentMainCompID) + "/teams/" + str(i) + ".json?per_page=100"
        teams = requests.get(pageUrl).json()['teams']
        for ID in teams:
            mainIDList.append(ID)

    if currentTopCompID != None:
        firstPageUrl = "https://api.etf2l.org/competition/" + str(currentTopCompID) + "/teams.json?per_page=100"
        totalPages = requests.get(firstPageUrl).json()['page']['total_pages']
        topIDList = []
        for i in range(1, totalPages + 1):
            pageUrl = "https://api.etf2l.org/competition/" + str(currentTopCompID) + "/teams/" + str(i) + ".json?per_page=100"
            teams = requests.get(pageUrl).json()['teams']
            for ID in teams:
                topIDList.append(ID)
    else:
        topIDList = []

    return sorted(list(dict.fromkeys(mainIDList + topIDList)))


# Search for all the seasons that happend within the old comp -> new comp range.
def getCompList(oldID, currentID):
    compList6v6 = []
    cleaned6sCompList = []
    compListHL = []
    cleanedHLCompList = []

    firstPageUrl6v6 = "https://api.etf2l.org/competition/list.json?per_page=100&category=6v6%20Season&archived=1"
    totalPages = requests.get(firstPageUrl6v6).json()['page']['total_pages']
    for i in range(1, totalPages + 1):
        pageUrl = "https://api.etf2l.org/competition/list/" + str(i) + ".json?per_page=100&category=6v6%20Season&archived=1"
        data = requests.get(pageUrl).json()['competitions']
        for key in data.keys():
            compList6v6.append(key)
    compList6v6 =sorted(compList6v6, key=int)

    for compId6s in compList6v6:
        if int(compId6s) >= oldID:
            cleaned6sCompList.append(compId6s)

    firstPageUrlHL = "https://api.etf2l.org/competition/list.json?per_page=100&category=Highlander%20Season&archived=1"
    totalPages = requests.get(firstPageUrlHL).json()['page']['total_pages']
    for i in range(1, totalPages + 1):
        pageUrl = "https://api.etf2l.org/competition/list/" + str(i) + ".json?per_page=100&category=Highlander%20Season&archived=1"
        data = requests.get(pageUrl).json()['competitions']
        for key in data.keys():
            compListHL.append(key)
    compListHL = sorted(compListHL, key=int)

    for compIdHl in compListHL:
        if int(compIdHl) >= oldID:
            cleanedHLCompList.append(compIdHl)

    return cleaned6sCompList, cleanedHLCompList


# Get all players ID's on a team
def getPlayers(teamID):
    playerIDList = []
    teamUrl = "https://api.etf2l.org/team/" + str(teamID) + ".json"
    team = requests.get(teamUrl).json()['team']['players']
    if team == None:
        print("Warning: [team id = " + str(teamID) + "] ,the API didn't parse the player list for this team correctly. \n")
    else:
        for i in range(0, len(team)):
            player = team[i]
            playerIDList.append(player['id'])

    return playerIDList


# Configures the script to work for the correct gamemode.
def setGameMode(gameType, currentMainCompID6s, currentTopCompID6s, oldCompID6s, currentMainCompIDHL, currentTopCompIDHL, oldCompIDHL, date6s, hour6s, dateHL, hourHL, allowedPlayerIDlist6s,
                allowedPlayerIDlistHL):
    if gameType == "6s":
        # Amount of active late players allowed to join after provisional tier release
        activeJoinLimit = 3

        # Skill contribution point limit, set to 2 for 6s and 3 for HL
        skillContribLimit = 2

        # Set correct competitions ID's, date and hour of provisionals release for the gamemode
        currentMainCompID = currentMainCompID6s
        currentTopCompID = currentTopCompID6s
        oldCompID = oldCompID6s
        date = date6s
        hour = hour6s
        allowedPlayerIDlist = allowedPlayerIDlist6s

    elif gameType == "HL":
        activeJoinLimit = 5

        skillContribLimit = 3

        currentMainCompID = currentMainCompIDHL
        currentTopCompID = currentTopCompIDHL
        oldCompID = oldCompIDHL
        date = dateHL
        hour = hourHL
        allowedPlayerIDlist = allowedPlayerIDlistHL

    else:
        raise KeyError("An incorrect gametype was selected, please pick either HL or 6s")

    return activeJoinLimit, skillContribLimit, currentMainCompID, currentTopCompID, oldCompID, date, hour, allowedPlayerIDlist


# Unix timestamps for when the provisionals are published.
def dateHourToUnix(date, hour):
    dateHour = list(reversed(date.split("/")))
    dateHour += hour.split(":")
    dateHourInt = [int(x) for x in dateHour]
    unixTime = datetime(dateHourInt[0], dateHourInt[1], dateHourInt[2], dateHourInt[3], dateHourInt[4], dateHourInt[5]).timestamp()

    return unixTime


# Get all players that joined after the release of the provisional tiers
def getTransfers(teamID, provisionalsRelease):
    url = "https://api.etf2l.org/team/" + str(teamID) + "/transfers.json?since=" + str(provisionalsRelease) + "&per_page=100"
    transfers = requests.get(url).json()['transfers']

    return transfers


# Check the division the team is in
def getTeamDiv(ID, currentMainCompID, currentTopCompID):
    url = "https://api.etf2l.org/team/" + str(ID) + ".json"
    data = requests.get(url).json()
    try:
        if data['team']['competitions'][str(currentMainCompID)]['division']['name'] is not None:
            return data['team']['competitions'][str(currentMainCompID)]['division']['name']
    except KeyError:
        return data['team']['competitions'][str(currentTopCompID)]['division']['name']


def getTeamName(teamID):
    teamUrl = "https://api.etf2l.org/team/" + str(teamID) + ".json"
    name = requests.get(teamUrl).json()['team']['name']

    return name


def getSteamID64(playerID):
    url = "https://api.etf2l.org/player/" + str(playerID) + ".json"
    id64 = requests.get(url).json()['player']['steam']['id64']

    return id64


def getSteamID3(playerID):
    url = "https://api.etf2l.org/player/" + str(playerID) + ".json"
    id3 = requests.get(url).json()['player']['steam']['id3']

    return id3


def getETTF2Lfromid64(ID):
    url = "https://etf2l.org/search/" + str(ID)
    searchPage = requests.get(url).content
    html = BeautifulSoup(searchPage, "lxml")
    searchResults = []
    playerPage = []
    i = 0
    while i is not None:
        try:
            searchResults.append(html.find_all("div", {"class": "post"})[i])
            i += 1
        except IndexError:
            i = None

    forumLink = searchResults[0].find("ul")
    try:
        for a in forumLink.find_all("a", href=True):
            playerPage.append(a['href'])
    except AttributeError:
        return playerPage

    return playerPage[0]

def getPlayerName(ID):
    url = "https://api.etf2l.org/player/" + str(ID) + ".json"
    playerName = requests.get(url).json()['player']['name']

    return playerName

def getPlayerCountry(ID):
    url = "https://api.etf2l.org/player/" + str(ID) + ".json"
    playerCountry = requests.get(url).json()['player']['country']

    return playerCountry