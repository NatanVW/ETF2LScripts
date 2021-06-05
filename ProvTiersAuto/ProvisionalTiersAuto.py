import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, teamSkill
from BaseFunctions.ETF2lBase import getCompList, getPlayers, getTeamName
from ProvTiersAuto.ProvTiersBase import makeTeamDict, getTeamIDList, setGameMode

# Input the team ID list and the requested tier list. Either input a list of strings or a string where each item is seperated by a tab
idList = "26973	33328	33680	33687	33656	13849	18974	32334	25693	33644	32388	32781	32957	32366	33631	33314	32786	32871	33527	33603	32475	32137	33559	33654	33634	27530	33523	33031	32897	32212	31684	32303	33673	31253	32362	32172	29616	33696	32342	32905	33337	33610	24746	31678	25734	32883	19335	32106	32804	30263	32972	25568	33316	32234	32500	32396	31477	17798	32422	33727	33695	33729	32373	33717	33611	32868	33690	33526	33734	33742	28121	33037	32861	33692	33355	32743	33721"
requestList = "Mid	Open	Open	Open	Open	Open	Premiership	Low	Premiership	Low	Low	Low	Open	Low	Open	Open	Mid	Low	Open	Low	Mid	Low	Open	Open	Open	Mid	Open	Mid	High	High	High	High	Open	High	Open	High	Premiership	Mid	Mid	Open	Open	Open	Premiership	High	High	High	Premiership	Mid	Mid	High	Open	High	Open	High	High	Open	Low	Mid	Mid	Premiership	Low	Premiership	Mid	Low	Mid	Low	Mid	Open	Open	Mid	High	High	Mid	Mid	Mid	Low	Low"
# Set the competition ID and the ID of the competition from which on forward results should be taken into account
currentMainCompID = 713
oldCompID = 628

# Enter the name of the season, will be used as the worksheet title
seasonName = "HL Season 24"

# Input the gamemode that needs to be checked. HL for highlander, 6s for 6v6
gameType = "HL"

# Input whether you want to make the "Base Sheet" or the sheet to "iframe", leave blank to generate both
sheetMode = "Base Sheet"

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
        teamHL = dict(prem=0, div1=0, high=0, div2=0, div3=0, mid=0, div4=0, low=0, div5=0, div6=0, open=0, none=0)
        team6s = dict(prem=0, div1=0, high=0, div2=0, div3=0, mid=0, div4=0, low=0, div5=0, div6=0, open=0, none=0)
        playerIDList = getPlayers(teamID)
        while playerIDList == []:
            playerIDList = getPlayers(teamID)
        teamName = getTeamName(teamID)
        for playerID in playerIDList:
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = getPlayerSkill(playerID, compList6v6, compListHL)
            team6s, teamHl = teamSkill(player6s, playerHL, team6s, teamHL, HLMatchCount, SMatchCount)

        Sseperate = 'Prem: ' + str(team6s['prem']) + ', Div1: ' + str(team6s['div1']) + ', high: ' + str(
            team6s['high']) + ', Div2: ' + str(team6s['div2']) + ', Div3: ' + str(team6s['div3']) + ', Mid: ' + str(
            team6s['mid']) + ', Div4: ' + str(team6s['div4']) + ', Low: ' + str(
            team6s['low']) + ', Div5: ' + str(team6s['div5']) + ', Open: ' + str(team6s['div6']) + ', None: ' + str(
            team6s['none'])
        STotal = team6s['prem'] * 28 + team6s['div1'] * 24 + team6s['high'] * 22 + team6s['div2'] * 20 + team6s[
            'div3'] * 16 + team6s['mid'] * 15 + team6s['div4'] * 12 + team6s['low'] * 9 + team6s['div5'] * 8 + team6s[
                     'div6'] * 4
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(teamHL['div1']) + ', high: ' + str(
            teamHL['high']) + ', Div2: ' + str(teamHL['div2']) + ', Div3: ' + str(teamHL['div3']) + ', Mid: ' + str(
            teamHL['mid']) + ', Div4: ' + str(teamHL['div4']) + ', Low: ' + str(
            teamHL['low']) + ', Div5: ' + str(teamHL['div5']) + ', Open: ' + str(teamHL['div6']) + ', None: ' + str(
            teamHL['none'])
        HlTotal = teamHL['prem'] * 28 + teamHL['div1'] * 24 + teamHL['high'] * 22 + teamHL['div2'] * 20 + teamHL[
            'div3'] * 16 + teamHL['mid'] * 15 + teamHL['div4'] * 12 + teamHL['low'] * 9 + teamHL['div5'] * 8 + teamHL[
                      'div6'] * 4
        teamLink = "https://etf2l.org/teams/" + str(teamID)
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
