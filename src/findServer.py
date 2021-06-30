import requests
import json
import threading
import os

def findServer(user, game):

    def getInfo(gameid):
        global firstQuery
        with open("config.json") as file:
            data = json.load(file)
        cookies = {"cookie":data["cookie"]}
        baseLink = data["game"]
        link = baseLink.replace("REPLACE", str(gameid), 1).replace("REPLACE", str(0))
        firstQuery = requests.get(link, cookies=cookies)
        firstQuery = firstQuery.json()["TotalCollectionSize"]

        indexList = []
        for i in range(100):
            tempList = []
            counter = 0
            while (i*10) + (1000 * counter) < firstQuery:
                tempList.append((i*10) + (1000 * counter))
                counter += 1
            indexList.append(tempList)
        return indexList



    def downloadServer(gameid, listOfIndex, searchNum):
        with open("config.json") as file:
            data = json.load(file)
        cookies = {"cookie":data["cookie"]}
        baseLink = data["game"]
        if len(listOfIndex) == 0:
            return
        for i in listOfIndex:
            newLink = baseLink.replace("REPLACE", str(gameid), 1).replace("REPLACE", str(i))
            query = requests.get(newLink, cookies=cookies).json()
            if len(query["Collection"]) == 0:
                break

            if str(searchNum) in os.listdir("download/"):
                pass
            else:
                os.mkdir("download/"+str(searchNum))
            with open("download/"+str(searchNum)+"/"+newLink.split("=")[-1]+".json", "w") as file:
                json.dump(query, file)


    def runDownload(gameid, listOfIndexes):
        threads  = []
        for i in listOfIndexes:
            processThread = threading.Thread(target=downloadServer, args=(gameid, i, currSearch))
            threads.append(processThread)
        return threads



    def searchForInfo(headshot, listOfFilenames, searchNum):
        global found
        if len(listOfFilenames) == 0:
            return

        for i in listOfFilenames:

            if found:
                break
            try:
                with open("download/"+str(searchNum)+"/"+str(i)+".json", "r") as file:
                    if headshot in file.read():
                        found = True
                        with open("download/"+str(searchNum)+"/"+str(i)+".json", "r") as file1:
                            data = json.load(file1)
                        stop = False
                        for k in data["Collection"]:
                            if stop:
                                break
                            guid = k["Guid"]
                            ping = k["Ping"]
                            currPlayers = k["PlayersCapacity"].split()[0]
                            maxCapacity = k["Capacity"]
                            for j in k["CurrentPlayers"]:
                                if headshot in j["Thumbnail"]["Url"]:
                                    stop = True
                                    serverAmount = str(data["TotalCollectionSize"])
                                    break
                        dict = {"In Game": True, "guid":guid, "server amount":serverAmount, "ping":ping, "players":currPlayers, "max players":maxCapacity, "searchid":int(searchNum)}
                        with open("result/results"+str(searchNum)+".json", "w") as file:
                            json.dump(dict, file)

                    else:
                        continue

            except:
                break



    def runSearch(headshot, listOfIndexes):
        threads = []
        for i in listOfIndexes:
            processThread = threading.Thread(target=searchForInfo, args=(headshot, i, currSearch))
            threads.append(processThread)
        return threads

    def clearJunk(directory):
        for i in os.listdir(directory):
            os.remove(directory+"/"+i)
        os.rmdir(directory)

    def createDirectory():
        result = False
        download = False
        for i in os.listdir():
            if i == "result":
                result = True
            elif i == "download":
                download = True
        
        if not(result):
            os.mkdir("result")
        if not(download):
            os.mkdir("download")

    createDirectory()

    with open("config.json", "r") as file:
        data = json.load(file)

    headshot = data["headshot"]

    with open("search.json", "r") as file:
        searchdata = json.load(file)

    global currSearch
    currSearch = searchdata["searchnum"]


    searchdata["searchnum"] += 1

    with open("search.json", "w") as file:
        json.dump(searchdata, file)

    gameid = game
    userid = user
    lists = getInfo(gameid)

    downloadThreads = runDownload(gameid, lists)

    headshotRequest = requests.get(headshot.replace("USERID", str(userid)))
    if headshotRequest.status_code == 400:
        return "error"
    elif headshotRequest.json()["Url"] == "https://t4.rbxcdn.com/b561617d22628c1d01dd10f02e80c384":
        return "error"
    headshotid = headshotRequest.json()["Url"].split("/")[3]


    searchThreads = runSearch(headshotid, lists)

    global found
    found = False

    for i in downloadThreads:
        i.start()

    for i in downloadThreads:
        i.join()

    for i in searchThreads:
        i.start()

    for i in searchThreads:
        i.join()

    print(found)
    if not(found):
        dict = {"In Game": False, "server amount":firstQuery, "searchid":int(currSearch)}
        with open("result/results"+str(currSearch)+".json", "w") as file:
            json.dump(dict, file)

    clearJunk("download/"+str(currSearch))
    return currSearch, headshotRequest.json()["Url"]
