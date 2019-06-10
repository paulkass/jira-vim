
from ..util.itemExtractor import ItemExtractor

class Board:
    def __init__(self, boardId, boardName, connection):
        self.connection = connection
        self.id = boardId
        self.boardName = boardName
        self.baseUrl = "/rest/agile/1.0/board/"+boardId
        self.requiredProperties = ["key", "status", "summary"]

        self.boardConf = self.connection.customRequest(self.baseUrl+"/configuration").json()
        self.statusToColumn = {}
        """
        The idea here is that each column can display many statuses. So the relationship from status to column is many to one. Then each instance sorts issues into columns on its own.
        """
        for col in self.boardConf["columnConfig"]["columns"]:
            cName = col["name"]
            for s in col["statuses"]:
                self.statusToColumn[s["id"]] = cName

        self.issueExtractor = ItemExtractor(self.connection, self.baseUrl+"/issue?fields=%s", lambda: (','.join(self.requiredProperties),))

    def getIssues(self, column=None):
        r = self.issueExtractor.__next__()
        return [("All Issues", [(i["key"], "") for i in r["issues"]])]
