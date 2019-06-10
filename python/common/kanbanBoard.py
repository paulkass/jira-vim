from .board import Board
from ..util.itemCategorizer import ItemCategorizer
from ..util.itemExtractor import ItemExtractor

class KanbanBoard(Board):
    def __init__(self, boardId, boardName, connection):
        Board.__init__(self, boardId, boardName, connection)
        self.__columnToIssues = {}
        self.issueExtractor = ItemExtractor(self.connection, self.baseUrl+"/issue?fields=%s", lambda: (','.join(self.requiredProperties),))

    def getIssues(self, column=None):
        r = self.issueExtractor.__next__()
        # Sort issues by Category
        return ItemCategorizer.issueCategorizer(r["issues"], self.statusToColumn, self.__columnToIssues)
