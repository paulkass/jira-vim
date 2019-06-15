import vim
from .connection import Connection

class SessionObject():
    def __init__(self):
        self.connection = SessionObject.getConnectionFromVars()

        # When retrieving buffers, we need to make sure that the buffer is valid.
        # If the buffer is cleared or wiped, it will be marked invalid and we can't retrieve it again.
        self.__bufferHash = {}
        self.__namesToIds = {}

        # Also cache board objects: this one maps buffer numbers to Board and Sprint objects
        self.__boardsHash = {}

        self.__sprintsHash = {}

    @staticmethod
    def getConnectionFromVars():
        domainName = vim.vars["jiraVimDomainName"].decode("utf-8")
        email = vim.vars["jiraVimEmail"].decode("utf-8")
        token = vim.vars["jiraVimToken"].decode("utf-8")

        return Connection(domainName, email, token)

    def assignBoard(self, board, buff):
        """
        Assigns associations between a board and a buffer to the caches.

        Parameters
        ----------
        board : Board or Sprint
            Object to be associated with the buffer
        buff : Vim Buffer
            A vim buffer object to be associated with board

        Returns
        -------
        Nothing

        """

        self.__bufferHash[board.id] = buff
        self.__namesToIds[board.boardName] = board.id
        self.__boardsHash[buff.number] = board
        self.__boardsHash[board.boardName] = board

    def assignSprint(self, sprint, buff):
        """
        Assigns a sprint to the session sprint cache. Note that it doesn't assign by sprint name.
        """
        self.__sprintsHash[buff.number] = sprint
        self.__sprintsHash[buff] = sprint

    def assignIssue(self, issue, buff):
        self.__bufferHash[issue.id] = buff
        self.__namesToIds[issue.issueKey] = issue.id

    def getBufferByIndex(self, key):
        if key in self.__bufferHash:
            buff = self.__bufferHash[key]
            return buff if buff.valid else None
        elif key in self.__namesToIds:
            buff = self.__bufferHash[self.__namesToIds[key]]
            return buff if buff.valid else None
        else:
            return None

    def getBoard(self, boardIdentifier):
        """
        Retrieve board object based on buffer number

        This function takes in an identifier and tries to retrieve an object from the cache corresponding to the identifier (which can be a buffer id, a buffer, or a string of the board name). If it does not find a string object, it goes ahead and creates one by calling the getBoard method of the connection object. If it does not find a buffer number of buffer object in the cache, it creates one based on the jiraVimBoardName variable. 

        This function only accounts for missing keys in the cache.

        Parameters
        ----------
        buf : Integer or Buffer or String
            Buffer object or integer representing the number of the buffer

        Returns
        -------
        Board
            Board corresponding to the buffer that was queried

        """
        create_new_object = self.connection.getBoard

        if isinstance(boardIdentifier, int):
            board = self.__boardsHash.get(boardIdentifier, create_new_object(vim.buffers[boardIdentifier].vars["jiraVimBoardName"]))
            self.assignBoard(board, vim.buffer[boardIdentifier])
            return board
        if isinstance(boardIdentifier, str):
            board = self.__boardsHash.get(boardIdentifier, create_new_object(boardIdentifier))
            return board
        if boardIdentifier in vim.buffers:
            board = self.__boardsHash.get(boardIdentifier.number, create_new_object(boardIdentifier.vars["jiraVimBoardName"]))
            self.assignBoard(board, boardIdentifier)
            return board
        return None

    def getSprint(self, sprintIdentifier):
        """
        Similar to getBoard for boards: returns cached sprint if it could find it for this buffer or name
        """
        if sprintIdentifier in vim.buffers:
            sprint = self.__sprintsHash.get(sprintIdentifier.number, None)
            if sprint:
                self.assignSprint(sprint, sprintIdentifier)
            return sprint
        sprint = self.__sprintsHash.get(sprintIdentifier, None)
        if sprint and isinstance(sprintIdentifier, int):
            self.assignSprint(sprint, vim.buffers[sprintIdentifier])
        return sprint

    # Returns the buffer, and a boolean that says whether the buffer is newly created or existing one
    def getBuff(self, objId=None, objName=None, createNew=True, isSplit=False):
        if objId is not None:
            buff = self.getBufferByIndex(objId)
            if buff is not None:
                return ( buff, False )
        if objName is not None:
            buff = self.getBufferByIndex(objName)
            if buff is not None:
                return (buff, False)
        # return new buffer
        if createNew:
            return (self.__createBuffer(), True)
        else:
            return (None, False)

    def __createBuffer(self):
        # Creates a new buffer, saves it, and then uses the hidden command to hide it
        vim.command("new")
        buf = vim.current.buffer
        vim.command("hide")
        return buf

