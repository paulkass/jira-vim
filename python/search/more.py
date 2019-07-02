
import sys
import vim
from ..util.drawUtil import DrawUtil

def JiraVimLoadMore(sessionStorage):
    _, more_line = tuple(sys.argv)

    buf = vim.current.buffer
    vim.command("set modifiable")

    del buf[more_line-1]
    del buf[more_line-1]

    search = sessionStorage.getSearch(buf.number)

    line = more_line
    DrawUtil.draw_items(buf, search, sessionStorage, line=line, withCategoryHeaders=False)
