def makeTeamDict(idList, requestList):
    teamDict = {}

    for i in range(0, len(idList)):
        update = {idList[i]: requestList[i]}
        teamDict.update(update)
    return teamDict


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = []
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


def getTeamIDList(teamDict):
    prem = getKeysByValue(teamDict, "Premiership")
    high = getKeysByValue(teamDict, "High")
    mid = getKeysByValue(teamDict, "Mid")
    low = getKeysByValue(teamDict, "Low")
    open = getKeysByValue(teamDict, "Fresh")
    none = getKeysByValue(teamDict, "")

    teamIDList = []
    counterDict = {}

    if prem != []:
        for ID in prem:
            teamIDList.append(ID)
        update = {"Premiership": len(prem)}
        counterDict.update(update)

    if high != []:
        for ID in high:
            teamIDList.append(ID)
        update = {"High": len(high)}
        counterDict.update(update)

    if mid != []:
        for ID in mid:
            teamIDList.append(ID)
        update = {"Mid": len(mid)}
        counterDict.update(update)

    if low != []:
        for ID in low:
            teamIDList.append(ID)
        update = {"Low": len(low)}
        counterDict.update(update)

    if open != []:
        for ID in open:
            teamIDList.append(ID)
        update = {"Open": len(open)}
        counterDict.update(update)
    if none != []:
        for ID in none:
            teamIDList.append(ID)

    return teamIDList, counterDict
