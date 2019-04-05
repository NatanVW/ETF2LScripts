from BaseFunctions.ETF2lBase import getCompList, getPlayers, getSteamID64, getTeamIDs
from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, higherSkillCheckETF2LFMC, playerSkill
from BaseFunctions.RGLSkillCheck import getPlayerHistory, getDivisionPlayed, higherSkillCheckRGL
from BaseFunctions.UGCSkillCheck import getPlayerHonors, higherSkillCheckUGC
from BaseFunctions.OZFortressSkillCheck import getPlayerPage, getSeasonsPlayed, higherSkillCheckOZ

# Set the competition ID and the ID of the competition from which on forward results should be taken into account
compID = 616
oldCompID = 1

# Don't edit anything past this point if you have no idea what you are doing

def main(compID, oldCompID):
    compList6v6, compListHL = getCompList(oldCompID, compID)
    teamIDList = getTeamIDs(compID)
    for teamID in teamIDList:
        higherSkilledPlayerIDListETF2L =[]

        higherSkilledPlayerIDListRGL =[]
        RGLNameList = []
        id64ListRGL = []

        higherSkilledPlayerIDListUGC = []
        id64ListUGC = []

        higherSkilledPlayerIDListOZ = []
        OZProfileList = []

        playerIDList = getPlayers(teamID)
        for playerID in playerIDList:
            # ETF2L skill check
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = getPlayerSkill(playerID, compList6v6, compListHL)
            higherSkilledPlayerIDListETF2L = higherSkillCheckETF2LFMC(player6s, playerHL, HLMatchCount, SMatchCount, playerID, higherSkilledPlayerIDListETF2L, previousFMC)

            # RGL skill check
            id64 = getSteamID64(playerID)
            playerHistory, name = getPlayerHistory(id64)
            if playerHistory != 0 and name != 0:
                seasonsPlayed, divisionsPlayed, matchCount = getDivisionPlayed(playerHistory)
                higherSkilledPlayerIDListRGL, id64ListRGL, RGLNameList = higherSkillCheckRGL(seasonsPlayed, divisionsPlayed, matchCount, higherSkilledPlayerIDListRGL, playerID, id64ListRGL, id64, RGLNameList, name)

            # UGC skill check
            playerHonors =  getPlayerHonors(id64)
            higherSkilledPlayerIDListUGC, id64ListUGC = higherSkillCheckUGC(playerHonors, higherSkilledPlayerIDListUGC, playerID, id64ListUGC, id64)

            # OZFortress skill check
            playerPage = getPlayerPage(id64)
            seasonsPlayed = getSeasonsPlayed(playerPage)
            higherSkilledPlayerIDListOZ, OZProfileList = higherSkillCheckOZ(seasonsPlayed, playerID, higherSkilledPlayerIDListOZ, playerPage, OZProfileList)

        if higherSkilledPlayerIDListETF2L != [] or higherSkilledPlayerIDListRGL != [] or higherSkilledPlayerIDListUGC != [] or higherSkilledPlayerIDListOZ != []:
            print("[team id = " + str(teamID) + "]:")
            if higherSkilledPlayerIDListETF2L != []:
                print("has " + str(len(higherSkilledPlayerIDListETF2L)) + " ETF2L players with a to high skill level to participate in the cup:")
                for i in range(0,len(higherSkilledPlayerIDListETF2L)):
                    print("[player id =" + str(higherSkilledPlayerIDListETF2L[i]) + "]")
                print("")

            if higherSkilledPlayerIDListRGL != []:
                print("has " + str(len(higherSkilledPlayerIDListRGL)) + " RGL players with a to high skill level to participate in the cup:")
                for j in range(0,len(higherSkilledPlayerIDListRGL)):
                    print("[player id =" + str(higherSkilledPlayerIDListRGL[j]) + "], RGL name: " + str(RGLNameList[j]) + " and steamid64: " + str(id64ListRGL[j]))
                print("")

            if higherSkilledPlayerIDListUGC != []:
                print("has " + str(len(higherSkilledPlayerIDListUGC)) + " UGC players with a to high skill level to participate in the cup:")
                for k in range(0,len(higherSkilledPlayerIDListUGC)):
                    print("[player id =" + str(higherSkilledPlayerIDListUGC[k]) + "], UGC profile: https://www.ugcleague.com/players_page.cfm?player_id=" + str(id64ListUGC[k]))
                print("")

            if higherSkilledPlayerIDListOZ != []:
                print("has " + str(len(higherSkilledPlayerIDListOZ)) + " OZFortress players with a to high skill level to participate in the cup:")
                for n in range(0, len(higherSkilledPlayerIDListOZ)):
                    print("[player id =" + str(higherSkilledPlayerIDListOZ[n]) + "], OZFortress profile:" + str(OZProfileList[n]))
                print("")


main(compID, oldCompID)
