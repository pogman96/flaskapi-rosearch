import json
import requests

def deepConvertID(uid):
    if not(str(uid).isnumeric()):
        return {"error":"previous id must be numeric"}

    with open("config.json") as file:
        data = json.load(file)

    convertLink = data["usernametoid"]

    deepLink = convertLink.replace("REPLACE", str(uid))
    request = requests.get(deepLink).json()

    checkLink = data["userinfo"]
    secondCheck = requests.get(checkLink.replace("REPLACE", str(uid))).json()
    if "errorMessage" in request.keys():
        if "errors" in secondCheck.keys():
            alreadyValid = False
            return {"alreadyvalid":alreadyValid, "conversion":False, "prevID":int(uid), "convertedID": None}
        alreadyValid = True
        return {"alreadyvalid":alreadyValid, "conversion":False, "prevID":int(uid), "convertedID": None}
    else:
        if "errors" in secondCheck.keys():
            alreadyValid = False
            return {"alreadyvalid":alreadyValid, "conversion":True, "prevID":int(uid), "convertedID":request["Id"]}
        else:
            alreadyValid = True
            return {"alreadyvalid":alreadyValid, "conversion":True, "prevID":int(uid), "convertedID":request["Id"]}
