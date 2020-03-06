
from ..util.itemExtractor import ObjectItemExtractor

class Board:
    def __init__(self, boardId, boardName, connection):
        self.connection = connection
        self.id = boardId
        self.boardName = boardName
        self.baseUrl = "/rest/agile/1.0/board/"+boardId
        self.requiredProperties = ["key", "status", "summary"]

        self.boardConf = self.connection.customRequest(self.baseUrl+"/configuration").json()
        self.statusToColumn = {}
        self.columns = list()

        """
        The idea here is that each column can display many statuses. So the relationship from status to column is many to one. Then each instance sorts issues into columns on its own.
        """
        col_set = set()
        for col in self.boardConf["columnConfig"]["columns"]:
            cName = col["name"]
            if cName not in col_set:
                self.columns.append(cName)
                col_set.add(cName)
            for s in col["statuses"]:
                self.statusToColumn[s["id"]] = cName

        def all_issues_provider(startAt, maxResults):
            vals = (','.join(self.requiredProperties), startAt, maxResults)
            response = self.connection.customRequest(self.baseUrl+"/issue?fields=%s&startAt=%d&maxResults=%d" % vals).json()
            return response["issues"]

        self.issueExtractor = ObjectItemExtractor(all_issues_provider)

    def getIssues(self):
        """
        Creates an category for all issues.

        Uses the built in issueExtractor object to extract all issues into a single "All Issues" category and return them.

        Parameters
        ----------
        None

        Returns
        -------
        List
            A list with a single tuple of the format ("All Issues", <whether all issues extractor is finished>, [list of (issue key, issue summary) tuples]).

        """

        r = self.issueExtractor.__next__()
        return [("All Issues", self.issueExtractor.finished, [(i["key"], "") for i in r])]
