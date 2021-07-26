from flask import Flask, jsonify
import json
import requests
from src.validityCheck import checkValidity
from src.findServer import findServer
from src.userInfo import getInfo
from src.gameInfo import getGameInfo
from src.findID import convertID
from src.findIDpersist import deepConvertID
from waitress import serve


app = Flask('')
app.config["JSON_SORT_KEYS"] = False

with open("config.json") as file:
    data = json.load(file)

@app.route('/')
def homePage():
  return "Roblox Searcher API"

@app.route("/api/v1/checkValid/<string:userID>/<string:gameID>", methods=["GET"])
def checkValid(userID, gameID):
  return jsonify(checkValidity(userID, gameID))

@app.route("/api/v1/checkUser/<string:username>", methods=["GET"])
def userToID(username):
    return jsonify(convertID(username))

@app.route("/api/v1/checkUserDeep/<string:username>", methods=["GET"])
def userToIDdepth(username):
    return jsonify(deepConvertID(username))
    
@app.route("/api/v1/findUser/<string:userID>/<string:gameID>", methods=["GET"])
def searchUser(userID, gameID):
    valid = checkValidity(userID, gameID)
    user = valid["user"]["valid"]
    game = valid["game"]["valid"]

    if user and game:

        userDetails = getInfo(userID)
        online = userDetails["ingame"]
        gameDetails = getGameInfo(gameID)

        if userDetails["banned"]:
            headshot = data["headshot"]
            link = headshot.replace("USERID", str(userDetails["id"]))
            url = requests.get(link).json()["Url"]
            return jsonify({
            "user":user, "game":game, "banned": userDetails["banned"], "online":online, "ingame":False,
            "userid":userDetails["id"], "gameid":gameDetails["id"],
            "gamename":gameDetails["name"],
            "username":userDetails["username"], "displayname":userDetails["display name"],
            "headshot":url
            })


        if online:

            searchid, url = findServer(userDetails["id"], gameDetails["id"])
            with open("result/results"+str(searchid)+".json") as file:
                results = json.load(file)

            if results["searchid"] != searchid:
                return jsonify({"error":"mismatched search id"})

            if results["In Game"]:
                return jsonify({
                "user":user, "game":game, "banned": userDetails["banned"], "online":online,
                "ingame":results["In Game"], "servercount":results["server amount"],
                "guid":results["guid"], "ping":results["ping"], "players":results["players"],
                "maxplayers":results["max players"], "searchid":results["searchid"],
                "userid":userDetails["id"], "gameid":gameDetails["id"], "gamename":gameDetails["name"],
                "username":userDetails["username"], "displayname":userDetails["display name"], "headshot":url
                })

            else:
                return jsonify({
                "user":user, "game":game, "banned": userDetails["banned"], "online":online,"ingame":False, "servercount":results["server amount"],
                "userid":userDetails["id"], "gameid":gameDetails["id"],
                "gamename":gameDetails["name"],
                "username":userDetails["username"], "displayname":userDetails["display name"], "headshot":url
                })

        else:
            headshot = data["headshot"]
            link = headshot.replace("USERID", str(userDetails["id"]))
            url = requests.get(link).json()["Url"]
            return jsonify({
            "user":user, "game":game, "banned": userDetails["banned"], "online":online, "ingame":False,
            "userid":userDetails["id"], "gameid":gameDetails["id"],
            "gamename":gameDetails["name"],
            "username":userDetails["username"], "displayname":userDetails["display name"],
            "headshot":url
            })

    else:
        return jsonify({"user":user, "game":game})

serve(app, host='0.0.0.0', port=8080)
