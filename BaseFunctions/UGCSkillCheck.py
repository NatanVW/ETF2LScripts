import requests
from bs4 import BeautifulSoup

# UGC functions
def getPlayerHonors(id64):
    url = "https://www.ugcleague.com/players_page.cfm?player_id=" + str(id64)
    playerPage = requests.get(url).content
    html = BeautifulSoup(playerPage, "lxml")
    playerHonorsGameModes = []
    for i in range(0,2):
        try:
            playerHonorsGameModes.append(html.find_all('ul', {"class": "list-unstyled"})[i])
        except IndexError:
            break
    playerSeasonPlayedHtml = []
    playerSeasonPlayed = []
    for j in range(0, len(playerHonorsGameModes)+1):
        for k in range(0,60):
            try:
                playerSeasonPlayedHtml.append(playerHonorsGameModes[j].find_all("div",{"style":"line-height:19px;"})[k])
            except IndexError:
                break
    for l in range(0,len(playerSeasonPlayedHtml)):
        playerSeasonPlayed.append(playerSeasonPlayedHtml[l].text.split("\n")[0])

    return playerSeasonPlayed

def higherSkillCheckUGC(playerSeasonPlayed, higherSkilledPlayerIDListUGC, playerID, id64List, id64):
    for i in range(0,len(playerSeasonPlayed)):
        if "Platinum" in playerSeasonPlayed[i] or "Premium" in playerSeasonPlayed[i] or "Gold" in playerSeasonPlayed[i] or "Silver" in playerSeasonPlayed[i]:
            if higherSkilledPlayerIDListUGC.count(playerID) == 0:
                higherSkilledPlayerIDListUGC.append(playerID)
                id64List.append(id64)
    return higherSkilledPlayerIDListUGC, id64List