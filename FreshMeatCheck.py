from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, higherSkillCheckETF2LFMC
from BaseFunctions.ETF2lBase import getCompList, getPlayers, getSteamID64, getTeamIDs
from BaseFunctions.OZFortressSkillCheck import getPlayerPage, getSeasonsPlayed, higherSkillCheckOZ
from BaseFunctions.RGLSkillCheck import getPlayerHistory, getDivisionPlayed, higherSkillCheckRGL
from BaseFunctions.UGCSkillCheck import getPlayerHonors, higherSkillCheckUGC

# Set the competition ID and the ID of the competition from which on forward results should be taken into account
compID = 616
oldCompID = 1

buddyList = ['92243', '115603', '125750', '128505', '124029', '119817', '132120', '134799', '100703', '120310', '130668', '105661', '119387', '128088', '119226', '113520', '76592','116844',
             '120821', '105723', '129856', '132748', '92166', '128843', '129693', '133392', '125974', '130747', '125288', '94955', '109742', '129461', '134022', '131198', '133068', '46526',
             '121437', '48288', '110553', '130585', '112758', '125319', '132189', '120255', '122019', '129763', '101292', '127614', '124688', '68635', '118996', '130898', '136112', '117770',
             '59560', '94026', '112699', '126040', '127879', '7243', '130169', '105093', '126757', '131140', '58862', '126665', '118980', '129551', '126473', '125181', '93023', '131953',
             '131953', '70534']


# Don't edit anything past this point if you have no idea what you are doing

def main(compID, oldCompID, buddyList):
    compList6v6, compListHL = getCompList(oldCompID, compID)
    teamIDList = getTeamIDs(compID)
    for teamID in teamIDList:
        higherSkilledPlayerIDListETF2L = []

        higherSkilledPlayerIDListRGL = []
        RGLNameList = []
        id64ListRGL = []

        higherSkilledPlayerIDListUGC = []
        id64ListUGC = []

        higherSkilledPlayerIDListOZ = []
        OZProfileList = []

        playerIDList = getPlayers(teamID)
        for playerID in playerIDList:
            if str(playerID) in buddyList:
                continue
            # ETF2L skill check
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = getPlayerSkill(playerID, compList6v6, compListHL)
            higherSkilledPlayerIDListETF2L = higherSkillCheckETF2LFMC(player6s, playerHL, HLMatchCount, SMatchCount, playerID, higherSkilledPlayerIDListETF2L, previousFMC)

            # RGL skill check
            id64 = getSteamID64(playerID)
            playerHistory, name = getPlayerHistory(id64)
            if playerHistory != 0 and name != 0:
                seasonsPlayed, divisionsPlayed, matchCount = getDivisionPlayed(playerHistory)
                higherSkilledPlayerIDListRGL, id64ListRGL, RGLNameList = higherSkillCheckRGL(seasonsPlayed, divisionsPlayed, matchCount, higherSkilledPlayerIDListRGL, playerID, id64ListRGL,
                                                                                             id64, RGLNameList, name)

            # UGC skill check
            playerHonors = getPlayerHonors(id64)
            higherSkilledPlayerIDListUGC, id64ListUGC = higherSkillCheckUGC(playerHonors, higherSkilledPlayerIDListUGC, playerID, id64ListUGC, id64)

            # OZFortress skill check
            playerPage = getPlayerPage(id64)
            if playerPage == []:
                continue
            seasonsPlayed = getSeasonsPlayed(playerPage)
            higherSkilledPlayerIDListOZ, OZProfileList = higherSkillCheckOZ(seasonsPlayed, playerID, higherSkilledPlayerIDListOZ, playerPage, OZProfileList)

        if higherSkilledPlayerIDListETF2L != [] or higherSkilledPlayerIDListRGL != [] or higherSkilledPlayerIDListUGC != [] or higherSkilledPlayerIDListOZ != []:
            print("[team id = " + str(teamID) + "]:")
            if higherSkilledPlayerIDListETF2L != []:
                print("has " + str(len(higherSkilledPlayerIDListETF2L)) + " ETF2L player(s) with a to high skill level to participate in the cup:")
                for i in range(0, len(higherSkilledPlayerIDListETF2L)):
                    print("[player id =" + str(higherSkilledPlayerIDListETF2L[i]) + "]")
                print("")

            if higherSkilledPlayerIDListRGL != []:
                print("has " + str(len(higherSkilledPlayerIDListRGL)) + " RGL player(s) with a to high skill level to participate in the cup:")
                for i in range(0, len(higherSkilledPlayerIDListRGL)):
                    print("[player id =" + str(higherSkilledPlayerIDListRGL[i]) + "], RGL name: " + str(RGLNameList[i]) + " and steamid64: " + str(id64ListRGL[i]))
                print("")

            if higherSkilledPlayerIDListUGC != []:
                print("has " + str(len(higherSkilledPlayerIDListUGC)) + " UGC player(s) with a to high skill level to participate in the cup:")
                for i in range(0, len(higherSkilledPlayerIDListUGC)):
                    print("[player id =" + str(higherSkilledPlayerIDListUGC[i]) + "], UGC profile: https://www.ugcleague.com/players_page.cfm?player_id=" + str(id64ListUGC[i]))
                print("")

            if higherSkilledPlayerIDListOZ != []:
                print("has " + str(len(higherSkilledPlayerIDListOZ)) + " OZFortress player(s) with a to high skill level to participate in the cup:")
                for i in range(0, len(higherSkilledPlayerIDListOZ)):
                    print("[player id =" + str(higherSkilledPlayerIDListOZ[i]) + "], OZFortress profile:" + str(OZProfileList[i]))
                print("")
            print("")


main(compID, oldCompID, buddyList)
