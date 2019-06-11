import sys
import vim
from ..util.drawUtil import DrawUtil
from ..common.kanbanBoard import KanbanBoard

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
        line = DrawUtil.draw_header(buf, board, boardName)
        if isinstance(board, KanbanBoard):
            # Need to account for columns
            for col in board.columns:
                line = DrawUtil.draw_items(buf, board, sessionStorage, itemExtractor=lambda b, col_name=col: b.getIssues(column=col_name))
        else:
            DrawUtil.draw_items(buf, board, sessionStorage)
        DrawUtil.set_filetype(board)
