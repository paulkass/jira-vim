
import sys
import uuid
import vim
from ..common.search import Search
from ..util.drawUtil import DrawUtil

def JiraVimSearchOpen(sessionStorage):
    query = str(sys.argv[0])
    connection = sessionStorage.connection

    sid = uuid.uuid4()
    buf, new = sessionStorage.getBuff(objId=sid)
    vim.command("sbuffer "+str(buf.number))
    vim.command("set modifiable")
    if new:
        search = Search(query, connection)
        search.query_id = sid
        sessionStorage.assignSearch(search, buf)
        line = 0
        line = DrawUtil.draw_header(buf, search, "Search for \""+query+"\"") + 1
        line = DrawUtil.draw_items(buf, search, sessionStorage, line=line)
    vim.command("set nomodifiable")
    DrawUtil.set_filetype(search)
