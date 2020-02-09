import requests
from bs4 import BeautifulSoup
import re
import sys

from BaseFunctions.ETF2lBase import getSteamID64


def urlInput():
    url = input("Input match url:")
    return re.findall("\d{4,}",url)

def getPlayersFromStatus(matchID):
    url = "http://etf2l.org/matches/" + str(matchID)
    searchPage = requests.get(url).content
    html = BeautifulSoup(searchPage, "lxml")
    table = html.find("table",{"class":"fix match-players"})
    teamResults = []
    playersPerTeam = []
    players = []
    teamOne = []
    teamTwo = []
    i = 0
    for i in range(0,2):
        try:
            teamResults.append(table.find_all("td",{"class":"left"})[i])
        except AttributeError:
            return teamOne, teamTwo

    for i in range(0,2):
        for j in range(0, int(teamResults[i].contents[0][2:3])):
            try:
                playersPerTeam.append(teamResults[i].find_all("a", href=True)[j])
                j += 1
            except AttributeError:
                return teamOne, teamTwo

    for player in playersPerTeam:
        try:
            players.append(re.findall("\d{3,}",player["href"])[0])
        except AttributeError:
            return teamOne, teamTwo
    teamOne = players[:int(teamResults[0].contents[0][2:3])]
    teamTwo = players[int(teamResults[0].contents[0][2:3]):]
    return teamOne, teamTwo

def getMatchTime(playerID, matchID):
    url = "http://api.etf2l.org/player/" + str(playerID) + "/results.json?since=0&per_page=100"
    results = requests.get(url).json()['results']
    for match in results:
        if str(match['id']) == matchID:
            matchStart = match['time']

    try:
        matchEnd = (24 * 60 * 60) + matchStart
    except UnboundLocalError:
        sys.exit("Error: Match is probably not verified")

    return matchStart, matchEnd

def getPlayerLogs(playerID64, matchStart, matchEnd):
    url = "http://logs.tf/api/v1/log?player=" + str(playerID64)
    logs = requests.get(url).json()['logs']
    logList = []
    for log in logs:
        if matchStart < log['date'] < matchEnd:
            logList.append(log['id'])
    return logList

def getLogsForMatch(matchID):
    teamOne, teamTwo = getPlayersFromStatus(matchID)
    print(teamOne, teamTwo)
    playerOneID64 = getSteamID64(teamOne[0])
    playerTwoID64 = getSteamID64(teamTwo[0])
    matchStart, matchEnd = getMatchTime(teamOne[0],matchID)
    playerOneLogs = getPlayerLogs(playerOneID64, matchStart, matchEnd)
    playerTwoLogs = getPlayerLogs(playerTwoID64, matchStart, matchEnd)
    matchingLogs = []
    for i in range(0,len(playerOneLogs)):
        for j in range(0,len(playerTwoLogs)):
            if playerOneLogs[i] == playerTwoLogs[j]:
                matchingLogs.append(playerOneLogs[i])

    for log in matchingLogs:
        print("http://logs.tf/" + str(log))

matchID = urlInput()
getLogsForMatch(matchID[0])
