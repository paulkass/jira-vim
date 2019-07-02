from .board import Board
from ..util.itemCategorizer import ItemCategorizer
from ..util.itemExtractor import ObjectItemExtractor

class KanbanBoard(Board):
    def __init__(self, boardId, boardName, connection):
        Board.__init__(self, boardId, boardName, connection)
        self.columnExtractors = {}

        for col in self.columns:
            self.columnExtractors[col] = ObjectItemExtractor.create_column_issue_extractor(self, col)

    def getIssues(self, column=None):
        """
        Get a batch of issues from board.

        Get a batch of issues from the board, either sorted by column. Returns at most 10 from the column specified. Otherwise, collects issues from all columns in batches and returns them, categorized.

        Parameters
        ----------
        column : String (Optional)
            Column from which to retrieve issues.

        Returns
        -------
        List
            Categorized list of (<column_name>, <more left>, [issue keys]) tuples according to the issue categorizer from ItemCategorizer.

        """

        if column:
            columns = [column]
        else:
            columns = self.columns
        returnIssues = []
        for c in columns:
            r = self.columnExtractors[c].__next__()
            returnIssues += ItemCategorizer.issueCategorizer(r, self.statusToColumn, self.columnExtractors)
        # Sort issues by Category
        return returnIssues
