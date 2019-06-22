
import sys
import vim
from ..common.issue import Issue
from ..util.drawUtil import DrawUtil

# Arguments are expected through sys.argv
def JiraVimIssueOpen(sessionStorage, isSplit=False):
    issueKey = str(sys.argv[0])
    connection = sessionStorage.connection
    filetype = "jiraissueview"
    # Carry on the board name from the previous buffer

    buf, new = sessionStorage.getBuff(objName=issueKey)
    if isSplit:
        vim.command("sbuffer "+str(buf.number))
    else:
        vim.command("buffer "+str(buf.number))
    vim.command("set modifiable")
    if new:
        issue = Issue(issueKey, connection)
        obj = issue.obj
        project = str(issue.getField("project"))
        summary = issue.getField("summary")
        description = issue.getField("description")

        sessionStorage.assignIssue(issue, buf)

        line = DrawUtil.draw_header(buf, issue, "%s %s" % (issueKey, project))

        buf.append("Summary: %s" % summary)
        buf.append("")

        buf.append("Description: %s" % description)
        buf.append("")

        vim.command("setl filetype=%s" % filetype)
    vim.command("set nomodifiable")
