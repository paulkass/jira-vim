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

    def getSprints(self):
        """
        Returns list of sprints for this board.

        Returns the list of the Sprints in the standard format for extraction (see DrawUtil).

        Parameters
        ----------
        None

        Returns
        -------
        List
            Returns a list in the format of ["Sprints, False, [(<name of sprint>, "")]]

        """

        # No pagination support for Sprints yet
        return [["Sprints", False, [(name, " ") for name in self.__sprintsByName]]]

    def getSprint(self, key):
        """
        Returns sprint object by either id or name.

        Parameters
        ----------
        key : Integer or String
            The key that is used to get the sprint, either an integer representing the id or a string representing the name

        Returns
        -------
        Sprint
            the sprint corresponding to the key

        """

        if key in self.__sprintsById:
            return self.__sprintsById[key]
        return self.__sprintsByName[key]
