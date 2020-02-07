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

        self.__searchesHash = {}

    @staticmethod
    def getConnectionFromVars():
        """
        Create connection from vars.

        Creates a connection from the global configuration variables and returns it

        Parameters
        ----------
        None

        Returns
        -------
        Connection
            The connection object created from the global variables.

        """

        domainName = SessionObject.decodeString(vim.vars["jiraVimDomainName"])
        email = SessionObject.decodeString(vim.vars["jiraVimEmail"])
        token = SessionObject.decodeString(vim.vars["jiraVimToken"])

        return Connection(domainName, email, token)

    def assignBoard(self, board, buff):
        """
        Assigns associations between a board and a buffer to the caches.

        Parameters
        ----------
        board : Board
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

    def assignSprint(self, sprint, buff):
        """
        Assigns a sprint to the session sprint cache. Note that it doesn't assign by sprint name.
        """
        self.__sprintsHash[buff.number] = sprint

    def assignSearch(self, search, buf):
        self.__bufferHash[search.query_id] = buf
        self.__searchesHash[buf.number] = search

    def assignIssue(self, issue, buff):
        self.__bufferHash[issue.issueId] = buff
        self.__namesToIds[issue.issueKey] = issue.issueId

    def getBufferByIndex(self, key):
        """
        Return buffer based on either item key or item name.

        Returns the buffer from the key or item name of the item you need the buffer for, and returns the buffer if the buffer is valid.

        Parameters
        ----------
        key : int or String
            Either the Id or the Name of the object

        Returns
        -------
        Buffer
            Buffer corresponding to the object

        """

        if key in self.__bufferHash:
            buff = self.__bufferHash[key]
            return buff if buff.valid else None
        if key in self.__namesToIds:
            buff = self.__bufferHash[self.__namesToIds[key]]
            return buff if buff.valid else None
        return None

    def getBoard(self, buf, boardName=None):
        """
        Retrieve board object based on buffer number

        This function takes in an identifier and tries to retrieve an object from the cache corresponding to the identifier (which can be a buffer id, a buffer, or a string of the board name). If it does not find a string object, it goes ahead and creates one by calling the getBoard method of the connection object. If it does not find a buffer number of buffer object in the cache, it creates one based on the jiraVimBoardName variable.

        This function only accounts for missing keys in the cache.

        Parameters
        ----------
        buf : Integer or Buffer
            Buffer object or integer representing the number of the buffer
        boardName : String
            Name of board to be created if board doesn't exist in cache

        Returns
        -------
        Board
            Board corresponding to the buffer that was queried

        """
        create_new_object = self.connection.getBoard

        if isinstance(buf, int):
            board = self.__boardsHash.get(buf, create_new_object(boardName))
            self.assignBoard(board, vim.buffers[buf])
            return board
        if buf in vim.buffers:
            board = self.__boardsHash.get(buf.number, create_new_object(boardName))
            self.assignBoard(board, buf)
            return board
        return None

    def getSprint(self, sprintIdentifier):
        """
        Similar to getBoard for boards: returns cached sprint if it could find it for this buffer or name.

        Note: doesn't work if you input
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

    def getSearch(self, buf_number):
        return self.__searchesHash[buf_number]

    def getBuff(self, objId=None, objName=None, createNew=True):
        """
        Creates a buffer if none exists for a given object ID or Name

        Tries to return a buffer based on the objId and objName fields, and if there is none, creates a new buffer for the object.

        Parameters
        ----------
        objId : Integer (Optional)
            Id of object.
        objName : String (Optional)
            Name of object
        createNew : Boolean (Optional)
            Determines whether to create a new buffer if the buffer for the object is not found in the hashes. Defaults to True

        Returns
        -------
        Tuple
            Returns a tuple that contains the Buffer, and a boolean. The boolean is True is this a newly created buffer, created by this method.

        """

        if objId is not None:
            buff = self.getBufferByIndex(objId)
            if buff is not None:
                return (buff, False)
        if objName is not None:
            buff = self.getBufferByIndex(objName)
            if buff is not None:
                return (buff, False)
        # return new buffer
        if createNew:
            return (self.__createBuffer(), True)
        return (None, False)

    def __createBuffer(self):
        # Creates a new buffer, saves it, and then uses the hidden command to hide it
        vim.command("new")
        buf = vim.current.buffer
        vim.command("hide")
        return buf

    @staticmethod
    def decodeString(candidate): 
        # Decodes the string in utf-8 only if in vim, neovim puts it in the default locale automatically
        if isinstance(candidate, str):
            return candidate
        else:
            return candidate.decode("utf-8")

