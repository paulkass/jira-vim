import vim
import sys
from ..common.scrumBoard import ScrumBoard
from ..util.drawObject import drawObject

def JiraVimSprintOpen(sessionStorage, isSplit=True):
    sprintName = str(sys.argv[0])
    connection = sessionStorage.connection

    boardBuffer = vim.current.buffer
    boardName = boardBuffer.vars["jiraVimBoardName"].decode("utf-8")
    
    if boardName is not None:
        board = connection.getBoard(boardName)
        buf, new = sessionStorage.getBuff(objName=sprintName)
        if isSplit:
            vim.command("sbuffer "+str(buf.number))
        else:
            vim.command("buffer "+str(buf.number))

        assert isinstance(board, ScrumBoard)
        drawObject(buf, board.getSprint(sprintName), sprintName, sessionStorage)
    
    
