import json
import requests

def convertID(uid):
    with open("config.json") as file:
        data = json.load(file)

    checkLink = data["userinfo"]
    convertLink = data["usernametoid"]

    valid = requests.get(checkLink.replace("REPLACE", str(uid)))
    responseCode = valid.status_code

    if responseCode == 404:
        alreadyValid = False
        
    elif responseCode == 200:
        alreadyValid = True
    
    else:
        print("Unexpected response code:", responseCode)
        alreadyValid = False

    if alreadyValid:
        return {"alreadyvalid":alreadyValid, "prevID":int(uid), "convertedID": None}
    
    else:
        convert = requests.get(convertLink.replace("REPLACE", uid)).json()
        if "errorMessage" in convert.keys():
            return {"alreadyvalid":alreadyValid, "conversion":False, "prevID":uid, "convertedID":None}
        else:
            return {"alreadyvalid":alreadyValid, "conversion":True, "prevID":uid, "convertedID":convert["Id"]}
