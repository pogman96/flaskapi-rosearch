import json
import requests

def getGameInfo(gameid):
    if not(str(gameid).isnumeric()):
        return {"ID":"Invalid"}

    with open("config.json") as file:
        data = json.load(file)

    gameCheck = data["gametouniverse"]
    link = gameCheck.replace("REPLACE", str(gameid))
    query = requests.get(link)

    if query.status_code == 500:
        return {"ID":"Invalid"}

    elif query.status_code == 200:
        universeID = query.json()["UniverseId"]
        gameDescription = data["universeinfo"]
        gameLink = gameDescription.replace("REPLACE", str(universeID))
        query = requests.get(gameLink)
        queryData = query.json()
        gameName = queryData["data"][0]["name"]
        return {"ID":"Valid", "name":gameName, "id":int(gameid)}

    else:
        return {"response": query.status_code}
