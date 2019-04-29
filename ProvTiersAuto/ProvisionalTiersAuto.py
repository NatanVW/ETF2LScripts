import sys

sys.path.append('\Etf2lScriptPackage\BaseFunctions')

import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, teamSkill
from BaseFunctions.ETF2lBase import getCompList, getPlayers, getTeamName
from ProvTiersAuto.ProvTiersBase import makeTeamDict, getTeamIDList

# Input the team ID list and the requested tier list
idList = []
requestList = []

# Set the competition ID and the ID of the competition from which on forward results should be taken into account
currentMainCompID = 609
oldCompID = 530

# Enter the name of the season, will be used as the worksheet title
seasonName = "Highlander Season 18"

# Don't edit anything past this point if you have no idea what you are doing

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('admin_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('ETF2L Provisional Tiers')


def mainSheet(oldCompID, compID, idList, requestList):
    baseSheet = sheet.add_worksheet(title=seasonName + " Base", rows="1000", cols="20")
    compList6v6, compListHL = getCompList(oldCompID, compID)
    teamDict = makeTeamDict(idList, requestList)
    teamIDList, counterDict = getTeamIDList(teamDict)
    premCounter, highCounter, midCounter, lowCounter, openCounter = counterDict["Premiership"], counterDict["High"], counterDict["Mid"], counterDict["Low"], counterDict["Open"]
    i = 1
    row = ["Premiership", "", "", "Players on roster", "Requested", "", "", "6s total", "6s seperate", "HL total", "HL total"]
    baseSheet.insert_row(row, i)
    i += 1
    for teamID in teamIDList:
        teamHL = dict(prem=0, div1=0, high=0, mid=0, low=0, open=0, none=0)
        team6s = dict(prem=0, div1=0, div2=0, mid=0, low=0, open=0, none=0)
        playerIDList = getPlayers(teamID)
        teamName = getTeamName(teamID)
        for playerID in playerIDList:
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = getPlayerSkill(playerID, compList6v6, compListHL)
            team6s, teamHl = teamSkill(player6s, playerHL, team6s, teamHL, HLMatchCount, SMatchCount)

        Sseperate = 'Prem: ' + str(team6s['prem']) + ', Div1: ' + str(team6s['div1']) + ', Div2: ' + str(team6s['div2']) + ', Mid: ' + str(team6s['mid']) + ', Low: ' + str(
            team6s['low']) + ', Open: ' + str(team6s['open']) + ', None: ' + str(team6s['none'])
        STotal = team6s['prem'] * 6 + team6s['div1'] * 5 + team6s['div2'] * 4 + team6s['mid'] * 3 + team6s['low'] * 2 + team6s['open']
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(team6s['div1']) + ', High: ' + str(teamHL['high']) + ', Mid: ' + str(teamHL['mid']) + ', Low: ' + str(
            teamHL['low']) + ', Open: ' + str(teamHL['open']) + ', None:' + str(teamHL['none'])
        HlTotal = teamHL['prem'] * 6 + teamHL['div1'] * 5 + teamHL['high'] * 4 + teamHL['mid'] * 3 + teamHL['low'] * 2 + teamHL['open']
        teamLink = "http://etf2l.org/teams/" + str(teamID)
        teamLinkName = '=HYPERLINK("' + teamLink + '";"' + teamName + '")'

        if premCounter >= 0:
            if premCounter == 0:
                baseSheet.insert_row(["Premiership", ], i)
                i += 1
                baseSheet.insert_row(["High", ], i)
                i += 1
                highCounter -= 1
            premCounter -= 1
        elif highCounter >= 0:
            if highCounter == 0:
                baseSheet.insert_row(["High", ], i)
                i += 1
                baseSheet.insert_row(["Mid", ], i)
                i += 1
                midCounter -= 1
            highCounter -= 1
        elif midCounter >= 0:
            if midCounter == 0:
                baseSheet.insert_row(["Mid", ], i)
                i += 1
                baseSheet.insert_row(["Open", ], i)
                i += 1
                lowCounter -= 1
            midCounter -= 1
        elif lowCounter >= 0:
            lowCounter -= 1
        elif openCounter >= 0:
            if openCounter == 0:
                baseSheet.insert_row(["Open", ], i)
                i += 1
            openCounter -= 1

        row = [str(teamID), teamLinkName, teamName, str(len(playerIDList)), teamDict[teamID], "", "", str(STotal), Sseperate, str(HlTotal), Hlseperate]
        baseSheet.insert_row(row, i, value_input_option='USER_ENTERED')
        i += 1

    return counterDict


def iframeSheet(counterDict):
    counterDictSum = counterDict["Premiership"] + counterDict["High"] + counterDict["Mid"] + counterDict["Low"] + counterDict["Open"]
    prem, high, mid, open = "Premiership", "High", "Mid", "Open"
    frameSheet = sheet.add_worksheet(title=seasonName, rows=counterDictSum / 2 + 9, cols="2")
    frameSheet.update_cell(1, 1, prem)
    j = 2
    k = j
    for i in range(k, counterDict["Premiership"] + k):
        referenceSheet = "='" + seasonName + " Base'!B" + str(j)
        if i < math.ceil(counterDict["Premiership"] / 2) + k:
            frameSheet.update_cell(i, 1, referenceSheet)
        else:
            frameSheet.update_cell(i - math.ceil(counterDict["Premiership"] / 2), 2, referenceSheet)
        j += 1
    frameSheet.update_cell(k + math.ceil(counterDict["Premiership"] / 2), 1, prem)
    frameSheet.update_cell(k + 1 + math.ceil(counterDict["Premiership"] / 2), 1, high)

    j += 2
    cell = frameSheet.find("High")
    k = cell.row + 1
    for i in range(k, counterDict["High"] + k):
        referenceSheet = "='" + seasonName + " Base'!B" + str(j)
        if i < math.ceil(counterDict["High"] / 2 + k):
            frameSheet.update_cell(i, 1, referenceSheet)
        else:
            frameSheet.update_cell(i - math.ceil(counterDict["High"] / 2), 2, referenceSheet)
        j += 1
    frameSheet.update_cell(k + math.ceil(counterDict["High"] / 2), 1, high)
    frameSheet.update_cell(k + 1 + math.ceil(counterDict["High"] / 2), 1, mid)

    j += 2
    cell = frameSheet.find("Mid")
    k = cell.row + 1
    for i in range(k, counterDict["Mid"] + k):
        referenceSheet = "='" + seasonName + " Base'!B" + str(j)
        if i < math.ceil(counterDict["Mid"] / 2 + k):
            frameSheet.update_cell(i, 1, referenceSheet)
        else:
            frameSheet.update_cell(i - math.ceil(counterDict["Mid"] / 2), 2, referenceSheet)
        j += 1
    frameSheet.update_cell(k + math.ceil(counterDict["Mid"] / 2), 1, mid)
    frameSheet.update_cell(k + 1 + math.ceil(counterDict["Mid"] / 2), 1, open)

    j += 2
    cell = frameSheet.find("Open")
    k = cell.row + 1
    for i in range(k, counterDict["Open"] + counterDict["Low"] + k):
        referenceSheet = "='" + seasonName + " Base'!B" + str(j)
        if i < math.ceil((counterDict["Open"] + counterDict["Low"]) / 2 + k):
            frameSheet.update_cell(i, 1, referenceSheet)
        else:
            frameSheet.update_cell(i - math.ceil((counterDict["Open"] + counterDict["Low"]) / 2), 2, referenceSheet)
        j += 1
    frameSheet.update_cell(k + math.ceil((counterDict["Open"] + counterDict["Low"]) / 2), 1, open)


counterDict = mainSheet(oldCompID, currentMainCompID, idList, requestList)
iframeSheet(counterDict)
