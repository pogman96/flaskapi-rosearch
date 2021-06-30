import json
import requests
from src.findID import convertID

def getInfo(userid):
    with open("config.json") as file:
        data = json.load(file)
    link = data["userinfo"]
    presence = data["presence"]
    request = requests.get(link.replace("REPLACE", str(userid)))
    if request.status_code == 404:
        conversion = convertID(userid)
        if conversion["conversion"]:
            userid = conversion["convertedID"]
            request = requests.get(link.replace("REPLACE", str(userid)))
        else:
            return {"ID":"Invalid"}

    queryData = {"userIds":[int(userid)]}
    query = requests.post(presence, data=queryData).json()
    if query["userPresences"][0]["userPresenceType"] == 2:
        inGame = True
    else:
        inGame = False
    info = request.json()
    return {"ID":"Valid", "username":info["name"], "display name":info["displayName"], "banned":info["isBanned"], "id":int(userid), "ingame":inGame}

