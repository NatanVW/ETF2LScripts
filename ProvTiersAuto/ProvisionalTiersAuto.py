import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, teamSkill
from BaseFunctions.ETF2lBase import getCompList, getPlayers, getTeamName
from ProvTiersAuto.ProvTiersBase import makeTeamDict, getTeamIDList, setGameMode

# Input the team ID list and the requested tier list. Either input a list of strings or a string where each item is seperated by a tab
idList = ""
requestList = ""
# Set the competition ID and the ID of the competition from which on forward results should be taken into account
currentMainCompID = 628
oldCompID = 1

# Enter the name of the season, will be used as the worksheet title
seasonName = ""

# Input the gamemode that needs to be checked. HL for highlander, 6s for 6v6
gameType = ""

# Input whether you want to make the "Base Sheet" or the sheet to "iframe", leave blank to generate both
sheetMode = ""

# Don't edit anything past this point if you have no idea what you are doing

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('admin_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('ETF2L Provisional Tiers')


def main(gameType, idList, requestList, sheetMode):
    if sheetMode == "Base Sheet":
        divList, teamIDList, counterDict, teamDict = setup(gameType, idList, requestList)
        mainSheet(oldCompID, currentMainCompID, divList, teamIDList, counterDict, teamDict)

    if sheetMode == "iframe":
        divList, teamIDList, counterDict, teamDict = setup(gameType, idList, requestList)
        iframeSheet(counterDict, divList)

    if sheetMode == "":
        divList, teamIDList, counterDict, teamDict = setup(gameType, idList, requestList)
        mainSheet(oldCompID, currentMainCompID, divList, teamIDList, counterDict, teamDict)
        iframeSheet(counterDict, divList)


def setup(gameType, idList, requestList):
    divList = setGameMode(gameType)
    teamDict = makeTeamDict(idList, requestList)
    teamIDList, counterDict = getTeamIDList(teamDict)

    if gameType == "HL":
        counterDict["Open"] += counterDict["Low"]
        counterDict.pop("Low")

    return divList, teamIDList, counterDict, teamDict


def mainSheet(oldCompID, compID, divList, teamIDList, counterDict, teamDict):
    try:
        baseSheet = sheet.worksheet(seasonName + " Base")
        sheet.del_worksheet(baseSheet)
        baseSheet = sheet.add_worksheet(title=seasonName + " Base", rows="4", cols="20")
    except gspread.exceptions.WorksheetNotFound:
        baseSheet = sheet.add_worksheet(title=seasonName + " Base", rows="4", cols="20")
    compList6v6, compListHL = getCompList(oldCompID, compID)
    counterList = []
    for value in counterDict.values():
        counterList.append(value)
    i = 1
    row = ["Premiership", "", "Players on roster", "Requested", "", "", "6s total", "6s seperate", "HL total", "HL total"]
    baseSheet.insert_row(row, i)
    i += 1
    for teamID in teamIDList:
        teamHL = dict(prem=0, div1=0, high=0, mid=0, low=0, open=0, none=0)
        team6s = dict(prem=0, div1=0, div2=0, mid=0, low=0, open=0, none=0)
        playerIDList = getPlayers(teamID)
        while playerIDList == []:
            playerIDList = getPlayers(teamID)
        teamName = getTeamName(teamID)
        for playerID in playerIDList:
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = getPlayerSkill(playerID, compList6v6, compListHL)
            team6s, teamHl = teamSkill(player6s, playerHL, team6s, teamHL, HLMatchCount, SMatchCount)

        Sseperate = 'Prem: ' + str(team6s['prem']) + ', Div1: ' + str(team6s['div1']) + ', Div2: ' + str(team6s['div2']) + ', Mid: ' + str(team6s['mid']) + ', Low: ' + str(
            team6s['low']) + ', Open: ' + str(team6s['open']) + ', None: ' + str(team6s['none'])
        STotal = team6s['prem'] * 6 + team6s['div1'] * 5 + team6s['div2'] * 4 + team6s['mid'] * 3 + team6s['low'] * 2 + team6s['open']
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(teamHL['div1']) + ', High: ' + str(teamHL['high']) + ', Mid: ' + str(teamHL['mid']) + ', Low: ' + str(
            teamHL['low']) + ', Open: ' + str(teamHL['open']) + ', None:' + str(teamHL['none'])
        HlTotal = teamHL['prem'] * 6 + teamHL['div1'] * 5 + teamHL['high'] * 4 + teamHL['mid'] * 3 + teamHL['low'] * 2 + teamHL['open']
        teamLink = "http://etf2l.org/teams/" + str(teamID)
        teamLinkName = '=HYPERLINK("' + teamLink + '";"' + teamName + '")'

        for k in range(0, len(counterList)):
            if counterList[k] >= 0:
                if counterList[k] == 0:
                    baseSheet.insert_row([divList[k]], i)
                    i += 1
                    try:
                        baseSheet.insert_row([divList[k + 1]], i)
                        i += 1
                    except IndexError:
                        break
                    counterList[k + 1] -= 1
                counterList[k] -= 1

                row = [str(teamID), teamLinkName, str(len(playerIDList)), teamDict[teamID], "", "", str(STotal), Sseperate, str(HlTotal), Hlseperate]
                baseSheet.insert_row(row, i, value_input_option='USER_ENTERED')
                i += 1
                break


def iframeSheet(counterDict, divList):
    counterDictSum = 0
    for value in counterDict.values():
        counterDictSum += value

    frameSheet = sheet.add_worksheet(title=seasonName, rows=math.ceil(counterDictSum / 2 + 9), cols="2")
    frameSheet.update_cell(1, 1, divList[0])
    j = 2
    k = j
    for l in range(0, len(divList)):
        for i in range(k, counterDict[divList[l]] + k):
            referenceSheet = "='" + seasonName + " Base'!B" + str(j)
            if i < math.ceil(counterDict[divList[l]] / 2) + k:
                frameSheet.update_cell(i, 1, referenceSheet)
            else:
                frameSheet.update_cell(i - math.ceil(counterDict[divList[l]] / 2), 2, referenceSheet)
            j += 1

        frameSheet.update_cell(k + math.ceil(counterDict[divList[l]] / 2), 1, divList[l])
        try:
            frameSheet.update_cell(k + 1 + math.ceil(counterDict[divList[l]] / 2), 1, divList[l + 1])
        except IndexError:
            break
        j += 2
        cell = frameSheet.find(divList[l + 1])
        k = cell.row + 1


main(gameType, idList, requestList, sheetMode)
