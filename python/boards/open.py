import vim
import sys
from ..common.connection import Connection
# Assumes that the common file was imported in the vimscript

domainName = vim.vars["jiraVimDomainName"].decode("utf-8")
email = vim.vars["jiraVimEmail"].decode("utf-8")
token = vim.vars["jiraVimToken"].decode("utf-8")

connection = Connection(domainName, email, token)

boardName = str( sys.argv[0]) 
board = connection.getBoard(boardName)
issues = board.getIssues()

vim.command("new")
vim.command("set ft=jiraboardview")
buf = vim.current.buffer
buf[0] = boardName
buf.append("="*len(boardName))
buf.append("\n")
buf.append(issues)
vim.command("set noma")

