from .board import Board
from .sprint import Sprint

class ScrumBoard(Board):
    def __init__(self, boardId, boardName, connection):
        Board.__init__(self, boardId, boardName, connection)

        sprintConf = self.connection.customRequest(self.baseUrl+"/sprint").json()

        self.__sprintsById = {}
        self.__sprintsByName = {}

        for sprintObj in sprintConf["values"]:
            sprint = Sprint(sprintId=sprintObj["id"],
                            url=sprintObj["self"],
                            name=sprintObj["name"],
                            board=self,
                            connection=connection,
                            state=sprintObj["state"],
                            startDate=sprintObj["startDate"],
                            endDate=sprintObj["endDate"])
            self.__sprintsById[int(sprintObj["id"])] = sprint
            self.__sprintsByName[sprintObj["name"]] = sprint

    def getSprints(self, startAt=0, maxResults=50):
        # No pagination support for Sprints yet
        return [["Sprints", False, [(name, " ") for name in self.__sprintsByName]]]

    def getSprint(self, key):
        if key in self.__sprintsById:
            return self.__sprintsById[key]
        return self.__sprintsByName[key]
