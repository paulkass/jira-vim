
import re
import requests

from jira import JIRA
from .board import Board
from .kanbanBoard import KanbanBoard
from .scrumBoard import ScrumBoard
from .issue import Issue

class Connection:
    def __init__(self, name, email, token):
        self.__constructUrl(name)
        self.__email = email
        self.__token = token
        self.__jira = JIRA(options={"server": self.__baseUrl}, basic_auth=(self.__email, self.__token))
        self.__buildBoardHash()

    def __constructUrl(self, site):
        """
        Constructs a base url from user input.

        This function is designed to take the user input and self-assign the __baseUrl variable with the base URL for any further requests. It supports naming the jira instance (so if you have a jira instance of antarctica.atlassian.net, you could input "atlassian") as well as full websites.

        Parameters
        ----------
        site : String
            A string that represents the connection host. It could either be a name (as explained above, "antarctica" is a valid site input for "antartica.atlassian.net") or a full website.

        Returns
        -------
        Nothing

        """

        # Pattern experiments at: https://pythex.org/?regex=%5CA(http(s)%3F%3A%2F%2F)%3F%5B%5Cw%5C%24%5C-%5C_%5C.%5C%2B%5C!%5C*%5C%27%5C(%5C)%5C%2C%5D%2B%5C.%5Cw%7B2%2C3%7D%5CZ&test_string=https%3A%2F%2Fhello.com&ignorecase=0&multiline=0&dotall=0&verbose=0
        # We could use urllib if the need arises
        website_pattern = "\A(http(s)?://)?[\w\$\-\_\.\+\!\*\'\(\)\,]+\.\w{2,3}\Z"
        if re.search(website_pattern, site):
            self.__baseUrl = site
        else:
            self.__baseUrl = "https://"+site+".atlassian.net"

    def __buildBoardHash(self):
        """
        Builds a board configuration lookup table.

        Builds a board hash that matches the name of the board to the configuration for that board.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        board_hash = {}
        reqStr = "/rest/agile/1.0/board"
        boardList = self.customRequest(reqStr).json()
        for v in boardList["values"]:
            # The board name in v comes as "<boardName> board"
            matches = re.match(r"\A([\s\w]+)\s[Bb]oard\Z", v["name"])
            if matches is None:
                bName = v["name"]
            else:
                bName = matches.group(1)
            board_hash[bName] = v
        self.__board_conf_hash = board_hash

    def getBaseUrl(self):
        """
        Getter for the base url
        """
        return self.__baseUrl

    def getJiraObject(self):
        """
        Getter for the jira object used to access information about issues.
        """
        return self.__jira

    def getBoard(self, board_name):
        """
        Returns a new board object.

        Looks up the board_name configuration and produces a board object of the correct subclass (KanbanBoard, ScrumBoard).

        Parameters
        ----------
        board_name : String
            Name of the board to create an object for.

        Returns
        -------
        Board
            Board object that corresponds to the board_name

        """

        if board_name in self.__board_conf_hash:
            boardType = self.__board_conf_hash[board_name]["type"]
            boardId = str(self.__board_conf_hash[board_name]["id"])
            if boardType == "kanban":
                return KanbanBoard(boardId, board_name, self)
            if boardType == "scrum":
                return ScrumBoard(boardId, board_name, self)
            return Board(boardId, board_name, self)
        return None

    def getIssue(self, issue_key):
        """
        Create a new Issue object

        Creates a new issue object from issue_key

        Parameters
        ----------
        issue_key : String
            Issue key for that the issue

        Returns
        -------
        Issue
            Issue object

        """

        return Issue(issue_key, self)

    def customRequest(self, request):
        """
        Make custom request through the connection to jira.

        This function is useful when the provided jira object cannot easily return the data you need. Then you can specify a custom request that will be sent to the appropriate jira domain, and the resutls returned to you.

        Parameters
        ----------
        request : String
            Path of the request to make

        Returns
        -------
        Response
            This is a requests.Response object that contains the response from Jira.

        """

        reqStr = self.__baseUrl + request
        return requests.get(reqStr, auth=(self.__email, self.__token))
