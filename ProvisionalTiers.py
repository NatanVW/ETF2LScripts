from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, teamSkill
from BaseFunctions.ETF2lBase import getCompList, getPlayers, getTeamName, getTeamIDs

# Set the competition ID and the ID of the competition from which on forward results should be taken into account
currentMainCompID = 670
oldCompID = 549


# Don't edit anything past this point if you have no idea what you are doing

def main(oldCompId, compID):
    compList6v6, compListHL = getCompList(oldCompID, compID)
    teamIDList = getTeamIDs(compID)
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
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(teamHL['div1']) + ', High: ' + str(teamHL['high']) + ', Mid: ' + str(teamHL['mid']) + ', Low: ' + str(
            teamHL['low']) + ', Open: ' + str(teamHL['open']) + ', None:' + str(teamHL['none'])
        HlTotal = teamHL['prem'] * 6 + teamHL['div1'] * 5 + teamHL['high'] * 4 + teamHL['mid'] * 3 + teamHL['low'] * 2 + teamHL['open']

        print(str(teamID) + "\t \t " + teamName + "\t" + str(len(playerIDList)) + "\t \t \t \t \t" + str(STotal) + "\t" + Sseperate + "\t" + str(HlTotal) + "\t" + Hlseperate)


main(oldCompID, currentMainCompID)
