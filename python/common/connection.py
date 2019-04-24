
from jira import JIRA
from .board import Board
from .kanbanBoard import KanbanBoard
from .issue import Issue
import requests
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
        reqStr = "/rest/agile/1.0/board"
        boardList = self.customRequest(reqStr).json()
        for v in boardList["values"]:
            bName = re.match(r"\A([\s\w]+)\sboard\Z", v["name"]).group(1)
            boardHash[bName] = v
        self.__boardHash = boardHash

    def getBaseUrl(self):
        return self.__baseUrl

    def getJiraObject(self):
        return self.__jira

    def getBoard(self, boardName):
        if boardName in self.__boardHash:
            boardType = self.__boardHash[boardName]["type"]
            boardId = str(self.__boardHash[boardName]["id"])
            if boardType == "type":
                return Board(boardId, boardName, self)
            else:
                return KanbanBoard(boardId, boardName, self)
        else:
            return None

    def getIssue(self, issueKey):
        return Issue(issueKey, self)

    def customRequest(self, request):
        reqStr = self.__baseUrl + request
        return requests.get(reqStr, auth=(self.__email, self.__token))
