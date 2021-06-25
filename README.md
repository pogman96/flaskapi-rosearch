# flaskapi-rosearch
 Roblox game server finder made as a Python Flask API optimized using multithreading

## Requirements
###Cookie - A Roblox cookie is required to make requests to a Roblox API
 Libraries
 - threading
 - os
 - flask
 - waitress
 - requests

## Usage
 ```python3 main.py```
 Navigate to localhost port 8080
 API Queries
 - Checking user/game id validity
  ```/api/v1/checkValid/<userID>/<gameID>```
  - Converting username to userid
  ```/api/v1/checkUser/<username>```
  - Doubly converting username to userid (Used in instances where the username is entirely numeric)
  ```/api/v1/checkUserDeep/<username>```
  - GUID searcher
  ```/api/v1/findUser/<userID>/<gameID>```
