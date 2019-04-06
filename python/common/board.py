import json

class Board:
    def __init__(self, boardId, connection):
        self.connection = connection
        self.boardId = boardId
        self.baseUrl = "/rest/agile/1.0/board/"+boardId

    def getIssues(self, startAt=0, maxResults=50):
        r = self.connection.customRequest(self.baseUrl+"/issue?fields=key,status&startAt=%d&maxResults=%d" % (startAt, maxResults)).json()
        return [("All Issues", [i["key"] for i in r["issues"]])]

