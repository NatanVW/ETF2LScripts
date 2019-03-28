import requests
from datetime import datetime

# Get a list of all teams from given compID.
def getTeamIDs(compID):
    firstPageUrl = "http://api.etf2l.org/competition/" + str(compID) + "/teams.json?per_page=100"
    data = requests.get(firstPageUrl).json()
    totalPages = data['page']['total_pages']
    idList = []
    for i in range(1, totalPages + 1):
        pageUrl = "http://api.etf2l.org/competition/" + str(compID) + "/teams/" + str(i) + ".json?per_page=100"
        data = requests.get(pageUrl).json()
        teams = data['teams']
        for ID in teams:
            idList.append(ID)

    return sorted(idList)

# Search for all the seasons that happend within the old comp -> new comp range.
def getCompList(oldID, currentID):
    compList6v6 = []
    compListHL = []
    for i in range(oldID, currentID+1):
        compURL = "http://api.etf2l.org/competition/" + str(i) + ".json"
        response = requests.get(compURL)
        data = response.json()
        try:
            category = data['competition']['category']
        except KeyError:
            continue
        if category == "6v6 Season":
            compList6v6.append(str(i))
        elif category == "Highlander Season":
            compListHL.append(str(i))

    return compList6v6, compListHL

# Get all players ID's on a team
def getPlayers(teamID):
    playerIDList = []
    teamUrl = "http://api.etf2l.org/team/" + str(teamID) + ".json"
    data = requests.get(teamUrl).json()
    team = data['team']['players']
    try:
        len(team)
    except TypeError:
        return playerIDList
    for i in range(0, len(team)):
        player = team[i]
        playerIDList.append(player['id'])

    return playerIDList

#Configures the script to work for the correct gamemode.
def setGameMode(gameType):
    if gameType == "6s":
        # Amount of active late players allowed to join after provisional tier release
        activeJoinLimit = 3

        # Skill contribution point limit, set to 2 for 6s and 3 for HL
        skillContribLimit = 2


    elif gameType == "HL":
        activeJoinLimit = 5

        skillContribLimit = 3


    return activeJoinLimit, skillContribLimit

# Unix timestamps for when the provisionals are published.
def dateHourToUnix(date,hour):
    dateHour = list(reversed(date.split("/")))
    dateHour += hour.split(":")
    dateHourInt = [ int(x) for x in dateHour ]
    unixTime = datetime(dateHourInt[0],dateHourInt[1],dateHourInt[2],dateHourInt[3],dateHourInt[4],dateHourInt[5]).timestamp()

    return unixTime

# Get all players that joined after the release of the provisional tiers
def getTransfers(teamID, provisionalsRelease):
    url = "http://api.etf2l.org/team/" + str(teamID) + "/transfers.json?since=" + str(provisionalsRelease)
    data = requests.get(url).json()
    transfers = data['transfers']

    return transfers

# Check the division the team is in
def getTeamDiv(ID, currentMainCompID, currentTopCompID):
    #print(ID)
    url = "http://api.etf2l.org/team/" + str(ID) + ".json"
    data = requests.get(url).json()
    if data['team']['competitions'][str(currentMainCompID)]['division']['name'] is not None:
        return data['team']['competitions'][str(currentMainCompID)]['division']['name']
    elif data['team']['competitions'][str(currentTopCompID)]['division']['name'] is not None:
        return data['team']['competitions'][str(currentTopCompID)]['division']['name']

def getTeamName(teamID):
    teamUrl = "http://api.etf2l.org/team/" + str(teamID) + ".json"
    data = requests.get(teamUrl).json()
    name = data['team']['name']

    return name

def getSteamID64(playerID):
    url = "http://api.etf2l.org/player/" + str(playerID) + ".json"
    data = requests.get(url).json()
    return data['player']['steam']['id64']