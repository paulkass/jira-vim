import vim
from .board import Board
from .sprint import Sprint
from .connection import Connection

class SessionObject():
    def __init__(self):
        self.connection = SessionObject.getConnectionFromVars()

        # When retrieving buffers, we need to make sure that the buffer is valid.
        # If the buffer is cleared or wiped, it will be marked invalid and we can't retrieve it again.
        self.__obj_id_to_buffers = {}
        self.__obj_aliases = {}
        self.__buf_num_to_objects = {}
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

        domainName = vim.vars["jiraVimDomainName"].decode("utf-8")
        email = vim.vars["jiraVimEmail"].decode("utf-8")
        token = vim.vars["jiraVimToken"].decode("utf-8")

        return Connection(domainName, email, token)


    def assignObject(self, obj, buff, *aliases):
        """
        Stores an association from an object to a buffer and vice versa.
        
        Stores an association between an object to a buffer. This will allow retrieval of a buffer associated with an object and an object associated with a buffer (or buffer number). It will also allow aliases to exist, that would map certain objects to an object id, and those would be mappend to buffers and vice versa.
        
        Parameters
        ----------
        obj : Object
            This is the object to be associated with the buffer.
        buff : vim.Buffer
            This is the buffer to be associated with the object.
        aliases : Array
            This is the array of objects (generally Strings) that will contain aliases for the object. Contains 0 or more elements.

        Returns
        -------
        Nothing
        """

        aliases = list(aliases)

        if isinstance(obj, Board):
            aliases.append(obj.boardName)
        if isinstance(obj, Sprint):
            aliases.append(obj.sprintName)
        self.__obj_id_to_buffers[id(obj)] = buff 
        for a in aliases:
            self.__obj_aliases[a] = obj
        self.__buf_num_to_objects[buff.number] = obj

    def getObject(self, buff, create_object=None):
        """
        Retrieves an object based on buffer.

        Tries to retrieve an object from the buffer number. If the object is not found, it tries to create one and assign it to the buffer.
        
        Parameters
        ----------
        buff : Object
            The buffer or buffer number of the buffer associated with the object.
        create_object : Function (Optional)
            This function is called if the object is not found in the hashes. If the function is None, the function returns none. Otherwise, if the object is not found in the hashes it assigns and returns the result of calling of this function (no arguments). Defaults to None.

        Returns
        -------
        Object
            Returns the object associated with the buffer or returns None if it doesn't exist.
        """
        if not create_object:
            # Set it to be a dud function that returns None
            create_object = lambda: None

        if isinstance(buff, int):
            obj = self.__buf_num_to_objects.get(buff, create_object())
            if obj:
                self.assignObject(obj, vim.buffers[buff])
            return obj 
        if buff in vim.buffers:
            obj = self.__buf_num_to_objects.get(buff.number, create_object())
            if obj:
                self.assignObject(obj, buff)
            return obj 
        return None

    def assignSprint(self, sprint, buff):
        """
        Assigns a sprint to the session sprint cache. Note that it doesn't assign by sprint name.
        """
        self.__sprintsHash[buff.number] = sprint

    def assignSearch(self, search, buf):
        self.__obj_id_to_buffers[search.query_id] = buf
        self.__searchesHash[buf.number] = search

    def assignIssue(self, issue, buff):
        self.__obj_id_to_buffers[issue.issueId] = buff
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

        if key in self.__obj_id_to_buffers:
            buff = self.__obj_id_to_buffers[key]
            return buff if buff.valid else None
        if key in self.__namesToIds:
            buff = self.__obj_id_to_buffers[self.__namesToIds[key]]
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

