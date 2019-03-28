from BaseFunctions.ETF2lBase import getCompList, getTeamIDs, dateHourToUnix, getTransfers, setGameMode, getTeamDiv
from BaseFunctions.HijackAndSkillContribBase import teamSkillHS, transferCheck, getPlayerSkillHS, activeLineup

# Set the 2 competition ID's and the ID of the competition from which on forward results should be taken into account
#currentMainCompID = 605
#currentTopCompID = 607
#oldCompID = 534
currentMainCompID = 609
currentTopCompID = 611
oldCompID = 540

#Input the date and time the provisional tiers were released. Also input how far back the system should look for results of teams and players.
#date= "25/01/2019"
#hour = "23:59:00"
date= "8/03/2019"
hour = "18:00:00"
daysToCheck = 7

# Input the gamemode that needs to be checked. HL for highlander, 6s for 6v6
gameType = "HL"

# Input the player id of players allowed as late joiners, between '' seperated by commas
#allowedPlayerIDlist = ['134441','131389','103093','130003','132451','121701','107775','6524','131404','119619','20688','133443','88995','32632','131255','']
allowedPlayerIDlist = ['96704','105085','122594','126619','93063','118721','82109','125630']


def main(currentMainCompID, currentTopCompID, oldCompID, date, hour, daysToCheck, gameType, allowedPlayerIDlist):

    activeJoinLimit, skillContribLimit = setGameMode(gameType)
    provisionalsRelease = dateHourToUnix(date,hour)
    compList6v6, compListHL = getCompList(oldCompID, currentTopCompID)
    fullCompList6v6, fullCompListHL = getCompList(1, currentTopCompID)
    teamIDList = getTeamIDs(currentMainCompID)


    for teamID in teamIDList:
        activePlayerIDlist = []
        teamHL = dict(prem=0, div1=0, high=0, mid=0, low=0, open=0, none=0)
        team6s = dict(prem=0, div1=0, div2=0, mid=0, low=0, open=0, none=0)
        activePlayer = 0
        totalJoins = 0
        playerScore = 0
        skillContribTotal6s = 0
        skillContribTotalHL = 0
        waterfall = []

        transfers = getTransfers(teamID, provisionalsRelease)
        if transfers is None:
            totalJoins = 0
        else:
            playerIDList, totalJoins = transferCheck(transfers, teamID, allowedPlayerIDlist, daysToCheck)
            if len(playerIDList) == 0:
                continue
            else:
                teamDiv = getTeamDiv(teamID, currentMainCompID, currentTopCompID)
                for playerID in playerIDList:
                    isActivePlayer = activeLineup(teamID, playerID, daysToCheck)
                    if isActivePlayer > 0:
                        activePlayer = activePlayer + 1
                        if playerID not in activePlayerIDlist:
                            activePlayerIDlist.append(playerID)
                    playerHL, player6s, HLMatchCount, SMatchCount = getPlayerSkillHS(playerID, teamDiv, fullCompList6v6,fullCompListHL, compList6v6, compListHL)
                    team6s, teamHl, skillContribTotal6s, skillContribTotalHL, waterfall = teamSkillHS(player6s, playerHL, team6s, teamHL,  skillContribTotal6s, skillContribTotalHL, HLMatchCount, SMatchCount, playerID, teamID, activePlayerIDlist, waterfall, currentMainCompID, currentTopCompID)

        # Log output to the cosole for each team
        Sseperate = 'Prem: ' + str(team6s['prem']) + ', Div1: ' + str(team6s['div1']) + ', Div2: ' + str(team6s['div2']) + ', Mid: ' + str(team6s['mid']) + ', Low: ' + str(team6s['low']) + ', Open: ' + str(team6s['open']) + ', None: ' + str(team6s['none'])
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(team6s['div1']) + ', High: ' + str(teamHL['high']) + ', Mid: ' + str(teamHL['mid']) + ', Low: ' + str(teamHL['low']) + ', Open: ' + str(teamHL['open']) + ', None:' + str(teamHL['none'])
        if ((activePlayer >= activeJoinLimit or (skillContribTotal6s >= skillContribLimit)) and gameType == "6s") or ((activePlayer >= activeJoinLimit or (skillContribTotalHL >= skillContribLimit)) and gameType == "HL"):
            print("[team id = " + str(teamID) + "], this team is a " + teamDiv + " team")
            print("Number of joins since provisionals released: " + str(totalJoins))
            print("PlayerID of the joiners:")
            for playerID in playerIDList:
                print("[player id = " + str(playerID) + "]")
            print("Number of late joiners actively playing for the team: " + str(activePlayer))
            print("PlayerID of active late joiners: ")
            for activePlayerID in activePlayerIDlist:
                print("[player id = " + str(activePlayerID) + "]")
            print("6S skill of joiners: " + str(Sseperate))
            print("6S skill  contirbution of joiners cummulitative: " + str(skillContribTotal6s))
            print("HL skill of joiners:" + str(Hlseperate))
            print("HL skill contirbution of joiners cummulitative: " + str(skillContribTotalHL) + "\n")
            for waterfallID in waterfall:
                print("[player id = " + str(waterfallID) + "], has three or more games played in different divisions, check his profile")
        if len(waterfall) >= activeJoinLimit:
            print("\n -------------------------------- \n Team Detected by waterfall \n -------------------------------- \n")
            print("[team id = " + str(teamID) + "], this team is a " + teamDiv + " team")
            print("Number of joins since provisionals released: " + str(totalJoins))
            for waterfallID in waterfall:
                print("[player id = " + str(waterfallID) + "], has three or more games played in different divisions, check his profile")

main(currentMainCompID, currentTopCompID, oldCompID, date, hour, daysToCheck, gameType, allowedPlayerIDlist)
