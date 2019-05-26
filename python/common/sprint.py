from ..util.itemCategorizer import ItemCategorizer

class Sprint(ItemCategorizer):
    def __init__(self, id, url, board, connection, state=None, name=None, startDate=None, endDate=None):
        self.id = id
        self.__url = url
        self.board = board
        self.name = name
        self.__state = state
        self.__startDate = startDate
        self.__endDate = endDate
        self.baseUrl = "/rest/agile/1.0/board/"+str(board.id)+"/sprint/"+str(id)
        self.connection = connection
        self.requiredProperties = ["key", "status", "summary"]
        self.__columnToIssues = {}

    def getIssues(self, startAt=0, maxResults=50):
        r = self.connection.customRequest(self.baseUrl+"/issue?fields=%s&startAt=%d&maxResults=%d" % (','.join(self.requiredProperties), startAt, maxResults)).json()

        return self.issueCategorizer(r["issues"], self.board.statusToColumn, self.__columnToIssues)
