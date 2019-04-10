import json

class Board:
    def __init__(self, boardId, boardName, connection):
        self.connection = connection
        self.boardId = boardId
        self.boardName = boardName
        self.baseUrl = "/rest/agile/1.0/board/"+boardId
        self.requiredProperties = ["key", "status", "summary"] 

    def getIssues(self, startAt=0, maxResults=50):
        r = self.connection.customRequest(self.baseUrl+"/issue?fields=%s&startAt=%d&maxResults=%d" % (','.join(self.requiredProperties), startAt, maxResults)).json()
        return [("All Issues", [i["key"] for i in r["issues"]])]

