from .board import Board
from ..util.itemCategorizer import ItemCategorizer

class KanbanBoard(Board):
    def __init__(self, boardId, boardName, connection):
        Board.__init__(self, boardId, boardName, connection)
        self.__columnToIssues = {}

    def getIssues(self, startAt=0, maxResults=50):
        r = self.connection.customRequest(self.baseUrl+"/issue?fields=%s&startAt=%d&maxResults=%d" % (','.join(self.requiredProperties), \
               startAt, maxResults)).json()
        # Sort issues by Category
        return ItemCategorizer.issueCategorizer(r["issues"], self.statusToColumn, self.__columnToIssues)
