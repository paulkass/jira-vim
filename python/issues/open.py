
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

        line = DrawUtil.draw_header(buf, issue, "%s %s" % (issueKey, project)) + 1

        categories = [(field.title(), [("", issue.getField(field))]) for field in issue.displayFields]

        def formatter(startLine, endLine, *args):
            vim.command("normal! %dG" % startLine)
            vim.command("normal! %dgqq" % (endLine - startLine + 1))
            # I know that the previous command should end up on this line, but this is just for clarity
            vim.command("normal! %dG" % endLine)

        for c in categories:
            line = DrawUtil.draw_category(buf, issue, c, line=line, formatter=formatter, with_header=True, str_generator=lambda item: ''.join(item)) + 1
            buf.append("") 
        
        vim.command("setl filetype=%s" % filetype)
    vim.command("set nomodifiable")
