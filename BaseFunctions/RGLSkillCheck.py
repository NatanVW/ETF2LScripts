import json
import requests


def getPlayerHistory(ID):
    baseUrl = "https://payload.tf/api/rgl/" + str(ID)
    data = requests.get(baseUrl).json()
    if data['success']==True:
        return data['name'], data['experience']
    else:
        return 0,0

def getDivisionPlayed(playerHistory,currentHL,current6s):
    playerHL = dict(invite=0, advanced=0, main=0, intermediate=0, amateur=0, newcomer=0)
    player6s = dict(invite=0, advanced=0, main=0, intermediate=0, amateur=0, newcomer=0)
    for i in range(0,len(playerHistory)):
        if playerHistory[i]['category']=="highlander" and (playerHistory[i]['season']=="hl season " + str(currentHL) or playerHistory[i]['season']=="hl season " + str(currentHL-1) or playerHistory[i]['season']=="hl season " + str(currentHL-2)):
            playerHL[playerHistory[i]['div']]+=1
        if playerHistory[i]['category']=="trad. sixes" and (playerHistory[i]['season']=="sixes s" + str(current6s) or playerHistory[i]['season']=="sixes s" + str(current6s-1) or playerHistory[i]['season']=="sixes s" + str(current6s-2)):
            player6s[playerHistory[i]['div']]+=1

    return playerHL, player6s

def getSkillLevel(playerHL,player6s):
    skillLevel6s = None
    skillLevelHL = None
    for key, value in player6s.items():
        if value != 0:
            skillLevel6s = key
    for key, value in playerHL.items():
        if value != 0:
            skillLevelHL = key

    return skillLevelHL, skillLevel6s

def RGLtoETF2L(skillLevelHL, skillLevel6s, teamHL, team6s):
    if skillLevelHL == "invite":
        teamHL['prem']+=1
    elif skillLevelHL == "advanced":
        teamHL['div1']+=1
    elif skillLevelHL == "main":
        teamHL['div2']+=1
    elif skillLevelHL == "intermediate":
        teamHL['mid']+=1
    elif skillLevelHL == "amateur":
        teamHL['low']+=1
    elif skillLevelHL == "newcomer":
        teamHL['open']+=1
    elif skillLevelHL == None:
        teamHL['none']+=1

    if skillLevel6s == "invite":
        team6s['prem']+=1
    elif skillLevel6s == "advanced":
        team6s['div1']+=1
    elif skillLevel6s == "main":
        team6s['div2']+=1
    elif skillLevel6s == "intermediate":
        team6s['mid']+=1
    elif skillLevel6s == "amateur":
        team6s['low']+=1
    elif skillLevel6s == "newcomer":
        team6s['open']+=1
    elif skillLevel6s == None:
        team6s['none']+=1

    return teamHL, team6s