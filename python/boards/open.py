import vim
import sys
from ..common.connection import Connection
from ..common.kanbanBoard import KanbanBoard

domainName = vim.vars["jiraVimDomainName"].decode("utf-8")
email = vim.vars["jiraVimEmail"].decode("utf-8")
token = vim.vars["jiraVimToken"].decode("utf-8")

connection = Connection(domainName, email, token)

boardName = str( sys.argv[0]) 
board = connection.getBoard(boardName)
issues = board.getIssues()

# Buff Setup Commands
vim.command("new")
if isinstance(board, KanbanBoard):
    filetype = "jirakanbanboardview"
else:
    filetype = "jiraboardview"
vim.command("setl filetype=%s" % filetype)
vim.command("setl buftype=nofile")
vim.command("setl noswapfile")

buf = vim.current.buffer
buf[0] = boardName + " BOARD"
buf.append("="*( len(boardName)+7 ) )
buf.append("")
for col in issues:
    buf.append(col[0].upper()+":")
    buf.append("-"*( len(col[0])+1 ))
    i = col[1]
    buf.append(i)
    buf.append("")
vim.command("set nomodifiable")

