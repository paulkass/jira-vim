
class Board:
    def __init__(self, boardId, connection):
        self.__connection = connection
        self.__boardId = boardId
        self.__baseUrl = "/rest/agile/1.0/board/"+boardId

    def getIssues(self):
        r = self.__connection.customRequest(self.__baseUrl+"/issue?fields=key").json()
        return [i["key"] for i in r["issues"]]
        
