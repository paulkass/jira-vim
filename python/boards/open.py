import vim
import sys
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
        issues = board.getIssues()

        if isinstance(board, KanbanBoard):
            filetype = "jirakanbanboardview"
        else:
            filetype = "jiraboardview"

        sessionStorage.assignBoard(board, buf)
        buf[0] = boardName + " board"
        buf.append("="*(len(boardName)+7))
        buf.append("")
        textWidth = vim.current.window.width

        # Print the issues by category
        for cat in issues:
            buf.append(cat[0].upper()+":")
            buf.append("-"*(len(cat[0])+1))
            startLine = len(buf)+1
            i = cat[1]
            endLine = startLine + len(i)-1
            maxKeyLen = 0
            maxSummLen = 0
            for key, summ in i:
                if len(key) >= maxKeyLen:
                    maxKeyLen = len(key)
                if len(summ) >= maxSummLen:
                    maxSummLen = len(summ)
                buf.append(key + " " + summ)
            vim.command("%d,%dTabularize /\\u\+-\d\+\s/r0l%dr0" % (startLine,\
                   endLine, textWidth-maxKeyLen-maxSummLen-7))
            buf.append("")

        vim.command("setl filetype=%s" % filetype)
