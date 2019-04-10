import vim
import sys
from ..common.connection import Connection
from ..common.issue import Issue

# Arguments are expected through sys.argv
def JiraVimIssueOpen(sessionStorage):
    issueKey = str(sys.argv[0])
    connection = sessionStorage.connection
    filetype = "jiraissueview"

    buf, new = sessionStorage.getBuff(objName=issueKey)
    if new:
        textWidth = vim.current.window.width
        issue = Issue(issueKey, connection)
        obj = issue.obj
        project = str( obj.fields.project )
        summary = obj.fields.summary
        description = obj.fields.description

        sessionStorage.assignIssue(issue, buf)

        # For now, assume that the this is command is called from an already opened board window
        buf[0] = "%s %s" % ( issueKey, project )
        vim.command("Tabularize /\\u\+-\d\+\s/r0c%dr0" % (textWidth-len(issueKey)-len(project)-7))
        buf.append("="*len(issueKey))
        buf.append("")

        buf.append("Summary: %s" % summary) 
        buf.append("")
        
        buf.append("Description: %s" % description)
        buf.append("")
        
        vim.command("setl filetype=%s" % filetype)
    else:
        # Open the buffer in the current window
        vim.command("buf "+str(buf.number))
