
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
        project = str(issue.getField("project"))
        summary = issue.getField("summary")
        description = issue.getField("description")

        sessionStorage.assignIssue(issue, buf)

        line = DrawUtil.draw_header(buf, issue, "%s %s" % (issueKey, project))

        for field in issue.displayFields:
            line, _, _ = DrawUtil.draw_item(buf, (field.title(), issue.getField(field)), line=line, str_generator=lambda t: ": ".join(t))
            buf.append("")
            buf.append("")
            line += 2
            
        vim.command("setl filetype=%s" % filetype)
    vim.command("set nomodifiable")
