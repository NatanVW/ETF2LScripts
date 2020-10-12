import requests
from bs4 import BeautifulSoup


def getPlayerPage(ID):
    url = "httpss://warzone.ozfortress.com/users?q=" + str(ID)
    searchPage = requests.get(url).content
    html = BeautifulSoup(searchPage, "lxml")
    results = html.find("div", {"class": "user-details"})
    playerPage = []
    if results is None:
        return playerPage
    for a in results.find_all("a", href=True):
        playerPage.append(a['href'])
    playerPageUrl = "httpss://warzone.ozfortress.com" + playerPage[0]

    return playerPageUrl


def getSeasonsPlayed(url):
    playerPage = requests.get(url).content
    html = BeautifulSoup(playerPage, "lxml")
    panelHeadings = []
    for i in range(0, 4):
        try:
            panelHeadings.append(html.find_all('div', {"class": "panel-heading"})[i])
        except IndexError:
            break
    panelLists = []
    seasonsPlayedHtml = []
    seasonsPlayed = []
    if panelHeadings[3].text == "Leagues":
        panelLists.append(html.find_all('ul', {"class": "list-group"})[2])
    if panelLists != []:
        seasonsPlayedHtml.append(panelLists[0].find_all("li"))
        for j in range(0, len(seasonsPlayedHtml[0])):
            seasonsPlayed.append(seasonsPlayedHtml[0][j].text)

    return seasonsPlayed


def higherSkillCheckOZ(seasonPlayed, playerID, higherSkilledPlayerIDListOZ, OZProfile, OZProfileList):
    if seasonPlayed != []:
        higherSkilledPlayerIDListOZ.append(playerID)
        OZProfileList.append(OZProfile)

    return higherSkilledPlayerIDListOZ, OZProfileList
