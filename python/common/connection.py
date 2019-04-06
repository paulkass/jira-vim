
from jira import JIRA
from .board import Board
import requests
import json
import re

class Connection:
    def __init__(self, name, email, token):
        self.__constructUrl(name)
        self.__email = email
        self.__token = token
        self.__jira = JIRA(options={"server": self.__baseUrl}, basic_auth=(self.__email, self.__token))
        self.__buildBoardHash()

    def __constructUrl(self, name):
        self.__baseUrl = "http://"+name+".atlassian.net"

    def __buildBoardHash(self):
        boardHash = {}
        reqStr = self.__baseUrl+"/rest/agile/1.0/board"
        boardList = requests.get(reqStr, auth=(self.__email, self.__token)).json()
        for v in boardList["values"]:
            bName = re.match(r"\A(\w+)\sboard\Z", v["name"]).group(1)
            boardHash[bName] = v
        self.__boardHash = boardHash

    def getBaseUrl(self):
        return self.__baseUrl

    def getBoard(self, boardName):
        if boardName in self.__boardHash:
            return Board(str(self.__boardHash[boardName]["id"]), self)
        else:
            return None

    def customRequest(self, request):
        reqStr = self.__baseUrl + request
        return requests.get(reqStr, auth=(self.__email, self.__token))


