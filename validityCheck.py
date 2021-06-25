import requests
import json

def checkGame(gameid):
    with open("config.json") as file:
        data = json.load(file)

    if not(str(gameid).isnumeric()):
        gameValid = False

    else:
        link = data["gametouniverse"]
        request = requests.get(link.replace("REPLACE", str(gameid)))
        if request.status_code == 404:
            gameValid = False
        elif request.status_code == 200:
            gameValid = True
        else:
            gameValid = False
            print("unexpected response code", request.status_code)
    if gameValid:
        return {"valid":gameValid, "id":int(gameid)}
    else:
        return {"valid":gameValid}

def checkUser(userid):
    with open("config.json") as file:
        data = json.load(file)

    userValid = False

    primaryCheck = data["userinfo"]
    secondaryCheck = data["usernametoid"]
    link1 = requests.get(primaryCheck.replace("REPLACE", str(userid)))
    if link1.status_code == 404:
        link2 = requests.get(secondaryCheck.replace("REPLACE", str(userid)))
        if "success" in link2.json().keys():
            userValid = False

        else:
            userid = link2.json()["Id"]
            userValid = True

    else:
        userValid = True

    if userValid:
        return {"valid":userValid, "id":int(userid)}
    else:
        return {"valid":userValid}

def checkValidity(userid, gameid):
    game = checkGame(gameid)
    user = checkUser(userid)
    return {"game":game, "user":user}

#print(checkValidity("bigswig996", "1818"))
