from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, teamSkill
from BaseFunctions.ETF2lBase import getCompList, getPlayers, getTeamName, getTeamIDs

# Set the competition ID and the ID of the competition from which on forward results should be taken into account
currentMainCompID = 692
oldCompID = 628


# Don't edit anything past this point if you have no idea what you are doing

def main(oldCompId, compID):
    compList6v6, compListHL = getCompList(oldCompID, compID)
    teamIDList = getTeamIDs(compID)
    for teamID in teamIDList:
        teamHL = dict(prem=0, div1=0, high=0, div2=0, div3=0, mid=0, div4=0, low=0, div5=0, div6=0, open=0, none=0)
        team6s = dict(prem=0, div1=0, high=0, div2=0, div3=0, mid=0, div4=0, low=0, div5=0, div6=0, open=0, none=0)
        playerIDList = getPlayers(teamID)
        teamName = getTeamName(teamID)
        for playerID in playerIDList:
            playerHL, player6s, HLMatchCount, SMatchCount, previousFMC = getPlayerSkill(playerID, compList6v6, compListHL)
            team6s, teamHl = teamSkill(player6s, playerHL, team6s, teamHL, HLMatchCount, SMatchCount)

        Sseperate = 'Prem: ' + str(team6s['prem']) + ', Div1: ' + str(team6s['div1']) + ', high: ' + str(team6s['high']) + ', Div2: ' + str(team6s['div2']) + ', Div3: ' + str(team6s['div3']) + ', Mid: ' + str(team6s['mid']) + ', Div4: ' + str(team6s['div4']) + ', Low: ' + str(
            team6s['low']) + ', Div5: ' + str(team6s['div5']) + ', Open: ' + str(team6s['div6']) + ', None: ' + str(team6s['none'])
        STotal = team6s['prem'] * 28 + team6s['div1'] * 24 + team6s['high'] * 22 + team6s['div2'] * 20 + team6s['div3'] * 16 + team6s['mid'] * 15 + team6s['div4'] * 12 + team6s['low'] * 9 + team6s['div5'] * 8 + team6s['div6'] * 4
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(teamHL['div1']) + ', high: ' + str(
            teamHL['high']) + ', Div2: ' + str(teamHL['div2']) + ', Div3: ' + str(teamHL['div3']) + ', Mid: ' + str(
            teamHL['mid']) + ', Div4: ' + str(teamHL['div4']) + ', Low: ' + str(
            teamHL['low']) + ', Div5: ' + str(teamHL['div5']) + ', Open: ' + str(teamHL['div6']) + ', None: ' + str(
            teamHL['none'])
        HlTotal = teamHL['prem'] * 28 + teamHL['div1'] * 24 + teamHL['high'] * 22 + teamHL['div2'] * 20 + teamHL[
            'div3'] * 16 + teamHL['mid'] * 15 + teamHL['div4'] * 12 + teamHL['low'] * 9 + teamHL['div5'] * 8 + teamHL[
                     'div6'] * 4

        print(str(teamID) + "\t \t " + teamName + "\t" + str(len(playerIDList)) + "\t \t \t \t \t" + str(STotal) + "\t" + Sseperate + "\t" + str(HlTotal) + "\t" + Hlseperate)


main(oldCompID, currentMainCompID)
