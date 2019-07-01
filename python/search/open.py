
import sys
import vim
from ..common.search import Search
from ..util.drawUtil import DrawUtil

def JiraVimSearchOpen(sessionStorage):
    query = str(sys.argv[0])
    connection = sessionStorage.connection

    buf, new = sessionStorage.getBuff(objId="")
    vim.command("sbuffer "+str(buf.number))
    vim.command("set modifiable")
    if new:
        search = Search(query, connection)
        line = 0
        line = DrawUtil.draw_header(buf, search, "Search for \""+query+"\"") + 1
        #line = DrawUtil.draw_category(buf, search, issues[0], line=line)
        line = DrawUtil.draw_items(buf, search, sessionStorage, line=line)
    vim.command("set nomodifiable")
    DrawUtil.set_filetype(search)
