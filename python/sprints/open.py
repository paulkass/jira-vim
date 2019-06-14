import sys
import vim
from ..util.drawUtil import DrawUtil

def JiraVimSprintOpen(sessionStorage, isSplit=True):
    sprintName = str(sys.argv[0])

    boardBuffer = vim.current.buffer
    boardName = boardBuffer.vars["jiraVimBoardName"].decode("utf-8")

    if boardName is not None:
        board = sessionStorage.getBoard(boardName)
        buf, _ = sessionStorage.getBuff(objName=sprintName)
        if isSplit:
            vim.command("sbuffer "+str(buf.number))
        else:
            vim.command("buffer "+str(buf.number))
        vim.command("let b:jiraVimBoardName = \"%s\"" % boardName)

        sprint = board.getSprint(sprintName)
        DrawUtil.draw_header(buf, sprint, sprintName)
        DrawUtil.draw_items(buf, sprint, sessionStorage)
        DrawUtil.set_filetype(sprint)
