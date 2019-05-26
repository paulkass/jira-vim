import vim
import sys
from ..util.drawObject import drawObject 

# arguments expected in sys.argv
def JiraVimBoardOpen(sessionStorage, isSplit=True):
    boardName = str(sys.argv[0]) 
    connection = sessionStorage.connection

    # Buff Setup Commands
    buf, new = sessionStorage.getBuff(objName=boardName)
    if isSplit:
        vim.command("sbuffer "+str(buf.number))
    else:
        vim.command("buffer "+str(buf.number))
    vim.command("let b:jiraVimBoardName = \"%s\"" % boardName)
    if new:
        board = connection.getBoard(boardName)
        drawObject(buf, board, boardName, sessionStorage)

