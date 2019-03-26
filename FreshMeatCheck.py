from BaseFunctions.ETF2lBase import getCompList, getPlayers, getSteamID64, getTeamIDs
from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, higherSkillCheckETF2LFMC, playerSkill
from BaseFunctions.RGLSkillCheck import getPlayerHistory, getDivisionPlayed, higherSkillCheckRGL
from BaseFunctions.UGCSkillCheck import getPlayerHonors, higherSkillCheckUGC

compID = 607
oldCompID = 1

def main(compID):
    compList6v6, compListHL = getCompList(oldCompID, compID)
    teamIDList = getTeamIDs(compID)
    for teamID in teamIDList:
        higherSkilledPlayerIDListETF2L =[]
        higherSkilledPlayerIDListRGL =[]
        RGLNameList = []
        higherSkilledPlayerIDListUGC = []
        playerIDList = getPlayers(teamID)
        for playerID in playerIDList:
            # ETF2L skill check
            playerHL, player6s, HLMatchCount, SMatchCount = getPlayerSkill(playerID, compList6v6, compListHL)
            higherSkilledPlayerIDListETF2L = higherSkillCheckETF2LFMC(player6s, playerHL, HLMatchCount, SMatchCount, playerID, higherSkilledPlayerIDListETF2L)

            # RGL skill check
            id64 = getSteamID64(playerID)
            playerHistory, name = getPlayerHistory(id64)
            RGLNameList.append(name)
            if playerHistory != 0 and name != 0:
                seasonsPlayed, divisionsPlayed, matchCount = getDivisionPlayed(playerHistory)
                higherSkilledPlayerIDListRGL = higherSkillCheckRGL(seasonsPlayed, divisionsPlayed, matchCount, higherSkilledPlayerIDListRGL, playerID)

            # UGC skill check
            playerHonors =  getPlayerHonors(id64)
            higherSkilledPlayerIDListUGC = higherSkillCheckUGC(playerHonors, higherSkilledPlayerIDListUGC, playerID)

        if higherSkilledPlayerIDListETF2L != [] or higherSkilledPlayerIDListRGL != [] or higherSkilledPlayerIDListUGC != []:
            print("[team id =" + str(teamID) + "]:")
            if higherSkilledPlayerIDListETF2L != []:
                print("has " + str(len(higherSkilledPlayerIDListETF2L)) + " ETF2L players with a to high skill level to participate in the cup:")
                for i in range(0,len(higherSkilledPlayerIDListETF2L)):
                    print("[player id =" + str(higherSkilledPlayerIDListETF2L[i]) + "]")
                print("")

            if higherSkilledPlayerIDListRGL != []:
                print("has " + str(len(higherSkilledPlayerIDListRGL)) + " RGL players with a to high skill level to participate in the cup:")
                for j in range(0,len(higherSkilledPlayerIDListRGL)):
                    print("[player id =" + str(higherSkilledPlayerIDListRGL[j]) + "], RGL name: " + RGLNameList[j])
                print("")

            if higherSkilledPlayerIDListUGC != []:
                print("has " + str(len(higherSkilledPlayerIDListUGC)) + " UGC players with a to high skill level to participate in the cup:")
                for k in range(0,len(higherSkilledPlayerIDListUGC)):
                    print("[player id =" + str(higherSkilledPlayerIDListUGC[k]) + "], UGC profile: https://www.ugcleague.com/players_page.cfm?player_id=" + str(id64))
                print("")


main(compID)