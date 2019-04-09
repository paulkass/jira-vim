import vim
import sys
from ..common.connection import Connection
from ..common.issue import Issue

# Arguments are expected through sys.argv
def JiraVimIssueOpen():
    issueKey = str(sys.argv[0])
    connection = Connection.getConnectionFromVars()
    filetype = "jiraissueview"
    textWidth = vim.current.window.width

    issue = Issue(issueKey, connection)
    obj = issue.obj
    project = str( obj.fields.project )
    summary = obj.fields.summary
    description = obj.fields.description

    # For now, assume that the this is command is called from an already opened board window
    buf = vim.current.buffer 
    buf[:] = None
    buf[0] = "%s %s" % ( issueKey, project )
    vim.command("Tabularize /\\u\+-\d\+\s/r0c%dr0" % (textWidth-len(issueKey)-len(project)-7))
    buf.append("="*len(issueKey))
    buf.append("")

    buf.append("Summary: %s" % summary) 
    buf.append("")
    
    buf.append("Description: %s" % description)
    buf.append("")
    
    vim.command("setl filetype=%s" % filetype)
