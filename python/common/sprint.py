from ..util.itemCategorizer import ItemCategorizer
from ..util.itemExtractor import ItemExtractor

class Sprint():
    def __init__(self, sprintId, url, board, connection, state=None, name=None, startDate=None, endDate=None):
        self.sprintId = sprintId
        self.__url = url
        self.board = board
        self.name = name
        self.__state = state
        self.__startDate = startDate
        self.__endDate = endDate
        self.baseUrl = "/rest/agile/1.0/board/"+str(board.id)+"/sprint/"+str(sprintId)
        self.connection = connection
        self.requiredProperties = ["key", "status", "summary"]
        self.__columnToIssues = {}

        self.issueExtractor = ItemExtractor(self.connection, self.baseUrl+"/issue?fields=%s", lambda: (','.join(self.requiredProperties),))

    def getIssues(self, column=None):
        r = self.issueExtractor.__next__()

        return ItemCategorizer.issueCategorizer(r["issues"], self.board.statusToColumn, self.__columnToIssues)
