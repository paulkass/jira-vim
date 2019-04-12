
from .connection import Connection
import vim

class SessionObject():
    def __init__(self):
        self.connection = self.getConnectionFromVars()

        # When retrieving buffers, we need to make sure that the buffer is valid. If the buffer is cleared or wiped, it will be marked invalid and we can't retriev it again.
        self.__bufferHash = {}
        self.__namesToIds = {}

    def getConnectionFromVars(self):
        domainName = vim.vars["jiraVimDomainName"].decode("utf-8")
        email = vim.vars["jiraVimEmail"].decode("utf-8")
        token = vim.vars["jiraVimToken"].decode("utf-8")

        return Connection(domainName, email, token)

    def assignBoard(self, board, buff):
        self.__bufferHash[board.boardId] = buff
        self.__namesToIds[board.boardName] = board.boardId

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

    # Returns the buffer, and a boolean that says whether the buffer is newly created or existing one
    def getBuff(self, objId=None, objName=None, isSplit=False):
        if objId is not None:
            buff = self.getBufferByIndex(objId)
            if buff is not None:
                return ( buff, False )
        if objName is not None:
            buff = self.getBufferByIndex(objName)
            if buff is not None:
                return ( buff, False )
        # return new buffer
        return (self.createBuffer(), True)

    def createBuffer(self):
        # Creates a new buffer, saves it, and then uses the hidden command to hide it
        vim.command("new")
        buf = vim.current.buffer
        vim.command("hide")
        return buf

