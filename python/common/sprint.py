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

        self.columnExtractors = {}
        for col in self.board.columns:
            self.columnExtractors[col] = ItemExtractor.create_column_issue_extractor(self.board, col)


    def getIssues(self, column=None):
        if column:
            columns = [column]
        else:
            columns = self.board.columns
        returnIssues = []
        for c in columns:
            r = self.columnExtractors[c].__next__()
            returnIssues += ItemCategorizer.issueCategorizer(r["issues"], self.board.statusToColumn, self.columnExtractors)
        return returnIssues
