
import sys
import vim
from ..common.search import Search
from ..util.drawUtil import DrawUtil

def JiraVimSearchOpen(sessionStorage):
    query = str(sys.argv[0])
    connection = sessionStorage.connection
    filetype = "jirasearchview"

    buf, new = sessionStorage.getBuff(objId="")
    vim.command("sbuffer "+str(buf.number))
    vim.command("set modifiable")
    vim.command("setl filetype=%s" % filetype)
    if new:
        search = Search(query, connection)
        issues = search.getBatchIssues()
        line = 0
        line = DrawUtil.draw_category(buf, search, issues[0], line=line)
    vim.command("set nomodifiable")
