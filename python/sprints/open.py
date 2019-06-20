import sys
import vim
from ..util.drawUtil import DrawUtil

def JiraVimSprintOpen(sessionStorage, isSplit=True):
    sprintName = str(sys.argv[0])

    boardBuffer = vim.current.buffer

    board = sessionStorage.getBoard(boardBuffer.number)
    buf, _ = sessionStorage.getBuff(objName=sprintName)
    if isSplit:
        vim.command("sbuffer "+str(buf.number))
    else:
        vim.command("buffer "+str(buf.number))
    vim.command("set modifiable")

    sprint = sessionStorage.getSprint(sprintName)
    if not sprint:
        sprint = board.getSprint(sprintName)
        sessionStorage.assignSprint(sprint, buf)
    DrawUtil.draw_header(buf, sprint, sprintName)
    DrawUtil.draw_items(buf, sprint, sessionStorage)
    DrawUtil.set_filetype(sprint)
    vim.command("set nomodifiable")
