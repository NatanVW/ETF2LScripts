from BaseFunctions.ETF2lBase import getCompList, getPlayers, getTeamName
from BaseFunctions.ETF2LSkillCheck import getPlayerSkill, teamSkill

# Set the competition ID and the ID of the competition from which on forward results should be taken into account
currentMainCompID = 609
oldCompID = 530

def main(oldCompId, compID):

    compList6v6, compListHL = getCompList(oldCompID, currentMainCompID)
    #teamIDList = getTeamIDs(compID)
    teamIDList = ['24746', '25734', '18974', '23483', '27488', '17127', '31651', '18707', '30835', '29616', '31499', '30263', '31155', '30688', '29912', '29042', '31646', '17798', '30395', '29771', '31253', '30320', '25568', '30679', '31272', '30834', '31614', '31230', '27530', '31629', '31292', '31236', '31678', '31684', '19273', '30792', '31641', '31633', '31619', '30300', '13849', '28121', '30545', '19058', '31653', '31477', '31630', '31510', '31412', '31623', '31405', '31023', '31029', '30316', '31592', '31240', '29174', '31605', '31568', '31638', '31551', '31615', '30801', '31300', '31612', '31679', '30266', '31672', '31637', '31654', '31685']
    for teamID in teamIDList:
        teamHL = dict(prem=0, div1=0, high=0, mid=0, low=0, open=0, none=0)
        team6s = dict(prem=0, div1=0, div2=0, mid=0, low=0, open=0, none=0)
        playerIDList = getPlayers(teamID)
        teamName = getTeamName(teamID)
        for playerID in playerIDList:
            playerHL, player6s, HLMatchCount, SMatchCount= getPlayerSkill(playerID, compList6v6, compListHL)
            #print(playerID, player6s)
            team6s, teamHl= teamSkill(player6s, playerHL, team6s, teamHL, HLMatchCount, SMatchCount)

        Sseperate = 'Prem: ' + str(team6s['prem']) + ', Div1: ' + str(team6s['div1']) + ', Div2: ' + str(team6s['div2']) + ', Mid: ' + str(team6s['mid']) + ', Low: ' + str(team6s['low']) + ', Open: ' + str(team6s['open']) + ', None: ' + str(team6s['none'])
        STotal = team6s['prem'] * 6 + team6s['div1'] * 5 + team6s['div2'] * 4 + team6s['mid'] * 3 + team6s['low'] * 2 + team6s['open']
        Hlseperate = 'Prem: ' + str(teamHL['prem']) + ', Div1: ' + str(team6s['div1']) + ', High: ' + str(teamHL['high']) + ', Mid: ' + str(teamHL['mid']) + ', Low: ' + str(teamHL['low']) + ', Open: ' + str(teamHL['open']) + ', None:' + str(teamHL['none'])
        HlTotal = teamHL['prem'] * 6 + teamHL['div1'] * 5 + teamHL['high'] * 4 + teamHL['mid'] * 3 + teamHL['low'] * 2 + teamHL['open']

        print(str(teamID) + "\t \t " + teamName + "\t" + str(len(playerIDList)) + "\t \t \t \t \t" + str(STotal) + "\t" + Sseperate + "\t" + str(HlTotal) + "\t" + Hlseperate)

main(oldCompID, currentMainCompID)