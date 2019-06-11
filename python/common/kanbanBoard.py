from .board import Board
from ..util.itemCategorizer import ItemCategorizer
from ..util.itemExtractor import ItemExtractor

class KanbanBoard(Board):
    def __init__(self, boardId, boardName, connection):
        Board.__init__(self, boardId, boardName, connection)
        self.columnExtractors = {}

        self.issueExtractor = ItemExtractor(self.connection, self.baseUrl+"/issue?fields=%s", lambda: (','.join(self.requiredProperties),))

        for col in self.columns:
            self.columnExtractors[col] = ItemExtractor.create_column_issue_extractor(self, col)


    def getIssues(self, column=None):
        if column and column in self.columnExtractors:
            r = self.columnExtractors[column].__next__()
        else:
            r = self.issueExtractor.__next__()
        # Sort issues by Category
        return ItemCategorizer.issueCategorizer(r["issues"], self.statusToColumn), bool(column and not self.columnExtractors[column].finished)
