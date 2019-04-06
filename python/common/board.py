import json

class Board:
    def __init__(self, boardId, connection):
        self.__connection = connection
        self.boardId = boardId
        self.__baseUrl = "/rest/agile/1.0/board/"+boardId

    def getIssues(self):
        columns = self.__connection.customRequest(self.__baseUrl+"/configuration").json()["columnConfig"]["columns"]
        #print(columns)
        r = self.__connection.customRequest(self.__baseUrl+"/issue?fields=key,status").json()
        #print(json.dumps(r, sort_keys=True, indent=4))
        return [i["key"] for i in r["issues"]]

