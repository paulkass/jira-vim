import sys
import vim

from ..util.drawUtil import DrawUtil

def JiraVimLoadMore(sessionStorage):
    category_name = sys.argv[0]

    more_line = int(sys.argv[1])
    buf = vim.current.buffer
    vim.command("set modifiable")

    # Delete the MORE line and the space below: that will be handled by DrawUtil
    del buf[more_line-1]
    del buf[more_line-1]

    board = sessionStorage.getBoard(buf.number)

    for c in board.columns:
        if c.upper() == category_name:
            category_name = c
            break

    line = more_line
    DrawUtil.draw_items(buf, board, sessionStorage, line=line, itemExtractor=lambda o: o.getIssues(column=category_name), withCategoryHeaders=False)
    vim.command("set nomodifiable")
