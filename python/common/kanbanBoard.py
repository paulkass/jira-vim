from .board import Board
from ..util.itemCategorizer import ItemCategorizer

class KanbanBoard(Board, ItemCategorizer):
    def __init__(self, id, boardName, connection):
        Board.__init__(self, id, boardName, connection)
        self.__columnToIssues = {}

    def getIssues(self, startAt=0, maxResults=50):
        r = self.connection.customRequest(self.baseUrl+"/issue?fields=%s&startAt=%d&maxResults=%d" % (','.join(self.requiredProperties), \
               startAt, maxResults)).json()
        # Sort issues by Category
        return self.issueCategorizer(r["issues"], self.statusToColumn, self.__columnToIssues)
