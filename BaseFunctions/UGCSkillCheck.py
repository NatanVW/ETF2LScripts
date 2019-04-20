import requests
from bs4 import BeautifulSoup


# UGC functions
def getPlayerHonors(id64):
    url = "https://www.ugcleague.com/players_page.cfm?player_id=" + str(id64)
    playerPage = requests.get(url).content
    html = BeautifulSoup(playerPage, "lxml")
    playerRows = []
    i = 0
    while i is not None:
        try:
            playerRows.append(html.find_all('div', {"class": "row-fluid"})[i])
            i += 1
        except IndexError:
            i = None
    playerSeasonPlayedHtml = []
    playerSeasonPlayed = []
    for i in range(0, len(playerRows)):
        try:
            if playerRows[i].find('h5').text == "TF2 Highlander Medals" or playerRows[i].find('h5').text == "TF2 6vs6 Medals":
                k = 0
                while k is not None:
                    try:
                        playerSeasonPlayedHtml.append(playerRows[i].find_all("div", {"style": "line-height:19px;"})[k])
                        k += 1
                    except IndexError:
                        k = None
        except AttributeError:
            continue
    for i in range(0, len(playerSeasonPlayedHtml)):
        playerSeasonPlayed.append(playerSeasonPlayedHtml[i].text.split("\n")[0])

    return playerSeasonPlayed


def higherSkillCheckUGC(playerSeasonPlayed, higherSkilledPlayerIDListUGC, playerID, id64List, id64):
    for i in range(0, len(playerSeasonPlayed)):
        if "Platinum" in playerSeasonPlayed[i] or "Premium" in playerSeasonPlayed[i] or "Gold" in playerSeasonPlayed[i] or "Silver" in playerSeasonPlayed[i]:
            if higherSkilledPlayerIDListUGC.count(playerID) == 0:
                higherSkilledPlayerIDListUGC.append(playerID)
                id64List.append(id64)
    return higherSkilledPlayerIDListUGC, id64List
